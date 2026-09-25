"""
Summary:
    定型文の表示用モデル（ViewModel）モジュール。
Description:
    View層での表示に最適化された定型文データ構造を定義します。
Attachment:
    なし
"""
from typing import Optional
from fws_apps.tkinter.fws_case_recorder.businesses.entity import fws_case_recorder_entity_template

class FwsCaseRecorderModelTemplate:
    """
    Summary:
        定型文ViewModel クラス。
    Description:
        UI表示用に加工された定型文データを保持します。
    """

    #region Constructor
    def __init__(self, entity: Optional[fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate] = None) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            各フィールドを初期化します。Entityが渡された場合は値を詰め替えます。
        Args:
            entity: Optional[FwsCaseRecorderEntityTemplate] - 詰め替え元の定型文Entity
        Returns:
            None - 戻り値なし。
        """
        if entity:
            self.template_id: Optional[int] = entity.template_id
            self.title: str = entity.title
            self.content: str = entity.content
            self.created_at: str = entity.created_at
            self.updated_at: str = entity.updated_at
            self.display_title: str = entity.title
        else:
            self.template_id: Optional[int] = None
            self.title: str = ""
            self.content: str = ""
            self.display_title: str = ""
            self.created_at: str = ""
            self.updated_at: str = ""
    #endregion
