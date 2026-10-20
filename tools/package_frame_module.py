from pathlib import Path
import shutil,hashlib,json,subprocess,sys
root=Path('work/module-frame')
shutil.copytree('work/module-surface',root,dirs_exist_ok=True)
(root/'system/lib').mkdir(exist_ok=True)
for n in ['libstagefright.so','libodin_frame_compat.so']:
 shutil.copy2(Path('work/frame-compat')/n,root/'system/lib'/n)
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility validation\nversion=0.5.0-frame-copy\nversionCode=5\nauthor=efface-yyy\ndescription=Exact 20260815 build; camera ABI and thumbnail copy fallback; full feature and quality validation incomplete\n',newline='\n')
p=root/'customize.sh';s=p.read_text()
s+='''
case "$(sha256sum /system/lib/libstagefright.so | cut -d ' ' -f 1)" in
 850f0604ba48deefe6d88c7d39085334a127bf48a662a263ab98068b7b8ffb67|893a7e70d74933c185b2e215a3fcbd8e2eeaa6d651d1860c7f27b495ffd56769) ;;
 *) abort "Unsupported 32-bit FrameDecoder build." ;;
esac
'''
for local,remote in [('evidence/lineage-libsfplugin-utils32.so','/system/lib/libsfplugin_ccodec_utils.so'),('evidence/lineage-libstagefright-foundation32.so','/system/lib/libstagefright_foundation.so'),('evidence/lineage-libutils32.so','/system/lib/libutils.so')]:
 h=hashlib.sha256(Path(local).read_bytes()).hexdigest()
 s+=f'[ "$(sha256sum {remote} | cut -d \' \' -f 1)" = {h} ] || abort "Unsupported frame bridge ABI dependency."\n'
p.write_text(s,newline='\n')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/frame-module-manifest.json').write_text(json.dumps(records,indent=2))
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.5.0-frame-copy.zip'],check=True)
