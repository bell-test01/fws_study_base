"""
Summary:
    チケット時系列タスクチェックリスト状態データアクセスモジュール。
Description:
    ticket_timeline_task_checklists テーブルに対するSQLiteデータベースアクセス処理（登録、論理削除、最新有効リビジョン検索）を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.database import fws_sqlite_util

from fws_apps.tkinter.fws_chat_template.businesses.entity import (
    fws_entity_chat_template_ticket_timeline_checklist,
)
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsDatabaseAccessChatTemplateTicketTimelineChecklist:
    """
    Summary:
        チケット時系列タスクチェックリスト状態データアクセスクラス。
    Description:
        ticket_timeline_task_checklists テーブルへのアクセス（SQL発行および取得データ処理、CRUD操作）を担当します。
    """

    #region Constructor
    def __init__(self, db_path: Path | None = None) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            対象のデータベースパスを保持して初期化します。
        Args:
            db_path: Path | None - データベースファイルパス（省略時は fws_const_chat_template.PATH_APP_DB_FILE）。
        Returns:
            None - 戻り値なし。
        """
        self._db_path: Path = (
            db_path if db_path is not None and str(db_path) else fws_const_chat_template.PATH_APP_DB_FILE
        )
        """Path - データベースファイルパス"""
    #endregion

    #region Public Methods
    def select_latest_by_ticket(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> list[fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist]:
        """
        Summary:
            指定された複合キーの最新有効リビジョンに属する全チェックリスト状態一覧を取得します。
        Description:
            ticket_timeline_task_checklists テーブルから指定された複合キーかつ有効（is_deleted = 0）な最大 revision に紐づくレコードを
            task_item_number 昇順、item_seq 昇順で取得し、Entityリストで返却します。存在しない場合は空リストを返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            list[fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist] - チェックリストエンティティのリスト。
        """
        sql_text: str = (
            "SELECT"
            "   ticket_number"
            "   ,prefecture"
            "   ,building_name"
            "   ,revision"
            "   ,task_item_number"
            "   ,item_seq"
            "   ,checklist_template_id"
            "   ,extra_builder"
            "   ,extra_data"
            "   ,display_text"
            "   ,append_text"
            "   ,is_checked"
            "   ,is_deleted"
            "   ,created_at"
            "   ,updated_at "
            "FROM"
            "   ticket_timeline_task_checklists "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND is_deleted = 0 "
            "   AND revision = ("
            "       SELECT MAX(revision) FROM ticket_timeline_task_checklists"
            "       WHERE ticket_number = ?"
            "         AND prefecture = ?"
            "         AND building_name = ?"
            "         AND is_deleted = 0"
            "   ) "
            "ORDER BY"
            "   task_item_number ASC"
            "   ,item_seq ASC"
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

    def insert(
        self,
        entity: fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist,
    ) -> None:
        """
        Summary:
            新規チケット時系列タスクチェックリスト状態レコードを登録します。
        Description:
            ticket_timeline_task_checklists テーブルへ指定されたEntityのレコードを挿入します。
        Args:
            entity: fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist - 登録対象のチェックリストエンティティ。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "INSERT INTO"
            "   ticket_timeline_task_checklists ("
            "       ticket_number"
            "       ,prefecture"
            "       ,building_name"
            "       ,revision"
            "       ,task_item_number"
            "       ,item_seq"
            "       ,checklist_template_id"
            "       ,extra_builder"
            "       ,extra_data"
            "       ,display_text"
            "       ,append_text"
            "       ,is_checked"
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
            "   ,?"
            "   ,?"
            "   ,?"
            ")"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    entity.ticket_number,
                    entity.prefecture,
                    entity.building_name,
                    entity.revision,
                    entity.task_item_number,
                    entity.item_seq,
                    entity.checklist_template_id,
                    entity.extra_builder,
                    entity.extra_data,
                    entity.display_text,
                    entity.append_text,
                    entity.is_checked,
                    entity.is_deleted,
                ),
            )

    def update_logical_delete(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int | None = None,
    ) -> None:
        """
        Summary:
            指定された複合キーのチェックリスト状態を論理削除します。
        Description:
            ticket_timeline_task_checklists テーブルの指定された複合キーのレコードについて、
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
            "   ticket_timeline_task_checklists "
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

    def update_check_status(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
        task_item_number: int,
        item_seq: int,
        is_checked: int,
    ) -> None:
        """
        Summary:
            指定チェック項目のチェック状態を更新します。
        Description:
            ticket_timeline_task_checklists テーブルの該当レコードの is_checked および updated_at を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
            task_item_number: int - 親タスク連番。
            item_seq: int - チェック項目連番。
            is_checked: int - チェック状態（1: ON、0: OFF）。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_timeline_task_checklists "
            "SET"
            "   is_checked = ?"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
            "   AND task_item_number = ?"
            "   AND item_seq = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    is_checked,
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                    task_item_number,
                    item_seq,
                ),
            )

    def update_logical_delete_by_task(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
        task_item_number: int,
    ) -> None:
        """
        Summary:
            指定された単一タスクに紐づく全チェックリストレコードを論理削除します。
        Description:
            ticket_timeline_task_checklists テーブルの該当タスクに属する全チェック項目の is_deleted を 1 に、updated_at を現在日時に更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
            task_item_number: int - 親タスク連番。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_timeline_task_checklists "
            "SET"
            "   is_deleted = 1"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
            "   AND task_item_number = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                    task_item_number,
                ),
            )

    def update_extra_data(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
        task_item_number: int,
        item_seq: int,
        extra_data: str,
    ) -> None:
        """
        Summary:
            指定チェック項目の補足UI入力データ（JSON）を更新します。
        Description:
            ticket_timeline_task_checklists テーブルの該当レコードの extra_data および updated_at を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
            task_item_number: int - 親タスク連番。
            item_seq: int - チェック項目連番。
            extra_data: str - 補足UI入力データ（JSON文字列）。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_timeline_task_checklists "
            "SET"
            "   extra_data = ?"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
            "   AND task_item_number = ?"
            "   AND item_seq = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    extra_data,
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                    task_item_number,
                    item_seq,
                ),
            )
    #endregion

    #region Private Methods
    def _map_row_to_entity(
        self,
        row: Any,
    ) -> fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist:
        """
        Summary:
            DB取得行データをチェックリストEntityへマッピングします。
        Description:
            sqlite3.Row オブジェクトの各列を FwsEntityChatTemplateTicketTimelineChecklist の属性に設定して返却します。
        Args:
            row: Any - sqlite3.Row またはマッピング互換オブジェクト。
        Returns:
            fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist - マッピングされたチェックリストエンティティ。
        """
        return fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist(
            ticket_number=str(row["ticket_number"]),
            prefecture=str(row["prefecture"]),
            building_name=str(row["building_name"]),
            revision=int(row["revision"]),
            task_item_number=int(row["task_item_number"]),
            item_seq=int(row["item_seq"]),
            checklist_template_id=str(row["checklist_template_id"]),
            extra_builder=str(row["extra_builder"]),
            extra_data=str(row["extra_data"]),
            display_text=str(row["display_text"]),
            append_text=str(row["append_text"]),
            is_checked=int(row["is_checked"]),
            is_deleted=int(row["is_deleted"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
    #endregion
#endregion
