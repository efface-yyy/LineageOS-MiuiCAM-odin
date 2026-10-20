from pathlib import Path
import re, shutil, zipfile

p=Path('work/smali14-1/com/android/camera/lib/compatibility/util/CompatibilityUtils.smali')
backup=p.with_suffix('.smali.before_trace')
if not backup.exists(): shutil.copy2(p,backup)
s=backup.read_text()
m=re.search(r'(?ms)^\.method public static createCaptureSessionWithSessionConfiguration\(.*?^\.end method',s)
assert m
body=m.group()
mark='    new-instance v0, Landroid/hardware/camera2/params/SessionConfiguration;'
assert body.count(mark)==1
hook='    invoke-static {p4, p3, p1}, Lcom/odin/compat/SessionTrace;->record(Landroid/hardware/camera2/CaptureRequest;Ljava/util/List;I)V\n\n'
s=s[:m.start()]+body.replace(mark,hook+mark)+s[m.end():]
p.write_text(s,newline='\n')
print('Metadata-only trace hook prepared')
