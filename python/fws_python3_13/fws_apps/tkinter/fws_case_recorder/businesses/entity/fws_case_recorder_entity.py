"""
Summary:
    fws_case_recorder アプリの状態管理エンティティモジュール。
Description:
    アプリケーション全体の状態（DBパス等）を保持します。
Attachment:
    なし
"""
from pathlib import Path
from typing import Optional

class FwsCaseRecorderEntity:
    """
    Summary:
        アプリケーション状態を保持するエンティティクラス。
    Description:
        現在のデータベースファイルパスなどのアプリ全体の状態を管理します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            アプリケーション状態を初期化します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.current_db_path: Optional[Path] = None
        """Optional[Path] - 現在接続しているデータベースのパス"""
    #endregion
