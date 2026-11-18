"""
Summary:
    作業別チェックリスト項目テンプレートエンティティモジュール。
Description:
    データベースの mst_task_checklist_templates テーブルの1レコードに対応するデータ構造を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from dataclasses import dataclass
#endregion

#region classes
@dataclass
class FwsEntityChatTemplateTaskChecklistTemplate:
    """
    Summary:
        作業別チェックリスト項目テンプレートエンティティクラス。
    Description:
        データベースの mst_task_checklist_templates テーブルの1レコード構造を保持します。
    """

    checklist_template_id: str = ""
    """str - チェックリストテンプレートID"""
    task_template_id: str = ""
    """str - 親タスクテンプレートID"""
    category_name: str = ""
    """str - 作業分類名"""
    task_name: str = ""
    """str - 作業項目名"""
    item_seq: int = 1
    """int - 項目連番"""
    display_text: str = ""
    """str - 表示文言"""
    append_text: str = ""
    """str - メモ自動追記文言"""
    extra_builder: str = ""
    """str - 拡張UIビルダー関数名"""
    created_at: str = ""
    """str - 作成日時"""
    updated_at: str = ""
    """str - 更新日時"""
#endregion
