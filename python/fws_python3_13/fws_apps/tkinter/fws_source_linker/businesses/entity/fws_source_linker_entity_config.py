"""
Summary:
    設定情報を保持するEntityクラスです。
Description:
    保存されている起点ディレクトリやコピー先ディレクトリのパスを保持します。
"""
from dataclasses import dataclass, field

@dataclass
class FwsSourceLinkerEntityConfig:
    """
    Summary:
        設定情報を保持するデータクラス。
    Description:
        root_dir: 起点ディレクトリのパス
        root_dir_history: 起点ディレクトリの入力履歴リスト
        dest_dir: コピー先のディレクトリパス
        dest_dir_history: コピー先の入力履歴リスト
        dest_sub_dir: コピー先のサブディレクトリ
    """
    root_dir: str = ""
    root_dir_history: list[str] = field(default_factory=list)
    dest_dir: str = ""
    dest_dir_history: list[str] = field(default_factory=list)
    dest_sub_dir: str = ""
