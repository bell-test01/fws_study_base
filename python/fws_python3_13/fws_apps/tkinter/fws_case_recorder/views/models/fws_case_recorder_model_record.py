"""
Summary:
    案件記録の表示用モデル（ViewModel）モジュール。
Description:
    View層での表示に最適化された案件記録データ構造を定義します。
Attachment:
    なし
"""
from typing import Optional
from fws_apps.tkinter.fws_case_recorder.businesses.entity import fws_case_recorder_entity_record

class FwsCaseRecorderModelRecord:
    """
    Summary:
        案件記録ViewModel クラス。
    Description:
        UI表示用に加工された案件記録データを保持します。
    """

    #region Constructor
    def __init__(self, entity: Optional[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord] = None) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            各フィールドを初期化します。Entityが渡された場合は値を詰め替えます。
        Args:
            entity: Optional[FwsCaseRecorderEntityRecord] - 詰め替え元の案件記録Entity
        Returns:
            None - 戻り値なし。
        """
        if entity:
            self.record_id: Optional[int] = entity.record_id
            self.region: str = entity.region
            self.building: str = entity.building
            self.case_number: str = entity.case_number
            self.record_time: str = entity.record_time
            self.content: str = entity.content
            self.created_at: str = entity.created_at
            self.updated_at: str = entity.updated_at
            self.display_header: str = f"案件:{entity.case_number}  {entity.record_time}  [{entity.region} {entity.building}]"
        else:
            self.record_id: Optional[int] = None
            self.region: str = ""
            self.building: str = ""
            self.case_number: str = ""
            self.record_time: str = ""
            self.content: str = ""
            self.display_header: str = ""
            self.created_at: str = ""
            self.updated_at: str = ""
    #endregion
