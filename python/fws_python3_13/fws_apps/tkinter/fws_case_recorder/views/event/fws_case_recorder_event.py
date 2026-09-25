"""
Summary:
    fws_case_recorder アプリのメイン画面イベントモジュール。
Description:
    各UIのイベントバインドおよびハンドラを管理します。
    ブロックの動的作成・削除、入力補助、検索、DB保存を制御します。
ScreenName:
    案件記録メイン画面
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Optional

from fws_apps.tkinter.fws_case_recorder.views.view import fws_case_recorder_view
from fws_apps.tkinter.fws_case_recorder.views.event import fws_case_recorder_template_event
from fws_apps.tkinter.fws_case_recorder.views.logic import fws_case_recorder_logic
from fws_apps.tkinter.fws_case_recorder.views.models import fws_case_recorder_model_record
from fws_apps.tkinter.fws_case_recorder.views.models import fws_case_recorder_model_template
from fws_apps.tkinter.fws_case_recorder.constant import fws_case_recorder_const

class FwsCaseRecorderEvent:
    """
    Summary:
        メイン画面のイベントハンドラクラス。
    Description:
        View・Logicをインスタンス化し、全イベントをバインドします。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            View・Logicを生成し、イベントを紐付けます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_view_obj: fws_case_recorder_view.FwsCaseRecorderView = fws_case_recorder_view.FwsCaseRecorderView()
        """FwsCaseRecorderView - ビューオブジェクト"""

        self._fws_case_recorder_logic_obj: fws_case_recorder_logic.FwsCaseRecorderLogic = fws_case_recorder_logic.FwsCaseRecorderLogic()
        """FwsCaseRecorderLogic - ロジックオブジェクト"""

        self._fws_case_recorder_template_event_obj: Optional[fws_case_recorder_template_event.FwsCaseRecorderTemplateEvent] = None
        """Optional[FwsCaseRecorderTemplateEvent] - 定型文管理画面イベントの参照"""

        self._block_counter: int = 0
        """int - ブロック連番カウンタ"""

        self._active_blocks: Dict[int, Dict] = {}
        """Dict[int, Dict] - アクティブブロックの管理辞書（キー:ブロックID, 値:ウィジェット辞書）"""

        self._status_timer_id: Optional[str] = None
        """Optional[str] - ステータスバー表示クリア用のタイマーID"""

        self._bind_events()

    def _bind_events(self) -> None:
        """
        Summary:
            全イベントをバインドします。
        Description:
            各ボタン、入力フィールド、メニューにイベントハンドラを紐付けます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # ブロック作成
        self._fws_case_recorder_view_obj.btn_create_block.config(command=self.btn_create_block_click)

        # 検索
        self._fws_case_recorder_view_obj.btn_search.config(command=self.btn_search_click)
        self._fws_case_recorder_view_obj.cmb_search_case.bind("<Return>", self.cmb_search_case_key_press)
        self._fws_case_recorder_view_obj.cmb_search_case.bind("<<ComboboxSelected>>", self.cmb_search_case_select)

        # 案件番号選択時の自動補正
        self._fws_case_recorder_view_obj.cmb_case_number.bind("<<ComboboxSelected>>", self.cmb_case_number_select)

        # 県域・ビル名変更時のサジェスト
        self._fws_case_recorder_view_obj.ent_region.bind("<KeyRelease>", self.ent_region_change)
        self._fws_case_recorder_view_obj.ent_building.bind("<KeyRelease>", self.ent_building_change)
        self._fws_case_recorder_view_obj.ent_search_region.bind("<KeyRelease>", self.ent_search_region_change)
        self._fws_case_recorder_view_obj.ent_search_building.bind("<KeyRelease>", self.ent_search_building_change)

        # メニュー
        self._fws_case_recorder_view_obj.mnu_tools.entryconfig("定型文管理", command=self.mnu_template_manage_click)

        # 最前面と透過度
        self._fws_case_recorder_view_obj.chk_topmost.config(command=self._toggle_topmost)
        self._fws_case_recorder_view_obj.scl_alpha.config(command=self._change_alpha)

        # マウスホイール
        self._fws_case_recorder_view_obj.bind_all("<MouseWheel>", self._on_mousewheel)

        # ウィンドウ終了
        self._fws_case_recorder_view_obj.protocol("WM_DELETE_WINDOW", self._win_main_close)

        # 起動時の復元
        self._restore_active_blocks()
    #endregion

    #region Public Methods
    def start(self) -> None:
        """
        Summary:
            アプリケーションを起動します。
        Description:
            メインループを開始します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_view_obj.mainloop()

    def btn_create_block_click(self) -> None:
        """
        Summary:
            ブロック作成ボタン押下時のイベント処理を行います。
        Description:
            左ペイン上部の入力値を基に新しい案件ブロックを作成します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            ブロック作成ボタンクリック - 新しい案件ブロックが左ペインに追加される。
        """
        region: str = self._fws_case_recorder_view_obj.ent_region.get().strip()
        """str - 県域入力値"""
        building: str = self._fws_case_recorder_view_obj.ent_building.get().strip()
        """str - ビル名入力値"""
        case_number: str = self._fws_case_recorder_view_obj.cmb_case_number.get().strip()
        """str - 案件番号入力値"""
        record_time: str = self._fws_case_recorder_logic_obj.generate_current_time()
        """str - 記録時刻"""

        try:
            record_id: int = self._fws_case_recorder_logic_obj.save_record(region, building, case_number, record_time, "", is_editing=1)
            self._create_block(record_id, region, building, case_number, record_time, "")
            self._update_status("ブロックを作成し、DBへ保存しました。")
        except Exception as e:
            messagebox.showerror("作成エラー", f"ブロック作成に失敗しました: {e}")

    def btn_save_click(self, block_id: int) -> None:
        """
        Summary:
            DB保存ボタン押下時のイベント処理を行います。
        Description:
            指定ブロックの内容をDBに更新保存し、左ペインからブロックを削除してis_editingを0にします。
        Args:
            block_id: int - 保存するブロックのID。
        Returns:
            None - 戻り値なし。
        UserAction:
            DB保存ボタンクリック - 記録がDBに保存され、ブロックが削除される。
        """
        if block_id not in self._active_blocks:
            return

        block_widgets: Dict = self._active_blocks[block_id]
        """Dict - ブロック内ウィジェット辞書"""

        region: str = block_widgets["ent_region"].get().strip()
        """str - 県域"""
        building: str = block_widgets["ent_building"].get().strip()
        """str - ビル名"""
        case_number: str = block_widgets["cmb_case_number"].get().strip()
        """str - 案件番号"""
        record_time: str = block_widgets["ent_record_time"].get().strip()
        """str - 記録時刻"""
        content: str = block_widgets["txt_content"].get("1.0", tk.END).strip()
        """str - 記録内容"""

        if not content:
            messagebox.showwarning("入力エラー", "記録内容を入力してください。")
            return

        try:
            self._fws_case_recorder_logic_obj.update_record(block_id, region, building, case_number, record_time, content)
            self._fws_case_recorder_logic_obj.update_editing_status(block_id, 0)
            block_widgets["frm_block"].destroy()
            del self._active_blocks[block_id]
            self._update_status(f"案件 {case_number} をDBへ保存しました。")
        except Exception as e:
            messagebox.showerror("保存エラー", f"保存に失敗しました: {e}")

    def btn_temp_save_click(self, block_id: int) -> None:
        """
        Summary:
            一時保存ボタン押下時のイベント処理を行います。
        Description:
            指定ブロックの内容をDBに更新保存します（ブロックは維持）。
        Args:
            block_id: int - 保存するブロックのID。
        Returns:
            None - 戻り値なし。
        UserAction:
            一時保存ボタンクリック - 記録がDBに更新保存される。
        """
        if block_id not in self._active_blocks:
            return

        block_widgets: Dict = self._active_blocks[block_id]
        """Dict - ブロック内ウィジェット辞書"""

        region: str = block_widgets["ent_region"].get().strip()
        """str - 県域"""
        building: str = block_widgets["ent_building"].get().strip()
        """str - ビル名"""
        case_number: str = block_widgets["cmb_case_number"].get().strip()
        """str - 案件番号"""
        record_time: str = block_widgets["ent_record_time"].get().strip()
        """str - 記録時刻"""
        content: str = block_widgets["txt_content"].get("1.0", tk.END).strip()
        """str - 記録内容"""

        if not content:
            messagebox.showwarning("入力エラー", "記録内容を入力してください。")
            return

        try:
            self._fws_case_recorder_logic_obj.update_record(block_id, region, building, case_number, record_time, content)
            self._update_status(f"案件 {case_number} を一時保存しました。")
        except Exception as e:
            messagebox.showerror("保存エラー", f"保存に失敗しました: {e}")

    def btn_delete_click(self, block_id: int) -> None:
        """
        Summary:
            左ペインの削除ボタン押下時のイベント処理を行います。
        Description:
            指定されたレコードをDBから削除し、左ペインからブロックを消去します。
        Args:
            block_id: int - 削除するレコードID。
        Returns:
            None - 戻り値なし。
        """
        if block_id not in self._active_blocks:
            return
        if not messagebox.askyesno("削除確認", "このブロックを削除しますか？"):
            return
            
        try:
            self._fws_case_recorder_logic_obj.delete_record(block_id)
            self._active_blocks[block_id]["frm_block"].destroy()
            del self._active_blocks[block_id]
            self._update_status("ブロックを削除しました。")
        except Exception as e:
            messagebox.showerror("削除エラー", f"削除に失敗しました: {e}")

    def btn_search_click(self) -> None:
        """
        Summary:
            検索ボタン押下時のイベント処理を行います。
        Description:
            右ペインの条件で検索し、結果をアコーディオン形式で表示します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            更新(検索)ボタンクリック - 条件に一致する過去の記録が右ペインに表示される。
        """
        region: str = self._fws_case_recorder_view_obj.ent_search_region.get().strip()
        """str - 検索用県域"""
        building: str = self._fws_case_recorder_view_obj.ent_search_building.get().strip()
        """str - 検索用ビル名"""
        case_number: str = self._fws_case_recorder_view_obj.cmb_search_case.get().strip()
        """str - 検索用案件番号"""

        try:
            search_result_list: List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord] = self._fws_case_recorder_logic_obj.search_records(case_number, region, building)
            """List[FwsCaseRecorderModelRecord] - 検索結果リスト"""
            self._display_search_results(search_result_list)
            self._update_status(f"検索結果: {len(search_result_list)} 件")
        except Exception as e:
            messagebox.showerror("検索エラー", f"検索に失敗しました: {e}")

    def ent_region_change(self, event: tk.Event) -> None:
        """
        Summary:
            県域入力変更時のイベント処理を行います。
        Description:
            県域とビル名の組み合わせで案件番号を曖昧検索し、コンボボックスを更新します。
        Args:
            event: tk.Event - キーリリースイベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            県域テキスト入力 - 案件番号のサジェストが更新される。
        """
        self._update_case_number_suggestions()

    def ent_building_change(self, event: tk.Event) -> None:
        """
        Summary:
            ビル名入力変更時のイベント処理を行います。
        Description:
            県域とビル名の組み合わせで案件番号を曖昧検索し、コンボボックスを更新します。
        Args:
            event: tk.Event - キーリリースイベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            ビル名テキスト入力 - 案件番号のサジェストが更新される。
        """
        self._update_case_number_suggestions()

    def ent_search_region_change(self, event: tk.Event) -> None:
        """
        Summary:
            検索用県域入力変更時のイベント処理を行います。
        Description:
            検索用県域とビル名の組み合わせで案件番号を曖昧検索し、コンボボックスを更新します。
        Args:
            event: tk.Event - キーリリースイベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            検索用県域テキスト入力 - 案件番号のサジェストが更新される。
        """
        self._update_search_case_number_suggestions()

    def ent_search_building_change(self, event: tk.Event) -> None:
        """
        Summary:
            検索用ビル名入力変更時のイベント処理を行います。
        Description:
            検索用県域とビル名の組み合わせで案件番号を曖昧検索し、コンボボックスを更新します。
        Args:
            event: tk.Event - キーリリースイベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            検索用ビル名テキスト入力 - 案件番号のサジェストが更新される。
        """
        self._update_search_case_number_suggestions()

    def cmb_case_number_select(self, event: tk.Event) -> None:
        """
        Summary:
            案件番号選択時のイベント処理を行います。
        Description:
            選択された案件番号でDBを検索し、県域とビル名を自動補正します。
        Args:
            event: tk.Event - コンボボックス選択イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            案件番号コンボボックス選択 - 県域とビル名が自動入力される。
        """
        self._autofill_region_building(
            self._fws_case_recorder_view_obj.cmb_case_number,
            self._fws_case_recorder_view_obj.ent_region,
            self._fws_case_recorder_view_obj.ent_building
        )

    def cmb_search_case_select(self, event: tk.Event) -> None:
        """
        Summary:
            検索用案件番号選択時のイベント処理を行います。
        Description:
            選択された案件番号でDBを検索し、検索用県域とビル名を自動補正します。
        Args:
            event: tk.Event - コンボボックス選択イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            検索用案件番号コンボボックス選択 - 検索用県域とビル名が自動入力される。
        """
        self._autofill_region_building(
            self._fws_case_recorder_view_obj.cmb_search_case,
            self._fws_case_recorder_view_obj.ent_search_region,
            self._fws_case_recorder_view_obj.ent_search_building
        )

    def btn_arrow_r_click(self, txt_widget: tk.Text) -> None:
        """
        Summary:
            右矢印ボタン押下時のイベント処理を行います。
        Description:
            指定テキストエリアのカーソル位置に→記号を挿入します。
        Args:
            txt_widget: tk.Text - 挿入対象のテキストウィジェット。
        Returns:
            None - 戻り値なし。
        UserAction:
            →ボタンクリック - カーソル位置に→が挿入される。
        """
        self._insert_symbol(txt_widget, fws_case_recorder_const.SYMBOL_ARROW_RIGHT)

    def btn_arrow_l_click(self, txt_widget: tk.Text) -> None:
        """
        Summary:
            左矢印ボタン押下時のイベント処理を行います。
        Description:
            指定テキストエリアのカーソル位置に←記号を挿入します。
        Args:
            txt_widget: tk.Text - 挿入対象のテキストウィジェット。
        Returns:
            None - 戻り値なし。
        UserAction:
            ←ボタンクリック - カーソル位置に←が挿入される。
        """
        self._insert_symbol(txt_widget, fws_case_recorder_const.SYMBOL_ARROW_LEFT)

    def btn_quote_click(self, txt_widget: tk.Text) -> None:
        """
        Summary:
            引用線ボタン押下時のイベント処理を行います。
        Description:
            指定テキストエリアのカーソル位置に引用線を挿入します。
        Args:
            txt_widget: tk.Text - 挿入対象のテキストウィジェット。
        Returns:
            None - 戻り値なし。
        UserAction:
            引用線ボタンクリック - カーソル位置に引用線が挿入される。
        """
        insert_text: str = self._fws_case_recorder_logic_obj.build_insert_text(fws_case_recorder_const.SYMBOL_QUOTE_LINE)
        """str - 挿入テキスト"""
        self._insert_symbol(txt_widget, insert_text)

    def btn_tmpl_click(self, txt_widget: tk.Text) -> None:
        """
        Summary:
            定型文挿入ボタン押下時のイベント処理を行います。
        Description:
            定型文選択ダイアログを表示し、選択された定型文をテキストエリアに挿入します。
        Args:
            txt_widget: tk.Text - 挿入対象のテキストウィジェット。
        Returns:
            None - 戻り値なし。
        UserAction:
            定型文ボタンクリック - 定型文選択メニューが表示される。
        """
        template_model_list: List[fws_case_recorder_model_template.FwsCaseRecorderModelTemplate] = self._fws_case_recorder_logic_obj.fetch_all_templates()
        """List[FwsCaseRecorderModelTemplate] - 定型文リスト"""

        if not template_model_list:
            messagebox.showinfo("情報", "定型文が登録されていません。\nメニューの「ツール」→「定型文管理」から登録してください。")
            return

        popup_menu: tk.Menu = tk.Menu(self._fws_case_recorder_view_obj, tearoff=0)
        """tk.Menu - 定型文ポップアップメニュー"""
        for model_obj in template_model_list:
            popup_menu.add_command(
                label=model_obj.display_title,
                command=lambda content=model_obj.content, widget=txt_widget: self._insert_symbol(widget, content)
            )

        try:
            popup_menu.tk_popup(
                txt_widget.winfo_rootx(),
                txt_widget.winfo_rooty()
            )
        finally:
            popup_menu.grab_release()

    def btn_history_save_click(self, record_id: int, widgets: Dict) -> None:
        """
        Summary:
            履歴レコード保存ボタン押下時のイベント処理を行います。
        Description:
            展開されたアコーディオン内の編集内容をDBに更新保存します。
        Args:
            record_id: int - 更新対象のレコードID。
            widgets: Dict - アコーディオンブロックのウィジェット辞書。
        Returns:
            None - 戻り値なし。
        UserAction:
            履歴保存ボタンクリック - 編集した履歴レコードがDBに更新保存される。
        """
        region_widget = widgets.get("region")
        region: str = region_widget.get().strip() if isinstance(region_widget, (ttk.Entry, tk.Entry, ttk.Combobox)) else str(region_widget)
        """str - 県域"""
        
        building_widget = widgets.get("building")
        building: str = building_widget.get().strip() if isinstance(building_widget, (ttk.Entry, tk.Entry, ttk.Combobox)) else str(building_widget)
        """str - ビル名"""
        
        case_number_widget = widgets.get("case_number")
        case_number: str = case_number_widget.get().strip() if isinstance(case_number_widget, (ttk.Entry, tk.Entry, ttk.Combobox)) else str(case_number_widget)
        """str - 案件番号"""
        
        record_time_widget = widgets.get("record_time")
        record_time: str = record_time_widget.get().strip() if isinstance(record_time_widget, (ttk.Entry, tk.Entry, ttk.Combobox)) else str(record_time_widget)
        """str - 記録時刻"""
        
        content: str = widgets["txt_content"].get("1.0", tk.END).strip()
        """str - 記録内容"""

        try:
            self._fws_case_recorder_logic_obj.update_record(record_id, region, building, case_number, record_time, content)
            self._update_status(f"レコード ID:{record_id} を更新しました。")
        except Exception as e:
            messagebox.showerror("更新エラー", f"更新に失敗しました: {e}")

    def btn_history_delete_click(self, record_id: int) -> None:
        """
        Summary:
            右ペイン履歴レコード削除ボタン押下時のイベント処理を行います。
        Description:
            指定レコードを削除し、右ペインの検索結果を更新します。
        Args:
            record_id: int - 削除するレコードID。
        Returns:
            None - 戻り値なし。
        """
        if not messagebox.askyesno("削除確認", "この履歴を削除しますか？"):
            return
            
        try:
            self._fws_case_recorder_logic_obj.delete_record(record_id)
            self._update_status(f"レコード ID:{record_id} を削除しました。")
            self.btn_search_click()
        except Exception as e:
            messagebox.showerror("削除エラー", f"削除に失敗しました: {e}")

    def mnu_template_manage_click(self) -> None:
        """
        Summary:
            定型文管理メニュー押下時のイベント処理を行います。
        Description:
            定型文管理画面を表示します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            メニュー「定型文管理」クリック - 定型文管理画面が表示される。
        """
        self._fws_case_recorder_template_event_obj = fws_case_recorder_template_event.FwsCaseRecorderTemplateEvent(self._fws_case_recorder_view_obj)

    def cmb_search_case_key_press(self, event: tk.Event) -> None:
        """
        Summary:
            検索フィールドでのEnterキー押下時のイベント処理を行います。
        Description:
            Enterキーで検索を実行します。
        Args:
            event: tk.Event - キー押下イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        UserAction:
            検索フィールドでEnterキー押下 - 検索が実行される。
        """
        self.btn_search_click()
    #endregion

    #region Private Methods
    def _toggle_topmost(self) -> None:
        self._fws_case_recorder_view_obj.attributes("-topmost", self._fws_case_recorder_view_obj.var_topmost.get())

    def _change_alpha(self, event=None) -> None:
        self._fws_case_recorder_view_obj.attributes("-alpha", self._fws_case_recorder_view_obj.scl_alpha.get())

    def _on_mousewheel(self, event: tk.Event) -> None:
        widget = self._fws_case_recorder_view_obj.winfo_containing(event.x_root, event.y_root)
        if widget:
            current = widget
            while current:
                if isinstance(current, tk.Canvas):
                    current.yview_scroll(int(-1*(event.delta/120)), "units")
                    break
                current = current.master

    def _create_block(self, block_id: int, region: str, building: str, case_number: str, record_time: str, content: str) -> None:
        """
        Summary:
            案件ブロックを動的に作成します。
        Description:
            左ペインのブロックコンテナに新しいブロックを追加します。
        Args:
            block_id: int - DBのレコードID。
            region: str - 県域。
            building: str - ビル名。
            case_number: str - 案件番号。
            record_time: str - 記録時刻。
            content: str - 記録内容。
        Returns:
            None - 戻り値なし。
        """

        # ブロックフレーム全体
        frm_block: ttk.Frame = ttk.Frame(self._fws_case_recorder_view_obj.frm_blocks_container)
        """ttk.Frame - ブロック全体フレーム"""
        frm_block.pack(fill=tk.X, padx=5, pady=5)

        # アコーディオンヘッダー
        frm_block_header: ttk.Frame = ttk.Frame(frm_block)
        """ttk.Frame - ヘッダーフレーム"""
        frm_block_header.pack(fill=tk.X)
        
        frm_block_content: ttk.LabelFrame = ttk.LabelFrame(frm_block, text="")
        """ttk.LabelFrame - ブロックコンテンツフレーム"""
        frm_block_content.pack(fill=tk.X)

        is_expanded: tk.BooleanVar = tk.BooleanVar(value=True)
        """tk.BooleanVar - 展開状態"""

        # コンボボックスは下で生成するため一時的に参照用の変数を保持する（後に設定）
        cmb_ref: dict = {"cmb": None}

        btn_header: ttk.Button = ttk.Button(
            frm_block_header,
            text=f"▼ ブロック #{block_id} [{case_number}]",
            command=lambda: self._toggle_block_accordion(btn_header, frm_block_content, is_expanded, block_id, cmb_ref),
            style="Left.TButton"
        )
        """ttk.Button - ヘッダーボタン"""
        btn_header.pack(fill=tk.X)

        # 1行目: 県域・ビル名
        frm_block_row1: ttk.Frame = ttk.Frame(frm_block_content)
        """ttk.Frame - ブロック1行目"""
        frm_block_row1.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frm_block_row1, text="県域:").pack(side=tk.LEFT, padx=(0, 2))
        ent_block_region: ttk.Entry = ttk.Entry(frm_block_row1, width=8)
        """ttk.Entry - ブロック内県域"""
        ent_block_region.pack(side=tk.LEFT, padx=(0, 2))
        ent_block_region.insert(0, region)

        ttk.Label(frm_block_row1, text="ビル名:").pack(side=tk.LEFT, padx=(0, 2))
        ent_block_building: ttk.Entry = ttk.Entry(frm_block_row1, width=10)
        """ttk.Entry - ブロック内ビル名"""
        ent_block_building.pack(side=tk.LEFT, padx=(0, 2))
        ent_block_building.insert(0, building)

        # 2行目: 案件番号・時間
        frm_block_row2: ttk.Frame = ttk.Frame(frm_block_content)
        """ttk.Frame - ブロック2行目"""
        frm_block_row2.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frm_block_row2, text="案件番号:").pack(side=tk.LEFT, padx=(0, 2))
        cmb_block_case_number: ttk.Combobox = ttk.Combobox(frm_block_row2, width=15)
        """ttk.Combobox - ブロック内案件番号"""
        cmb_block_case_number.pack(side=tk.LEFT, padx=(0, 2))
        cmb_block_case_number.set(case_number)
        cmb_ref["cmb"] = cmb_block_case_number

        ttk.Label(frm_block_row2, text="時間:").pack(side=tk.LEFT, padx=(0, 2))
        ent_block_record_time: ttk.Entry = ttk.Entry(frm_block_row2, width=15)
        """ttk.Entry - ブロック内記録時刻"""
        ent_block_record_time.pack(side=tk.LEFT)
        ent_block_record_time.insert(0, record_time)

        var_time_check: tk.BooleanVar = tk.BooleanVar(value=False)
        """tk.BooleanVar - 時間更新チェック状態"""
        chk_time: ttk.Checkbutton = ttk.Checkbutton(
            frm_block_row2, 
            text="更新", 
            variable=var_time_check, 
            command=lambda: self._on_time_check(var_time_check, ent_block_record_time)
        )
        """ttk.Checkbutton - 時間更新チェックボックス"""
        chk_time.pack(side=tk.LEFT, padx=(2, 8))

        # ブロック内の県域・ビル名変更でサジェスト更新
        ent_block_region.bind("<KeyRelease>", lambda e, r=ent_block_region, b=ent_block_building, c=cmb_block_case_number: self._update_block_case_suggestions(r, b, c))
        ent_block_building.bind("<KeyRelease>", lambda e, r=ent_block_region, b=ent_block_building, c=cmb_block_case_number: self._update_block_case_suggestions(r, b, c))
        # ブロック内の案件番号選択時に自動補正
        cmb_block_case_number.bind("<<ComboboxSelected>>", lambda e, c=cmb_block_case_number, r=ent_block_region, b=ent_block_building: self._autofill_region_building(c, r, b))

        # 3行目: ツールバー
        frm_block_toolbar: ttk.Frame = ttk.Frame(frm_block_content)
        """ttk.Frame - ブロックツールバー"""
        frm_block_toolbar.pack(fill=tk.X, padx=5, pady=2)

        # テキストエリア（先に変数を宣言し、ツールバーボタンのcommandで参照可能にする）
        txt_block_content: tk.Text = tk.Text(frm_block_content, height=8, undo=True)
        """tk.Text - ブロック内記録内容テキストエリア"""

        btn_block_arrow_r: ttk.Button = ttk.Button(frm_block_toolbar, text="→", width=3,
            command=lambda: self.btn_arrow_r_click(txt_block_content))
        """ttk.Button - 右矢印ボタン"""
        btn_block_arrow_r.pack(side=tk.LEFT, padx=(0, 2))

        btn_block_arrow_l: ttk.Button = ttk.Button(frm_block_toolbar, text="←", width=3,
            command=lambda: self.btn_arrow_l_click(txt_block_content))
        """ttk.Button - 左矢印ボタン"""
        btn_block_arrow_l.pack(side=tk.LEFT, padx=(0, 2))

        btn_block_quote: ttk.Button = ttk.Button(frm_block_toolbar, text="---", width=4,
            command=lambda: self.btn_quote_click(txt_block_content))
        """ttk.Button - 引用線ボタン"""
        btn_block_quote.pack(side=tk.LEFT, padx=(0, 2))

        btn_block_tmpl: ttk.Button = ttk.Button(frm_block_toolbar, text="定型文▼", width=7,
            command=lambda: self.btn_tmpl_click(txt_block_content))
        """ttk.Button - 定型文ボタン"""
        btn_block_tmpl.pack(side=tk.LEFT, padx=(0, 2))

        btn_block_time: ttk.Button = ttk.Button(frm_block_toolbar, text="時刻挿入", width=8,
            command=lambda: self._insert_symbol(txt_block_content, self._fws_case_recorder_logic_obj.generate_current_time()))
        """ttk.Button - 時刻挿入ボタン"""
        btn_block_time.pack(side=tk.LEFT, padx=(0, 2))

        # テキストエリア配置
        txt_block_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        txt_block_content.insert("1.0", content)

        # キーボードショートカットバインド
        txt_block_content.bind("<Control-Right>", lambda e: self._insert_symbol(txt_block_content, fws_case_recorder_const.SYMBOL_ARROW_RIGHT) or "break")
        txt_block_content.bind("<Control-Left>", lambda e: self._insert_symbol(txt_block_content, fws_case_recorder_const.SYMBOL_ARROW_LEFT) or "break")
        txt_block_content.bind("<Control-q>", lambda e: self.btn_quote_click(txt_block_content) or "break")
        txt_block_content.bind("<Control-t>", lambda e: self.btn_tmpl_click(txt_block_content) or "break")

        # 保存・削除ボタン
        frm_block_buttons: ttk.Frame = ttk.Frame(frm_block_content)
        """ttk.Frame - ブロックボタン行"""
        frm_block_buttons.pack(fill=tk.X, padx=5, pady=(2, 5))

        btn_block_delete: ttk.Button = ttk.Button(frm_block_buttons, text="削除",
            command=lambda bid=block_id: self.btn_delete_click(bid))
        """ttk.Button - 削除ボタン"""
        btn_block_delete.pack(side=tk.LEFT)

        btn_block_save: ttk.Button = ttk.Button(frm_block_buttons, text="DB保存(閉じる)",
            command=lambda bid=block_id: self.btn_save_click(bid))
        """ttk.Button - DB保存ボタン"""
        btn_block_save.pack(side=tk.RIGHT, padx=(5, 0))

        btn_block_temp_save: ttk.Button = ttk.Button(frm_block_buttons, text="一時保存",
            command=lambda bid=block_id: self.btn_temp_save_click(bid))
        """ttk.Button - 一時保存ボタン"""
        btn_block_temp_save.pack(side=tk.RIGHT)

        # ブロック管理辞書に登録
        self._active_blocks[block_id] = {
            "frm_block": frm_block,
            "ent_region": ent_block_region,
            "ent_building": ent_block_building,
            "cmb_case_number": cmb_block_case_number,
            "ent_record_time": ent_block_record_time,
            "txt_content": txt_block_content
        }

        # キャンバスのスクロール領域を更新
        self._fws_case_recorder_view_obj.frm_blocks_container.update_idletasks()
        self._fws_case_recorder_view_obj.cvs_blocks.configure(
            scrollregion=self._fws_case_recorder_view_obj.cvs_blocks.bbox("all")
        )

    def _toggle_block_accordion(self, btn_header: ttk.Button, frm_content: ttk.Frame, is_expanded: tk.BooleanVar, block_id: int, cmb_ref: dict) -> None:
        case_number = cmb_ref["cmb"].get().strip() if cmb_ref["cmb"] else ""
        if is_expanded.get():
            frm_content.pack_forget()
            btn_header.config(text=f"▶ ブロック #{block_id} [{case_number}]")
            is_expanded.set(False)
        else:
            frm_content.pack(fill=tk.X)
            btn_header.config(text=f"▼ ブロック #{block_id} [{case_number}]")
            is_expanded.set(True)
        self._fws_case_recorder_view_obj.frm_blocks_container.update_idletasks()
        self._fws_case_recorder_view_obj.cvs_blocks.configure(scrollregion=self._fws_case_recorder_view_obj.cvs_blocks.bbox("all"))

    def _on_time_check(self, var_time_check: tk.BooleanVar, ent_time: ttk.Entry) -> None:
        if var_time_check.get():
            ent_time.delete(0, tk.END)
            ent_time.insert(0, self._fws_case_recorder_logic_obj.generate_current_time())

    def _display_search_results(self, result_list: List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord]) -> None:
        """
        Summary:
            検索結果をアコーディオン形式で右ペインに表示します。
        Description:
            既存の検索結果をクリアし、新しい結果をアコーディオンブロックとして追加します。
        Args:
            result_list: List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord] - 検索結果リスト。
        Returns:
            None - 戻り値なし。
        """
        # 既存結果をクリア
        for widget in self._fws_case_recorder_view_obj.frm_history_container.winfo_children():
            widget.destroy()

        if not result_list:
            lbl_no_result: ttk.Label = ttk.Label(self._fws_case_recorder_view_obj.frm_history_container, text="該当する記録がありません。")
            """ttk.Label - 結果なしラベル"""
            lbl_no_result.pack(padx=10, pady=10)
            return

        for model_obj in result_list:
            self._create_accordion_item(model_obj)

        # スクロール領域を更新
        self._fws_case_recorder_view_obj.frm_history_container.update_idletasks()
        self._fws_case_recorder_view_obj.cvs_history.configure(
            scrollregion=self._fws_case_recorder_view_obj.cvs_history.bbox("all")
        )

    def _create_accordion_item(self, model_obj: fws_case_recorder_model_record.FwsCaseRecorderModelRecord) -> None:
        """
        Summary:
            アコーディオンアイテムを作成します。
        Description:
            折りたたみ可能なヘッダーと編集可能なコンテンツ領域を作成します。
        Args:
            model_obj: fws_case_recorder_model_record.FwsCaseRecorderModelRecord - 表示するレコードModel。
        Returns:
            None - 戻り値なし。
        """
        frm_accordion: ttk.Frame = ttk.Frame(self._fws_case_recorder_view_obj.frm_history_container)
        """ttk.Frame - アコーディオンフレーム"""
        frm_accordion.pack(fill=tk.X, padx=5, pady=2)

        # コンテンツフレーム（折りたたみ対象）
        frm_content: ttk.Frame = ttk.Frame(frm_accordion)
        """ttk.Frame - コンテンツフレーム"""

        is_expanded: tk.BooleanVar = tk.BooleanVar(value=False)
        """tk.BooleanVar - 展開状態"""

        # ヘッダーボタン
        btn_header: ttk.Button = ttk.Button(
            frm_accordion,
            text=f"▶ {model_obj.display_header}",
            command=lambda: self._toggle_accordion(btn_header, frm_content, is_expanded, model_obj.display_header),
            style="Left.TButton"
        )
        """ttk.Button - アコーディオンヘッダーボタン"""
        btn_header.pack(fill=tk.X)

        # 1行目: 県域・ビル名
        frm_hist_row1: ttk.Frame = ttk.Frame(frm_content)
        frm_hist_row1.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frm_hist_row1, text="県域:").pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_region: ttk.Entry = ttk.Entry(frm_hist_row1, width=8)
        ent_hist_region.pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_region.insert(0, model_obj.region)
        
        ttk.Label(frm_hist_row1, text="ビル名:").pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_building: ttk.Entry = ttk.Entry(frm_hist_row1, width=10)
        ent_hist_building.pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_building.insert(0, model_obj.building)

        # 2行目: 案件番号・時間
        frm_hist_row2: ttk.Frame = ttk.Frame(frm_content)
        frm_hist_row2.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frm_hist_row2, text="案件番号:").pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_case: ttk.Entry = ttk.Entry(frm_hist_row2, width=15)
        ent_hist_case.pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_case.insert(0, model_obj.case_number)
        
        ttk.Label(frm_hist_row2, text="時間:").pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_time: ttk.Entry = ttk.Entry(frm_hist_row2, width=15)
        ent_hist_time.pack(side=tk.LEFT, padx=(0, 2))
        ent_hist_time.insert(0, model_obj.record_time)

        # 3行目: ツールバー
        frm_hist_toolbar: ttk.Frame = ttk.Frame(frm_content)
        frm_hist_toolbar.pack(fill=tk.X, padx=5, pady=2)

        # テキストエリア（先に宣言）
        txt_history_content: tk.Text = tk.Text(frm_content, height=6, undo=True)

        btn_hist_arrow_r: ttk.Button = ttk.Button(frm_hist_toolbar, text="→", width=3,
            command=lambda: self.btn_arrow_r_click(txt_history_content))
        btn_hist_arrow_r.pack(side=tk.LEFT, padx=(0, 2))

        btn_hist_arrow_l: ttk.Button = ttk.Button(frm_hist_toolbar, text="←", width=3,
            command=lambda: self.btn_arrow_l_click(txt_history_content))
        btn_hist_arrow_l.pack(side=tk.LEFT, padx=(0, 2))

        btn_hist_quote: ttk.Button = ttk.Button(frm_hist_toolbar, text="---", width=4,
            command=lambda: self.btn_quote_click(txt_history_content))
        btn_hist_quote.pack(side=tk.LEFT, padx=(0, 2))

        btn_hist_tmpl: ttk.Button = ttk.Button(frm_hist_toolbar, text="定型文▼", width=7,
            command=lambda: self.btn_tmpl_click(txt_history_content))
        btn_hist_tmpl.pack(side=tk.LEFT, padx=(0, 2))

        btn_hist_time: ttk.Button = ttk.Button(frm_hist_toolbar, text="時刻挿入", width=8,
            command=lambda: self._insert_symbol(txt_history_content, self._fws_case_recorder_logic_obj.generate_current_time()))
        btn_hist_time.pack(side=tk.LEFT, padx=(0, 2))

        # コンテンツ
        """tk.Text - 履歴編集テキストエリア"""
        txt_history_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        txt_history_content.insert("1.0", model_obj.content)

        accordion_widgets: Dict = {
            "txt_content": txt_history_content,
            "region": ent_hist_region,
            "building": ent_hist_building,
            "case_number": ent_hist_case,
            "record_time": ent_hist_time
        }
        """Dict - アコーディオンウィジェット辞書"""

        btn_history_delete: ttk.Button = ttk.Button(
            frm_content, text="削除",
            command=lambda rid=model_obj.record_id: self.btn_history_delete_click(rid)
        )
        """ttk.Button - 履歴削除ボタン"""
        btn_history_delete.pack(side=tk.LEFT, padx=5, pady=(0, 5))

        btn_history_save: ttk.Button = ttk.Button(
            frm_content, text="保存",
            command=lambda rid=model_obj.record_id, w=accordion_widgets: self.btn_history_save_click(rid, w)
        )
        """ttk.Button - 履歴保存ボタン"""
        btn_history_save.pack(side=tk.RIGHT, padx=5, pady=(0, 5))

    def _toggle_accordion(self, btn_header: ttk.Button, frm_content: ttk.Frame, is_expanded: tk.BooleanVar, display_header: str) -> None:
        """
        Summary:
            アコーディオンの展開/折りたたみを切り替えます。
        Description:
            展開状態を反転し、コンテンツフレームの表示/非表示を制御します。
        Args:
            btn_header: ttk.Button - ヘッダーボタン。
            frm_content: ttk.Frame - コンテンツフレーム。
            is_expanded: tk.BooleanVar - 展開状態。
            display_header: str - ヘッダー表示テキスト。
        Returns:
            None - 戻り値なし。
        """
        if is_expanded.get():
            frm_content.pack_forget()
            btn_header.config(text=f"▶ {display_header}")
            is_expanded.set(False)
        else:
            frm_content.pack(fill=tk.X)
            btn_header.config(text=f"▼ {display_header}")
            is_expanded.set(True)

        # スクロール領域を更新
        self._fws_case_recorder_view_obj.frm_history_container.update_idletasks()
        self._fws_case_recorder_view_obj.cvs_history.configure(
            scrollregion=self._fws_case_recorder_view_obj.cvs_history.bbox("all")
        )

    def _insert_symbol(self, txt_widget: tk.Text, symbol: str) -> None:
        """
        Summary:
            テキストウィジェットのカーソル位置に記号を挿入します。
        Description:
            現在のカーソル位置に指定された記号文字列を挿入します。
        Args:
            txt_widget: tk.Text - 挿入対象のテキストウィジェット。
            symbol: str - 挿入する記号文字列。
        Returns:
            None - 戻り値なし。
        """
        txt_widget.insert(tk.INSERT, symbol)
        txt_widget.focus_set()

    def _update_case_number_suggestions(self) -> None:
        """
        Summary:
            左ペイン上部の案件番号サジェストを更新します。
        Description:
            県域とビル名でLogic層を呼び出し、コンボボックスの選択肢を更新します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        region: str = self._fws_case_recorder_view_obj.ent_region.get().strip()
        """str - 県域"""
        building: str = self._fws_case_recorder_view_obj.ent_building.get().strip()
        """str - ビル名"""

        if not region and not building:
            self._fws_case_recorder_view_obj.cmb_case_number["values"] = []
            return

        try:
            case_number_list: List[str] = self._fws_case_recorder_logic_obj.search_case_numbers(region, building)
            """List[str] - サジェスト案件番号リスト"""
            self._fws_case_recorder_view_obj.cmb_case_number["values"] = case_number_list
        except Exception:
            self._fws_case_recorder_view_obj.cmb_case_number["values"] = []

    def _update_block_case_suggestions(self, ent_region: ttk.Entry, ent_building: ttk.Entry, cmb_case_number: ttk.Combobox) -> None:
        """
        Summary:
            ブロック内の案件番号サジェストを更新します。
        Description:
            ブロック内の県域・ビル名でLogic層を呼び出し、ブロック内コンボボックスを更新します。
        Args:
            ent_region: ttk.Entry - ブロック内県域入力。
            ent_building: ttk.Entry - ブロック内ビル名入力。
            cmb_case_number: ttk.Combobox - ブロック内案件番号コンボボックス。
        Returns:
            None - 戻り値なし。
        """
        region: str = ent_region.get().strip()
        """str - 県域"""
        building: str = ent_building.get().strip()
        """str - ビル名"""

        if not region and not building:
            cmb_case_number["values"] = []
            return

        try:
            case_number_list: List[str] = self._fws_case_recorder_logic_obj.search_case_numbers(region, building)
            """List[str] - サジェスト案件番号リスト"""
            cmb_case_number["values"] = case_number_list
        except Exception:
            cmb_case_number["values"] = []

    def _update_search_case_number_suggestions(self) -> None:
        """
        Summary:
            右ペイン上部の検索用案件番号サジェストを更新します。
        Description:
            検索用県域とビル名でLogic層を呼び出し、コンボボックスの選択肢を更新します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        region: str = self._fws_case_recorder_view_obj.ent_search_region.get().strip()
        """str - 検索用県域"""
        building: str = self._fws_case_recorder_view_obj.ent_search_building.get().strip()
        """str - 検索用ビル名"""

        if not region and not building:
            self._fws_case_recorder_view_obj.cmb_search_case["values"] = []
            return

        try:
            case_number_list: List[str] = self._fws_case_recorder_logic_obj.search_case_numbers(region, building)
            """List[str] - サジェスト案件番号リスト"""
            self._fws_case_recorder_view_obj.cmb_search_case["values"] = case_number_list
        except Exception:
            self._fws_case_recorder_view_obj.cmb_search_case["values"] = []

    def _restore_active_blocks(self) -> None:
        """
        Summary:
            アプリ起動時に編集中のレコードを復元します。
        Description:
            is_editing=1 のレコードを取得し、左ペインにブロックを作成します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        try:
            active_records = self._fws_case_recorder_logic_obj.fetch_active_records()
            for record in active_records:
                self._create_block(record.record_id, record.region, record.building, record.case_number, record.record_time, record.content)
        except Exception as e:
            print(f"復元エラー: {e}")

    def _autofill_region_building(self, cmb_case_number: ttk.Combobox, ent_region: ttk.Entry, ent_building: ttk.Entry) -> None:
        """
        Summary:
            案件番号に基づく県域・ビル名の自動補正を行います。
        Description:
            指定された案件番号で記録を検索し、結果があれば県域・ビル名フィールドを上書きします。
        Args:
            cmb_case_number: ttk.Combobox - 案件番号コンボボックス。
            ent_region: ttk.Entry - 県域入力フィールド。
            ent_building: ttk.Entry - ビル名入力フィールド。
        Returns:
            None - 戻り値なし。
        """
        case_number: str = cmb_case_number.get().strip()
        if not case_number:
            return
        
        try:
            records: List[fws_case_recorder_model_record.FwsCaseRecorderModelRecord] = self._fws_case_recorder_logic_obj.search_records(case_number=case_number)
            if records:
                record = records[0]
                ent_region.delete(0, tk.END)
                ent_region.insert(0, record.region)
                ent_building.delete(0, tk.END)
                ent_building.insert(0, record.building)
        except Exception:
            pass

    def _update_status(self, message: str) -> None:
        """
        Summary:
            ステータスバーのメッセージを更新します。
        Description:
            指定メッセージを表示し、一定時間後に初期メッセージに戻します。
        Args:
            message: str - 表示するメッセージ。
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_view_obj.lbl_status.config(text=message)
        if self._status_timer_id:
            self._fws_case_recorder_view_obj.after_cancel(self._status_timer_id)
        self._status_timer_id = self._fws_case_recorder_view_obj.after(
            fws_case_recorder_const.STATUS_MESSAGE_TIMEOUT_MS,
            lambda: self._fws_case_recorder_view_obj.lbl_status.config(text=fws_case_recorder_const.STATUS_MSG_READY)
        )

    def _win_main_close(self) -> None:
        """
        Summary:
            メインウィンドウ終了時の処理を行います。
        Description:
            アプリケーションを終了します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_case_recorder_view_obj.destroy()
    #endregion
