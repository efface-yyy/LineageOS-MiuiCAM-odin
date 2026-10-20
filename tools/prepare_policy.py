from pathlib import Path
rules=['allow priv_app_36 vendor_file dir { search getattr }','allow priv_app_36 vendor_file file { open read map execute getattr }','allow priv_app_36 vendor_camera_sensor_prop file { open read getattr map }','allow priv_app_36 vendor_display_prop file { open read getattr map }','allow priv_app_36 vendor_hal_camerapostproc_xiaomi_hwservice hwservice_manager find','allow priv_app_36 hal_camera_default binder { call transfer }','allow hal_camera_default priv_app_36 binder { call transfer }']
Path('work/module/sepolicy.rule').write_text('\n'.join(rules)+'\n',newline='\n')
Path('tools/apply_policy.sh').write_text('#!/system/bin/sh\n'+''.join('magiskpolicy --live "'+r+'"\n' for r in rules),newline='\n')
