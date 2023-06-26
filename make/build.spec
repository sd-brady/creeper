# -*- mode: python ; coding: utf-8 -*-
import gmsh
from os import path
#import PyInstaller.config

# Specify the location of the build and dist folders that are generated
# when running pyinstaller
#PyInstaller.config.CONF['workpath'] = "../"
#PyInstaller.config.CONF['distpath'] = "../"

# get the location of the gmsh dll which sits next to the gmsh.py file
libname = 'gmsh-4.11.dll'
bundle_dir = path.dirname(path.abspath(path.dirname(gmsh.__file__)))
path_gmsh_dll = path.join(bundle_dir, libname)

print('Adding {} to binaries'.format(path_gmsh_dll))

block_cipher = None


a = Analysis(
    ['../src/run.py'],
    pathex=[],
    binaries=[(str(path_gmsh_dll), '.')],
    datas=[],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='Weaver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Weaver v1.0',
)
