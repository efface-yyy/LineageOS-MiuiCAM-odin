from pathlib import Path
import shutil,hashlib,json,subprocess,sys
root=Path('work/module-codec')
shutil.copytree('work/module-frame',root,dirs_exist_ok=True)
(root/'system/vendor/etc').mkdir(parents=True,exist_ok=True)
for n in ['media_codecs.xml','media_codecs_lahaina.xml']:
 shutil.copy2(Path('work/codec-compat')/n,root/'system/vendor/etc'/n)
(root/'module.prop').write_text('id=odin_lineage_miuicamera\nname=MIX 4 MIUI Camera compatibility validation\nversion=0.6.0-hevc8k\nversionCode=6\nauthor=efface-yyy\ndescription=Exact 20260815 build; camera/thumbnail ABI and official HEVC8K declaration; full validation incomplete\n',newline='\n')
p=root/'customize.sh';s=p.read_text(encoding='utf-8')
for n in ['media_codecs.xml','media_codecs_lahaina.xml']:
 s+=f'''
case "$(sha256sum /vendor/etc/{n} | cut -d ' ' -f 1)" in
 83947422456cc6971fed634e4b889834a38ff16f6bd0bed06be26ba51c75ca57|27e5be030f46dfcb0486d458296413b095d2e86d7718af1b3c4884528217bbbd) ;;
 *) abort "Unsupported codec configuration build." ;;
esac
'''
p.write_text(s,encoding='utf-8',newline='\n')
p=root/'post-fs-data.sh';s=p.read_text(encoding='utf-8')
s+='chcon u:object_r:vendor_configs_file:s0 "$MODDIR/system/vendor/etc/media_codecs.xml" "$MODDIR/system/vendor/etc/media_codecs_lahaina.xml"\n'
p.write_text(s,encoding='utf-8',newline='\n')
records={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
Path('evidence/codec-module-manifest.json').write_text(json.dumps(records,indent=2))
subprocess.run([sys.executable,'tools/build_module.py',str(root),'modules/odin_lineage_miuicamera_0.6.0-hevc8k.zip'],check=True)
