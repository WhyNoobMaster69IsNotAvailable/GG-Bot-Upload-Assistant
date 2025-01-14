from enum import Enum


class TorrentPieceSize(Enum):
    KB_16 = 16 * 1024  # 16 KiB
    KB_32 = 32 * 1024  # 32 KiB
    KB_64 = 64 * 1024  # 64 KiB
    MB_1 = 1 * 1024 * 1024  # 1 MiB
    MB_2 = 2 * 1024 * 1024  # 2 MiB
    MB_4 = 4 * 1024 * 1024  # 4 MiB
    MB_8 = 8 * 1024 * 1024  # 8 MiB
    MB_16 = 16 * 1024 * 1024  # 16 MiB
    MB_32 = 32 * 1024 * 1024  # 32 MiB
    MB_64 = 64 * 1024 * 1024  # 64 MiB
