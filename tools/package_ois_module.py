from pathlib import Path
import shutil,hashlib,json,subprocess,sys
root=Path('work/module-ois');shutil.copytree('work/module-codec',root,dirs_exist_ok=True)
record=json.loads(Path('evidence/ois-post-init-patch.json').read_text())
p=root/'system/vendor/lib64/hw/camera.qcom.so';p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2('work/ois-post-init/camera.qcom.so',p)
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility validation\nversion=0.7.0-ois-post-init\nversionCode=7\nauthor=efface-yyy\ndescription=Exact 20260815 build; restore factory wide OIS post-init on the identified old driver; full validation incomplete\n',encoding='utf-8',newline='\n')
p=root/'customize.sh';s=p.read_text(encoding='utf-8');old=next(x for x in s.splitlines() if x.startswith('[ "$(sha256sum /vendor/lib64/hw/camera.qcom.so'))
s=s.replace(old,'''case "$(sha256sum /vendor/lib64/hw/camera.qcom.so | cut -d ' ' -f 1)" in
 BASE|PATCH) ;;
 *) abort "Unsupported camera HAL build." ;;
esac
[ "$(sha256sum /vendor/lib/modules/camera.ko | cut -d ' ' -f 1)" = DRIVER ] || abort "Unsupported OIS driver. Use the matching build; disable this module before a ROM update."
'''.replace('BASE',record['baseline_sha256']).replace('PATCH',record['patched_sha256']).replace('DRIVER',record['driver_sha256']))
p.write_text(s,encoding='utf-8',newline='\n')
p=root/'post-fs-data.sh';s=p.read_text(encoding='utf-8');s+='''
# Runtime-only opt-in for the exact driver missing Xiaomi post-init support.
resetprop -n persist.vendor.camera.odin_postinit_compat 0
if [ "$(sha256sum /vendor/lib/modules/camera.ko | cut -d ' ' -f 1)" = DRIVER ]; then
 resetprop -n persist.vendor.camera.odin_postinit_compat 1
fi
chcon u:object_r:vendor_file:s0 "$MODDIR/system/vendor/lib64/hw/camera.qcom.so"
'''.replace('DRIVER',record['driver_sha256']);p.write_text(s,encoding='utf-8',newline='\n')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/ois-module-manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.7.0-ois-post-init.zip'],check=True)
