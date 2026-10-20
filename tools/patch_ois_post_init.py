"""Exact old-driver adapter: retain and execute the factory post-init buffer.

Redirect only the OIS initialization CSLSubmit call. If the per-boot exact
kernel-driver guard is enabled, submit the existing last descriptor again as
OIS_CONTROL after INIT succeeds. Restore packet fields and propagate failures.
No register values, firmware, sensor data, or algorithm outputs are fabricated.
"""
from pathlib import Path
import hashlib,struct,json
from elftools.elf.elffile import ELFFile
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
from capstone import Cs,CS_ARCH_ARM64,CS_MODE_ARM
src=Path('work/lineage-hal/camera.qcom.so');data=bytearray(src.read_bytes())
assert hashlib.sha256(data).hexdigest()=='a2c7bbb1d54b154d95e14acb33d2f25a5e99707d787bd3119362ff95075c39d4'
site=0xaae3dc;cave=0xc23260;prop=cave+0x300
ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
def asm(s,a):return bytes(ks.asm(s,addr=a)[0])
assert data[site:site+4]==asm('bl 0xbb47b0',site)
assert set(data[cave:0xc24000])=={0}
code=asm(f"""
stp x29,x30,[sp,#-96]!
mov x29,sp
stp x19,x20,[sp,#16]
stp x21,x23,[sp,#32]
stp x0,x1,[sp,#48]
stp x2,x3,[sp,#64]
mov x19,x22
bl 0xbb47b0
cbnz w0,done
ldr x8,[x24,#0x70]
ldrh w9,[x8,#0x28]
cmp w9,#124
b.ne done
ldr w9,[x8,#0xc8]
cmp w9,#1
b.ne done
ldr x20,[x19,#0x60]
cbz x20,done
ldr w8,[x20]
mov w9,#0x6000000
cmp w8,w9
b.ne done
ldr w8,[x20,#0x1c]
cmp w8,#6
b.ne done
ldr w8,[x20,#0x24]
cbnz w8,done
ldr w8,[x20,#0x2c]
cbnz w8,done
ldr w21,[x20,#0x18]
add x9,x20,x21
ldr w10,[x9,#0xb0]
ldr w11,[x25,#8]
cmp w10,w11
b.ne done
ldr w10,[x9,#0xc0]
cmp w10,#7
b.ne done
adrp x0,{hex(prop & ~0xfff)}
add x0,x0,#{hex(prop & 0xfff)}
mov w1,wzr
bl 0xc224b0
cbz w0,done
mov w8,#1
movk w8,#0x600,lsl #16
str w8,[x20]
add w8,w21,#120
str w8,[x20,#0x18]
mov w8,#1
str w8,[x20,#0x1c]
ldp x0,x1,[sp,#48]
ldp x2,x3,[sp,#64]
bl 0xbb47b0
mov w23,w0
mov w8,#0x6000000
str w8,[x20]
str w21,[x20,#0x18]
mov w8,#6
str w8,[x20,#0x1c]
mov w0,w23
done:
ldp x21,x23,[sp,#32]
ldp x19,x20,[sp,#16]
ldp x29,x30,[sp],#96
ret
""",cave)
assert len(code)<0x300
name=b'persist.vendor.camera.odin_postinit_compat\0';end=prop+len(name)
data[cave:cave+len(code)]=code;data[prop:end]=name
data[site:site+4]=asm(f'bl {hex(cave)}',site)
with src.open('rb') as f:
 e=ELFFile(f)
 found=False
 for i,p in enumerate(e.iter_segments()):
  if p['p_type']=='PT_LOAD' and p['p_flags']==5:
   assert p['p_offset']==p['p_vaddr']==0x278000
   struct.pack_into('<QQ',data,e['e_phoff']+i*e['e_phentsize']+32,end-p['p_offset'],end-p['p_vaddr']);found=True
 assert found
out=Path('work/ois-post-init');out.mkdir(exist_ok=True)
(out/'camera.qcom.so').write_bytes(data)
(out/'wrapper.asm').write_text('\n'.join(f'{i.address:x}: {i.mnemonic} {i.op_str}' for i in Cs(CS_ARCH_ARM64,CS_MODE_ARM).disasm(code,cave)),encoding='utf-8')
record={'baseline_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'patched_sha256':hashlib.sha256(data).hexdigest(),'driver_sha256':'054b477e19cd0cb8a015f0ce28295db6c688e14a022fed90ad5919caa12ef51c','site':hex(site),'cave':hex(cave),'code_size':len(code),'property':name[:-1].decode(),'upstream_fix':'https://github.com/Inkypen79/kernel_xiaomi_odin/pull/4','scope':'wide OIS factory post-init via original control parser; no kernel flash; no algorithm changes'}
Path('evidence/ois-post-init-patch.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(record)
