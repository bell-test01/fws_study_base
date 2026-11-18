"""
Summary:
    チケット基本情報（ヘッダ）エンティティモジュール。
Description:
    データベースの tickets テーブルの1レコードに対応するデータ構造を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from dataclasses import dataclass
#endregion

#region classes
@dataclass
class FwsEntityChatTemplateTicket:
    """
    Summary:
        チケット基本情報（ヘッダ）エンティティクラス。
    Description:
        データベースの tickets テーブルの1レコード構造を保持します。
    """

    ticket_number: str = ""
    """str - チケット管理番号（複合主キー）"""
    prefecture: str = ""
    """str - 都道府県（複合主キー）"""
    building_name: str = ""
    """str - 物件名（複合主キー）"""
    is_deleted: int = 0
    """int - 論理削除フラグ（0: 有効, 1: 削除済み）"""
    created_at: str = ""
    """str - 作成日時"""
    updated_at: str = ""
    """str - 更新日時"""
#endregion
