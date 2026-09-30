"""
Summary:
    fws_source_linkerの表示用ロジックを担うモジュールです。
Description:
    ディレクトリ構造の取得や、Business層のEntityとView用のデータの変換を行います。
Attachment:
    なし
"""
from pathlib import Path

# app
from fws_apps.tkinter.fws_source_linker.businesses.business import fws_source_linker_business
from fws_apps.tkinter.fws_source_linker.businesses.entity import fws_source_linker_entity_config
from fws_apps.tkinter.fws_source_linker.constant import fws_source_linker_const


class FwsSourceLinkerLogic:
    """
    Summary:
        ViewとBusinessを繋ぐロジッククラス。
    Description:
        ディレクトリ一覧の取得、設定の変換などを行います。
    """

    # region Constructor
    def __init__(self) -> None:
        """
        Summary:
            FwsSourceLinkerLogicを初期化します。
        """
        self._fws_source_linker_business_obj: fws_source_linker_business.FwsSourceLinkerBusiness = fws_source_linker_business.FwsSourceLinkerBusiness()
    # endregion

    # region Public Methods
    def get_config(self) -> dict:
        """
        Summary:
            Business層から設定情報を取得し、辞書形式で返します。
        Args:
            なし
        Returns:
            dict - root_dir, root_dir_history, dest_dirをキーとする辞書。
        """
        entity: fws_source_linker_entity_config.FwsSourceLinkerEntityConfig = self._fws_source_linker_business_obj.get_config()
        return {
            "root_dir": entity.root_dir,
            "root_dir_history": entity.root_dir_history,
            "dest_dir": entity.dest_dir,
            "dest_dir_history": entity.dest_dir_history,
            "dest_sub_dir": entity.dest_sub_dir
        }

    def save_config(self, root_dir: str, root_dir_history: list[str], 
                    dest_dir: str, dest_dir_history: list[str], dest_sub_dir: str) -> None:
        """
        Summary:
            設定情報をBusiness層に渡して保存します。
        Args:
            root_dir: str - 起点ディレクトリ。
            root_dir_history: list[str] - 履歴リスト。
            dest_dir: str - コピー先ディレクトリ。
            dest_dir_history: list[str] - コピー先履歴リスト。
            dest_sub_dir: str - コピー先のサブディレクトリ。
        Returns:
            None
        """
        entity = fws_source_linker_entity_config.FwsSourceLinkerEntityConfig(
            root_dir=root_dir,
            root_dir_history=root_dir_history,
            dest_dir=dest_dir,
            dest_dir_history=dest_dir_history,
            dest_sub_dir=dest_sub_dir
        )
        self._fws_source_linker_business_obj.save_config(entity)

    def add_to_history(self, path: str, current_history: list[str]) -> list[str]:
        """
        Summary:
            指定パスが読み込み可能な場合に履歴の先頭に追加します。
        Args:
            path: str - 追加するパス。
            current_history: list[str] - 現在の履歴リスト。
        Returns:
            list[str] - 更新された履歴リスト。
        """
        if not path:
            return current_history
            
        p = Path(path)
        if not (p.exists() and p.is_dir()):
            return current_history
            
        new_history = [h for h in current_history if h != path]
        new_history.insert(0, path)
        return new_history[:fws_source_linker_const.MAX_HISTORY_COUNT]

    def get_directory_contents(self, path: str) -> list[tuple[str, str, str]]:
        """
        Summary:
            指定パスのディレクトリ内容を取得します。
        Args:
            path: str - ディレクトリパス。
        Returns:
            list[tuple[str, str, str]] - (フルパス, 表示名, 'dir'または'file') のリスト。
        """
        contents: list[tuple[str, str, str]] = []
        try:
            p: Path = Path(path)
            if not p.exists() or not p.is_dir():
                return contents
                
            for item in p.iterdir():
                type_str: str = "dir" if item.is_dir() else "file"
                contents.append((str(item.resolve()), item.name, type_str))
            
            # ディレクトリ優先でソート
            contents.sort(key=lambda x: (0 if x[2] == "dir" else 1, x[1].lower()))
        except Exception:
            pass # アクセス権限等
            
        return contents

    def execute_copy(self, items: list[str], dest_dir: str) -> list[str]:
        """
        Summary:
            コピー処理を実行します。
        Args:
            items: list[str] - コピー元のパスリスト。
            dest_dir: str - コピー先のディレクトリ。
        Returns:
            list[str] - 同名競合のためスキップされたアイテム。
        """
        return self._fws_source_linker_business_obj.copy_items(items, dest_dir)

    def execute_force_copy(self, items: list[str], dest_dir: str) -> None:
        """
        Summary:
            強制コピー処理を実行します。
        Args:
            items: list[str] - コピー元のパスリスト。
            dest_dir: str - コピー先のディレクトリ。
        Returns:
            None
        """
        self._fws_source_linker_business_obj.force_copy_items(items, dest_dir)
    # endregion
