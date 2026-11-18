"""
Summary:
    メイン画面ロジックモジュール。
Description:
    fws_chat_template アプリケーションの画面表示に関連する制御およびデータ処理の基盤を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from typing import Any

from fws_apps.tkinter.fws_chat_template.businesses.business import fws_business_chat_template
from fws_apps.tkinter.fws_chat_template.businesses.entity import (
    fws_entity_chat_template_task_checklist_template,
    fws_entity_chat_template_task_template,
    fws_entity_chat_template_ticket,
    fws_entity_chat_template_ticket_device,
)
#endregion

#region classes
class FwsLogicChatTemplate:
    """
    Summary:
        メイン画面ロジッククラス。
    Description:
        Viewインスタンスを直接操作せず、ビジネスデータの中継や表示用データの加工処理を担当します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            メイン画面ロジックの初期化を行い、ビジネスロジックインスタンスを生成・保持します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_business_chat_template_obj: fws_business_chat_template.FwsBusinessChatTemplate = (
            fws_business_chat_template.FwsBusinessChatTemplate()
        )
        """fws_business_chat_template.FwsBusinessChatTemplate - メイン業務ロジックインスタンス"""
    #endregion

    #region Public Methods
    def get_ticket_candidates(
        self,
        ticket_number: str = "",
        prefecture: str = "",
        building_name: str = "",
    ) -> dict[str, list[str]]:
        """
        Summary:
            指定条件に紐づくチケット番号・県域・ビル名の候補一覧を取得します。
        Description:
            Business層の get_ticket_candidates を呼び出し、候補リスト辞書を取得して返却します。
        Args:
            ticket_number: str - チケット管理番号（未指定時は空文字）。
            prefecture: str - 都道府県（未指定時は空文字）。
            building_name: str - 物件名（未指定時は空文字）。
        Returns:
            dict[str, list[str]] - 候補リスト辞書（ticket_numbers, prefectures, building_names）。
        """
        return self._fws_business_chat_template_obj.get_ticket_candidates(
            ticket_number=ticket_number,
            prefecture=prefecture,
            building_name=building_name,
        )

    def get_device_model_names(self) -> list[str]:
        """
        Summary:
            機器機種名一覧を取得します。
        Description:
            Business層経由で機器機種名一覧を取得して返却します。
        Args:
            なし
        Returns:
            list[str] - 機種名の文字列リスト。
        """
        return self._fws_business_chat_template_obj.get_device_model_names()

    def get_work_categories(self) -> list[str]:
        """
        Summary:
            作業分類名一覧を取得します。
        Description:
            Business層経由で全作業分類名を取得し、UI表示用として先頭に "ALL" を付与したリストを返却します。
        Args:
            なし
        Returns:
            list[str] - 先頭に "ALL" が付与された作業分類名リスト。
        """
        categories: list[str] = self._fws_business_chat_template_obj.get_work_categories()
        return ["ALL"] + [cat for cat in categories if cat != "ALL"]

    def get_task_menu_items(self, category_name: str) -> list[dict[str, str]]:
        """
        Summary:
            指定分類に属するタスクメニュー項目一覧を取得します。
        Description:
            Business層経由で指定分類（または "ALL"）のタスクテンプレート Entity リストを取得し、UI表示用の辞書リストに変換して返却します。
        Args:
            category_name: str - 作業分類名（"ALL" または個別分類名）。
        Returns:
            list[dict[str, str]] - タスクメニュー情報の辞書リスト。
        """
        templates: list[
            fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate
        ] = self._fws_business_chat_template_obj.get_task_templates_by_category(category_name)
        return [
            {
                "task_template_id": t.task_template_id,
                "category_name": t.category_name,
                "task_name": t.task_name,
            }
            for t in templates
        ]

    def get_checklist_templates(self, category_name: str, task_name: str) -> list[dict[str, Any]]:
        """
        Summary:
            指定された作業のチェックリストテンプレート一覧を取得します。
        Description:
            Business層経由で作業分類名および作業名に対応するチェックリストテンプレート Entity リストを取得し、UI表示用の辞書リストに変換して返却します。
        Args:
            category_name: str - 作業分類名。
            task_name: str - 作業項目名。
        Returns:
            list[dict[str, Any]] - チェックリストテンプレート項目の辞書リスト。
        """
        checklists: list[
            fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate
        ] = self._fws_business_chat_template_obj.get_checklist_templates(category_name, task_name)
        return [
            {
                "checklist_template_id": c.checklist_template_id,
                "task_template_id": c.task_template_id,
                "category_name": c.category_name,
                "task_name": c.task_name,
                "item_seq": c.item_seq,
                "display_text": c.display_text,
                "append_text": c.append_text,
                "extra_builder": c.extra_builder,
            }
            for c in checklists
        ]

    def get_ticket_numbers(self) -> list[str]:
        """
        Summary:
            全チケット番号一覧を取得します。
        Description:
            Business層経由で tickets テーブルの全チケット番号一覧を取得して返却します。
        Args:
            なし
        Returns:
            list[str] - チケット番号の文字列リスト。
        """
        return self._fws_business_chat_template_obj.get_all_ticket_numbers()

    def get_prefectures_by_ticket_number(self, ticket_number: str) -> list[str]:
        """
        Summary:
            指定されたチケット番号に紐づく県域一覧を取得します。
        Description:
            Business層経由で県域一覧を取得して返却します。
        Args:
            ticket_number: str - チケット管理番号。
        Returns:
            list[str] - 県域の文字列リスト。
        """
        return self._fws_business_chat_template_obj.get_prefectures_by_ticket_number(ticket_number)

    def get_building_names_by_ticket_number(self, ticket_number: str, prefecture: str) -> list[str]:
        """
        Summary:
            指定されたチケット番号および県域に紐づくビル名一覧を取得します。
        Description:
            Business層経由でビル名一覧を取得して返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
        Returns:
            list[str] - ビル名の文字列リスト。
        """
        return self._fws_business_chat_template_obj.get_building_names_by_ticket_number(
            ticket_number,
            prefecture,
        )

    def get_ticket(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> dict[str, Any] | None:
        """
        Summary:
            指定された複合キーのチケット情報を取得します。
        Description:
            Business層経由でチケット基本情報および最新Descriptionを取得して辞書形式で返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            dict[str, Any] | None - チケット情報の辞書、または未存在時は None。
        """
        ticket: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None = (
            self._fws_business_chat_template_obj.get_ticket(
                ticket_number,
                prefecture,
                building_name,
            )
        )
        if ticket is None:
            return None

        description: str = self._fws_business_chat_template_obj.get_ticket_description(
            ticket_number,
            prefecture,
            building_name,
        )

        return {
            "ticket_number": ticket.ticket_number,
            "prefecture": ticket.prefecture,
            "building_name": ticket.building_name,
            "description": description,
        }

    def save_ticket(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        description: str,
    ) -> None:
        """
        Summary:
            チケット基本情報およびDescriptionを保存します。
        Description:
            チケット基本情報Entityを生成し、Business層経由でデータベースへ保存します。
            必須項目（チケット番号、県域、ビル名）が未入力の場合は ValueError を送出します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            description: str - 概要・詳細。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        ticket_entity: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket = (
            fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket(
                ticket_number=trimmed_number,
                prefecture=trimmed_prefecture,
                building_name=trimmed_building,
            )
        )
        self._fws_business_chat_template_obj.save_ticket_and_description(
            ticket_entity=ticket_entity,
            description=description,
        )

    def compare_description(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        current_description: str,
    ) -> None:
        """
        Summary:
            現在入力中のDescriptionとDB最新レコードの差分比較を要求します。
        Description:
            Business層の compare_description を呼び出し、WinMergeによる差分比較を非同期で開始します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            current_description: str - 現在画面で入力中のDescription文字列。
        Returns:
            None - 戻り値なし。
        """
        self._fws_business_chat_template_obj.compare_description(
            ticket_number=ticket_number.strip(),
            prefecture=prefecture.strip(),
            building_name=building_name.strip(),
            current_description=current_description,
        )

    def get_ticket_devices(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> list[dict[str, str]]:
        """
        Summary:
            指定された複合キーの機器明細一覧を取得します。
        Description:
            Business層経由で機器明細 Entity リストを取得し、UI表示用辞書リストへ変換して返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            list[dict[str, str]] - 機器明細情報の辞書リスト。
        """
        devices: list[
            fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice
        ] = self._fws_business_chat_template_obj.get_ticket_devices(
            ticket_number,
            prefecture,
            building_name,
        )
        return [
            {
                "rack_name": d.rack_name,
                "hostname": d.hostname,
                "model_name": d.model_name,
                "serial_number": d.serial_number,
            }
            for d in devices
        ]

    def save_ticket_devices(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        devices_data: list[dict[str, str]],
    ) -> None:
        """
        Summary:
            指定された複合キーの機器明細情報を保存します。
        Description:
            必須入力チェックおよび機器明細の有効性チェックを行い、Business層経由で機器明細情報をデータベースへ保存します。
            必須項目（チケット番号、県域、ビル名）が未入力の場合、または有効な機器情報が存在しない場合は ValueError を送出します。
            各行について、ラック名、ホスト名、機種名のいずれかが空文字の場合も ValueError を送出します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            devices_data: list[dict[str, str]] - 機器明細情報の辞書リスト。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        if not devices_data or not any(any(d.values()) for d in devices_data):
            raise ValueError("機器情報が入力されていません。")

        for d in devices_data:
            rack_name: str = str(d.get("rack_name", "")).strip()
            hostname: str = str(d.get("hostname", "")).strip()
            model_name: str = str(d.get("model_name", "")).strip()
            if not (rack_name and hostname and model_name):
                raise ValueError("ラック名・ホスト名・機種名は必須入力です。")

        self._fws_business_chat_template_obj.save_ticket_devices(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
            devices_data=devices_data,
        )

    def get_ticket_timeline(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> list[dict[str, Any]]:
        """
        Summary:
            指定された複合キーの最新有効リビジョンに属する時系列タスク一覧を取得します。
        Description:
            Business層経由で時系列タスクおよびチェックリスト情報を取得し、UI表示用辞書リストとして返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            list[dict[str, Any]] - 時系列タスクカード情報の辞書リスト。
        """
        return self._fws_business_chat_template_obj.get_ticket_timeline(
            ticket_number=ticket_number,
            prefecture=prefecture,
            building_name=building_name,
        )

    def add_timeline_task(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        category_name: str,
        task_name: str,
        task_template_id: str = "",
    ) -> dict[str, Any]:
        """
        Summary:
            指定チケットに新規時系列タスクおよびチェックリストを追加登録（オートセーブ）します。
        Description:
            必須キーバリデーション後、Business層経由でタスクおよびチェックリストレコードをDBへ即時登録し、
            生成されたタスクデータ（item_number等を含む辞書）を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            category_name: str - 作業分類名。
            task_name: str - 作業項目名。
            task_template_id: str - タスクテンプレートID（未指定時は空文字）。
        Returns:
            dict[str, Any] - 登録された新規タスクおよびチェックリスト情報の辞書。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        return self._fws_business_chat_template_obj.add_timeline_task(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
            category_name=category_name,
            task_name=task_name,
            task_template_id=task_template_id,
        )

    def delete_timeline_task(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        item_number: int,
    ) -> None:
        """
        Summary:
            指定された単一時系列タスクおよび紐づくチェックリストを論理削除します。
        Description:
            必須キーバリデーション後、Business層経由で該当タスクおよびチェックリストを論理削除します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            item_number: int - タスク連番。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        self._fws_business_chat_template_obj.delete_timeline_task(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
            item_number=item_number,
        )

    def update_timeline_task_memo(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        item_number: int,
        memo: str,
    ) -> None:
        """
        Summary:
            指定タスクのメモ文字列を即時更新（オートセーブ）します。
        Description:
            必須キーバリデーション後、Business層経由で該当タスクの memo を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            item_number: int - タスク連番。
            memo: str - 更新後メモ文字列。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        self._fws_business_chat_template_obj.update_timeline_task_memo(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
            item_number=item_number,
            memo=memo,
        )

    def update_timeline_checklist_status(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        task_item_number: int,
        item_seq: int,
        is_checked: int,
    ) -> None:
        """
        Summary:
            指定チェック項目のチェック状態を即時更新（オートセーブ）します。
        Description:
            必須キーバリデーション後、Business層経由で該当チェック項目の is_checked を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            task_item_number: int - 親タスク連番。
            item_seq: int - チェック項目連番。
            is_checked: int - チェック状態（1: ON、0: OFF）。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        self._fws_business_chat_template_obj.update_timeline_checklist_status(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
            task_item_number=task_item_number,
            item_seq=item_seq,
            is_checked=is_checked,
        )

    def update_timeline_checklist_extra_data(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        task_item_number: int,
        item_seq: int,
        extra_data: str,
    ) -> None:
        """
        Summary:
            指定チェック項目の補足UI入力データ（JSON）を即時更新（オートセーブ）します。
        Description:
            必須キーバリデーション後、Business層経由で該当チェック項目の extra_data を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            task_item_number: int - 親タスク連番。
            item_seq: int - チェック項目連番。
            extra_data: str - 補足UI入力データ（JSON文字列）。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        self._fws_business_chat_template_obj.update_timeline_checklist_extra_data(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
            task_item_number=task_item_number,
            item_seq=item_seq,
            extra_data=extra_data,
        )

    def update_timeline_task_completed(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        item_number: int,
        is_completed: int,
    ) -> None:
        """
        Summary:
            指定タスクの作業完了フラグを即時更新（オートセーブ）します。
        Description:
            必須キーバリデーション後、Business層経由で該当タスクの is_completed を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            item_number: int - タスク連番。
            is_completed: int - 作業完了フラグ（1: 完了、0: 未完了）。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        self._fws_business_chat_template_obj.update_timeline_task_completed(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
            item_number=item_number,
            is_completed=is_completed,
        )

    def delete_ticket(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> None:
        """
        Summary:
            指定された複合キーのチケット情報を論理削除します。
        Description:
            Business層経由でチケット基本情報、最新Description、機器明細および時系列タスク・チェックリストを論理削除します。
            必須項目（チケット番号、県域、ビル名）が未入力の場合は ValueError を送出します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            None - 戻り値なし。
        """
        trimmed_number: str = ticket_number.strip()
        trimmed_prefecture: str = prefecture.strip()
        trimmed_building: str = building_name.strip()
        if not (trimmed_number and trimmed_prefecture and trimmed_building):
            raise ValueError("チケット番号・県域・ビル名は必須入力です。")

        self._fws_business_chat_template_obj.delete_ticket(
            ticket_number=trimmed_number,
            prefecture=trimmed_prefecture,
            building_name=trimmed_building,
        )
    #endregion
#endregion
