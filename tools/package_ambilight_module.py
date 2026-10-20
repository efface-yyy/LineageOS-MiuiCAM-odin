"""Bind only an exact plugin loader-name adaptation; original cache is retained."""
from pathlib import Path
import shutil,hashlib,json,subprocess,sys,zipfile,lief
root=Path('work/module-ambilight');shutil.copytree('work/module-audio',root,dirs_exist_ok=True)
private=root/'compat/ambilight';private.mkdir(parents=True,exist_ok=True)
src=Path('work/ambilight-extracted/lib/arm64-v8a/libcamera_ambilight_ambt_qcom.so')
raw=src.read_bytes();baseline=hashlib.sha256(raw).hexdigest()
assert baseline=='43a09f5ab1599d15c385a1b2cdc5051323e435e55ece4961c59bd6212089ead2'
old=b'libdmabufheap.so\0';new=b'libodinheap.so\0';assert raw.count(old)==1
patched=raw.replace(old,new+bytes(len(old)-len(new)))
(private/src.name).write_bytes(patched)
original_elf=lief.parse(list(raw));patched_elf=lief.parse(list(patched))
assert bytes(original_elf.get_section('.text').content)==bytes(patched_elf.get_section('.text').content)
with zipfile.ZipFile(root/'system/priv-app/MiuiCamera/MiuiCamera.apk') as z:
 allocator=z.read('lib/arm64-v8a/libdmabufheap.so')
assert hashlib.sha256(allocator).hexdigest()=='7a4109b13a5a8e98d1a0df8269c2f355e1e313a10b4509cffbd2cfaa79a32570'
binary=lief.parse(list(allocator));text=bytes(binary.get_section('.text').content)
binary.get(lief.ELF.DynamicEntry.TAG.SONAME).name='libodinheap.so'
binary.write(str(private/'libodinheap.so'))
check=lief.parse(str(private/'libodinheap.so'));assert bytes(check.get_section('.text').content)==text
script='''#!/system/bin/sh
MODDIR=${0%/*}
LIBDIR=/data/data/com.android.camera/app_qigsaw/5.0.0.0/ambilight/v1.3.5@20220126/nativeLib/arm64-v8a
TARGET=$LIBDIR/libcamera_ambilight_ambt_qcom.so
SRC=$MODDIR/compat/ambilight
LOG=$MODDIR/ambilight-bind.log
exec >"$LOG" 2>&1
echo "Ambilight loader compatibility; $(date)"
[ -f "$TARGET" ] || { echo "Exact cached plugin not present; no changes"; exit 0; }
[ ! -d /dev/dma_heap ] && [ -c /dev/ion ] || { echo "ION-only guard not met"; exit 0; }
[ "$(sha256sum "$TARGET" | cut -d ' ' -f 1)" = BASE ] || { echo "Plugin hash mismatch; no changes"; exit 1; }
OWNER=$(stat -c %u:%g "$TARGET")
CONTEXT=$(ls -Zd "$TARGET" | cut -d ' ' -f 1)
for NAME in libcamera_ambilight_ambt_qcom.so libodinheap.so; do
 chown "$OWNER" "$SRC/$NAME" || exit 1
 chmod 0600 "$SRC/$NAME" || exit 1
 chcon "$CONTEXT" "$SRC/$NAME" || exit 1
done
ALIAS=$LIBDIR/libodinheap.so
if [ ! -e "$ALIAS" ]; then
 touch "$ALIAS" || exit 1
 chown "$OWNER" "$ALIAS" || exit 1
 chmod 0600 "$ALIAS" || exit 1
 chcon "$CONTEXT" "$ALIAS" || exit 1
fi
[ "$(stat -c %s "$ALIAS")" = 0 ] || { echo "Alias already exists; no changes"; exit 1; }
mount --bind "$SRC/libodinheap.so" "$ALIAS" || exit 1
mount --bind "$SRC/libcamera_ambilight_ambt_qcom.so" "$TARGET" || { umount "$ALIAS"; exit 1; }
sha256sum "$TARGET" "$ALIAS"
echo "Bound loader name and private original allocator; original plugin file unchanged beneath bind"
'''.replace('BASE',baseline)
(root/'ambilight-bind.sh').write_text(script,encoding='utf-8',newline='\n')
p=root/'service.sh';s=p.read_text(encoding='utf-8');s+='\nMODDIR=${0%/*}\nsu -mm -c "sh $MODDIR/ambilight-bind.sh"\n';p.write_text(s,encoding='utf-8',newline='\n')
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility validation\nversion=0.10.0-ambilight-ion\nversionCode=10\nauthor=efface-yyy\ndescription=Exact 20260815 build and ambilight v1.3.5; original algorithm with private ION allocator; concurrent audio compatibility; full validation incomplete\n',encoding='utf-8',newline='\n')
record={'plugin_baseline_sha256':baseline,'plugin_overlay_sha256':hashlib.sha256(patched).hexdigest(),'allocator_original_sha256':hashlib.sha256(allocator).hexdigest(),'allocator_alias_sha256':hashlib.sha256((private/'libodinheap.so').read_bytes()).hexdigest(),'scope':'Only plugin dlopen name and allocator SONAME changed; both .text sections unchanged; cache original untouched beneath reboot-reversible binds'}
Path('evidence/ambilight-ion-patch.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/ambilight-module-manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.10.0-ambilight-ion.zip'],check=True)
print(json.dumps(record))
