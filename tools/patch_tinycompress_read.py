"""Restore AVAIL re-query after POLLIN; retain original capture/read/error paths.

Exact 32-bit Lineage library only. Mirrors the loop in original Xiaomi and
LineageOS compress_read instead of reusing the pre-poll zero availability.
"""
from pathlib import Path
import hashlib,json,lief
from elftools.elf.elffile import ELFFile
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
src=Path('work/lineage-hal/libtinycompress.so');raw=src.read_bytes()
baseline='9a7215d1bfe46aeff0ea0c680dcd45aaf4b0fdd0e5eed1457793325cdd805cfe'
assert hashlib.sha256(raw).hexdigest()==baseline
binary=lief.parse(str(src));text=bytes(binary.get_section('.text').content)
segment=lief.ELF.Segment();segment.type=lief.ELF.Segment.TYPE.LOAD
segment.flags=lief.ELF.Segment.FLAGS.R|lief.ELF.Segment.FLAGS.X
segment.alignment=4096;segment.virtual_address=0x10000
marker=b'ODIN_CIN_AVAIL_LOOP'+bytes(46);segment.content=list(marker)
binary.add(segment)
out=Path('work/audio-compat/libtinycompress.so');out.parent.mkdir(exist_ok=True)
binary.write(str(out));check=lief.parse(str(out))
assert bytes(check.get_section('.text').content)==text
delta=check.get_dynamic_symbol('compress_read').value-0x27e9
cave=next(s.virtual_address for s in check.segments if bytes(s.content[:len(marker)])==marker)
ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);asm=lambda s,a:bytes(ks.asm(s,addr=a)[0])
code=asm(f'''
tst.w r1,#1
bne ready
b.w {hex(0x28be+delta)}
ready:
ldr.w r1,[r8,#0x88]
ldr r7,[r1]
mov r0,r8
b.w {hex(0x2830+delta)}
''',cave)
decoded=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(code,cave))
branches=[i for i in decoded if i.mnemonic=='b.w']
assert [int(i.op_str.lstrip('#'),16) for i in branches]==[0x28be+delta,0x2830+delta]
data=bytearray(out.read_bytes())
with out.open('rb') as f:
 e=ELFFile(f)
 def offset(va):
  s=next(s for s in e.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=va<s['p_vaddr']+s['p_filesz'])
  return s['p_offset']+va-s['p_vaddr']
 site=0x28ba+delta;i=offset(site);j=offset(cave)
 assert data[i:i+4]==asm(f'lsls r0,r1,#31; bne {hex(0x28f0+delta)}',site)
 branch=asm(f'b.w {hex(cave)}',site);assert len(branch)==4 and len(code)<=len(marker)
 data[i:i+4]=branch;data[j:j+len(marker)]=code+bytes(len(marker)-len(code))
out.write_bytes(data)
record={'baseline_sha256':baseline,'patched_sha256':hashlib.sha256(data).hexdigest(),'branch_va':hex(site),'text_relocation_delta':delta,'helper_va':hex(cave),'helper_size':len(code),'scope':'32-bit compress_read POLLIN: refresh AVAIL before reading; no audio source, codec or routing changes'}
Path('evidence/tinycompress-read-patch.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record))
