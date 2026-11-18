"""
Summary:
    チケット時系列タスクカード（世代管理・リスト順序インデックスPK）データアクセスモジュール。
Description:
    ticket_timeline_tasks テーブルに対するSQLiteデータベースアクセス処理（登録、論理削除、最新有効リビジョン検索）を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.database import fws_sqlite_util

from fws_apps.tkinter.fws_chat_template.businesses.entity import (
    fws_entity_chat_template_ticket_timeline_task,
)
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsDatabaseAccessChatTemplateTicketTimelineTask:
    """
    Summary:
        チケット時系列タスクカードデータアクセスクラス。
    Description:
        ticket_timeline_tasks テーブルへのアクセス（SQL発行および取得データ処理、CRUD操作）を担当します。
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
    ) -> list[fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask]:
        """
        Summary:
            指定された複合キーの最新有効リビジョンに属する時系列タスク一覧を取得します。
        Description:
            ticket_timeline_tasks テーブルから指定された複合キーかつ有効（is_deleted = 0）な最大 revision に紐づくレコードを
            item_number 昇順で取得し、Entityリストで返却します。存在しない場合は空リストを返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            list[fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask] - 時系列タスクエンティティのリスト。
        """
        sql_text: str = (
            "SELECT"
            "   ticket_number"
            "   ,prefecture"
            "   ,building_name"
            "   ,revision"
            "   ,item_number"
            "   ,task_template_id"
            "   ,category_name"
            "   ,task_name"
            "   ,task_time"
            "   ,memo"
            "   ,is_completed"
            "   ,is_deleted"
            "   ,created_at"
            "   ,updated_at "
            "FROM"
            "   ticket_timeline_tasks "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND is_deleted = 0 "
            "   AND revision = ("
            "       SELECT MAX(revision) FROM ticket_timeline_tasks"
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
            ticket_timeline_tasks テーブルから指定キーの MAX(revision) を取得します。
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
            "   ticket_timeline_tasks "
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

    def select_max_item_number(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
    ) -> int | None:
        """
        Summary:
            指定された複合キーおよびリビジョンにおける最大タスク連番（item_number）を取得します。
        Description:
            ticket_timeline_tasks テーブルから指定キーおよびリビジョンの MAX(item_number) を取得します。
            レコードが未登録の場合は None を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
        Returns:
            int | None - 最大タスク連番（レコード未存在時は None）。
        """
        sql_text: str = (
            "SELECT"
            "   MAX(item_number) "
            "FROM"
            "   ticket_timeline_tasks "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            max_item: Any = fws_sqlite_util_obj.execute_scalar(
                sql_text,
                (ticket_number, prefecture, building_name, revision),
            )
            return int(max_item) if max_item is not None else None

    def update_memo(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
        item_number: int,
        memo: str,
    ) -> None:
        """
        Summary:
            指定タスクのメモ文字列を更新します。
        Description:
            ticket_timeline_tasks テーブルの該当タスクレコードの memo および updated_at を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
            item_number: int - タスク連番。
            memo: str - 更新後メモ文字列。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_timeline_tasks "
            "SET"
            "   memo = ?"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
            "   AND item_number = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    memo,
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                    item_number,
                ),
            )

    def update_completed(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
        item_number: int,
        is_completed: int,
    ) -> None:
        """
        Summary:
            指定タスクの作業完了フラグを更新します。
        Description:
            ticket_timeline_tasks テーブルの該当タスクレコードの is_completed および updated_at を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
            item_number: int - タスク連番。
            is_completed: int - 作業完了フラグ（1: 完了、0: 未完了）。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_timeline_tasks "
            "SET"
            "   is_completed = ?"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
            "   AND item_number = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    is_completed,
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                    item_number,
                ),
            )

    def update_logical_delete_item(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        revision: int,
        item_number: int,
    ) -> None:
        """
        Summary:
            指定された単一タスクレコードを論理削除します。
        Description:
            ticket_timeline_tasks テーブルの該当タスクレコードの is_deleted を 1 に、updated_at を現在日時に更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            revision: int - リビジョン番号。
            item_number: int - タスク連番。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "UPDATE"
            "   ticket_timeline_tasks "
            "SET"
            "   is_deleted = 1"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND revision = ?"
            "   AND item_number = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    ticket_number,
                    prefecture,
                    building_name,
                    revision,
                    item_number,
                ),
            )

    def insert(
        self,
        entity: fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask,
    ) -> None:
        """
        Summary:
            新規チケット時系列タスクレコードを登録します。
        Description:
            ticket_timeline_tasks テーブルへ指定されたEntityのレコードを挿入します。
        Args:
            entity: fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask - 登録対象のタスクエンティティ。
        Returns:
            None - 戻り値なし。
        """
        sql_text: str = (
            "INSERT INTO"
            "   ticket_timeline_tasks ("
            "       ticket_number"
            "       ,prefecture"
            "       ,building_name"
            "       ,revision"
            "       ,item_number"
            "       ,task_template_id"
            "       ,category_name"
            "       ,task_name"
            "       ,task_time"
            "       ,memo"
            "       ,is_completed"
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
                    entity.item_number,
                    entity.task_template_id,
                    entity.category_name,
                    entity.task_name,
                    entity.task_time,
                    entity.memo,
                    entity.is_completed,
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
            指定された複合キーの時系列タスクを論理削除します。
        Description:
            ticket_timeline_tasks テーブルの指定された複合キーのレコードについて、
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
            "   ticket_timeline_tasks "
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
    ) -> fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask:
        """
        Summary:
            DB取得行データを時系列タスクEntityへマッピングします。
        Description:
            sqlite3.Row オブジェクトの各列を FwsEntityChatTemplateTicketTimelineTask の属性に設定して返却します。
        Args:
            row: Any - sqlite3.Row またはマッピング互換オブジェクト。
        Returns:
            fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask - マッピングされたタスクエンティティ。
        """
        return fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask(
            ticket_number=str(row["ticket_number"]),
            prefecture=str(row["prefecture"]),
            building_name=str(row["building_name"]),
            revision=int(row["revision"]),
            item_number=int(row["item_number"]),
            task_template_id=str(row["task_template_id"]),
            category_name=str(row["category_name"]),
            task_name=str(row["task_name"]),
            task_time=str(row["task_time"]),
            memo=str(row["memo"]),
            is_completed=int(row["is_completed"]),
            is_deleted=int(row["is_deleted"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
    #endregion
#endregion
