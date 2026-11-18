"""
Summary:
    チケット時系列タスクカードエンティティモジュール。
Description:
    データベースの ticket_timeline_tasks テーブルの1レコードに対応するデータ構造を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from dataclasses import dataclass
#endregion

#region classes
@dataclass
class FwsEntityChatTemplateTicketTimelineTask:
    """
    Summary:
        チケット時系列タスクカードエンティティクラス。
    Description:
        データベースの ticket_timeline_tasks テーブルの1レコード構造を保持します。
    """

    ticket_number: str = ""
    """str - チケット管理番号"""
    prefecture: str = ""
    """str - 都道府県"""
    building_name: str = ""
    """str - 物件名"""
    revision: int = 1
    """int - リビジョン番号（世代管理）"""
    item_number: int = 0
    """int - リストインデックス（0始まり）"""
    task_template_id: str = ""
    """str - タスクテンプレートID"""
    category_name: str = ""
    """str - カテゴリ名"""
    task_name: str = ""
    """str - タスク名"""
    task_time: str = ""
    """str - 時刻文字列（例: '10:00'）"""
    memo: str = ""
    """str - タスクメモ"""
    is_completed: int = 0
    """int - 完了状態フラグ（0: 未完了, 1: 完了）"""
    is_deleted: int = 0
    """int - 論理削除フラグ（0: 有効, 1: 削除済み）"""
    created_at: str = ""
    """str - 作成日時"""
    updated_at: str = ""
    """str - 更新日時"""
#endregion
