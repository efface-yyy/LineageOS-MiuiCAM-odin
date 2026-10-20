"""Replace SSC range-start frequency estimate with existing bounded timestamp scan.

Keep all locking, validity/range checks, ring wrap handling, end selection,
reference tracking, sample payloads and original Vidhance code unchanged.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
from elftools.elf.elffile import ELFFile
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
from capstone import Cs,CS_ARCH_ARM64,CS_MODE_ARM
root=Path('work/module-ncs');shutil.copytree('work/module-ambilight',root,dirs_exist_ok=True)
p=root/'system/vendor/lib64/hw/camera.qcom.so';data=bytearray(p.read_bytes())
baseline=hashlib.sha256(data).hexdigest()
assert baseline=='0b869f9ec111681f90100db0bbe47196a55f2f44ff22ef20039d90ec3a05ed0a'
site=0xbf9128
with p.open('rb') as f:
 elf=ELFFile(f);seg=next(s for s in elf.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=site<s['p_vaddr']+s['p_filesz']);off=site-seg['p_vaddr']+seg['p_offset']
ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
asm=lambda s:bytes(ks.asm(s,addr=site)[0])
before=asm('add w9,w10,w15; sub w1,w15,w14')
assert data[off:off+8]==before
# w14 is the oldest valid ring index established under the SSC mutex.
# Existing code scans forward by real timestamps and handles ring wrap.
after=asm('mov w28,w14; b 0xbf91c8')
instructions=list(Cs(CS_ARCH_ARM64,CS_MODE_ARM).disasm(after,site))
assert len(after)==8 and instructions[1].op_str=='#0xbf91c8'
data[off:off+8]=after;p.write_bytes(data)
patched=hashlib.sha256(data).hexdigest()
original=(Path('work/module-ambilight')/'system/vendor/lib64/hw/camera.qcom.so').read_bytes()
assert all(original[i]==data[i] for i in range(len(data)) if not off<=i<off+8)
p=root/'customize.sh';s=p.read_text();s=s.replace(baseline+')',baseline+'|'+patched+')');p.write_text(s,encoding='utf-8',newline='\n')
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility validation\nversion=0.11.0-ncs-timestamp-range\nversionCode=11\nauthor=efface-yyy\ndescription=Exact 20260815 build; SSC gyro range uses actual timestamp scan; original algorithms and previous compatibility fixes retained\n',encoding='utf-8',newline='\n')
record=dict(baseline_sha256=baseline,patched_sha256=patched,va=hex(site),file_offset=hex(off),before=before.hex(),after=after.hex(),instructions=[f'{x.mnemonic} {x.op_str}' for x in instructions],scope='SSC synchronous range start: oldest valid index then existing bounded timestamp scan; original algorithms, samples and timestamps unchanged',rollback='Build tools/package_ncs_rollback.py, install 0.10.0-rollback-from-0.11.zip and reboot')
Path('evidence/ncs-range-patch.json').write_text(json.dumps(record,indent=2))
manifest={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/ncs-module-manifest.json').write_text(json.dumps(manifest,indent=2))
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.11.0-ncs-timestamp-range.zip'],check=True)
print(json.dumps(record,indent=2))
