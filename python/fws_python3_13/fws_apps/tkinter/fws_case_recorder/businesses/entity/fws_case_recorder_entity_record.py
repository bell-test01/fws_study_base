"""
Summary:
    案件記録データのエンティティモジュール。
Description:
    データベースの case_records テーブルに対応するデータ構造を定義します。
Attachment:
    なし
"""
from typing import Optional

class FwsCaseRecorderEntityRecord:
    """
    Summary:
        案件記録エンティティクラス。
    Description:
        1件の案件記録データを保持します。DBテーブル構造に対応します。
    """

    #region Constructor
    def __init__(self, record_id: Optional[int] = None, region: str = "", building: str = "", case_number: str = "", record_time: str = "", content: str = "", created_at: str = "", updated_at: str = "", is_editing: int = 0) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            各フィールドを初期化します。
        Args:
            record_id: Optional[int] - レコードID。
            region: str - 県域。
            building: str - ビル名。
            case_number: str - 案件番号。
            record_time: str - 記録時刻。
            content: str - 記録内容。
            created_at: str - 作成日時。
            updated_at: str - 更新日時。
            is_editing: int - 編集中フラグ（1=編集中, 0=完了）。
        Returns:
            None - 戻り値なし。
        """
        self.record_id: Optional[int] = record_id
        """Optional[int] - レコードID（AUTOINCREMENT）"""
        self.region: str = region
        """str - 県域"""
        self.building: str = building
        """str - ビル名"""
        self.case_number: str = case_number
        """str - 案件番号"""
        self.record_time: str = record_time
        """str - 記録時刻"""
        self.content: str = content
        """str - 記録内容（自由記述）"""
        self.created_at: str = created_at
        """str - 作成日時"""
        self.updated_at: str = updated_at
        """str - 更新日時"""
        self.is_editing: int = is_editing
        """int - 編集中フラグ"""
    #endregion
