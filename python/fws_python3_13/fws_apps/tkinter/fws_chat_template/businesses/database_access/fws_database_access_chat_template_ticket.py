"""
Summary:
    チケット基本情報（ヘッダ）データアクセスモジュール。
Description:
    tickets テーブルに対するSQLiteデータベースアクセス処理（登録、更新、検索）を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.database import fws_sqlite_util

from fws_apps.tkinter.fws_chat_template.businesses.entity import fws_entity_chat_template_ticket
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsDatabaseAccessChatTemplateTicket:
    """
    Summary:
        チケット基本情報（ヘッダ）データアクセスクラス。
    Description:
        tickets テーブルへのアクセス（SQL発行および取得データ処理、CRUD操作）を担当します。
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
    def select_all_ticket_numbers(self) -> list[str]:
        """
        Summary:
            全チケット番号一覧を取得します。
        Description:
            tickets テーブルから重複を除いたチケット番号を昇順で取得し、リストで返却します。
        Args:
            なし
        Returns:
            list[str] - チケット番号の文字列リスト。
        """
        sql_text: str = (
            "SELECT DISTINCT"
            "   ticket_number "
            "FROM"
            "   tickets "
            "WHERE"
            "   is_deleted = 0 "
            "ORDER BY"
            "   ticket_number ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(sql_text)
            return [str(row["ticket_number"]) for row in rows]

    def select_prefectures_by_ticket_number(self, ticket_number: str) -> list[str]:
        """
        Summary:
            指定されたチケット番号に紐づく県域一覧を取得します。
        Description:
            tickets テーブルから指定された ticket_number の重複を除いた県域を昇順で取得し、リストで返却します。
        Args:
            ticket_number: str - チケット管理番号。
        Returns:
            list[str] - 県域の文字列リスト。
        """
        sql_text: str = (
            "SELECT DISTINCT"
            "   prefecture "
            "FROM"
            "   tickets "
            "WHERE"
            "   ticket_number = ?"
            "   AND is_deleted = 0 "
            "ORDER BY"
            "   prefecture ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(sql_text, (ticket_number,))
            return [str(row["prefecture"]) for row in rows]

    def select_building_names_by_ticket_number(self, ticket_number: str, prefecture: str) -> list[str]:
        """
        Summary:
            指定されたチケット番号および県域に紐づくビル名一覧を取得します。
        Description:
            tickets テーブルから指定された ticket_number および prefecture の重複を除いたビル名を昇順で取得し、リストで返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
        Returns:
            list[str] - ビル名の文字列リスト。
        """
        sql_text: str = (
            "SELECT DISTINCT"
            "   building_name "
            "FROM"
            "   tickets "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND is_deleted = 0 "
            "ORDER BY"
            "   building_name ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(sql_text, (ticket_number, prefecture))
            return [str(row["building_name"]) for row in rows]

    def select_tickets_filter(
        self,
        ticket_number: str = "",
        prefecture: str = "",
        building_name: str = "",
    ) -> list[dict[str, str]]:
        """
        Summary:
            条件に一致するチケット基本情報のユニーク一覧を取得します。
        Description:
            ticket_number, prefecture, building_name の各条件（空文字時は全件対象）で tickets テーブルを検索し、
            重複を除いたレコードを辞書リストで返却します。論理削除されたレコードは除外されます。
        Args:
            ticket_number: str - チケット管理番号（未指定時は空文字）。
            prefecture: str - 都道府県（未指定時は空文字）。
            building_name: str - 物件名（未指定時は空文字）。
        Returns:
            list[dict[str, str]] - チケット基本情報辞書リスト（ticket_number, prefecture, building_name）。
        """
        sql_text: str = (
            "SELECT DISTINCT"
            "   ticket_number"
            "   ,prefecture"
            "   ,building_name "
            "FROM"
            "   tickets "
            "WHERE"
            "   (? = '' OR ticket_number = ?)"
            "   AND (? = '' OR prefecture = ?)"
            "   AND (? = '' OR building_name = ?)"
            "   AND is_deleted = 0 "
            "ORDER BY"
            "   ticket_number ASC"
            "   ,prefecture ASC"
            "   ,building_name ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (ticket_number, ticket_number, prefecture, prefecture, building_name, building_name),
            )
            return [
                {
                    "ticket_number": str(row["ticket_number"]),
                    "prefecture": str(row["prefecture"]),
                    "building_name": str(row["building_name"]),
                }
                for row in rows
            ]

    def select_distinct_ticket_numbers(
        self,
        ticket_number: str = "",
        prefecture: str = "",
        building_name: str = "",
    ) -> list[str]:
        """
        Summary:
            条件に一致するチケット番号の重複排除（DISTINCT）一覧を取得します。
        Description:
            ticket_number, prefecture, building_name の各条件（空文字時は全件対象）で tickets テーブルを検索し、
            重複を除いたチケット番号を昇順で取得してリストで返却します。論理削除されたレコードは除外されます。
        Args:
            ticket_number: str - チケット管理番号（未指定時は空文字）。
            prefecture: str - 都道府県（未指定時は空文字）。
            building_name: str - 物件名（未指定時は空文字）。
        Returns:
            list[str] - 重複を除いたチケット番号の文字列リスト。
        """
        sql_text: str = (
            "SELECT DISTINCT"
            "   ticket_number "
            "FROM"
            "   tickets "
            "WHERE"
            "   (? = '' OR ticket_number = ?)"
            "   AND (? = '' OR prefecture = ?)"
            "   AND (? = '' OR building_name = ?)"
            "   AND is_deleted = 0 "
            "ORDER BY"
            "   ticket_number ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (ticket_number, ticket_number, prefecture, prefecture, building_name, building_name),
            )
            return [str(row["ticket_number"]) for row in rows]

    def select_distinct_prefectures(
        self,
        ticket_number: str = "",
        prefecture: str = "",
        building_name: str = "",
    ) -> list[str]:
        """
        Summary:
            条件に一致する県域の重複排除（DISTINCT）一覧を取得します。
        Description:
            ticket_number, prefecture, building_name の各条件（空文字時は全件対象）で tickets テーブルを検索し、
            重複を除いた県域を昇順で取得してリストで返却します。論理削除されたレコードは除外されます。
        Args:
            ticket_number: str - チケット管理番号（未指定時は空文字）。
            prefecture: str - 都道府県（未指定時は空文字）。
            building_name: str - 物件名（未指定時は空文字）。
        Returns:
            list[str] - 重複を除いた県域の文字列リスト。
        """
        sql_text: str = (
            "SELECT DISTINCT"
            "   prefecture "
            "FROM"
            "   tickets "
            "WHERE"
            "   (? = '' OR ticket_number = ?)"
            "   AND (? = '' OR prefecture = ?)"
            "   AND (? = '' OR building_name = ?)"
            "   AND is_deleted = 0 "
            "ORDER BY"
            "   prefecture ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (ticket_number, ticket_number, prefecture, prefecture, building_name, building_name),
            )
            return [str(row["prefecture"]) for row in rows]

    def select_distinct_building_names(
        self,
        ticket_number: str = "",
        prefecture: str = "",
        building_name: str = "",
    ) -> list[str]:
        """
        Summary:
            条件に一致するビル名の重複排除（DISTINCT）一覧を取得します。
        Description:
            ticket_number, prefecture, building_name の各条件（空文字時は全件対象）で tickets テーブルを検索し、
            重複を除いたビル名を昇順で取得してリストで返却します。論理削除されたレコードは除外されます。
        Args:
            ticket_number: str - チケット管理番号（未指定時は空文字）。
            prefecture: str - 都道府県（未指定時は空文字）。
            building_name: str - 物件名（未指定時は空文字）。
        Returns:
            list[str] - 重複を除いたビル名の文字列リスト。
        """
        sql_text: str = (
            "SELECT DISTINCT"
            "   building_name "
            "FROM"
            "   tickets "
            "WHERE"
            "   (? = '' OR ticket_number = ?)"
            "   AND (? = '' OR prefecture = ?)"
            "   AND (? = '' OR building_name = ?)"
            "   AND is_deleted = 0 "
            "ORDER BY"
            "   building_name ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (ticket_number, ticket_number, prefecture, prefecture, building_name, building_name),
            )
            return [str(row["building_name"]) for row in rows]

    def select_by_key(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None:
        """
        Summary:
            複合主キーを指定してチケット基本情報を取得します。
        Description:
            tickets テーブルから指定された ticket_number, prefecture, building_name のレコードを検索し、Entityへマッピングして返却します。
            論理削除されていないレコード（is_deleted = 0）のみが対象です。レコードが存在しない場合は None を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None - チケットエンティティ、または存在しない場合は None。
        """
        sql_text: str = (
            "SELECT"
            "   ticket_number"
            "   ,prefecture"
            "   ,building_name"
            "   ,is_deleted"
            "   ,created_at"
            "   ,updated_at "
            "FROM"
            "   tickets "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
            "   AND is_deleted = 0 "
            "LIMIT 1"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (ticket_number, prefecture, building_name),
            )
            return self._map_row_to_entity(rows[0]) if rows else None

    def select_by_key_raw(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None:
        """
        Summary:
            論理削除状態を問わず複合主キーを指定してチケット基本情報を取得します。
        Description:
            tickets テーブルから指定された ticket_number, prefecture, building_name のレコードを is_deleted の条件なしで検索し、
            Entityへマッピングして返却します。レコードが存在しない場合は None を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None - チケットエンティティ、または存在しない場合は None。
        """
        sql_text: str = (
            "SELECT"
            "   ticket_number"
            "   ,prefecture"
            "   ,building_name"
            "   ,is_deleted"
            "   ,created_at"
            "   ,updated_at "
            "FROM"
            "   tickets "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ? "
            "LIMIT 1"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (ticket_number, prefecture, building_name),
            )
            return self._map_row_to_entity(rows[0]) if rows else None

    def insert(self, entity: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket) -> bool:
        """
        Summary:
            新規チケット基本情報レコードを登録します。
        Description:
            tickets テーブルへ新規レコードを挿入します。
        Args:
            entity: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket - 登録対象のチケットエンティティ。
        Returns:
            bool - 登録に成功した場合は True、失敗した場合は False。
        """
        sql_text: str = (
            "INSERT INTO"
            "   tickets ("
            "       ticket_number"
            "       ,prefecture"
            "       ,building_name"
            "       ,is_deleted"
            "   )"
            "VALUES ("
            "   ?"
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
                    entity.is_deleted,
                ),
            )
            return row_count > 0

    def update(self, entity: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket) -> bool:
        """
        Summary:
            チケット基本情報の論理削除フラグおよび更新日時を更新します。
        Description:
            tickets テーブルの指定された複合主キーのレコードの is_deleted および updated_at を更新します。
        Args:
            entity: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket - 更新対象のチケットエンティティ。
        Returns:
            bool - 更新件数が 0 より大きければ True、そうでなければ False。
        """
        sql_text: str = (
            "UPDATE"
            "   tickets "
            "SET"
            "   is_deleted = ?"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            row_count: int = fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (
                    entity.is_deleted,
                    entity.ticket_number,
                    entity.prefecture,
                    entity.building_name,
                ),
            )
            return row_count > 0

    def update_logical_delete(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> int:
        """
        Summary:
            指定された複合キーのチケット基本情報を論理削除します。
        Description:
            tickets テーブルの指定レコードの is_deleted を 1 に、updated_at を現在日時に更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            int - 更新された行数。
        """
        sql_text: str = (
            "UPDATE"
            "   tickets "
            "SET"
            "   is_deleted = 1"
            "   ,updated_at = DATETIME('now', 'localtime') "
            "WHERE"
            "   ticket_number = ?"
            "   AND prefecture = ?"
            "   AND building_name = ?"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            row_count: int = fws_sqlite_util_obj.execute_non_query(
                sql_text,
                (ticket_number, prefecture, building_name),
            )
            return row_count
    #endregion

    #region Private Methods
    def _map_row_to_entity(
        self,
        row: Any,
    ) -> fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket:
        """
        Summary:
            DB取得行データをチケット基本情報Entityへマッピングします。
        Description:
            sqlite3.Row オブジェクトの各列を FwsEntityChatTemplateTicket の属性に設定して返却します。
        Args:
            row: Any - sqlite3.Row またはマッピング互換オブジェクト。
        Returns:
            fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket - マッピングされたチケットエンティティ。
        """
        return fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket(
            ticket_number=str(row["ticket_number"]),
            prefecture=str(row["prefecture"]),
            building_name=str(row["building_name"]),
            is_deleted=int(row["is_deleted"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
    #endregion
#endregion
