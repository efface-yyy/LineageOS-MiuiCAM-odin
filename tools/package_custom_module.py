from pathlib import Path
import shutil,hashlib,json,subprocess,sys
root=Path('work/module-custom-stream')
shutil.copytree('work/module-trace',root,dirs_exist_ok=True)
shutil.copy2('work/lineage-cameraserver-custom-stream',root/'system/bin/cameraserver')
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility diagnostic\nversion=0.3.0-custom-stream\nversionCode=3\nauthor=efface-yyy\ndescription=Exact 20260815 build; Xiaomi advertised custom size compatibility; quality validation incomplete\n',newline='\n')
p=root/'customize.sh';s=p.read_text()
s=s.replace('[ "${CURRENT%% *}" = "$BASELINE" ] || abort',
'''case "${CURRENT%% *}" in
 "$BASELINE"|b40953304dee7654c498f7f85527dba1e03798c6f3b615fe6a879c59678890e9|599325278fd4721293a051d8852d5eeb54109778786c5ec2b619b57fe22c2df7) ;;
 *) abort "Unsupported cameraserver build." ;;
esac
[ "$(sha256sum /vendor/lib64/hw/camera.qcom.so | cut -d ' ' -f 1)" = a2c7bbb1d54b154d95e14acb33d2f25a5e99707d787bd3119362ff95075c39d4 ] || abort''')
p.write_text(s,newline='\n')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/custom-stream-module-manifest.json').write_text(json.dumps(records,indent=2))
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.3.0-custom-stream.zip'],check=True)
