"""Build ARMv7 buffer-copy ABI bridge for the FrameDecoder diagnostic.

Equivalent to checking converter.wrap(), allocating backBufferSize() and using
setBackBuffer()/copyToMediaImage() when direct wrapping is unavailable.
"""
from pathlib import Path
import struct,subprocess,json,hashlib
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB,KS_MODE_LITTLE_ENDIAN
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
out=Path('work/frame-compat');out.mkdir(exist_ok=True)
imports=[
'_ZNK7android31GraphicView2MediaImageConverter4wrapEv',
'_ZNK7android31GraphicView2MediaImageConverter14backBufferSizeEv',
'calloc','_ZN7android7ABuffer12CreateAsCopyEPKvj','free',
'_ZN7android31GraphicView2MediaImageConverter13setBackBufferERKNS_2spINS_7ABufferEEE',
'_ZN7android31GraphicView2MediaImageConverter16copyToMediaImageEv',
'_ZNK7android7RefBase9decStrongEPKv']
source='''
push.w {r4,r5,r6,r7,r8,lr}
mov r4,r0
mov r5,r1
call0: bl call0
ldr r0,[r4]
cmp r0,#0
bne done
mov r0,r5
call1: bl call1
mov r6,r0
cmp r6,#0
beq done
movs r0,#1
mov r1,r6
call2: bl call2
mov r7,r0
cmp r7,#0
beq done
mov r0,r4
mov r1,r7
mov r2,r6
call3: bl call3
mov r0,r7
call4: bl call4
ldr r0,[r4]
cmp r0,#0
beq done
mov r0,r5
mov r1,r4
call5: bl call5
cmp r0,#0
beq fail
mov r0,r5
call6: bl call6
cmp r0,#0
bne fail
done:
mov r0,r4
pop.w {r4,r5,r6,r7,r8,pc}
fail:
ldr r0,[r4]
mov r1,r4
call7: bl call7
movs r0,#0
str r0,[r4]
b done
'''
code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB|KS_MODE_LITTLE_ENDIAN).asm(source,addr=0)[0])
calls=[i.address for i in Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(code,0) if i.mnemonic=='bl']
assert len(calls)==len(imports)
names=['$t','odin_frame_wrap']+imports
strings=b'\0';offsets={}
for n in names:offsets[n]=len(strings);strings+=n.encode()+b'\0'
sym=bytes(16)
sym+=struct.pack('<IIIBBH',offsets['$t'],0,0,0,0,1)
sym+=struct.pack('<IIIBBH',offsets['odin_frame_wrap'],1,len(code),0x12,0,1)
for n in imports:sym+=struct.pack('<IIIBBH',offsets[n],0,0,0x12,0,0)
rel=b''.join(struct.pack('<II',a,((3+i)<<8)|10) for i,a in enumerate(calls))
shnames=b'\0.text\0.rel.text\0.symtab\0.strtab\0.shstrtab\0.note.GNU-stack\0'
data=bytearray(52)
def add(b,align=1):
 while len(data)%align:data.append(0)
 off=len(data);data.extend(b);return off
co=add(code,4);ro=add(rel,4);so=add(sym,4);st=add(strings);sn=add(shnames)
while len(data)%4:data.append(0)
shoff=len(data)
def sh(name,typ,flags,off,size,link=0,info=0,align=1,entsize=0):
 return struct.pack('<IIIIIIIIII',shnames.index(name.encode()+b'\0') if name else 0,typ,flags,0,off,size,link,info,align,entsize)
data+=bytes(40)
data+=sh('.text',1,6,co,len(code),align=4)
data+=sh('.rel.text',9,0,ro,len(rel),3,1,4,8)
data+=sh('.symtab',2,0,so,len(sym),4,2,4,16)
data+=sh('.strtab',3,0,st,len(strings))
data+=sh('.shstrtab',3,0,sn,len(shnames))
data+=sh('.note.GNU-stack',1,0,0,0)
data[:52]=struct.pack('<16sHHIIIIIHHHHHH',b'\x7fELF\x01\x01\x01'+bytes(9),1,40,1,0,0,shoff,0x5000200,52,0,0,40,7,5)
obj=out/'frame_bridge.o';obj.write_bytes(data)
lib=out/'libodin_frame_compat.so'
subprocess.run(['C:/Android/Sdk/build-tools/36.0.0/lld-bin/lld.exe','-flavor','gnu','-shared','--hash-style=both','--no-undefined','--allow-shlib-undefined','-z','max-page-size=4096','-soname',lib.name,'-o',str(lib),str(obj),
 'evidence/lineage-libsfplugin-utils32.so','evidence/lineage-libstagefright-foundation32.so','evidence/lineage-libc32.so','evidence/lineage-libutils32.so'],check=True)
Path('evidence/frame-bridge-build.json').write_text(json.dumps({'sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'imports':imports,'assembly':source,'purpose':'FrameDecoder copy fallback only; no codec replacement'},indent=2))
print(lib,len(code))
