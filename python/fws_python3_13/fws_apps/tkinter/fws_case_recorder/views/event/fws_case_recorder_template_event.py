"""
Summary:
    fws_case_recorder アプリの定型文管理画面イベントモジュール。
Description:
    定型文管理画面のイベントバインドおよびハンドラを管理します。
ScreenName:
    定型文管理画面
Attachment:
    なし
"""
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional, Callable

from fws_apps.tkinter.fws_case_recorder.views.view import fws_case_recorder_template_view
from fws_apps.tkinter.fws_case_recorder.views.logic import fws_case_recorder_template_logic
from fws_apps.tkinter.fws_case_recorder.views.models import fws_case_recorder_model_template

class FwsCaseRecorderTemplateEvent:
    """
    Summary:
        定型文管理画面のイベントハンドラクラス。
    Description:
        定型文管理のView・Logicをインスタンス化し、イベントをバインドします。
    """

    #region Constructor
    def __init__(self, master: tk.Tk, width: int = 600, height: int = 500, on_close: Optional[Callable] = None) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            定型文管理のView・Logicを生成し、イベントを紐付けます。
        Args:
            master: tk.Tk - 親ウィンドウ。
            width: int - 幅。
            height: int - 高さ。
            on_close: Callable - 閉じる際のコールバック。
        Returns:
            None - 戻り値なし。
        """
        self._on_close = on_close
        self._fws_case_recorder_template_view_obj: fws_case_recorder_template_view.FwsCaseRecorderTemplateView = fws_case_recorder_template_view.FwsCaseRecorderTemplateView(master, width, height)
        """FwsCaseRecorderTemplateView - ビューオブジェクト"""

        self._fws_case_recorder_template_logic_obj: fws_case_recorder_template_logic.FwsCaseRecorderTemplateLogic = fws_case_recorder_template_logic.FwsCaseRecorderTemplateLogic()
        """FwsCaseRecorderTemplateLogic - ロジックオブジェクト"""

        self._selected_template_id: Optional[int] = None
        """Optional[int] - 選択中のテンプレートID"""

        self._bind_events()
        self._load_templates()

    def _bind_events(self) -> None:
        """
        Summary:
            イベントをバインドします。
        Description:
            各ボタンにコマンドを設定し、ツリービューに選択イベントを紐付けます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_template_view_obj.btn_template_add.config(command=self.btn_template_add_click)
        self._fws_case_recorder_template_view_obj.btn_template_update.config(command=self.btn_template_update_click)
        self._fws_case_recorder_template_view_obj.btn_template_delete.config(command=self.btn_template_delete_click)
        self._fws_case_recorder_template_view_obj.btn_template_close.config(command=self.btn_template_close_click)
        self._fws_case_recorder_template_view_obj.trv_templates.bind("<<TreeviewSelect>>", self.trv_templates_select)
        self._fws_case_recorder_template_view_obj.protocol("WM_DELETE_WINDOW", self.btn_template_close_click)
    #endregion

    #region Public Methods
    def btn_template_add_click(self) -> None:
        """
        Summary:
            追加ボタン押下時のイベント処理を行います。
        Description:
            入力内容をバリデーションし、新規定型文をDBに保存します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            追加ボタンクリック - 入力値が検証され、定型文が追加される。
        """
        title: str = self._fws_case_recorder_template_view_obj.ent_template_title.get().strip()
        """str - タイトル入力値"""
        content: str = self._fws_case_recorder_template_view_obj.txt_template_content.get("1.0", tk.END).strip()
        """str - 本文入力値"""

        error_message: str = self._fws_case_recorder_template_logic_obj.validate_template_input(title, content)
        """str - バリデーションエラーメッセージ"""
        if error_message:
            messagebox.showwarning("入力エラー", error_message, parent=self._fws_case_recorder_template_view_obj)
            return

        self._fws_case_recorder_template_logic_obj.save_template(title, content)
        self._clear_input_fields()
        self._load_templates()

    def btn_template_update_click(self) -> None:
        """
        Summary:
            更新ボタン押下時のイベント処理を行います。
        Description:
            選択中の定型文を入力値で更新します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            更新ボタンクリック - 選択中の定型文が更新される。
        """
        if self._selected_template_id is None:
            messagebox.showwarning("選択エラー", "更新する定型文を一覧から選択してください。", parent=self._fws_case_recorder_template_view_obj)
            return

        title: str = self._fws_case_recorder_template_view_obj.ent_template_title.get().strip()
        """str - タイトル入力値"""
        content: str = self._fws_case_recorder_template_view_obj.txt_template_content.get("1.0", tk.END).strip()
        """str - 本文入力値"""

        error_message: str = self._fws_case_recorder_template_logic_obj.validate_template_input(title, content)
        """str - バリデーションエラーメッセージ"""
        if error_message:
            messagebox.showwarning("入力エラー", error_message, parent=self._fws_case_recorder_template_view_obj)
            return

        self._fws_case_recorder_template_logic_obj.update_template(self._selected_template_id, title, content)
        self._load_templates()

        # 選択状態を復元
        if self._selected_template_id is not None:
            target_id_str: str = str(self._selected_template_id)
            for item in self._fws_case_recorder_template_view_obj.trv_templates.get_children():
                tags = self._fws_case_recorder_template_view_obj.trv_templates.item(item, "tags")
                if tags and tags[0] == target_id_str:
                    self._fws_case_recorder_template_view_obj.trv_templates.selection_set(item)
                    self._fws_case_recorder_template_view_obj.trv_templates.focus(item)
                    self._fws_case_recorder_template_view_obj.trv_templates.see(item)
                    break

    def btn_template_delete_click(self) -> None:
        """
        Summary:
            削除ボタン押下時のイベント処理を行います。
        Description:
            選択中の定型文を確認後に削除します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            削除ボタンクリック - 確認後、選択中の定型文が削除される。
        """
        if self._selected_template_id is None:
            messagebox.showwarning("選択エラー", "削除する定型文を一覧から選択してください。", parent=self._fws_case_recorder_template_view_obj)
            return

        confirm: bool = messagebox.askyesno("確認", "選択した定型文を削除しますか？", parent=self._fws_case_recorder_template_view_obj)
        """bool - 確認結果"""
        if not confirm:
            return

        self._fws_case_recorder_template_logic_obj.delete_template(self._selected_template_id)
        self._clear_input_fields()
        self._selected_template_id = None
        self._load_templates()

    def btn_template_close_click(self) -> None:
        """
        Summary:
            閉じるボタン押下時のイベント処理を行います。
        Description:
            定型文管理画面を閉じます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            閉じるボタンクリック - 定型文管理画面が閉じられる。
        """
        if self._on_close:
            self._on_close(self._fws_case_recorder_template_view_obj)
        self._fws_case_recorder_template_view_obj.destroy()

    def trv_templates_select(self, event: tk.Event) -> None:
        """
        Summary:
            一覧のアイテム選択時のイベント処理を行います。
        Description:
            選択された定型文の内容を入力フィールドに表示します。
        Args:
            event: tk.Event - 選択イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            一覧の行選択 - 選択された定型文の内容が入力フィールドに表示される。
        """
        selected_items: tuple = self._fws_case_recorder_template_view_obj.trv_templates.selection()
        """tuple - 選択されたアイテムのID"""
        if not selected_items:
            return

        item_values: dict = self._fws_case_recorder_template_view_obj.trv_templates.item(selected_items[0])
        """dict - 選択アイテムの値"""
        self._selected_template_id = int(self._fws_case_recorder_template_view_obj.trv_templates.item(selected_items[0], "tags")[0])

        values: tuple = item_values["values"]
        """tuple - アイテムの列値"""
        self._fws_case_recorder_template_view_obj.ent_template_title.delete(0, tk.END)
        self._fws_case_recorder_template_view_obj.ent_template_title.insert(0, values[0])
        self._fws_case_recorder_template_view_obj.txt_template_content.delete("1.0", tk.END)
        self._fws_case_recorder_template_view_obj.txt_template_content.insert("1.0", values[1])
    #endregion

    #region Private Methods
    def _load_templates(self) -> None:
        """
        Summary:
            定型文一覧をリロードします。
        Description:
            Logic層から全定型文を取得し、Treeviewに表示します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # 一覧をクリア
        for item in self._fws_case_recorder_template_view_obj.trv_templates.get_children():
            self._fws_case_recorder_template_view_obj.trv_templates.delete(item)

        template_model_list: List[fws_case_recorder_model_template.FwsCaseRecorderModelTemplate] = self._fws_case_recorder_template_logic_obj.fetch_all_templates()
        """List[FwsCaseRecorderModelTemplate] - 定型文Modelリスト"""
        for model_obj in template_model_list:
            self._fws_case_recorder_template_view_obj.trv_templates.insert(
                "", tk.END,
                values=(model_obj.display_title, model_obj.content),
                tags=(str(model_obj.template_id),)
            )

    def _clear_input_fields(self) -> None:
        """
        Summary:
            入力フィールドをクリアします。
        Description:
            タイトルと本文の入力フィールドを空にします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_template_view_obj.ent_template_title.delete(0, tk.END)
        self._fws_case_recorder_template_view_obj.txt_template_content.delete("1.0", tk.END)
    #endregion
