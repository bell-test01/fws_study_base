"""
Summary:
    チケット機器明細情報エンティティモジュール。
Description:
    データベースの ticket_devices テーブルの1レコードに対応するデータ構造を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from dataclasses import dataclass
#endregion

#region classes
@dataclass
class FwsEntityChatTemplateTicketDevice:
    """
    Summary:
        チケット機器明細情報エンティティクラス。
    Description:
        データベースの ticket_devices テーブルの1レコード構造を保持します。
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
    rack_name: str = ""
    """str - ラック名"""
    hostname: str = ""
    """str - ホスト名"""
    model_name: str = ""
    """str - 機器機種名"""
    serial_number: str = ""
    """str - シリアル番号"""
    is_deleted: int = 0
    """int - 論理削除フラグ（0: 有効, 1: 削除済み）"""
    created_at: str = ""
    """str - 作成日時"""
    updated_at: str = ""
    """str - 更新日時"""
#endregion
