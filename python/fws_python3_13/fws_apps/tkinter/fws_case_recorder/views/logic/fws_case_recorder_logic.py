"""
Summary:
    fws_case_recorder アプリのメイン画面ロジックモジュール。
Description:
    Business層との中継、Entity→Model変換、入力補助ロジックを提供します。
Attachment:
    なし
"""
from typing import List, Optional
from datetime import datetime

from fws_apps.tkinter.fws_case_recorder.businesses.business import fws_case_recorder_business
from fws_apps.tkinter.fws_case_recorder.businesses.entity import fws_case_recorder_entity_record
from fws_apps.tkinter.fws_case_recorder.businesses.entity import fws_case_recorder_entity_template
from fws_apps.tkinter.fws_case_recorder.views.models import fws_case_recorder_model_record
from fws_apps.tkinter.fws_case_recorder.views.models import fws_case_recorder_model_template
from fws_apps.tkinter.fws_case_recorder.constant import fws_case_recorder_const

class FwsCaseRecorderLogic:
    """
    Summary:
        メイン画面のロジッククラス。
    Description:
        Business層を呼び出しEntity→Model変換を行い、入力補助ロジックを提供します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            Business層のインスタンスを生成します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_business_obj: fws_case_recorder_business.FwsCaseRecorderBusiness = fws_case_recorder_business.FwsCaseRecorderBusiness()
        """fws_case_recorder_business.FwsCaseRecorderBusiness - ビジネスロジックオブジェクト"""
    #endregion

    #region Public Methods
    def save_record(self, region: str, building: str, case_number: str, record_time: str, content: str, is_editing: int = 1) -> int:
        """
        Summary:
            案件記録を保存します。
        Description:
            入力値からEntityを構築してBusiness層に挿入を委譲し、挿入されたIDを返却します。
        Args:
            region: str - 県域。
            building: str - ビル名。
            case_number: str - 案件番号。
            record_time: str - 記録時刻。
            content: str - 記録内容。
            is_editing: int - 編集中フラグ（デフォルト1）。
        Returns:
            int - 挿入されたレコードのID。
        """
        fws_case_recorder_entity_record_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord = fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord(
            region=region,
            building=building,
            case_number=case_number,
            record_time=record_time,
            content=content,
            is_editing=is_editing
        )
        """FwsCaseRecorderEntityRecord - 案件記録エンティティ"""
        inserted_id: int = self._fws_case_recorder_business_obj.insert_record(fws_case_recorder_entity_record_obj)
        """int - 挿入されたレコードID"""
        return inserted_id

    def update_record(self, record_id: int, region: str, building: str, case_number: str, record_time: str, content: str) -> None:
        """
        Summary:
            案件記録を更新します。
        Description:
            入力値からEntityを構築してBusiness層に更新を委譲します。
        Args:
            record_id: int - レコードID。
            region: str - 県域。
            building: str - ビル名。
            case_number: str - 案件番号。
            record_time: str - 記録時刻。
            content: str - 記録内容。
        Returns:
            None - 戻り値なし。
        """
        fws_case_recorder_entity_record_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord = fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord(
            record_id=record_id,
            region=region,
            building=building,
            case_number=case_number,
            record_time=record_time,
            content=content
        )
        """FwsCaseRecorderEntityRecord - 案件記録エンティティ"""
        self._fws_case_recorder_business_obj.update_record(fws_case_recorder_entity_record_obj)

    def update_editing_status(self, record_id: int, is_editing: int) -> None:
        """
        Summary:
            指定レコードの編集中フラグを更新します。
        Description:
            Business層に更新を委譲します。
        Args:
            record_id: int - 更新対象のレコードID。
            is_editing: int - 編集中フラグの値。
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_business_obj.update_editing_status(record_id, is_editing)

    def delete_record(self, record_id: int) -> None:
        """
        Summary:
            案件記録を削除します。
        Description:
            Business層に削除を委譲します。
        Args:
            record_id: int - 削除するレコードID。
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_business_obj.delete_record(record_id)

    def search_records(self, case_number: str, region: str = "", building: str = "") -> List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord]:
        """
        Summary:
            案件番号、県域、ビル名で記録を検索し、Modelリストとして返却します。
        Description:
            Business層から取得したEntityリストをModelリストに変換します。
        Args:
            case_number: str - 検索する案件番号。
            region: str - 検索する県域。
            building: str - 検索するビル名。
        Returns:
            List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord] - 検索結果のModelリスト。
        """
        entity_list: List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord] = self._fws_case_recorder_business_obj.search_records(case_number, region, building)
        """List[FwsCaseRecorderEntityRecord] - 検索結果Entityリスト"""
        model_list: List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord] = []
        """List[FwsCaseRecorderModelRecord] - 変換後Modelリスト"""
        for entity_obj in entity_list:
            model_list.append(self._convert_record_entity_to_model(entity_obj))
        return model_list

    def fetch_active_records(self) -> List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord]:
        """
        Summary:
            編集中（is_editing=1）の案件記録を取得し、Modelリストとして返却します。
        Description:
            Business層から取得した編集中EntityリストをModelリストに変換します。
        Args:
            なし
        Returns:
            List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord] - 編集中Modelリスト。
        """
        entity_list: List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord] = self._fws_case_recorder_business_obj.fetch_active_records()
        """List[FwsCaseRecorderEntityRecord] - 編集中Entityリスト"""
        model_list: List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord] = []
        """List[FwsCaseRecorderModelRecord] - 変換後Modelリスト"""
        for entity_obj in entity_list:
            model_list.append(self._convert_record_entity_to_model(entity_obj))
        return model_list

    def search_case_numbers(self, region: str, building: str) -> List[str]:
        """
        Summary:
            県域とビル名から案件番号を曖昧検索します。
        Description:
            Business層に検索を委譲し、案件番号リストを返却します。
        Args:
            region: str - 県域（部分一致）。
            building: str - ビル名（部分一致）。
        Returns:
            List[str] - 該当する案件番号のリスト。
        """
        case_number_list: List[str] = self._fws_case_recorder_business_obj.search_case_numbers_by_region_building(region, building)
        """List[str] - 案件番号リスト"""
        return case_number_list

    def fetch_all_templates(self) -> List[fws_case_recorder_model_template.FwsCaseRecorderModelTemplate]:
        """
        Summary:
            全定型文を取得し、Modelリストとして返却します。
        Description:
            Business層から取得したEntityリストをModelリストに変換します。
        Args:
            なし
        Returns:
            List[fws_case_recorder_model_template.FwsCaseRecorderModelTemplate] - 定型文Modelリスト。
        """
        entity_list: List[fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate] = self._fws_case_recorder_business_obj.fetch_all_templates()
        """List[FwsCaseRecorderEntityTemplate] - 定型文Entityリスト"""
        model_list: List[fws_case_recorder_model_template.FwsCaseRecorderModelTemplate] = []
        """List[FwsCaseRecorderModelTemplate] - 変換後Modelリスト"""
        for entity_obj in entity_list:
            model_list.append(self._convert_template_entity_to_model(entity_obj))
        return model_list

    def generate_current_time(self) -> str:
        """
        Summary:
            現在時刻を記録用フォーマットで取得します。
        Description:
            yyyy/MM/dd HH:mm 形式の現在時刻文字列を返却します。
        Args:
            なし
        Returns:
            str - フォーマット済み現在時刻文字列。
        """
        current_time: str = datetime.now().strftime("%Y/%m/%d %H:%M")
        """str - 現在時刻文字列"""
        return current_time

    def build_insert_text(self, symbol: str) -> str:
        """
        Summary:
            挿入用テキストを構築します。
        Description:
            指定された記号に応じた挿入テキストを返却します。
            引用線の場合は前後に改行を付与します。
        Args:
            symbol: str - 挿入する記号種別。
        Returns:
            str - 挿入用テキスト。
        """
        if symbol == fws_case_recorder_const.SYMBOL_QUOTE_LINE:
            insert_text: str = f"\n{fws_case_recorder_const.SYMBOL_QUOTE_LINE}\n"
            """str - 改行付き引用線テキスト"""
            return insert_text
        return symbol
    #endregion

    #region Private Methods
    def _convert_record_entity_to_model(self, entity_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord) -> fws_case_recorder_model_record.FwsCaseRecorderModelRecord:
        """
        Summary:
            案件記録EntityをModelに変換します。
        Description:
            Entityの各フィールドをModelにコピーし、表示用ヘッダーを構築します。
        Args:
            entity_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord - 変換元Entity。
        Returns:
            fws_case_recorder_model_record.FwsCaseRecorderModelRecord - 変換後Model。
        """
        return fws_case_recorder_model_record.FwsCaseRecorderModelRecord(entity_obj)

    def _convert_template_entity_to_model(self, entity_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate) -> fws_case_recorder_model_template.FwsCaseRecorderModelTemplate:
        """
        Summary:
            定型文EntityをModelに変換します。
        Description:
            Entityの各フィールドをModelにコピーし、表示用タイトルを構築します。
        Args:
            entity_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate - 変換元Entity。
        Returns:
            fws_case_recorder_model_template.FwsCaseRecorderModelTemplate - 変換後Model。
        """
        return fws_case_recorder_model_template.FwsCaseRecorderModelTemplate(entity_obj)
    #endregion
