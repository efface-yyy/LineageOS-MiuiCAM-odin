"""Restore only the normal HEVC decoder's already supplied vendor 8K limits.
The actual device has independently decoded all 1629 frames of its 8K clip.
"""
from pathlib import Path
import re,hashlib,json,xml.etree.ElementTree as ET
reference=Path('evidence/device-media-codecs-system-default-lahaina.xml').read_text(encoding='utf-8')
pattern=r'<MediaCodec\s+name="c2\.qti\.hevc\.decoder"\s+type="video/hevc"[^>]*>.*?</MediaCodec>'
matches=re.findall(pattern,reference,re.S);assert len(matches)==1
block=matches[0]
assert 'max="7680x7680"' in block and 'range="36-138240"' in block
out=Path('work/codec-compat');out.mkdir(exist_ok=True)
records=[]
for name in ['media_codecs.xml','media_codecs_lahaina.xml']:
 src=Path('evidence')/('device-'+name.replace('_','-'))
 # Saved pulls use human-readable filenames.
 src=Path('evidence/device-media-codecs.xml' if name=='media_codecs.xml' else 'evidence/device-media-codecs-lahaina.xml')
 before=src.read_text(encoding='utf-8');assert len(re.findall(pattern,before,re.S))==1
 original=ET.fromstring(re.findall(pattern,before,re.S)[0])
 assert original.find("Limit[@name='size']").get('max')=='4096x2176'
 after=re.sub(pattern,lambda m:block,before,flags=re.S)
 ET.fromstring(after)
 dest=out/name;dest.write_text(after,encoding='utf-8',newline='\n')
 records.append({'file':name,'baseline_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'patched_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'change':'normal HEVC decoder block from existing official system_default_lahaina configuration'})
Path('evidence/codec-8k-config-patch.json').write_text(json.dumps(records,indent=2))
print(records)
