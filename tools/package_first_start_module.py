"""Build 0.12 from the exact released 0.11 payload plus reviewed module scripts.

Usage: python tools/package_first_start_module.py BASE_0_11_ZIP OUTPUT_ZIP
Run from any directory. Only three module text files and two added scripts differ.
"""
from pathlib import Path
import copy, hashlib, json, sys, zipfile

base, output = map(Path, sys.argv[1:])
repo = Path(__file__).resolve().parents[1]
template = repo / 'module-template'
with zipfile.ZipFile(base) as src:
    assert src.testzip() is None
    prop = src.read('module.prop').decode()
    assert 'version=0.11.0-ncs-timestamp-range\n' in prop
    assert hashlib.sha256(src.read('system/priv-app/MiuiCamera/MiuiCamera.apk')).hexdigest() == 'e744879ea93177b190938afb5dfca9038daa365a4cc32d5784147ea07f626f86'
    assert hashlib.sha256(src.read('system/vendor/lib64/hw/camera.qcom.so')).hexdigest() == 'c3d262079c7c09efaa060b69a6c10eb90442e1cb1ddacc7641ca046ffc159d52'
    replacements = {n: (template / n).read_bytes() for n in ['module.prop', 'service.sh', 'customize.sh', 'first-start.sh', 'action.sh']}
    assert b'versionCode=12\n' in replacements['module.prop']
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            dst.writestr(copy.copy(info), replacements.get(info.filename, src.read(info.filename)))
        for name in ['first-start.sh', 'action.sh']:
            info = zipfile.ZipInfo(name, (2026, 10, 26, 0, 0, 0))
            info.external_attr = 0o100755 << 16
            dst.writestr(info, replacements[name], compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(output) as dst:
        assert dst.testzip() is None
        changed = [n for n in src.namelist() if src.read(n) != dst.read(n)]
        assert set(changed) == {'module.prop', 'service.sh', 'customize.sh'}
        manifest = {n: hashlib.sha256(dst.read(n)).hexdigest() for n in dst.namelist()}
record = dict(base_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),
              module_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
              changed=changed, added=['first-start.sh', 'action.sh'], manifest=manifest)
(output.parent / 'first-start-build.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k != 'manifest'}, indent=2))
