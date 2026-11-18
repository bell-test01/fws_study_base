"""
Summary:
    チャットテンプレート業務ロジックモジュール。
Description:
    fws_chat_template アプリケーションにおける業務判定およびデータアクセスの調停処理を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from datetime import datetime
from pathlib import Path
from typing import Any

from fws_lib.common import (
    fws_file_util,
    fws_process_util,
)

from fws_apps.tkinter.fws_chat_template.businesses.database_access import (
    fws_database_access_chat_template_device_model,
    fws_database_access_chat_template_task_template,
    fws_database_access_chat_template_ticket,
    fws_database_access_chat_template_ticket_description,
    fws_database_access_chat_template_ticket_device,
    fws_database_access_chat_template_ticket_timeline_checklist,
    fws_database_access_chat_template_ticket_timeline_task,
)
from fws_apps.tkinter.fws_chat_template.businesses.entity import (
    fws_entity_chat_template_task_checklist_template,
    fws_entity_chat_template_task_template,
    fws_entity_chat_template_ticket,
    fws_entity_chat_template_ticket_description,
    fws_entity_chat_template_ticket_device,
    fws_entity_chat_template_ticket_timeline_checklist,
    fws_entity_chat_template_ticket_timeline_task,
)
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsBusinessChatTemplate:
    """
    Summary:
        チャットテンプレート業務ロジッククラス。
    Description:
        各DAOモジュールを呼び出してEntityやデータを取得・加工し、上位層（Logic層）へ提供する業務ロジックを担当します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            ビジネスロジックの初期化を行い、各種DAOインスタンスを生成・保持します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_database_access_chat_template_device_model_obj: (
            fws_database_access_chat_template_device_model.FwsDatabaseAccessChatTemplateDeviceModel
        ) = fws_database_access_chat_template_device_model.FwsDatabaseAccessChatTemplateDeviceModel()
        """fws_database_access_chat_template_device_model.FwsDatabaseAccessChatTemplateDeviceModel - 機器機種マスタDAOインスタンス"""

        self._fws_database_access_chat_template_task_template_obj: (
            fws_database_access_chat_template_task_template.FwsDatabaseAccessChatTemplateTaskTemplate
        ) = fws_database_access_chat_template_task_template.FwsDatabaseAccessChatTemplateTaskTemplate()
        """fws_database_access_chat_template_task_template.FwsDatabaseAccessChatTemplateTaskTemplate - タスクテンプレートDAOインスタンス"""

        self._fws_database_access_chat_template_ticket_obj: (
            fws_database_access_chat_template_ticket.FwsDatabaseAccessChatTemplateTicket
        ) = fws_database_access_chat_template_ticket.FwsDatabaseAccessChatTemplateTicket()
        """fws_database_access_chat_template_ticket.FwsDatabaseAccessChatTemplateTicket - チケット基本情報DAOインスタンス"""

        self._fws_database_access_chat_template_ticket_description_obj: (
            fws_database_access_chat_template_ticket_description.FwsDatabaseAccessChatTemplateTicketDescription
        ) = fws_database_access_chat_template_ticket_description.FwsDatabaseAccessChatTemplateTicketDescription()
        """fws_database_access_chat_template_ticket_description.FwsDatabaseAccessChatTemplateTicketDescription - チケット詳細テキストDAOインスタンス"""

        self._fws_database_access_chat_template_ticket_device_obj: (
            fws_database_access_chat_template_ticket_device.FwsDatabaseAccessChatTemplateTicketDevice
        ) = fws_database_access_chat_template_ticket_device.FwsDatabaseAccessChatTemplateTicketDevice()
        """fws_database_access_chat_template_ticket_device.FwsDatabaseAccessChatTemplateTicketDevice - チケット機器明細情報DAOインスタンス"""

        self._fws_database_access_chat_template_ticket_timeline_task_obj: (
            fws_database_access_chat_template_ticket_timeline_task.FwsDatabaseAccessChatTemplateTicketTimelineTask
        ) = fws_database_access_chat_template_ticket_timeline_task.FwsDatabaseAccessChatTemplateTicketTimelineTask()
        """fws_database_access_chat_template_ticket_timeline_task.FwsDatabaseAccessChatTemplateTicketTimelineTask - チケット時系列タスクDAOインスタンス"""

        self._fws_database_access_chat_template_ticket_timeline_checklist_obj: (
            fws_database_access_chat_template_ticket_timeline_checklist.FwsDatabaseAccessChatTemplateTicketTimelineChecklist
        ) = fws_database_access_chat_template_ticket_timeline_checklist.FwsDatabaseAccessChatTemplateTicketTimelineChecklist()
        """fws_database_access_chat_template_ticket_timeline_checklist.FwsDatabaseAccessChatTemplateTicketTimelineChecklist - チケット時系列タスクチェックリストDAOインスタンス"""
    #endregion

    #region Public Methods
    def get_device_model_names(self) -> list[str]:
        """
        Summary:
            機器機種名一覧を取得します。
        Description:
            DAO経由で mst_device_models テーブルから sort_order 昇順で機種名一覧を取得して返却します。
        Args:
            なし
        Returns:
            list[str] - 機種名の文字列リスト。
        """
        return self._fws_database_access_chat_template_device_model_obj.select_model_names()

    def get_work_categories(self) -> list[str]:
        """
        Summary:
            全作業分類名一覧を取得します。
        Description:
            DAO経由で mst_task_templates テーブルから全作業分類名を取得して返却します。
        Args:
            なし
        Returns:
            list[str] - 作業分類名の文字列リスト。
        """
        return self._fws_database_access_chat_template_task_template_obj.select_all_categories()

    def get_task_templates_by_category(
        self,
        category_name: str,
    ) -> list[fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate]:
        """
        Summary:
            指定分類に属するタスクテンプレート一覧を取得します。
        Description:
            DAO経由で指定分類（または "ALL"）のタスクテンプレート Entity リストを取得して返却します。
        Args:
            category_name: str - 作業分類名（"ALL" または個別分類名）。
        Returns:
            list[fws_entity_chat_template_task_template.FwsEntityChatTemplateTaskTemplate] - タスクテンプレート Entity リスト。
        """
        return self._fws_database_access_chat_template_task_template_obj.select_task_templates_by_category(category_name)

    def get_checklist_templates(
        self,
        category_name: str,
        task_name: str,
    ) -> list[fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate]:
        """
        Summary:
            指定された作業のチェックリストテンプレート一覧を取得します。
        Description:
            DAO経由で作業分類名および作業名に対応するチェックリストテンプレート Entity リストを取得し、返却します。
        Args:
            category_name: str - 作業分類名。
            task_name: str - 作業項目名。
        Returns:
            list[fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate] - チェックリストテンプレート Entity リスト。
        """
        return self._fws_database_access_chat_template_task_template_obj.select_checklist_templates(
            category_name,
            task_name,
        )

    def get_all_ticket_numbers(self) -> list[str]:
        """
        Summary:
            全チケット番号一覧を取得します。
        Description:
            DAO経由で tickets テーブルから全チケット番号を取得して返却します。
        Args:
            なし
        Returns:
            list[str] - チケット番号の文字列リスト。
        """
        return self._fws_database_access_chat_template_ticket_obj.select_all_ticket_numbers()

    def get_prefectures_by_ticket_number(self, ticket_number: str) -> list[str]:
        """
        Summary:
            指定されたチケット番号に紐づく県域一覧を取得します。
        Description:
            DAO経由で tickets テーブルから指定チケット番号の県域一覧を取得して返却します。
        Args:
            ticket_number: str - チケット管理番号。
        Returns:
            list[str] - 県域の文字列リスト。
        """
        return self._fws_database_access_chat_template_ticket_obj.select_prefectures_by_ticket_number(ticket_number)

    def get_building_names_by_ticket_number(self, ticket_number: str, prefecture: str) -> list[str]:
        """
        Summary:
            指定されたチケット番号および県域に紐づくビル名一覧を取得します。
        Description:
            DAO経由で tickets テーブルから指定チケット番号および県域のビル名一覧を取得して返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
        Returns:
            list[str] - ビル名の文字列リスト。
        """
        return self._fws_database_access_chat_template_ticket_obj.select_building_names_by_ticket_number(
            ticket_number,
            prefecture,
        )

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
            チケットDAOの select_distinct_* メソッドを呼び出し、SQLレベルで重複排除（DISTINCT）された ticket_numbers, prefectures, building_names のリストを辞書で返却します。
        Args:
            ticket_number: str - チケット管理番号（未指定時は空文字）。
            prefecture: str - 都道府県（未指定時は空文字）。
            building_name: str - 物件名（未指定時は空文字）。
        Returns:
            dict[str, list[str]] - 候補リスト辞書（ticket_numbers, prefectures, building_names）。
        """
        ticket_numbers: list[str] = self._fws_database_access_chat_template_ticket_obj.select_distinct_ticket_numbers(
            ticket_number=ticket_number,
            prefecture=prefecture,
            building_name=building_name,
        )
        prefectures: list[str] = self._fws_database_access_chat_template_ticket_obj.select_distinct_prefectures(
            ticket_number=ticket_number,
            prefecture=prefecture,
            building_name=building_name,
        )
        building_names: list[str] = self._fws_database_access_chat_template_ticket_obj.select_distinct_building_names(
            ticket_number=ticket_number,
            prefecture=prefecture,
            building_name=building_name,
        )
        return {
            "ticket_numbers": ticket_numbers,
            "prefectures": prefectures,
            "building_names": building_names,
        }

    def get_ticket(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None:
        """
        Summary:
            指定された複合キーのチケット基本情報を取得します。
        Description:
            DAO経由で tickets テーブルから指定複合キーの Entity を取得して返却します。
            存在しない場合は None を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None - チケット基本情報エンティティ、または存在しない場合は None。
        """
        return self._fws_database_access_chat_template_ticket_obj.select_by_key(
            ticket_number,
            prefecture,
            building_name,
        )

    def get_ticket_description(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> str:
        """
        Summary:
            指定された複合キーに対応する最新の有効な詳細テキストを取得します。
        Description:
            DAO経由で ticket_descriptions テーブルから指定キーの最新有効リビジョン（is_deleted = 0）を取得し、
            description 文字列を返却します。レコードが存在しない場合は空文字を返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            str - チケット詳細テキスト（存在しない場合は空文字）。
        """
        desc_entity: (
            fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription | None
        ) = self._fws_database_access_chat_template_ticket_description_obj.select_latest(
            ticket_number,
            prefecture,
            building_name,
        )
        if desc_entity is None:
            return ""
        return desc_entity.description

    def compare_description(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        current_description: str,
    ) -> None:
        """
        Summary:
            現在入力中のDescriptionとDB保存済み最新DescriptionをWinMergeで差分比較します。
        Description:
            指定キーに一致する最新有効レコードのDescriptionを取得し、現在のDescriptionとともに
            一時ファイルへ書き出した上でWinMergeを非同期起動します。
            DBレコードが存在しない場合やWinMerge実行ファイルが存在しない場合は例外を送出します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            current_description: str - 現在画面で入力中のDescription文字列。
        Returns:
            None - 戻り値なし。
        Raises:
            ValueError - 比較対象となる保存済みデータがDBに存在しない場合。
            FileNotFoundError - WinMergeの実行ファイルが存在しない場合。
        """
        desc_entity: (
            fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription | None
        ) = self._fws_database_access_chat_template_ticket_description_obj.select_latest(
            ticket_number,
            prefecture,
            building_name,
        )
        if desc_entity is None:
            raise ValueError(fws_const_chat_template.get_message(fws_const_chat_template.MSG_ERR_COMPARE_NO_DB_RECORD))

        winmerge_path: Path = fws_const_chat_template.get_winmerge_path()
        if not fws_file_util.is_file(winmerge_path):
            raise FileNotFoundError(fws_const_chat_template.get_message(fws_const_chat_template.MSG_ERR_WINMERGE_NOT_FOUND))

        tmp_dir: Path = fws_const_chat_template.DIR_APP_TMP
        if not fws_file_util.is_dir(tmp_dir):
            fws_file_util.create_dir(tmp_dir)

        db_file: Path = tmp_dir / "db_latest_description.txt"
        current_file: Path = tmp_dir / "current_description.txt"

        fws_file_util.write_text_all(db_file, desc_entity.description, encoding_type="utf-8")
        fws_file_util.write_text_all(current_file, current_description, encoding_type="utf-8")

        fws_process_util.start_process([str(winmerge_path), str(db_file), str(current_file), "/e", "/u"])

    def save_ticket_and_description(
        self,
        ticket_entity: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket,
        description: str,
    ) -> None:
        """
        Summary:
            チケット基本情報および詳細テキスト（世代管理）を保存します。
        Description:
            1. 複合キーに基づきヘッダを検索（論理削除状態も含む）し、存在すれば is_deleted = 0 に設定して update、存在しなければ insert を実行します。
            2. 詳細テキストの最大リビジョン番号を取得し、既存リビジョンがあれば論理削除（is_deleted = 1）に更新した上で、
               新たなリビジョン番号（既存+1、初回は1）で新レコード（is_deleted = 0）を insert します。
        Args:
            ticket_entity: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket - 保存対象のチケット基本情報エンティティ。
            description: str - チケット詳細テキスト本文。
        Returns:
            None - 戻り値なし。
        """
        existing_ticket: fws_entity_chat_template_ticket.FwsEntityChatTemplateTicket | None = (
            self._fws_database_access_chat_template_ticket_obj.select_by_key_raw(
                ticket_entity.ticket_number,
                ticket_entity.prefecture,
                ticket_entity.building_name,
            )
        )
        ticket_entity.is_deleted = 0
        if existing_ticket is not None:
            self._fws_database_access_chat_template_ticket_obj.update(ticket_entity)
        else:
            self._fws_database_access_chat_template_ticket_obj.insert(ticket_entity)

        max_rev: int = self._fws_database_access_chat_template_ticket_description_obj.select_max_revision(
            ticket_entity.ticket_number,
            ticket_entity.prefecture,
            ticket_entity.building_name,
        )
        if max_rev > 0:
            self._fws_database_access_chat_template_ticket_description_obj.update_logical_delete(
                ticket_entity.ticket_number,
                ticket_entity.prefecture,
                ticket_entity.building_name,
                max_rev,
            )
        new_rev: int = max_rev + 1

        desc_entity: fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription = (
            fws_entity_chat_template_ticket_description.FwsEntityChatTemplateTicketDescription(
                ticket_number=ticket_entity.ticket_number,
                prefecture=ticket_entity.prefecture,
                building_name=ticket_entity.building_name,
                revision=new_rev,
                description=description,
                is_deleted=0,
            )
        )
        self._fws_database_access_chat_template_ticket_description_obj.insert(desc_entity)

    def get_ticket_devices(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> list[fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice]:
        """
        Summary:
            指定された複合キーの最新有効リビジョンに属する機器明細一覧を取得します。
        Description:
            DAO経由で ticket_devices テーブルから指定キーの最新有効リビジョン（is_deleted = 0）の機器明細 Entity リストを取得して返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            list[fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice] - 機器明細 Entity リスト。
        """
        return self._fws_database_access_chat_template_ticket_device_obj.select_latest_by_ticket(
            ticket_number,
            prefecture,
            building_name,
        )

    def save_ticket_devices(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        devices_data: list[dict[str, str]],
    ) -> None:
        """
        Summary:
            指定された複合キーの機器明細一覧（世代管理・リスト順序インデックス）を保存します。
        Description:
            1. 既存の最新リビジョン番号を取得し、存在すればそのリビジョンを論理削除（is_deleted = 1）します。
            2. 新規リビジョン番号（既存+1、初回は1）および 0 始まりのリストインデックス（item_number）を付与して insert します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            devices_data: list[dict[str, str]] - 機器明細データの辞書リスト。
        Returns:
            None - 戻り値なし。
        """
        max_rev: int = self._fws_database_access_chat_template_ticket_device_obj.select_max_revision(
            ticket_number,
            prefecture,
            building_name,
        )
        if max_rev > 0:
            self._fws_database_access_chat_template_ticket_device_obj.update_logical_delete(
                ticket_number,
                prefecture,
                building_name,
                max_rev,
            )
        new_rev: int = max_rev + 1

        for item_number, device in enumerate(devices_data, start=0):
            entity: fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice = (
                fws_entity_chat_template_ticket_device.FwsEntityChatTemplateTicketDevice(
                    ticket_number=ticket_number,
                    prefecture=prefecture,
                    building_name=building_name,
                    revision=new_rev,
                    item_number=item_number,
                    rack_name=str(device.get("rack_name", "")).strip(),
                    hostname=device["hostname"],
                    model_name=device["model_name"],
                    serial_number=device["serial_number"],
                    is_deleted=0,
                )
            )
            self._fws_database_access_chat_template_ticket_device_obj.insert(entity)

    def get_ticket_timeline(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> list[dict[str, Any]]:
        """
        Summary:
            指定された複合キーの最新有効リビジョンに属する時系列タスク一覧およびチェックリストを取得します。
        Description:
            DAO経由で ticket_timeline_tasks および ticket_timeline_task_checklists テーブルから指定キーの最新有効リビジョンのデータを取得し、
            タスクごとに check_items をネストした辞書リストとして返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            list[dict[str, Any]] - 時系列タスクカード情報の辞書リスト。
        """
        tasks: list[
            fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask
        ] = self._fws_database_access_chat_template_ticket_timeline_task_obj.select_latest_by_ticket(
            ticket_number,
            prefecture,
            building_name,
        )
        checklists: list[
            fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist
        ] = self._fws_database_access_chat_template_ticket_timeline_checklist_obj.select_latest_by_ticket(
            ticket_number,
            prefecture,
            building_name,
        )

        checklist_map: dict[
            int,
            list[fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist],
        ] = {}
        for chk in checklists:
            checklist_map.setdefault(chk.task_item_number, []).append(chk)

        timeline_list: list[dict[str, Any]] = []
        for task in tasks:
            task_checklists: list[
                fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist
            ] = checklist_map.get(task.item_number, [])
            check_items: list[dict[str, Any]] = [
                {
                    "checklist_template_id": chk.checklist_template_id,
                    "task_template_id": task.task_template_id,
                    "item_seq": chk.item_seq,
                    "display_text": chk.display_text,
                    "append_text": chk.append_text,
                    "extra_builder": chk.extra_builder,
                    "extra_data": chk.extra_data,
                    "is_checked": bool(chk.is_checked),
                }
                for chk in task_checklists
            ]
            timeline_list.append(
                {
                    "item_number": task.item_number,
                    "task_time": task.task_time,
                    "category_name": task.category_name,
                    "task_name": task.task_name,
                    "task_template_id": task.task_template_id,
                    "is_completed": bool(task.is_completed),
                    "memo": task.memo,
                    "check_items": check_items,
                }
            )
        return timeline_list

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
            新規時系列タスクおよびチェックリストレコードをDBに登録（オートセーブ）します。
        Description:
            チケットの最新有効リビジョン番号およびそのリビジョンの最大 item_number を取得し、
            item_number = max + 1（初回は0）としてタスクおよびチェックリストを即時 INSERT します。
            登録されたタスク情報を辞書形式で返却します。
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
        current_rev: int = self._get_current_revision(ticket_number, prefecture, building_name)

        max_item: int | None = self._fws_database_access_chat_template_ticket_timeline_task_obj.select_max_item_number(
            ticket_number,
            prefecture,
            building_name,
            current_rev,
        )
        new_item_number: int = 0 if max_item is None else max_item + 1
        task_time: str = datetime.now().strftime("%H:%M")

        task_entity: (
            fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask
        ) = fws_entity_chat_template_ticket_timeline_task.FwsEntityChatTemplateTicketTimelineTask(
            ticket_number=ticket_number,
            prefecture=prefecture,
            building_name=building_name,
            revision=current_rev,
            item_number=new_item_number,
            task_template_id=task_template_id,
            category_name=category_name,
            task_name=task_name,
            task_time=task_time,
            memo="",
            is_completed=0,
            is_deleted=0,
        )
        self._fws_database_access_chat_template_ticket_timeline_task_obj.insert(task_entity)

        templates: list[
            fws_entity_chat_template_task_checklist_template.FwsEntityChatTemplateTaskChecklistTemplate
        ] = self.get_checklist_templates(category_name, task_name)

        check_items: list[dict[str, Any]] = []
        for tmpl in templates:
            chk_entity: (
                fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist
            ) = fws_entity_chat_template_ticket_timeline_checklist.FwsEntityChatTemplateTicketTimelineChecklist(
                ticket_number=ticket_number,
                prefecture=prefecture,
                building_name=building_name,
                revision=current_rev,
                task_item_number=new_item_number,
                item_seq=tmpl.item_seq,
                checklist_template_id=tmpl.checklist_template_id,
                extra_builder=tmpl.extra_builder,
                extra_data="",
                display_text=tmpl.display_text,
                append_text=tmpl.append_text,
                is_checked=0,
                is_deleted=0,
            )
            self._fws_database_access_chat_template_ticket_timeline_checklist_obj.insert(chk_entity)
            check_items.append(
                {
                    "checklist_template_id": tmpl.checklist_template_id,
                    "task_template_id": task_template_id,
                    "item_seq": tmpl.item_seq,
                    "display_text": tmpl.display_text,
                    "append_text": tmpl.append_text,
                    "extra_builder": tmpl.extra_builder,
                    "extra_data": "",
                    "is_checked": False,
                }
            )

        return {
            "item_number": new_item_number,
            "revision": current_rev,
            "task_time": task_time,
            "category_name": category_name,
            "task_name": task_name,
            "task_template_id": task_template_id,
            "is_completed": False,
            "memo": "",
            "check_items": check_items,
        }

    def delete_timeline_task(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
        item_number: int,
    ) -> None:
        """
        Summary:
            最新リビジョンの単一時系列タスクおよびチェックリストを論理削除します。
        Description:
            チケットの最新有効リビジョン番号を取得し、該当 item_number のタスクおよびチェックリストレコードの is_deleted を 1 に更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            item_number: int - タスク連番。
        Returns:
            None - 戻り値なし。
        """
        current_rev: int = self._get_current_revision(ticket_number, prefecture, building_name)

        self._fws_database_access_chat_template_ticket_timeline_task_obj.update_logical_delete_item(
            ticket_number,
            prefecture,
            building_name,
            current_rev,
            item_number,
        )
        self._fws_database_access_chat_template_ticket_timeline_checklist_obj.update_logical_delete_by_task(
            ticket_number,
            prefecture,
            building_name,
            current_rev,
            item_number,
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
            最新リビジョンの単一時系列タスクのメモ文字列を即時更新（オートセーブ）します。
        Description:
            チケットの最新有効リビジョン番号を取得し、該当 item_number のタスクの memo を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            item_number: int - タスク連番。
            memo: str - 更新後メモ文字列。
        Returns:
            None - 戻り値なし。
        """
        current_rev: int = self._get_current_revision(ticket_number, prefecture, building_name)

        self._fws_database_access_chat_template_ticket_timeline_task_obj.update_memo(
            ticket_number,
            prefecture,
            building_name,
            current_rev,
            item_number,
            memo,
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
            最新リビジョンの単一チェック項目のチェック状態を即時更新（オートセーブ）します。
        Description:
            チケットの最新有効リビジョン番号を取得し、該当チェック項目の is_checked を更新します。
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
        current_rev: int = self._get_current_revision(ticket_number, prefecture, building_name)

        self._fws_database_access_chat_template_ticket_timeline_checklist_obj.update_check_status(
            ticket_number,
            prefecture,
            building_name,
            current_rev,
            task_item_number,
            item_seq,
            is_checked,
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
            最新リビジョンの単一チェック項目の補足UIデータ（JSON）を即時更新（オートセーブ）します。
        Description:
            チケットの最新有効リビジョン番号を取得し、該当チェック項目の extra_data を更新します。
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
        current_rev: int = self._get_current_revision(ticket_number, prefecture, building_name)
        self._fws_database_access_chat_template_ticket_timeline_checklist_obj.update_extra_data(
            ticket_number=ticket_number,
            prefecture=prefecture,
            building_name=building_name,
            revision=current_rev,
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
            最新リビジョンの単一時系列タスクの作業完了フラグを即時更新（オートセーブ）します。
        Description:
            チケットの最新有効リビジョン番号を取得し、該当 item_number のタスクの is_completed を更新します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
            item_number: int - タスク連番。
            is_completed: int - 作業完了フラグ（1: 完了、0: 未完了）。
        Returns:
            None - 戻り値なし。
        """
        current_rev: int = self._get_current_revision(ticket_number, prefecture, building_name)

        self._fws_database_access_chat_template_ticket_timeline_task_obj.update_completed(
            ticket_number,
            prefecture,
            building_name,
            current_rev,
            item_number,
            is_completed,
        )

    def delete_ticket(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> None:
        """
        Summary:
            指定された複合キーのチケット（基本情報、最新詳細テキスト、機器明細、時系列タスク、チェックリスト）を論理削除します。
        Description:
            1. tickets テーブルの対象レコードを論理削除（is_deleted = 1）します。
            2. ticket_descriptions テーブルの最新リビジョンのレコードを論理削除（is_deleted = 1）します。
            3. ticket_devices テーブルの全リビジョンを論理削除（is_deleted = 1）します。
            4. ticket_timeline_tasks テーブルの全リビジョンを論理削除（is_deleted = 1）します。
            5. ticket_timeline_task_checklists テーブルの全リビジョンを論理削除（is_deleted = 1）します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            None - 戻り値なし。
        """
        self._fws_database_access_chat_template_ticket_obj.update_logical_delete(
            ticket_number,
            prefecture,
            building_name,
        )
        max_rev: int = self._fws_database_access_chat_template_ticket_description_obj.select_max_revision(
            ticket_number,
            prefecture,
            building_name,
        )
        if max_rev > 0:
            self._fws_database_access_chat_template_ticket_description_obj.update_logical_delete(
                ticket_number,
                prefecture,
                building_name,
                max_rev,
            )
        self._fws_database_access_chat_template_ticket_device_obj.update_logical_delete(
            ticket_number,
            prefecture,
            building_name,
        )
        self._fws_database_access_chat_template_ticket_timeline_task_obj.update_logical_delete(
            ticket_number,
            prefecture,
            building_name,
        )
        self._fws_database_access_chat_template_ticket_timeline_checklist_obj.update_logical_delete(
            ticket_number,
            prefecture,
            building_name,
        )
    #endregion

    #region Private Methods
    def _get_current_revision(
        self,
        ticket_number: str,
        prefecture: str,
        building_name: str,
    ) -> int:
        """
        Summary:
            対象チケットの時系列タスクの最新有効リビジョン番号を取得します。
        Description:
            時系列タスクテーブルから最新リビジョン番号（未登録時は 1）を取得して返却します。
        Args:
            ticket_number: str - チケット管理番号。
            prefecture: str - 都道府県。
            building_name: str - 物件名。
        Returns:
            int - 最新リビジョン番号（最小 1）。
        """
        task_rev: int = self._fws_database_access_chat_template_ticket_timeline_task_obj.select_max_revision(
            ticket_number,
            prefecture,
            building_name,
        )
        return task_rev if task_rev > 0 else 1
    #endregion
#endregion
