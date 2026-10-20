from pathlib import Path
src=Path('work/hyper14/vendor_a/lib64/libwa_sat.so')
d=src.read_bytes()
old=b'/system/lib64\0';new=b'/vendor/lib64\0'
assert d.count(old)==1
Path('work/libwa_sat-compat.so').write_bytes(d.replace(old,new))
print('SAT allocator path adapted; algorithm instructions untouched')
