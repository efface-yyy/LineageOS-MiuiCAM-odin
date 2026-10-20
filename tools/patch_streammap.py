from pathlib import Path
import re, shutil, zipfile
p = Path('work/smali14-2/com/xiaomi/compat/camera2/CameraConstructCompat.smali')
s = p.read_text()
backup = p.with_suffix('.smali.original')
if not backup.exists():
    shutil.copy2(p, backup)
else:
    s = backup.read_text()
m = re.search(r'(?ms)^\.method public static getStreamConfigurationMap\(.*?^\.end method', s)
assert m
header = m.group().splitlines()[0]
body = [header, '    .registers 21', '    const/16 v0, 0xf', '    new-array v0, v0, [Ljava/lang/Object;']
for i in range(14):
    body += [f'    const/16 v1, {i}', f'    aput-object p{i}, v0, v1']
body += ['    invoke-static/range {p14 .. p14}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;',
         '    move-result-object v2', '    const/16 v1, 14', '    aput-object v2, v0, v1',
         '    invoke-static {v0}, Lcom/odin/compat/StreamMapBridge;->build([Ljava/lang/Object;)Ljava/lang/Object;',
         '    move-result-object v0', '    check-cast v0, Landroid/hardware/camera2/params/StreamConfigurationMap;',
         '    return-object v0', '.end method']
p.write_text(s[:m.start()] + '\n'.join(body) + s[m.end():], newline='\n')
print('Replaced only CameraConstructCompat.getStreamConfigurationMap adapter')
