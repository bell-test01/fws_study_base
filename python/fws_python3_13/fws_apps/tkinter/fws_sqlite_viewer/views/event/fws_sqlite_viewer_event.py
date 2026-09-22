"""
Summary:
    fws_sqlite_viewer アプリのイベントモジュール。
Description:
    各UIのイベントバインドおよび処理の呼び出しを行います。
ScreenName:
    SQLite Viewer メイン画面
Attachment:
    なし
"""
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import re
import json
import os
from typing import List, Optional, Dict

from fws_apps.tkinter.fws_sqlite_viewer.views.view import fws_sqlite_viewer_view
from fws_apps.tkinter.fws_sqlite_viewer.views.event import fws_sqlite_viewer_history_event
from fws_apps.tkinter.fws_sqlite_viewer.views.logic import fws_sqlite_viewer_logic
from fws_apps.tkinter.fws_sqlite_viewer.views.models import fws_sqlite_viewer_model_query_result
from fws_apps.tkinter.fws_sqlite_viewer.views.models import fws_sqlite_viewer_model_table_schema
from fws_apps.tkinter.fws_sqlite_viewer.constant import fws_sqlite_viewer_const

class FwsSqliteViewerEvent:
    """
    Summary:
        イベントハンドラクラス。
    Description:
        各クラスをインスタンス化し、イベントをバインドします。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            各クラスを生成し、イベントを紐付けます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_sqlite_viewer_view_obj: fws_sqlite_viewer_view.FwsSqliteViewerView = fws_sqlite_viewer_view.FwsSqliteViewerView()
        """fws_sqlite_viewer_view.FwsSqliteViewerView - ビューオブジェクト"""
        
        self._fws_sqlite_viewer_logic_obj: fws_sqlite_viewer_logic.FwsSqliteViewerLogic = fws_sqlite_viewer_logic.FwsSqliteViewerLogic()
        """fws_sqlite_viewer_logic.FwsSqliteViewerLogic - ロジックオブジェクト"""

        self._fws_sqlite_viewer_history_event_obj: Optional[fws_sqlite_viewer_history_event.FwsSqliteViewerHistoryEvent] = None
        """Optional[FwsSqliteViewerHistoryEvent] - 履歴ダイアログの参照"""

        self._session_file: Path = fws_sqlite_viewer_const.DATA_DIR / fws_sqlite_viewer_const.SESSION_FILE_NAME

        self._status_timer_id: Optional[str] = None
        """Optional[str] - ステータスバー表示クリア用のタイマーID"""

        self._last_query_sql: str = ""
        self._last_query_result: Optional[fws_sqlite_viewer_model_query_result.FwsSqliteViewerModelQueryResult] = None

        self._bind_events()
        self._restore_session()
        self._set_status(fws_sqlite_viewer_const.STATUS_MSG_READY)
    #endregion

    #region Public Methods
    def start(self) -> None:
        """
        Summary:
            メインループを開始します。
        """
        self._fws_sqlite_viewer_view_obj.mainloop()

    def _restore_session(self) -> None:
        """
        Summary:
            起動時に session.json を読み込み、前回接続していたDBを復元します。
        """
        if not self._session_file.exists():
            return
            
        try:
            with open(self._session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            main_db = data.get("main_db")
            if main_db and Path(main_db).exists():
                self._load_db(main_db, is_main=True)
                
                attached_dbs = data.get("attached_dbs", [])
                for att in attached_dbs:
                    path = att.get("path")
                    alias = att.get("alias")
                    if path and alias and Path(path).exists():
                        try:
                            self._fws_sqlite_viewer_logic_obj.attach_db(path, alias)
                        except Exception as e:
                            print(f"Skipping restore for {path}: {e}")
                
                # 全てアタッチし終わったらUI更新
                tables = self._fws_sqlite_viewer_logic_obj.get_tables()
                self._update_tables_list(tables)
        except Exception as e:
            self._set_status(f"Error restoring session: {e}", is_error=True)

    def _bind_events(self) -> None:
        """
        Summary:
            UIイベントをバインドします。
        Description:
            ボタンクリックやツリー選択などを紐付けます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_sqlite_viewer_view_obj.btn_open_db.config(command=self.btn_open_db_click)
        self._fws_sqlite_viewer_view_obj.btn_new_db.config(command=self.btn_new_db_click)

        self._fws_sqlite_viewer_view_obj.btn_run_query.config(command=self.btn_run_query_click)
        for key_bind in ("<Alt-x>", "<Alt-X>"):
            self._fws_sqlite_viewer_view_obj.txt_sql.bind(key_bind, self.btn_run_query_click)

        self._fws_sqlite_viewer_view_obj.trv_tables.bind("<<TreeviewSelect>>", self.trv_tables_select)
        self._fws_sqlite_viewer_view_obj.trv_tables.bind("<Button-3>", self.trv_tables_right_click)
        
        # テキスト入力欄でEnterキーを押した際にもDBを読み込む
        self._fws_sqlite_viewer_view_obj.ent_db_path.bind("<Return>", self.ent_db_path_return)
        
        # クリップボードコピー（データのみ）
        for key_bind in ("<Control-c>", "<Control-C>"):
            self._fws_sqlite_viewer_view_obj.trv_schema.bind(key_bind, self.trv_schema_copy_key_press)
            self._fws_sqlite_viewer_view_obj.trv_results.bind(key_bind, self.trv_results_copy_key_press)
        
        # クリップボードコピー（ヘッダー付き）
        for key_bind in ("<Control-Shift-c>", "<Control-Shift-C>"):
            self._fws_sqlite_viewer_view_obj.trv_schema.bind(key_bind, self.trv_schema_copy_header_key_press)
            self._fws_sqlite_viewer_view_obj.trv_results.bind(key_bind, self.trv_results_copy_header_key_press)
        
        # ダブルクリックでセル単体・テーブル名・スキーマタイトルコピー
        self._fws_sqlite_viewer_view_obj.trv_tables.bind("<Double-1>", self.trv_tables_double_click)
        self._fws_sqlite_viewer_view_obj.trv_schema.bind("<Double-1>", self.trv_schema_double_click)
        self._fws_sqlite_viewer_view_obj.trv_results.bind("<Double-1>", self.trv_results_double_click)
        self._fws_sqlite_viewer_view_obj.frm_schema.bind("<Double-1>", self.frm_schema_double_click)
        
        # SQLエディタのオートインデントとショートカット
        self._fws_sqlite_viewer_view_obj.txt_sql.bind("<Return>", self.txt_sql_return)

        self._fws_sqlite_viewer_view_obj.protocol("WM_DELETE_WINDOW", self.win_main_close)
    #endregion

    #region Public Methods
    def btn_open_db_click(self) -> None:
        """
        Summary:
            Open DBボタンクリック時の処理。
        Description:
            ファイルダイアログを開き、選択されたDBのパスを入力欄にセットして読み込みます。
        UserAction:
            「Open DB」ボタンをクリック - ファイルダイアログが開き、選択したDBを読み込む。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        file_path = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[("SQLite DB", "*.db *.sqlite *.sqlite3"), ("All Files", "*.*")]
        )
        if file_path:
            self._load_db(file_path)

    def btn_new_db_click(self) -> None:
        """
        Summary:
            New DBボタンクリック時の処理。
        Description:
            保存先を指定させ、空のDBファイルを作成して読み込みます。
        UserAction:
            「New DB」ボタンをクリック - ファイル保存ダイアログが開き、指定したパスに空のDBを作成して接続する。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        file_path = filedialog.asksaveasfilename(
            title="Create New SQLite Database",
            defaultextension=".db",
            filetypes=[("SQLite DB", "*.db *.sqlite *.sqlite3"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'a') as f:
                    pass
                self._load_db(file_path)
            except Exception as e:
                self._set_status(f"Error creating DB: {e}", is_error=True)

    def ent_db_path_return(self, event: tk.Event) -> None:
        """
        Summary:
            テキスト入力欄でのEnterキー押下時の処理。
        Description:
            入力されているパス文字列を取得し、DBを読み込みます。
        UserAction:
            DB Path の入力欄でEnterキーを押下 - 入力されたパスのDBを読み込む。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        db_path = self._get_db_path()
        if db_path and Path(db_path).exists():
            self._load_db(db_path)
        else:
            self._set_status("Error: Invalid database path.", is_error=True)

    def txt_sql_return(self, event: tk.Event) -> str:
        """
        Summary:
            SQLエディタでEnterキーを押した際のオートインデント処理。
        Description:
            前の行の先頭の空白（スペース・タブ）を引き継いで改行します。
        UserAction:
            SQLエディタ内でEnterキーを押下 - 前の行のインデントを引き継いで改行される。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            str - デフォルトの改行イベントをキャンセルするため "break" を返す。
        """
        current_line = event.widget.get("insert linestart", "insert lineend")
        leading_whitespace = ""
        for char in current_line:
            if char in (' ', '\t'):
                leading_whitespace += char
            else:
                break
        
        event.widget.insert("insert", "\n" + leading_whitespace)
        return "break"

    def btn_run_query_click(self, event: tk.Event = None) -> None:
        """
        Summary:
            Run Queryボタンクリック（またはAlt+X）時の処理。
        Description:
            入力されたSQLを実行し、結果をビューに反映します。
        UserAction:
            「Run Query」ボタンをクリックするかAlt+Xを押下 - 入力されたSQLを実行し結果を表示する。
        Args:
            event: tk.Event - イベントオブジェクト（省略可）
        Returns:
            None - 戻り値なし。
        """
        sql = self._get_sql_query()
        if not sql:
            self._set_status("Error: Query is empty.", is_error=True)
            return
            
        self._last_query_sql = sql
        result_dto = self._fws_sqlite_viewer_logic_obj.run_query(sql)
        self._last_query_result = result_dto
        
        self._update_results(result_dto)
        
        if hasattr(result_dto, 'execution_history') and len(result_dto.execution_history) > 1:
            self._show_execution_history_dialog(result_dto.execution_history)
            
        self._refresh_tables_after_query(result_dto)

    def _refresh_tables_after_query(self, result_dto: fws_sqlite_viewer_model_query_result.FwsSqliteViewerModelQueryResult) -> None:
        """
        Summary:
            クエリ実行後、スキーマ変更の可能性があるためテーブル一覧を再読み込みします。
        Args:
            result_dto: FwsSqliteViewerModelQueryResult - クエリ実行結果
        Returns:
            None - 戻り値なし。
        """
        if result_dto.is_success:
            try:
                tables = self._fws_sqlite_viewer_logic_obj.get_tables()
                self._update_tables_list(tables)
            except Exception as e:
                pass


    def trv_tables_select(self, event: tk.Event) -> None:
        """
        Summary:
            テーブル一覧でアイテムが選択された時の処理。
        UserAction:
            テーブル一覧から任意のテーブルまたはビューをクリックして選択 - そのスキーマ情報が取得され表示される。
        """
        trv = self._fws_sqlite_viewer_view_obj.trv_tables
        selection = trv.selection()
        if not selection:
            return
            
        item_id = selection[0]
        
        # 値がセットされていないノード（DBノードやフォルダノード）の場合はスキーマをクリア
        values = trv.item(item_id, "values")
        if not values:
            self._update_schema_list([])
            self._fws_sqlite_viewer_view_obj.frm_schema.configure(text="Schema Details")
            return
            
        table_name, alias = self._get_table_info(item_id)
        
        # スキーマ表示とタイトル更新
        try:
            schema_list = self._fws_sqlite_viewer_logic_obj.read_table_schema(table_name, alias)
            self._update_schema_list(schema_list)
            self._fws_sqlite_viewer_view_obj.frm_schema.configure(text=f"Schema Details - {alias}.{table_name}")
        except Exception as e:
            self._set_status(f"Error reading table: {e}", is_error=True)
            self._fws_sqlite_viewer_view_obj.frm_schema.configure(text="Schema Details")

    def trv_schema_copy_key_press(self, event: tk.Event) -> None:
        """
        Summary:
            スキーマ詳細の選択行をコピーします。
        UserAction:
            スキーマ詳細リストでCtrl+Cを押下 - 選択行のデータがクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        self._copy_treeview_selection(self._fws_sqlite_viewer_view_obj.trv_schema)

    def trv_results_copy_key_press(self, event: tk.Event) -> None:
        """
        Summary:
            クエリ結果の選択行をコピーします。
        UserAction:
            クエリ結果リストでCtrl+Cを押下 - 選択行のデータがクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        self._copy_treeview_selection(self._fws_sqlite_viewer_view_obj.trv_results)

    def frm_schema_double_click(self, event: tk.Event) -> None:
        """
        Summary:
            スキーマ詳細ペインのタイトルをコピーします。
        UserAction:
            スキーマ詳細ペインの空白部分（タイトル付近）をダブルクリック - タイトルからスキーマ名.テーブル名を抽出してクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        if event.widget != self._fws_sqlite_viewer_view_obj.frm_schema:
            return
            
        title_text = self._fws_sqlite_viewer_view_obj.frm_schema.cget("text")
        if " - " in title_text:
            schema_info = title_text.split(" - ", 1)[1]
            self._copy_text_to_clipboard(schema_info, f"Copied '{schema_info}' to clipboard.")

    def trv_schema_double_click(self, event: tk.Event) -> None:
        """
        Summary:
            スキーマ詳細のセルをコピーします。
        UserAction:
            スキーマ詳細リストのセルをダブルクリック - セルの値がクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        self._copy_cell_value(self._fws_sqlite_viewer_view_obj.trv_schema, event)

    def trv_results_double_click(self, event: tk.Event) -> None:
        """
        Summary:
            クエリ結果のセルを編集モードにします。
        UserAction:
            クエリ結果リストのセルをダブルクリック - 対象のセルを直接編集可能にする。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        trv = self._fws_sqlite_viewer_view_obj.trv_results
        item_id = trv.identify_row(event.y)
        column_id = trv.identify_column(event.x)
        
        if not item_id or not column_id:
            return
            
        # SQLが単純なSELECTかどうかを判定
        last_result = getattr(self, "_last_query_result", None)
        if not last_result or not last_result.is_success:
            return
            
        last_sql = getattr(last_result, "executed_select_sql", "").strip()
        if not last_sql:
            last_sql = getattr(self, "_last_query_sql", "").strip()
            
        match = re.match(r"^\s*SELECT\s+.*?\s+FROM\s+([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)?)(?:\s+WHERE|\s+ORDER|\s+LIMIT|\s*$)?", last_sql, re.IGNORECASE | re.DOTALL)
        if not match:
            self._set_status("テーブル名が特定できないため直接編集できません", is_error=True, timeout_ms=3000)
            return
            
        table_name = match.group(1)
        
        try:
            row_index = trv.index(item_id)
            original_tuple = last_result.rows[row_index]
        except (ValueError, IndexError):
            return
            
        col_index = int(column_id.replace('#', '')) - 1
        if col_index < 0 or col_index >= len(last_result.columns):
            return
            
        target_col_name = last_result.columns[col_index]
        
        self._start_inline_editing(trv, item_id, column_id, table_name, original_tuple, last_result.columns, target_col_name)

    def _start_inline_editing(self, trv: tk.ttk.Treeview, item_id: str, column_id: str, table_name: str, original_tuple: tuple, columns: list, target_col_name: str) -> None:
        """
        Summary:
            クエリ結果グリッド上でインライン編集（Entry配置）を開始します。
        Args:
            trv: tk.ttk.Treeview - 結果表示用Treeview
            item_id: str - 対象の行ID
            column_id: str - 対象の列ID
            table_name: str - 対象のテーブル名
            original_tuple: tuple - 編集前の行データ
            columns: list - カラム名のリスト
            target_col_name: str - 編集対象のカラム名
        Returns:
            None - 戻り値なし。
        """
        # entryウィジェットの配置
        x, y, w, h = trv.bbox(item_id, column_id)
        
        entry = tk.Entry(trv)
        entry.place(x=x, y=y, width=w, height=h)
        
        # 初期値をセット
        current_val = trv.set(item_id, column_id)
        entry.insert(0, current_val)
        entry.select_range(0, tk.END)
        entry.focus()
        
        def commit_edit(e: tk.Event) -> None:
            new_val = entry.get()
            entry.destroy()
            if new_val == current_val:
                return
                
            old_row_dict = {col: val for col, val in zip(columns, original_tuple)}
            try:
                updated_count = self._fws_sqlite_viewer_logic_obj.update_record(table_name, target_col_name, new_val, old_row_dict)
                if updated_count > 0:
                    self._set_status(f"Updated {updated_count} row(s) successfully.", is_error=False, timeout_ms=3000)
                    # 再読み込み
                    self.btn_run_query_click()
                else:
                    self._set_status("No rows updated.", is_error=True, timeout_ms=3000)
            except Exception as ex:
                self._set_status(f"Error updating record: {ex}", is_error=True, timeout_ms=5000)
                
        def cancel_edit(e: tk.Event) -> None:
            entry.destroy()
            
        entry.bind("<Return>", commit_edit)
        entry.bind("<Escape>", cancel_edit)
        entry.bind("<FocusOut>", cancel_edit)

    def trv_tables_double_click(self, event: tk.Event) -> None:
        """
        Summary:
            ダブルクリックされたテーブル名をクリップボードにコピーします。
        UserAction:
            テーブル一覧のテーブル名をダブルクリック - テーブル名がクリップボードにコピーされる。
        Args:
            event: tk.Event - イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        trv = self._fws_sqlite_viewer_view_obj.trv_tables
        item = trv.identify_row(event.y)
        if item:
            values = trv.item(item, "values")
            if values:
                table_name, alias = self._get_table_info(item)
                copy_text = f"{alias}.{table_name}"
            else:
                copy_text = trv.item(item, "text")
            
            self._copy_text_to_clipboard(copy_text, f"Copied: '{copy_text}'")

    def trv_schema_copy_header_key_press(self, event: tk.Event) -> None:
        """
        Summary:
            スキーマ詳細の選択行をヘッダー付きでコピーします。
        Description:
            選択されたスキーマ行をヘッダー名とともにクリップボードへコピーします。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        UserAction:
            スキーマ詳細リストでCtrl+Shift+Cを押下 - ヘッダー行を含む選択行のデータがクリップボードにコピーされる。
        """
        self._copy_treeview_selection_with_header(self._fws_sqlite_viewer_view_obj.trv_schema)

    def trv_results_copy_header_key_press(self, event: tk.Event) -> None:
        """
        Summary:
            クエリ結果の選択行をヘッダー付きでコピーします。
        Description:
            選択されたクエリ結果のデータ行をヘッダー名とともにクリップボードへコピーします。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        UserAction:
            クエリ結果リストでCtrl+Shift+Cを押下 - ヘッダー行を含む選択行のデータがクリップボードにコピーされる。
        """
        self._copy_treeview_selection_with_header(self._fws_sqlite_viewer_view_obj.trv_results)

    def win_main_close(self) -> None:
        """
        Summary:
            ウィンドウ終了時の処理。
        Description:
            セッションを保存し、データベース接続を閉じた上でアプリケーションを終了します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        UserAction:
            ウィンドウの「×」ボタンをクリック - アプリケーションが終了し、DB接続が閉じられる。
        """
        try:
            self._save_session()
            self._fws_sqlite_viewer_logic_obj.close_db()
        except Exception as e:
            print(f"Error in win_main_close: {e}")
        finally:
            self._fws_sqlite_viewer_view_obj.destroy()
    #endregion

    #region Private Methods
    def _set_db_path(self, db_path: str) -> None:
        """
        Summary:
            テキスト入力欄にDBパスをセットします。
        Description:
            エントリの内容を上書きします。
        Args:
            db_path: str - DBパス
        Returns:
            None - 戻り値なし。
        """
        self._fws_sqlite_viewer_view_obj.ent_db_path.delete(0, tk.END)
        self._fws_sqlite_viewer_view_obj.ent_db_path.insert(0, db_path)

    def _get_db_path(self) -> str:
        """
        Summary:
            テキスト入力欄からDBパスを取得します。
        Returns:
            str - 入力されたDBパス。
        """
        return self._fws_sqlite_viewer_view_obj.ent_db_path.get().strip()

    def _get_sql_query(self) -> str:
        """
        Summary:
            テキストエリアからSQLクエリを取得します。
            テキストが選択（ハイライト）されている場合は、その選択範囲のテキストを返します。
            選択されていない場合は、エディタ全体のテキストを返します。
        Returns:
            str - 入力（または選択）されたSQL。
        """
        sel_ranges = self._fws_sqlite_viewer_view_obj.txt_sql.tag_ranges(tk.SEL)
        if sel_ranges:
            return self._fws_sqlite_viewer_view_obj.txt_sql.get(sel_ranges[0], sel_ranges[1]).strip()
        else:
            return self._fws_sqlite_viewer_view_obj.txt_sql.get("1.0", tk.END).strip()

    def _set_sql_query(self, sql: str) -> None:
        """
        Summary:
            テキストエリアにSQLをセットします。
        Args:
            sql: str - セットするSQL。
        Returns:
            None - 戻り値なし。
        """
        self._fws_sqlite_viewer_view_obj.txt_sql.delete("1.0", tk.END)
        self._fws_sqlite_viewer_view_obj.txt_sql.insert("1.0", sql)

    def _update_tables_list(self, tables_dict: Dict[str, Dict[str, List[str]]]) -> None:
        """
        Summary:
            テーブル一覧ツリーを階層化して更新します。
        Args:
            tables_dict: dict - DB名をキー、テーブル・ビューリストを値とする辞書。
        """
        trv: tk.ttk.Treeview = self._fws_sqlite_viewer_view_obj.trv_tables
        
        # 既存ノードの開閉状態を記憶
        open_states = {}
        nodes_to_process = list(trv.get_children())
        while nodes_to_process:
            node = nodes_to_process.pop()
            open_states[node] = trv.item(node, "open")
            nodes_to_process.extend(trv.get_children(node))
                
        for item in trv.get_children():
            trv.delete(item)
            
        for db_alias, obj_dict in tables_dict.items():
            db_id = f"db_{db_alias}"
            is_open = open_states.get(db_id, True)
            parent_id = trv.insert("", tk.END, iid=db_id, text=db_alias, open=is_open)
            
            # Tables フォルダノード
            tables = obj_dict.get('Tables', [])
            if tables:
                tbl_folder_id = f"folder_tables_{db_alias}"
                is_open = open_states.get(tbl_folder_id, False)
                trv.insert(parent_id, tk.END, iid=tbl_folder_id, text="Tables", open=is_open)
                for table in tables:
                    trv.insert(tbl_folder_id, tk.END, iid=f"tbl_{db_alias}_{table}", text=table, values=(db_alias, table))
                    
            # Views フォルダノード
            views = obj_dict.get('Views', [])
            if views:
                vw_folder_id = f"folder_views_{db_alias}"
                is_open = open_states.get(vw_folder_id, False)
                trv.insert(parent_id, tk.END, iid=vw_folder_id, text="Views", open=is_open)
                for view in views:
                    trv.insert(vw_folder_id, tk.END, iid=f"vw_{db_alias}_{view}", text=view, values=(db_alias, view))

    def _get_table_info(self, item_id: str) -> tuple[str, str]:
        """
        Summary:
            ツリーのアイテムIDからテーブル名とエイリアスを取得します。
        Args:
            item_id: str - TreeviewのアイテムID。
        Returns:
            tuple[str, str] - (テーブル名, エイリアス名)のタプル。
        """
        trv: tk.ttk.Treeview = self._fws_sqlite_viewer_view_obj.trv_tables
        table_name = trv.item(item_id, "text")
        values = trv.item(item_id, "values")
        alias = values[0] if values else "main"
        return table_name, alias

    def _copy_text_to_clipboard(self, text: str, status_msg: str) -> None:
        """
        Summary:
            テキストをクリップボードにコピーし、ステータスを更新します。
        Args:
            text: str - コピーするテキスト。
            status_msg: str - ステータスバーに表示するメッセージ。
        Returns:
            None - 戻り値なし。
        """
        self._fws_sqlite_viewer_view_obj.clipboard_clear()
        self._fws_sqlite_viewer_view_obj.clipboard_append(text)
        self._set_status(status_msg, timeout_ms=fws_sqlite_viewer_const.STATUS_MESSAGE_TIMEOUT_MS)

    def _update_schema_list(self, schema_list: List[fws_sqlite_viewer_model_table_schema.FwsSqliteViewerModelTableSchema]) -> None:
        """
        Summary:
            スキーマリスト表示を更新します。
        Args:
            schema_list: List[fws_sqlite_viewer_model_table_schema.FwsSqliteViewerModelTableSchema] - スキーマModelのリスト。
        Returns:
            None - 戻り値なし。
        """
        trv: tk.ttk.Treeview = self._fws_sqlite_viewer_view_obj.trv_schema
        for item in trv.get_children():
            trv.delete(item)
            
        for index, schema in enumerate(schema_list):
            tag = "even" if index % 2 == 0 else "odd"
            trv.insert("", tk.END, values=(
                schema.name,
                schema.type_name,
                "YES" if schema.pk > 0 else "",
                "YES" if schema.notnull == 1 else ""
            ), tags=(tag,))

    def _clear_results(self) -> None:
        """
        Summary:
            結果データグリッドをクリアします。
        Returns:
            None - 戻り値なし。
        """
        trv: tk.ttk.Treeview = self._fws_sqlite_viewer_view_obj.trv_results
        trv.delete(*trv.get_children())
        trv["columns"] = ()

    def _update_results(self, result_dto: fws_sqlite_viewer_model_query_result.FwsSqliteViewerModelQueryResult) -> None:
        """
        Summary:
            クエリ実行結果を画面に反映します。
        Args:
            result_dto: fws_sqlite_viewer_model_query_result.FwsSqliteViewerModelQueryResult - 実行結果Model。
        Returns:
            None - 戻り値なし。
        """
        self._clear_results()
        
        if not result_dto.is_success:
            self._set_status(f"Error: {result_dto.error_message}", is_error=True)
            return

        trv: tk.ttk.Treeview = self._fws_sqlite_viewer_view_obj.trv_results
        
        # カラム設定
        if result_dto.columns:
            trv["columns"] = result_dto.columns
            for col in result_dto.columns:
                trv.heading(col, text=col)
                trv.column(col, width=100, anchor=tk.W)
                
            # データ行挿入
            for index, row in enumerate(result_dto.rows):
                tag = "even" if index % 2 == 0 else "odd"
                trv.insert("", tk.END, values=row, tags=(tag,))
                
            status_msg = f"Status: {result_dto.rowcount} rows returned in {result_dto.execution_time_ms:.2f} ms"
        else:
            # 更新系クエリの場合
            status_msg = f"Status: Query successful ({result_dto.rowcount} rows affected) in {result_dto.execution_time_ms:.2f} ms"
            
        self._set_status(status_msg, is_error=False)
    def _set_status(self, msg: str, is_error: bool = False, timeout_ms: int = 0) -> None:
        """
        Summary:
            ステータスラベルのメッセージを更新します。
        Args:
            msg: str - メッセージ文字列。
            is_error: bool - エラーの場合はTrue。
            timeout_ms: int - 0より大きい場合、指定ミリ秒後に元の状態（Status: Ready）に戻します。
        Returns:
            None - 戻り値なし。
        """
        if getattr(self, '_status_timer_id', None) is not None:
            self._fws_sqlite_viewer_view_obj.after_cancel(self._status_timer_id)
            self._status_timer_id = None

        self._fws_sqlite_viewer_view_obj.lbl_status.config(text=msg)
        if is_error:
            self._fws_sqlite_viewer_view_obj.lbl_status.config(foreground="red")
        else:
            self._fws_sqlite_viewer_view_obj.lbl_status.config(foreground="black")

        if timeout_ms > 0:
            self._status_timer_id = self._fws_sqlite_viewer_view_obj.after(timeout_ms, self._reset_status)

    def _reset_status(self) -> None:
        """
        Summary:
            ステータスバーをデフォルト状態に戻します。
        Returns:
            None - 戻り値なし。
        """
        self._set_status(fws_sqlite_viewer_const.STATUS_MSG_READY)

    def _load_db(self, db_path: str, is_main: bool = False) -> None:
        """
        Summary:
            DBに接続またはアタッチし、テーブル一覧を更新します。
        Args:
            db_path: str - DBファイルパス。
            is_main: bool - メインDBとして読み込むかどうか。
        """
        if not is_main and self._fws_sqlite_viewer_logic_obj.is_connected():
            self._attach_db(db_path)
            return

        try:
            tables = self._fws_sqlite_viewer_logic_obj.load_db(db_path)
            self._set_db_path(db_path)
            self._set_status("Connected to DB.")
            
            self._update_tables_list(tables)
            self._clear_results()
            self._update_schema_list([])
            
        except Exception as e:
            self._set_status(f"Error connecting to DB: {e}", is_error=True)
            self._update_tables_list({})
            self._clear_results()
            self._fws_sqlite_viewer_logic_obj.close_db()

    def _attach_db(self, db_path: str) -> None:
        """
        Summary:
            追加のDBをアタッチします。
        Description:
            Logic層を呼び出してDBをアタッチし、UIに反映します。
        Args:
            db_path: str - DBファイルパス。
        Returns:
            None - 戻り値なし。
        """
        try:
            alias = self._fws_sqlite_viewer_logic_obj.attach_db(db_path)
            self._set_status(f"Attached DB as {alias}")
            
            tables = self._fws_sqlite_viewer_logic_obj.get_tables()
            self._update_tables_list(tables)
        except Exception as e:
            self._set_status(f"Error attaching DB: {e}", is_error=True)

    def _copy_treeview_selection(self, trv: tk.ttk.Treeview) -> None:
        """
        Summary:
            Treeviewの選択行をクリップボードにコピーします。
        Args:
            trv: tk.ttk.Treeview - 対象のTreeview。
        Returns:
            None - 戻り値なし。
        """
        selected_items = trv.selection()
        if not selected_items:
            return
            
        copied_data = []
        for item in selected_items:
            values = trv.item(item, 'values')
            copied_data.append("\t".join(str(v) for v in values))
            
        clipboard_text = "\n".join(copied_data)
        self._fws_sqlite_viewer_view_obj.clipboard_clear()
        self._fws_sqlite_viewer_view_obj.clipboard_append(clipboard_text)
        self._set_status(f"Copied {len(selected_items)} rows to clipboard.", timeout_ms=fws_sqlite_viewer_const.STATUS_MESSAGE_TIMEOUT_MS)

    def _copy_cell_value(self, trv: tk.ttk.Treeview, event: tk.Event) -> None:
        """
        Summary:
            ダブルクリックされたセルの値をクリップボードにコピーします。
        Args:
            trv: tk.ttk.Treeview - 対象のTreeview。
            event: tk.Event - イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        region = trv.identify("region", event.x, event.y)
        if region != "cell":
            return
            
        col = trv.identify_column(event.x)
        item = trv.identify_row(event.y)
        
        if col and item:
            col_index = int(col.replace('#', '')) - 1
            values = trv.item(item, 'values')
            if col_index < len(values):
                cell_value = values[col_index]
                self._fws_sqlite_viewer_view_obj.clipboard_clear()
                self._fws_sqlite_viewer_view_obj.clipboard_append(str(cell_value))
                
                # 文字列が長い場合は省略してStatusに表示
                display_val = str(cell_value)
                if len(display_val) > 30:
                    display_val = display_val[:27] + "..."
                self._set_status(f"Copied cell value: '{display_val}'", timeout_ms=fws_sqlite_viewer_const.STATUS_MESSAGE_TIMEOUT_MS)

    def _copy_treeview_selection_with_header(self, trv: tk.ttk.Treeview) -> None:
        """
        Summary:
            Treeviewの選択行をヘッダー（列名）付きでクリップボードにコピーします。
        Description:
            先頭行にTreeviewのカラム見出しをタブ区切りで付与し、
            続けて選択されたデータ行をタブ区切り（TSV）で連結してクリップボードに格納します。
        Args:
            trv: tk.ttk.Treeview - 対象のTreeview。
        Returns:
            None - 戻り値なし。
        """
        selected_items = trv.selection()
        if not selected_items:
            return

        # ヘッダー行の構築（heading の表示テキストを使用）
        columns = trv["columns"]
        header_texts = []
        for col in columns:
            header_texts.append(trv.heading(col, "text"))
        header_line = "\t".join(header_texts)

        # データ行の構築
        copied_data = []
        for item in selected_items:
            values = trv.item(item, 'values')
            copied_data.append("\t".join(str(v) for v in values))

        clipboard_text = header_line + "\n" + "\n".join(copied_data)
        self._fws_sqlite_viewer_view_obj.clipboard_clear()
        self._fws_sqlite_viewer_view_obj.clipboard_append(clipboard_text)
        self._set_status(f"Copied {len(selected_items)} rows with header to clipboard.", timeout_ms=fws_sqlite_viewer_const.STATUS_MESSAGE_TIMEOUT_MS)

    def _show_execution_history_dialog(self, history: List[tuple]) -> None:
        """
        Summary:
            複数クエリの実行履歴をポップアップで表示します。
        Args:
            history: List[tuple] - クエリ文字列と処理件数のタプルリスト。
        """
        # 既存のウィンドウがあれば破棄して再表示する
        if self._fws_sqlite_viewer_history_event_obj is not None and self._fws_sqlite_viewer_history_event_obj.winfo_exists():
            self._fws_sqlite_viewer_history_event_obj.destroy()

        # 新規Eventクラスのインスタンス化
        self._fws_sqlite_viewer_history_event_obj = fws_sqlite_viewer_history_event.FwsSqliteViewerHistoryEvent(self._fws_sqlite_viewer_view_obj)
        
        # ダイアログの表示
        self._fws_sqlite_viewer_history_event_obj.show_dialog(history)

    def trv_tables_right_click(self, event: tk.Event) -> None:
        """
        Summary:
            テーブル一覧の右クリック時にコンテキストメニューを表示します。
        Description:
            クリックされたノードがDBエイリアス（ルートノード）である場合のみ、
            Refresh や Detach メニューを表示します。
        UserAction:
            テーブル一覧のDBノード上で右クリック - RefreshおよびDetachメニューが表示される。
        Args:
            event: tk.Event - イベントオブジェクト
        Returns:
            None - 戻り値なし。
        """
        trv = self._fws_sqlite_viewer_view_obj.trv_tables
        item = trv.identify_row(event.y)
        if not item:
            return
            
        trv.selection_set(item)
        parent_id = trv.parent(item)
        menu = self._fws_sqlite_viewer_view_obj.menu_tables
        
        if not parent_id:
            alias = trv.item(item, "text")
            menu.entryconfigure("Refresh", state="normal", command=self._refresh_db_tables)
            if alias != "main":
                menu.entryconfigure("Detach Database", state="normal", command=lambda a=alias: self._detach_db(a))
            else:
                menu.entryconfigure("Detach Database", state="disabled")
            
            # DBノードではテーブル用メニューを無効化
            try:
                menu.entryconfigure("Generate Recreate Script", state="disabled")
            except tk.TclError:
                pass # メニューが存在しない場合は無視
                
            menu.post(event.x_root, event.y_root)
            
        elif str(item).startswith("tbl_"):
            table_name, alias = self._get_table_info(item)
            menu.entryconfigure("Refresh", state="disabled")
            menu.entryconfigure("Detach Database", state="disabled")
            
            try:
                menu.entryconfigure("Generate Recreate Script", state="normal", command=lambda t=table_name, a=alias: self._generate_recreate_script(t, a))
            except tk.TclError:
                pass
                
            menu.post(event.x_root, event.y_root)

    def _refresh_db_tables(self) -> None:
        """
        Summary:
            データベース一覧とテーブル一覧を再読み込みします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        tables = self._fws_sqlite_viewer_logic_obj.get_tables()
        self._update_tables_list(tables)

    def _detach_db(self, alias: str) -> None:
        """
        Summary:
            指定されたエイリアスのデータベースをデタッチします。
        Args:
            alias: str - デタッチするDBのエイリアス名
        Returns:
            None - 戻り値なし。
        """
        try:
            self._fws_sqlite_viewer_logic_obj.detach_db(alias)
            self._set_status(f"Detached DB: {alias}")
            self._refresh_db_tables()
        except Exception as e:
            self._set_status(f"Error detaching DB: {e}", is_error=True)

    def _generate_recreate_script(self, table_name: str, alias: str) -> None:
        """
        Summary:
            テーブル再作成スクリプトを生成し、エディタに挿入します。
        Args:
            table_name: str - 対象テーブル名
            alias: str - 対象データベースのエイリアス
        Returns:
            None - 戻り値なし。
        """
        try:
            script = self._fws_sqlite_viewer_logic_obj.generate_recreate_script(table_name, alias)
            if not script:
                self._set_status(f"Failed to generate script for {table_name}", is_error=True)
                return
                
            txt = self._fws_sqlite_viewer_view_obj.txt_sql
            current_text = txt.get("1.0", tk.END).strip()
            
            if current_text:
                txt.insert(tk.END, "\n\n" + script)
            else:
                txt.insert(tk.END, script)
                
            self._set_status(f"Generated recreate script for {table_name}")
        except Exception as e:
            self._set_status(f"Error generating script: {e}", is_error=True)

    def _save_session(self) -> None:
        """
        Summary:
            現在の接続状態を session.json に保存します。
        Description:
            メインDBおよびアタッチされているDBのパスとエイリアスを保存します。
            未接続の場合はファイルを削除します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        try:
            if not self._fws_sqlite_viewer_logic_obj.is_connected():
                if self._session_file.exists():
                    self._session_file.unlink()
                return

            db_list = self._fws_sqlite_viewer_logic_obj.get_database_list()
            
            main_db = None
            attached_dbs = []
            
            for seq, name, file in db_list:
                if name == "main":
                    main_db = file
                elif name != "temp" and file:
                    attached_dbs.append({"alias": name, "path": file})
                    
            with open(self._session_file, "w", encoding="utf-8") as f:
                json.dump({"main_db": main_db, "attached_dbs": attached_dbs}, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")
    #endregion
