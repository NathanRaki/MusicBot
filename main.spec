# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( '.\extensions\incognito.zip', 'extensions' ),
         ( '.\chromedriver.exe', '.' ),
         ( '.\\napster.png', '.' )
         ]

a = Analysis(['main.py', 'bot.py', 'bot_window.py', 'logger.py', 'login_window.py', 'methods.py', 'napster_thread.py', 'napster_user.py', 'scroll.py'],
             pathex=['C:\\Users\\natha\\Desktop\\napster'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='OmegaMM v1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
