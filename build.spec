# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# 项目根目录
root_dir = Path(__file__).parent

# 需要包含的额外文件
added_files = [
    (str(root_dir / "style"), "style"),           # 样式文件
    (str(root_dir / "icons"), "icons"),           # 图标文件
    (str(root_dir / "data"), "data"),             # 数据目录（确保存在）
]

# 主程序入口
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,  # 包含额外文件
    hiddenimports=[
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyd = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyd,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TodoManager',                     # 生成的 exe 名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                           # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/app.ico',                   # 程序图标
)

# ===== 打包成单个文件（可选） =====
# 如果使用 --onefile 模式，用下面这个代替上面的 EXE
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='TodoManager',
# )
