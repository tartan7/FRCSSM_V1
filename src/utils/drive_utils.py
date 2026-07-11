"""
ドライブ種別判定ユーティリティ
USBメモリ（リムーバブルメディア）かPC内蔵ドライブ（SATA/NVMe等）かを判定する
"""
import ctypes
import os

DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3


def is_removable_drive(path: str) -> bool:
    """指定パスが存在するドライブがリムーバブルメディア（USBメモリ等）か判定する"""
    try:
        drive = os.path.splitdrive(os.path.abspath(path))[0]
        if not drive:
            return False
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive + '\\')
        return drive_type == DRIVE_REMOVABLE
    except Exception:
        return False
