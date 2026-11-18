"""
Summary:
    作業テンプレートデータベースアクセス用モジュール。
Description:
    mst_task_templates および mst_task_checklist_templates テーブルに対するデータ検索SQL実行およびEntityへのマッピングを行います。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.database import fws_sqlite_util

from fws_apps.tkinter.fws_chat_template.businesses.entity import (
    fws_entity_chat_template_task_checklist_template,
    fws_entity_chat_template_task_template,
)
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsDatabaseAccessChatTemplateTaskTemplate:
    """
    Summary:
        作業テンプレートデータベースアクセスクラス。
    Description:
        mst_task_templates および mst_task_checklist_templates テーブルに対する検索操作を提供します。
    """

    #region Constructor
    def __init__(self, db_path: Path = fws_const_chat_template.PATH_APP_DB_FILE) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            データベースアクセスクラスを初期化し、DB接続パスを保持します。
        Args:
            db_path: Path - データベースファイルパス。
        Returns:
            None - 戻り値なし。
        """
        self._db_path: Path = db_path
        """Path - データベースファイルパス"""
    #endregion

    #region Public Methods
    def select_all_categories(self) -> list[str]:
        """
        Summary:
            全作業分類名一覧を取得します。
        Description:
            mst_task_templates テーブルに登録されている作業分類名を sort_order 昇順でグループ化して取得します。
        Args:
            なし
        Returns:
            list[str] - 作業分類名の文字列リスト。
        """
        sql_text: str = (
            "SELECT"
            "   category_name "
            "FROM"
            "   mst_task_templates "
            "GROUP BY"
            "   category_name "
            "ORDER BY"
            "   MIN(sort_order) ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(sql_text)
        
        return [str(row["category_name"]) for row in rows]

    def select_task_templates_by_category(
        self,
        category_name: str,
    ) -> list[fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate]:
        """
        Summary:
            指定された作業分類に属するタスクテンプレートエンティティ一覧を取得します。
        Description:
            指定された作業分類名に対応するタスクテンプレートを sort_order 昇順で取得し返却します。
            category_name が "ALL" または空文字の場合は全タスクテンプレートを取得します。
        Args:
            category_name: str - 作業分類名（"ALL" または個別分類名）。
        Returns:
            list[fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate] - タスクテンプレートエンティティのリスト。
        """
        sql_text: str = (
            "SELECT"
            "   task_template_id"
            "   ,category_name"
            "   ,task_name"
            "   ,sort_order"
            "   ,created_at"
            "   ,updated_at "
            "FROM"
            "   mst_task_templates "
            "WHERE"
            "   (? = '' OR ? = 'ALL' OR category_name = ?) "
            "ORDER BY"
            "   sort_order ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (category_name, category_name, category_name),
            )
        
        return [self._map_row_to_task_template_entity(row) for row in rows]

    def select_checklist_templates(
        self,
        category_name: str,
        task_name: str,
    ) -> list[fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate]:
        """
        Summary:
            指定された作業のチェックリスト項目テンプレート一覧を取得します。
        Description:
            作業分類名および作業項目名に紐づくチェックリスト項目を item_seq 昇順で取得します。
        Args:
            category_name: str - 作業分類名。
            task_name: str - 作業項目名。
        Returns:
            list[fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate] - チェックリストテンプレートエンティティのリスト。
        """
        sql_text: str = (
            "SELECT"
            "   checklist_template_id"
            "   , task_template_id"
            "   , category_name"
            "   , task_name, item_seq"
            "   , display_text, append_text"
            "   , extra_builder"
            "   , created_at, updated_at "
            "FROM"
            "   mst_task_checklist_templates "
            "WHERE"
            "   category_name = ?"
            "   AND task_name = ? "
            "ORDER BY"
            "   item_seq ASC"
        )
        with fws_sqlite_util.FwsSqliteUtil(self._db_path) as fws_sqlite_util_obj:
            rows: list[Any] = fws_sqlite_util_obj.execute_fetch_all(
                sql_text,
                (category_name, task_name),
            )
        
        return [self._map_row_to_checklist_template_entity(row) for row in rows]
    #endregion

    #region Private Methods
    def _map_row_to_checklist_template_entity(
        self,
        row: Any,
    ) -> fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate:
        """
        Summary:
            DB取得行データをチェックリストテンプレートEntityへマッピングします。
        Description:
            sqlite3.Row オブジェクトの各列を FwsEntityChatTemplateTaskChecklistTemplate の属性に設定して返却します。
        Args:
            row: Any - sqlite3.Row またはマッピング互換オブジェクト。
        Returns:
            fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate - マッピングされたエンティティ。
        """
        return fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate(
            checklist_template_id=str(row["checklist_template_id"]),
            task_template_id=str(row["task_template_id"]),
            category_name=str(row["category_name"]),
            task_name=str(row["task_name"]),
            item_seq=int(row["item_seq"]),
            display_text=str(row["display_text"]),
            append_text=str(row["append_text"]),
            extra_builder=str(row["extra_builder"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )

    def _map_row_to_task_template_entity(
        self,
        row: Any,
    ) -> fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate:
        """
        Summary:
            DB取得行データをタスクテンプレートEntityへマッピングします。
        Description:
            sqlite3.Row オブジェクトの各列を FwsEntityChatTemplateTaskTemplate の属性に設定して返却します。
        Args:
            row: Any - sqlite3.Row またはマッピング互換オブジェクト。
        Returns:
            fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate - マッピングされたエンティティ。
        """
        return fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate(
            task_template_id=str(row["task_template_id"]),
            category_name=str(row["category_name"]),
            task_name=str(row["task_name"]),
            sort_order=int(row["sort_order"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
    #endregion
#endregion
