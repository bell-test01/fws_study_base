"""
Summary:
    チケット機器明細情報（世代管理・リスト順序インデックスPK）データアクセスモジュール。
Description:
    ticket_devices テーブルに対するSQLiteデータベースアクセス処理（登録、論理削除、最新有効リビジョン検索）を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.database import fws_sqlite_util

from fws_apps.tkinter.fws_chat_template.businesses.entity import (
    fws_entity_chat_template_ticket_device,
)
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsDatabaseAccessChatTemplateTicketDevice:
    """
    Summary:
        チケット機器明細情報データアクセスクラス。
    Description:
        ticket_devices テーブルへのアクセス（SQL発行および取得データ処理、CRUD操作）を担当します。
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
    def select_latest_by_ticket(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> list[fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice]:
        """
        Summary:
            指定された複合キーの最新有効リビジョンに属する機器明細一覧を取得します。
        Description:
            ticket_devices テーブルから指定された複合キーかつ有効（is_deleted = 0）な最大 revision に紐づくレコードを
            item_number 昇順で取得し、Entityリストで返却します。存在しない場合は空リストを返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            list[fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice] - 機器明細エンティティのリスト。
        """
        sql_text: str = (
            "SELECT"
            "   ticket_number"
            "   ,prefecture"
            "   ,building_name"
            "   ,revision"
            "   ,item_number"
            "   ,rack_name"
            "   ,hostname"
            "   ,model_name"
            "   ,serial_number"
            "   ,is_deleted"
            "   ,created_at"
            "   ,updated_at "
            "FROM"
            "   ticket_devices "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND is_deleted = 0 "
            "   AND revision = ("
            "       SELECT MAX(revision) FROM ticket_devices"
            "       WHERE ticket_number = ?"
            "         AND prefecture = ?"
            "         AND building_name = ?"
            "         AND is_deleted = 0"
            "   ) "
            "ORDER BY"
            "   item_number ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (
                    ticket_number,
                    prefecture,
                    building_name,
                    ticket_number,
                    prefecture,
                    building_name,
                ),
            )
            return [self._map_row_to_entity(row) for row in rows]

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
            ticket_devices テーブルから指定キーの MAX(revision) を取得します。
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
            "   ticket_devices "
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
        entity: fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice,
    ) -> bool:
        """
        Summary:
            新規チケット機器明細情報レコードを登録します。
        Description:
            ticket_devices テーブルへ指定されたEntity（リビジョン番号、明細インデックス、論理削除フラグを含む）を挿入します。
        Args:
            entity: fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice - 登録対象の機器明細エンティティ。
        Returns:
            bool - 登録に成功した場合は True、失敗した場合は False。
        """
        sql_text: str = (
            "INSERT INTO"
            "   ticket_devices ("
            "       ticket_number"
            "       ,prefecture"
            "       ,building_name"
            "       ,revision"
            "       ,item_number"
            "       ,rack_name"
            "       ,hostname"
            "       ,model_name"
            "       ,serial_number"
            "       ,is_deleted"
            "   )"
            "VALUES ("
            "   ?"
            "   ,?"
            "   ,?"
            "   ,?"
            "   ,?"
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
                    entity.item_number,
                    entity.rack_name,
                    entity.hostname,
                    entity.model_name,
                    entity.serial_number,
                    entity.is_deleted,
                ),
            )
            return row_count > 0

    def update_logical_delete(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int | None = None,
    ) -> None:
        """
        Summary:
            指定された複合キーの機器明細を論理削除します。
        Description:
            ticket_devices テーブルの指定された複合キーのレコードについて、
            revision が指定された場合はそのリビジョンのみ、省略された場合は全リビジョンの
            is_deleted を 1 に、updated_at を現在日時に更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int | None - 対象リビジョン番号（デフォルト: None。None の場合は全リビジョン対象）。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_devices "
            "SET"
            "   is_deleted = 1"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND (? IS NULL OR revision = ?)"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                    revision,
                ),
            )
    #endregion

    #region Private Methods
    def _map_row_to_entity(
        self,
        row: Any,
    ) -> fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice:
        """
        Summary:
            DB取得行データを機器明細Entityへマッピングします。
        Description:
            sqlite3.Row オブジェクトの各列を FwsEntityChatTemplateTicketDevice の属性に設定して返却します。
        Args:
            row: Any - sqlite3.Row またはマッピング互換オブジェクト。
        Returns:
            fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice - マッピングされた機器明細エンティティ。
        """
        return fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice(
            ticket_number=str(row["ticket_number"]),
            prefecture=str(row["prefecture"]),
            building_name=str(row["building_name"]),
            revision=int(row["revision"]),
            item_number=int(row["item_number"]),
            rack_name=str(row["rack_name"]),
            hostname=str(row["hostname"]),
            model_name=str(row["model_name"]),
            serial_number=str(row["serial_number"]),
            is_deleted=int(row["is_deleted"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
    #endregion
#endregion
