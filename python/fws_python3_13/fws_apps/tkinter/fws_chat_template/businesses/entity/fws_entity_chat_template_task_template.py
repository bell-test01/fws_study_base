"""
Summary:
    作業テンプレートエンティティモジュール。
Description:
    データベースの mst_task_templates テーブルの1レコードに対応するデータ構造を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from dataclasses import dataclass
#endregion

#region classes
@dataclass
class FwsEntityChatTemplateTaskTemplate:
    """
    Summary:
        作業テンプレートエンティティクラス。
    Description:
        データベースの mst_task_templates テーブルの1レコード構造を保持します。
    """

    task_template_id: str = ""
    """str - タスクテンプレートID"""
    category_name: str = ""
    """str - 作業分類名"""
    task_name: str = ""
    """str - 作業項目名"""
    sort_order: int = 0
    """int - 表示順序"""
    created_at: str = ""
    """str - 作成日時"""
    updated_at: str = ""
    """str - 更新日時"""
#endregion
