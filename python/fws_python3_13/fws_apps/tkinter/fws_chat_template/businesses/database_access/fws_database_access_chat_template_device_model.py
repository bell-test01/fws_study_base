"""
Summary:
    機器機種マスタデータアクセスモジュール。
Description:
    mst_device_models テーブルに対するSQLiteデータベースアクセス処理（機種名一覧取得等）を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.database import fws_sqlite_util

from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsDatabaseAccessChatTemplateDeviceModel:
    """
    Summary:
        機器機種マスタデータアクセスクラス。
    Description:
        mst_device_models テーブルへのアクセス（SQL発行および取得データ処理）を担当します。
    """

    #region Constructor
    def __init__(self, db_path: Path = fws_const_chat_template.PATH_APP_DB_FILE) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            対象のデータベースパスを保持して初期化します。
        Args:
            db_path: Path - データベースファイルパス（デフォルト: PATH_APP_DB_FILE）。
        Returns:
            None - 戻り値なし。
        """
        self._db_path: Path = db_path
        """Path - データベースファイルパス"""
    #endregion

    #region Public Methods
    def select_model_names(self) -> list[str]:
        """
        Summary:
            機器機種名一覧を取得します。
        Description:
            mst_device_models テーブルから sort_order 昇順で機器機種名を取得し、リストで返却します。
        Args:
            なし
        Returns:
            list[str] - 機器機種名のリスト。
        """
        sql_text: str = (
            "SELECT model_name "
            "FROM mst_device_models "
            "ORDER BY sort_order ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(sql_text)
            return [str(row["model_name"]) for row in rows]
    #endregion
#endregion
