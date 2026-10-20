"""Build minimal AArch64 ABI bridge; never alters proprietary algorithm instructions.
The stock BnProducerListener::onBufferDetached implementation only logs its slot.
This bridge preserves the empty callback behavior without that debug log.
"""
from pathlib import Path
import struct,subprocess,lief,hashlib,json
from keystone import Ks, KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN
out=Path('work/compat');out.mkdir(exist_ok=True)
symbol='_ZN7android18BnProducerListener16onBufferDetachedEi'
text=bytes.fromhex('5f2403d5c0035fd6') # bti c; ret
strtab=b'\0'+symbol.encode()+b'\0'
shnames=b'\0.text\0.symtab\0.strtab\0.shstrtab\0.note.GNU-stack\0'
data=bytearray(64)
def append(blob,align=1):
 while len(data)%align:data.append(0)
 off=len(data);data.extend(blob);return off
textoff=append(text,4)
symoff=append(bytes(24)+struct.pack('<IBBHQQ',1,0x12,0,1,0,len(text)),8)
stroff=append(strtab);shstroff=append(shnames)
while len(data)%8:data.append(0)
shoff=len(data)
def sh(name,typ,flags,off,size,link=0,info=0,align=1,entsize=0):
 return struct.pack('<IIQQQQIIQQ',shnames.index(name.encode()+b'\0') if name else 0,typ,flags,0,off,size,link,info,align,entsize)
data.extend(bytes(64))
data.extend(sh('.text',1,6,textoff,len(text),align=4))
data.extend(sh('.symtab',2,0,symoff,48,3,1,8,24))
data.extend(sh('.strtab',3,0,stroff,len(strtab)))
data.extend(sh('.shstrtab',3,0,shstroff,len(shnames)))
data.extend(sh('.note.GNU-stack',1,0,0,0))
data[:64]=struct.pack('<16sHHIQQQIHHHHHH',b'\x7fELF\x02\x01\x01'+bytes(9),1,183,1,0,0,shoff,0,64,0,0,64,6,4)
obj=out/'producer_listener.o';obj.write_bytes(data)
lib=out/'libmiuicam_compat.so'
subprocess.run(['C:/Android/Sdk/build-tools/36.0.0/lld-bin/lld.exe','-flavor','gnu','-shared','-z','max-page-size=16384','-soname',lib.name,'-o',str(lib),str(obj)],check=True)
root=Path('work/module/system')
(root/'lib64').mkdir(parents=True,exist_ok=True)
(root/'lib64'/lib.name).write_bytes(lib.read_bytes())
records=[]
for name in ['libcamera_algoup_jni.xiaomi.so','libcamera_mianode_jni.xiaomi.so']:
 src=Path('work/hyper14/system_ext_a/lib64')/name
 binary=lief.parse(str(src));before=bytes(binary.get_section('.text').content)
 if name == 'libcamera_algoup_jni.xiaomi.so':
  # OEM probes legacy MIVI 1 before the real MIVI 2 service. This ROM's V2
  # engine can be opened but does not export miOpenLib. Stock dereferences
  # that null pointer. Return -1 via the existing error epilogue, allowing
  # the stock init function to continue into its original MIVI 2 fallback.
  expected=bytes(binary.get_content_from_virtual_address(0xb260,4))
  assert expected == bytes(Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN).asm('bl #0xfb78',addr=0xb260)[0])
  binary.patch_address(0xb260,Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN).asm('cbz x23, #0xb344',addr=0xb260)[0])
 adapted=bytes(binary.get_section('.text').content)
 binary.add_library(lib.name)
 dst=root/'priv-app/MiuiCamera/lib/arm64'/name
 binary.write(str(dst))
 check=lief.parse(str(dst))
 after=bytes(check.get_section('.text').content)
 assert adapted==after, 'unplanned proprietary code change'
 records.append({'library':name,'original_text_sha256':hashlib.sha256(before).hexdigest(),'patched_text_sha256':hashlib.sha256(after).hexdigest(),'changed_text_bytes':sum(a!=b for a,b in zip(before,after)),'change':'DT_NEEDED ABI bridge; algoup only: null legacy MIVI function pointer guard at original VA 0xb260'})
Path('evidence/jni-integrity.json').write_text(json.dumps(records,indent=2))
print('ABI bridge built; algorithm processing code unchanged; algoup init null guard added')
