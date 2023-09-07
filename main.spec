# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['E:\\Documents\\Python_Scripts\\deploy_env\\local_xml_reader\\src\\main.py'],
    pathex=[],
    binaries=[('E:\\Documents\\Python_Scripts\\deploy_env\\local_xml_reader\\local_venv\\Lib\\site-packages\\pywin32_system32\\pythoncom39.dll', '.')],
    datas=[],
    hiddenimports=['win32com'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
