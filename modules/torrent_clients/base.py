from abc import ABC, abstractmethod
from typing import Optional, Dict, List


class GGBotTorrentClientTemplate(ABC):
    @abstractmethod
    def hello(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def upload_torrent(
        self,
        torrent_path: str,
        save_path: str,
        use_auto_torrent_management: bool,
        is_skip_checking: bool,
        category: Optional[str] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_torrent_category(
        self, info_hash: str, category_name: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_torrents(self) -> List[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def list_all_torrents(self) -> List[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def get_dynamic_trackers(self, torrent: Dict[str, str]) -> List[str]:
        raise NotImplementedError
