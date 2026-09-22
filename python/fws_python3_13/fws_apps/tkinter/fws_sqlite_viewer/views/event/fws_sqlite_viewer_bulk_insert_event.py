"""
Summary:
    バルクインサート設定ダイアログのEventモジュール。
Description:
    ViewとLogicを連携させ、UIイベントのバインドおよび処理を行います。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable

from fws_apps.tkinter.fws_sqlite_viewer.views.view import fws_sqlite_viewer_bulk_insert_view
from fws_apps.tkinter.fws_sqlite_viewer.views.logic import fws_sqlite_viewer_bulk_insert_logic

class FwsSqliteViewerBulkInsertEvent:
    """
    Summary:
        バルクインサート設定ダイアログのEventクラス。
    Description:
        Viewクラスのイベント(ボタン押下や状態変更)を処理します。
    """

    #region Constructor
    def __init__(self, parent_view: tk.Widget, table_name: str, alias: str, logic_obj, on_success_callback: Callable[[str], None]) -> None:
        """
        Summary:
            コンストラクタ。
        Args:
            parent_view: tk.Widget - 親画面のViewオブジェクト
            table_name: str - 対象テーブル名
            alias: str - 対象DBエイリアス
            logic_obj: FwsSqliteViewerLogic - メインのロジックオブジェクト
            on_success_callback: Callable[[str], None] - 成功時のコールバック(テーブル名を渡しリフレッシュ用)
        """
        self._logic = fws_sqlite_viewer_bulk_insert_logic.FwsSqliteViewerBulkInsertLogic()
        self._main_logic = logic_obj
        self._table_name = table_name
        self._alias = alias
        self._on_success_callback = on_success_callback
        
        self._view = fws_sqlite_viewer_bulk_insert_view.FwsSqliteViewerBulkInsertView(parent_view, table_name)
        
        self._bind_events()
        self._update_states()

    def _bind_events(self) -> None:
        """
        Summary:
            各ウィジェットのイベントをバインドします。
        """
        self._view.btn_browse.configure(command=self._on_browse)
        self._view.btn_execute.configure(command=self._on_execute)
        self._view.var_source.trace_add("write", lambda *args: self._update_states())
        
    def _update_states(self) -> None:
        """
        Summary:
            入力ソースの選択状態に応じてウィジェットの有効/無効を切り替えます。
        """
        if self._view.var_source.get() == "file":
            self._view.ent_filepath.configure(state="normal")
            self._view.btn_browse.configure(state="normal")
            self._view.txt_data.configure(state="disabled")
        else:
            self._view.ent_filepath.configure(state="disabled")
            self._view.btn_browse.configure(state="disabled")
            self._view.txt_data.configure(state="normal")

    def _on_browse(self) -> None:
        """
        Summary:
            ファイル選択ダイアログを表示します。
        """
        path = filedialog.askopenfilename(
            parent=self._view.dlg, 
            filetypes=[("CSV/TSV Files", "*.csv *.tsv"), ("All Files", "*.*")]
        )
        if path:
            self._view.var_filepath.set(path)

    def _on_execute(self) -> None:
        """
        Summary:
            実行ボタン押下時の処理。
        """
        is_file = (self._view.var_source.get() == "file")
        if is_file:
            data = self._view.var_filepath.get()
        else:
            data = self._view.txt_data.get("1.0", tk.END).strip()
            
        is_valid, err_msg = self._logic.validate_input(data, is_file)
        if not is_valid:
            messagebox.showerror("Error", err_msg, parent=self._view.dlg)
            return
                
        delimiter = "\t" if "\\t" in self._view.var_delimiter.get() else ","
        has_header = self._view.var_header.get()
        
        try:
            rowcount = self._logic.bulk_insert(
                main_logic=self._main_logic,
                table_name=self._table_name,
                alias=self._alias,
                data=data,
                is_file=is_file,
                delimiter=delimiter,
                has_header=has_header
            )
            messagebox.showinfo("Success", f"Successfully inserted {rowcount} rows.", parent=self._view.dlg)
            self._view.dlg.destroy()
            
            if self._on_success_callback:
                self._on_success_callback(self._table_name)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert data:\n{str(e)}", parent=self._view.dlg)
    #endregion

