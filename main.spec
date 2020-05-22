# -*- mode: python ; coding: utf-8 -*-

added_files = [
   ('README.md', '.'),
   ('globals.py', '.'),
   ('map.py', '.'),
   ('sprites.py', '.'),
   ('settings.yml', '.'),
   ('content', 'content'),
]

block_cipher = None

a = Analysis(['main.pyw'],
             pathex=['C:\\Users\\Jones\\Documents\\GitHub\\rpg-test'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='RPG Test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='C:\\Users\\Jones\\Documents\\GitHub\\rpg-test\\favicon.ico')

coll = COLLECT(exe,
         a.binaries,
         a.zipfiles,
         a.datas,
         strip=False,
         upx=True,
         upx_exclude=[],
         name='main')
