"""Android 17 Surface::connect vtable/signature adapter; no imaging changes."""
import hashlib,json
from pathlib import Path
from elftools.elf.elffile import ELFFile
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
src=Path('work/module-custom-stream/system/priv-app/MiuiCamera/lib/arm64/libcamera_algoup_jni.xiaomi.so')
data=bytearray(src.read_bytes());before=bytes(data)
with src.open('rb') as f:
 e=ELFFile(f)
 sym=next(s for s in e.get_section_by_name('.dynsym').iter_symbols() if s.name=='_Z16getANativeWindowP7_JNIEnvP8_jobject')
 va=sym['st_value']+0x1e8
 seg=next(s for s in e.iter_segments() if s['p_type']=='PT_LOAD' and s['p_vaddr']<=va<s['p_vaddr']+s['p_filesz'])
 off=va-seg['p_vaddr']+seg['p_offset']
ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
asm=lambda s,a:bytes(ks.asm(s,addr=a)[0])
assert data[off:off+8]==asm('ldp x8,x21,[sp,#8];str x8,[sp]',va)
assert data[off+52:off+60]==asm('ldr x8,[x8,#0x158];blr x8',va+52)
# A14 slot 0x158 = connect(IProducerListener,bool). A17 uses slot 0x150
# = connect(SurfaceListener,bool,bool,bool). This wrapper has no custom buffer
# callback overrides; replace its legacy listener with the framework default.
# Keep the existing own-reference release at getANativeWindow+0x268; skip only
# the extra temporary listener ref pair, since the new call receives null.
code=asm('''
ldp x8,x21,[sp,#8]
str xzr,[sp]
ldr x8,[x21]
ldr x8,[x8,#0x150]
mov x0,x21
mov w1,#2
mov x2,sp
mov w3,wzr
mov w4,wzr
mov w5,wzr
blr x8
nop
nop
nop
nop
''',va)
assert len(code)==60
data[off:off+60]=code
out=Path('work/libcamera_algoup_jni-surface-compat.so');out.write_bytes(data)
Path('evidence/surface-connect-patch.json').write_text(json.dumps({
 'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(data).hexdigest(),
 'va':hex(va),'size':len(code),'change':'Surface connect virtual ABI and default listener signature',
 'scope':'exact LineageOS 20260815 libgui ABI; no algorithm processing changes'},indent=2))
print(out,hashlib.sha256(data).hexdigest())
