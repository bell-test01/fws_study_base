"""
Summary:
    チケット詳細テキスト（本文・世代管理）データアクセスモジュール。
Description:
    ticket_descriptions テーブルに対するSQLiteデータベースアクセス処理（登録、論理削除、最新検索）を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.database import fws_sqlite_util

from fws_apps.tkinter.fws_chat_template.businesses.entity import (
    fws_entity_chat_template_ticket_description,
)
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsDatabaseAccessChatTemplateTicketDescription:
    """
    Summary:
        チケット詳細テキスト（本文・世代管理）データアクセスクラス。
    Description:
        ticket_descriptions テーブルへのアクセス（SQL発行および取得データ処理、CRUD操作）を担当します。
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
    def select_latest(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription | None:
        """
        Summary:
            指定された複合キーの最新有効リビジョンの詳細テキスト情報を取得します。
        Description:
            ticket_descriptions テーブルから指定キーかつ is_deleted = 0 のレコードを revision 降順で検索し、
            最新の1件を Entity へマッピングして返却します。存在しない場合は None を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription | None - 詳細テキストエンティティ、または存在しない場合は None。
        """
        sql_text: str = (
            "SELECT"
            "   ticket_number"
            "   ,prefecture"
            "   ,building_name"
            "   ,revision"
            "   ,description"
            "   ,is_deleted"
            "   ,created_at"
            "   ,updated_at "
            "FROM"
            "   ticket_descriptions "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND is_deleted = 0 "
            "ORDER BY"
            "   revision DESC "
            "LIMIT 1"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (ticket_number, prefecture, building_name),
            )
            if not rows:
                return None
            return self._map_row_to_entity(rows[0])

    def select_max_revision(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> int:
        """
        Summary:
            指定された複合キーの最大リビジョン番号を取得します。
        Description:
            ticket_descriptions テーブルから指定キーの MAX(revision) を取得します。
            レコードが未登録の場合は 0 を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            int - 最大リビジョン番号（未登録時は 0）。
        """
        sql_text: str = (
            "SELECT"
            "   MAX(revision) "
            "FROM"
            "   ticket_descriptions "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            max_rev: Any = fws_sqlite_util_obj.execute_scalar(
                sql_text,
                (ticket_number, prefecture, building_name),
            )
            return int(max_rev or 0)

    def insert(
        self,
        entity: fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription,
    ) -> bool:
        """
        Summary:
            新規チケット詳細テキストレコードを登録します。
        Description:
            ticket_descriptions テーブルへ指定されたEntity（リビジョン番号、論理削除フラグを含む）を挿入します。
        Args:
            entity: fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription - 登録対象の詳細テキストエンティティ。
        Returns:
            bool - 登録に成功した場合は True、失敗した場合は False。
        """
        sql_text: str = (
            "INSERT INTO"
            "   ticket_descriptions ("
            "       ticket_number"
            "       ,prefecture"
            "       ,building_name"
            "       ,revision"
            "       ,description"
            "       ,is_deleted"
            "   )"
            "VALUES ("
            "   ?"
            "   ,?"
            "   ,?"
            "   ,?"
            "   ,?"
            "   ,?"
            ")"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            row_count: int = fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    entity.ticket_number,
                    entity.prefecture,
                    entity.building_name,
                    entity.revision,
                    entity.description,
                    entity.is_deleted,
                ),
            )
            return row_count > 0

    def update_logical_delete(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
    ) -> int:
        """
        Summary:
            指定された複合キーおよびリビジョンのレコードを論理削除します。
        Description:
            ticket_descriptions テーブルの指定レコードの is_deleted を 1 に、updated_at を現在日時に更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
        Returns:
            int - 更新された行数。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_descriptions "
            "SET"
            "   is_deleted = 1"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            row_count: int = fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                ),
            )
            return row_count
    #endregion

    #region Private Methods
    def _map_row_to_entity(
        self,
        row: Any,
    ) -> fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription:
        """
        Summary:
            DB取得行データを詳細テキストEntityへマッピングします。
        Description:
            sqlite3.Row オブジェクトの各列を FwsEntityChatTemplateTicketDescription の属性に設定して返却します。
        Args:
            row: Any - sqlite3.Row またはマッピング互換オブジェクト。
        Returns:
            fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription - マッピングされた詳細テキストエンティティ。
        """
        return fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription(
            ticket_number=str(row["ticket_number"]),
            prefecture=str(row["prefecture"]),
            building_name=str(row["building_name"]),
            revision=int(row["revision"]),
            description=str(row["description"]),
            is_deleted=int(row["is_deleted"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
    #endregion
#endregion
