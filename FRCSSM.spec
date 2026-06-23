# -*- mode: python ; coding: utf-8 -*-
# FRCSSM_V1 PyInstaller spec
# USB ポータブル運用用: onedir モードでビルドする

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

# xlwings の全リソースを収集
xlwings_datas, xlwings_binaries, xlwings_hiddenimports = collect_all('xlwings')

# TkEasyGUI の全リソースを収集
tkeasygui_datas, tkeasygui_binaries, tkeasygui_hiddenimports = collect_all('TkEasyGUI')

# comtypes の全サブモジュールを収集
comtypes_hiddenimports = collect_submodules('comtypes')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[
        'src',        # src 直下モジュール(config, calenderdialog 等)を解決
    ],
    binaries=xlwings_binaries + tkeasygui_binaries,
    datas=[
        # src 以下の Python パッケージ群をそのまま同梱
        ('src', 'src'),
        # xlwings / TkEasyGUI のデータファイル
        *xlwings_datas,
        *tkeasygui_datas,
    ],
    hiddenimports=[
        # xlwings が動的インポートするモジュール
        'xlwings._xlwindows',
        'xlwings.pro',
        # comtypes COM 関連
        'comtypes.client',
        'comtypes.automation',
        'comtypes.typeinfo',
        'comtypes.server',
        'comtypes.server.automation',
        'comtypes.server.localserver',
        # Python 標準 (frozen 環境で欠落しやすい)
        'configparser',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        # psutil (メモリ監視)
        'psutil',
        # その他
        'PIL._tkinter_finder',
        *xlwings_hiddenimports,
        *tkeasygui_hiddenimports,
        *comtypes_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 不要なモジュールを除外してサイズ削減
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
        'unittest',
        'IPython',
        'jupyter',
    ],
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
    name='FRCSSM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,           # UPX 圧縮は xlwings との相性問題を避けるため無効
    console=False,        # コンソールウィンドウを表示しない
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='FRCSSM',       # dist/FRCSSM/ フォルダが生成される
)
