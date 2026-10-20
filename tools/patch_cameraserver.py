"""Adapt ANativeWindow allocation usage without changing HAL stream usage.
Only for the exact baseline binary saved in evidence/lineage-cameraserver.
"""
from pathlib import Path
import hashlib,json
from elftools.elf.elffile import ELFFile
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
src=Path('evidence/lineage-cameraserver')
data=bytearray(src.read_bytes())
va=0x24a554
with src.open('rb') as f:
 e=ELFFile(f)
 seg=next(s for s in e.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=va<s['p_vaddr']+s['p_filesz'])
 off=seg['p_offset']+va-seg['p_vaddr']
ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
before=bytes(ks.asm('mov x2, x21',addr=va)[0])
after=bytes(ks.asm('orr x2, x21, #0x20000',addr=va)[0])
assert data[off:off+4]==before
data[off:off+4]=after
out=Path('work/lineage-cameraserver-compat');out.write_bytes(data)
Path('evidence/cameraserver-patch.json').write_text(json.dumps({'baseline_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'patched_sha256':hashlib.sha256(data).hexdigest(),'virtual_address':hex(va),'original':before.hex(),'patched':after.hex(),'change':'ANativeWindow usage includes GRALLOC_USAGE_HW_CAMERA_WRITE; HAL-visible stream usage unchanged'},indent=2))
print('cameraserver: one allocation instruction patched')
