from pathlib import Path
import shutil,hashlib,json,subprocess,sys
root=Path('work/module-audio');shutil.copytree('work/module-ois',root,dirs_exist_ok=True)
record=json.loads(Path('evidence/tinycompress-read-patch.json').read_text(encoding='utf-8'))
p=root/'system/vendor/lib/libtinycompress.so';p.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2('work/audio-compat/libtinycompress.so',p)
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility validation\nversion=0.8.0-cin-read\nversionCode=8\nauthor=efface-yyy\ndescription=Exact 20260815 build; restore compressed concurrent capture AVAIL loop; full validation incomplete\n',encoding='utf-8',newline='\n')
p=root/'customize.sh';s=p.read_text(encoding='utf-8')
s+='\ncase "$(sha256sum /vendor/lib/libtinycompress.so | cut -d \' \' -f 1)" in\n BASE|PATCH) ;;\n *) abort "Unsupported 32-bit tinycompress build." ;;\nesac\n'.replace('BASE',record['baseline_sha256']).replace('PATCH',record['patched_sha256'])
p.write_text(s,encoding='utf-8',newline='\n')
p=root/'post-fs-data.sh';s=p.read_text(encoding='utf-8');s+='chcon u:object_r:vendor_file:s0 "$MODDIR/system/vendor/lib/libtinycompress.so"\n';p.write_text(s,encoding='utf-8',newline='\n')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/audio-module-manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.8.0-cin-read.zip'],check=True)
