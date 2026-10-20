"""Exact-build FrameDecoder copy fallback, with a null-safe failure exit.

Only the single wrap() import used by FrameDecoder is redirected. The helper
uses the original converter and original hardware codec; no decoder is disabled.
"""
from pathlib import Path
import lief,hashlib,json
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from elftools.elf.elffile import ELFFile
src=Path('evidence/lineage-libstagefright32.so')
binary=lief.parse(str(src))
original_text=bytes(binary.get_section('.text').content)
sym=binary.get_dynamic_symbol('_ZNK7android31GraphicView2MediaImageConverter4wrapEv')
assert sym.value==0
sym.name='odin_frame_wrap'
binary.add_library('libodin_frame_compat.so')
segment=lief.ELF.Segment();segment.type=lief.ELF.Segment.TYPE.LOAD
segment.flags=lief.ELF.Segment.FLAGS.R|lief.ELF.Segment.FLAGS.X
segment.alignment=4096;segment.virtual_address=0x1b0000
marker=b'ODIN_FRAME_GUARD'+bytes(49)
segment.content=list(marker)
binary.add(segment)
out=Path('work/frame-compat/libstagefright.so');binary.write(str(out))
check=lief.parse(str(out))
assert bytes(check.get_section('.text').content)==original_text
func=check.get_dynamic_symbol('_ZN7android12FrameDecoder23handleOutputBufferAsyncEix')
delta=(func.value&~1)-0xb7438
cave=next(s.virtual_address for s in check.segments if bytes(s.content[:len(marker)])==marker)
call=0xb77c4+delta
ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
asm=lambda s,a:bytes(ks.asm(s,addr=a)[0])
code=asm(f'''
ldr.w r10,[sp,#0x80]
cmp.w r10,#0
bne good
ldr.w r10,[sp,#0x14]
b.w {hex(0xb779c+delta)}
good:
b.w {hex(call+4)}
''',cave)
data=bytearray(out.read_bytes())
with out.open('rb') as f:
 elf=ELFFile(f)
 def offset(va):
  s=next(s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=va<s['p_vaddr']+s['p_filesz'])
  return s['p_offset']+va-s['p_vaddr']
 i=offset(call);j=offset(cave)
 assert data[i:i+4]==asm('ldr.w r10,[sp,#0x80]',call)
 branch=asm(f'b.w {hex(cave)}',call);assert len(branch)==4
 assert len(code)<=len(marker)
 data[i:i+4]=branch;data[j:j+len(marker)]=code+bytes(len(marker)-len(code))
out.write_bytes(data)
Path('evidence/frame-decoder-patch.json').write_text(json.dumps({
 'baseline_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'patched_sha256':hashlib.sha256(data).hexdigest(),
 'original_text_sha256':hashlib.sha256(original_text).hexdigest(),
 'text_relocation_delta':delta,'null_guard_at':hex(call),'guard_va':hex(cave),'guard_size':len(code),
 'scope':'32-bit FrameDecoder wrap call only; original codec and converter retained'},indent=2))
print(out,'delta',hex(delta),'guard',hex(cave),'at',hex(call),len(code))
