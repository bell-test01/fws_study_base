"""
Summary:
    fws_case_recorder アプリの定型文管理ロジックモジュール。
Description:
    定型文のバリデーション、Entity→Model変換を提供します。
Attachment:
    なし
"""
from typing import List

from fws_apps.tkinter.fws_case_recorder.businesses.business import fws_case_recorder_business
from fws_apps.tkinter.fws_case_recorder.businesses.entity import fws_case_recorder_entity_template
from fws_apps.tkinter.fws_case_recorder.views.models import fws_case_recorder_model_template

class FwsCaseRecorderTemplateLogic:
    """
    Summary:
        定型文管理画面のロジッククラス。
    Description:
        定型文のバリデーション、CRUD操作のBusiness層委譲、Entity→Model変換を行います。
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

    def save_template(self, title: str, content: str) -> int:
        """
        Summary:
            定型文を新規保存します。
        Description:
            入力値からEntityを構築してBusiness層に挿入を委譲します。
        Args:
            title: str - 定型文タイトル。
            content: str - 定型文本文。
        Returns:
            int - 挿入されたレコードのID。
        """
        fws_case_recorder_entity_template_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate = fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate(
            title=title,
            content=content
        )
        """FwsCaseRecorderEntityTemplate - 定型文エンティティ"""
        inserted_id: int = self._fws_case_recorder_business_obj.insert_template(fws_case_recorder_entity_template_obj)
        """int - 挿入されたレコードID"""
        return inserted_id

    def update_template(self, template_id: int, title: str, content: str) -> None:
        """
        Summary:
            定型文を更新します。
        Description:
            入力値からEntityを構築してBusiness層に更新を委譲します。
        Args:
            template_id: int - 更新対象のテンプレートID。
            title: str - 定型文タイトル。
            content: str - 定型文本文。
        Returns:
            None - 戻り値なし。
        """
        fws_case_recorder_entity_template_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate = fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate(
            template_id=template_id,
            title=title,
            content=content
        )
        """FwsCaseRecorderEntityTemplate - 定型文エンティティ"""
        self._fws_case_recorder_business_obj.update_template(fws_case_recorder_entity_template_obj)

    def delete_template(self, template_id: int) -> None:
        """
        Summary:
            定型文を削除します。
        Description:
            Business層に削除を委譲します。
        Args:
            template_id: int - 削除対象のテンプレートID。
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_business_obj.delete_template(template_id)

    def validate_template_input(self, title: str, content: str) -> str:
        """
        Summary:
            定型文の入力値をバリデーションします。
        Description:
            タイトルと本文が空でないことを検証し、エラーメッセージを返却します。
        Args:
            title: str - 定型文タイトル。
            content: str - 定型文本文。
        Returns:
            str - エラーメッセージ。空文字列の場合はバリデーション成功。
        """
        if not title.strip():
            return "タイトルを入力してください。"
        if not content.strip():
            return "本文を入力してください。"
        return ""
    #endregion

    #region Private Methods
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
        fws_case_recorder_model_template_obj: fws_case_recorder_model_template.FwsCaseRecorderModelTemplate = fws_case_recorder_model_template.FwsCaseRecorderModelTemplate()
        """FwsCaseRecorderModelTemplate - 定型文Model"""
        fws_case_recorder_model_template_obj.template_id = entity_obj.template_id
        fws_case_recorder_model_template_obj.title = entity_obj.title
        fws_case_recorder_model_template_obj.content = entity_obj.content
        fws_case_recorder_model_template_obj.created_at = entity_obj.created_at
        fws_case_recorder_model_template_obj.updated_at = entity_obj.updated_at
        fws_case_recorder_model_template_obj.display_title = entity_obj.title
        return fws_case_recorder_model_template_obj
    #endregion
