"""
Summary:
    チケット時系列タスクチェックリスト状態エンティティモジュール。
Description:
    データベースの ticket_timeline_task_checklists テーブルの1レコードに対応するデータ構造を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from dataclasses import dataclass
#endregion

#region classes
@dataclass
class FwsEntityChatTemplateTicketTimelineChecklist:
    """
    Summary:
        チケット時系列タスクチェックリスト状態エンティティクラス。
    Description:
        データベースの ticket_timeline_task_checklists テーブルの1レコード構造を保持します。
    """

    ticket_number: str = ""
    """str - チケット管理番号"""
    prefecture: str = ""
    """str - 都道府県"""
    building_name: str = ""
    """str - 物件名"""
    revision: int = 1
    """int - リビジョン番号（世代管理）"""
    task_item_number: int = 0
    """int - 親タスクリストインデックス（0始まり）"""
    item_seq: int = 0
    """int - チェックリスト項目連番（1始まり）"""
    checklist_template_id: str = ""
    """str - チェックリストテンプレートID"""
    extra_builder: str = ""
    """str - 補足UIビルダー識別子"""
    extra_data: str = ""
    """str - 補足UI入力データ（JSON文字列）"""
    display_text: str = ""
    """str - チェックリスト表示文言"""
    append_text: str = ""
    """str - 追記用文言"""
    is_checked: int = 0
    """int - チェック状態フラグ（0: 未チェック, 1: チェック済み）"""
    is_deleted: int = 0
    """int - 論理削除フラグ（0: 有効, 1: 削除済み）"""
    created_at: str = ""
    """str - 作成日時"""
    updated_at: str = ""
    """str - 更新日時"""
#endregion
