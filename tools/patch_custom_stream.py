"""Exact-build diagnostic port of MIUI's advertised custom stream size lookup.

Uses existing unused RX alignment padding, without moving ELF sections, adding
dependencies, or modifying vendor algorithms. Tag 0x80850000 is verified from
this phone's vendor descriptor. Only privileged PRIVATE streams are affected.
"""
import hashlib,json,struct
from pathlib import Path
from elftools.elf.elffile import ELFFile
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN

src=Path('evidence/lineage-cameraserver')
original=src.read_bytes()
assert hashlib.sha256(original).hexdigest()=='4a3237bc7cc0e50c5e7b4d5cbba3843882e06809846a5e8862033057a5077ac2'
data=bytearray(original)
ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
def asm(s,a):return bytes(ks.asm(s,addr=a)[0])
def patch(a,old,new):
 assert bytes(data[a:a+len(old)])==old,(hex(a),data[a:a+len(old)].hex(),old.hex())
 data[a:a+len(new)]=new

# Keep the previously verified gralloc allocation ABI adaptation.
patch(0x24a554,asm('mov x2,x21',0x24a554),asm('orr x2,x21,#0x20000',0x24a554))
cave=0x3a9ea0
code=asm('''
 tbnz w23,#0,privileged
 b 0x2d6370
privileged:
 cmp w21,#0x22
 b.ne 0x2d62e0
 sub x8,x29,#0x30
 mov x0,x25
 mov w1,#0x80850000
 bl 0x3a72f0
 ldur x8,[x29,#-0x20]
 ldur x9,[x29,#-0x18]
 cbz x8,0x2d62e0
 tst x8,#3
 b.ne 0x2d62e0
loop:
 ldr w10,[x9]
 cmp w10,w21
 b.ne next
 ldp w10,w11,[x9,#4]
 cmp w10,w22
 ccmp w11,w19,#0,eq
 b.ne next
 mov w27,w22
 mov w20,w19
 b 0x2d6370
next:
 add x9,x9,#16
 subs x8,x8,#4
 b.ne loop
 b 0x2d62e0
''',cave)
assert cave+len(code)<=0x3aa000
assert set(data[cave:0x3aa000])=={0}
patch(0x2d62dc,asm('tbz w23,#0,0x2d6370',0x2d62dc),asm(f'b {hex(cave)}',0x2d62dc))
data[cave:cave+len(code)]=code
with src.open('rb') as f:
 elf=ELFFile(f)
 for i,s in enumerate(elf.iter_segments()):
  if s['p_type']=='PT_LOAD' and s['p_flags']==5:
   assert s['p_offset']==0xb6000 and s['p_vaddr']==0xb6000
   n=cave+len(code)-s['p_offset']
   off=elf['e_phoff']+i*elf['e_phentsize']
   struct.pack_into('<QQ',data,off+32,n,n)
out=Path('work/lineage-cameraserver-custom-stream');out.write_bytes(data)
Path('evidence/custom-stream-binary-patch.json').write_text(json.dumps({
 'baseline_sha256':hashlib.sha256(original).hexdigest(),
 'patched_sha256':hashlib.sha256(data).hexdigest(),
 'custom_tag':'0x80850000','custom_tag_name':'xiaomi.scaler.availableStreamConfigurations',
 'cave_va':hex(cave),'cave_size':len(code),
 'scope':'exact ROM/vendor build; privileged PRIVATE advertised exact sizes only',
 'vendor_algorithm_changes':0},indent=2))
print(out,hashlib.sha256(data).hexdigest(),len(code))
