"""Unchanged 0.10 payload; installer additionally recognizes the 0.11 HAL."""
from pathlib import Path
import shutil,json,hashlib,subprocess,sys
root=Path('work/module-ncs-rollback');shutil.copytree('work/module-ambilight',root,dirs_exist_ok=True)
patch=json.loads(Path('evidence/ncs-range-patch.json').read_text())
p=root/'customize.sh';s=p.read_text();old=patch['baseline_sha256']+')';assert old in s
s=s.replace(old,patch['baseline_sha256']+'|'+patch['patched_sha256']+')');p.write_text(s,encoding='utf-8',newline='\n')
for source in Path('work/module-ambilight').rglob('*'):
 if source.is_file() and source.name!='customize.sh':assert source.read_bytes()==(root/source.relative_to('work/module-ambilight')).read_bytes()
target=Path('modules/odin_lineage_miuicamera_0.10.0-rollback-from-0.11.zip')
subprocess.run([sys.executable,'tools/build_module.py',str(root),str(target)],check=True)
record=dict(path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),scope='0.10 unchanged payload; only installer current-HAL allowlist adds verified 0.11 hash')
Path('evidence/ncs-rollback-package.json').write_text(json.dumps(record,indent=2));print(json.dumps(record))
