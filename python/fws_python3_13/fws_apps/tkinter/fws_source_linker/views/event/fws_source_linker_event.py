"""
Summary:
    fws_source_linkerのイベントハンドラモジュールです。
Description:
    UIイベントの受付とLogicへの委譲、画面更新を行います。
ScreenName:
    メイン画面
Attachment:
    なし
"""
import os
from pathlib import Path
import tkinter as tk

# fws_lib
from fws_lib.tkinter import fws_dialog_utils, fws_window_utils
from fws_lib.common import fws_error_handler

# app
from fws_apps.tkinter.fws_source_linker.views.view import fws_source_linker_view
from fws_apps.tkinter.fws_source_linker.views.logic import fws_source_linker_logic


class FwsSourceLinkerEvent:
    """
    Summary:
        イベントハンドラクラス。
    Description:
        ユーザーアクションを受け付け、モデル更新とビューへの反映を行います。
    """

    # region Constructor
    def __init__(self) -> None:
        """
        Summary:
            FwsSourceLinkerEventを初期化し、イベントをバインドします。
        """
        self._fws_source_linker_view_obj: fws_source_linker_view.FwsSourceLinkerView = fws_source_linker_view.FwsSourceLinkerView()
        self._fws_source_linker_logic_obj: fws_source_linker_logic.FwsSourceLinkerLogic = fws_source_linker_logic.FwsSourceLinkerLogic()
        
        self._bind_events()
        self._initialize_view()
        
    def _bind_events(self) -> None:
        """
        Summary:
            UIイベントをバインドします。
        """
        self._fws_source_linker_view_obj.chk_topmost.config(command=self.chk_topmost_click)
        self._fws_source_linker_view_obj.scl_alpha.config(command=self.scl_alpha_change)
        
        self._fws_source_linker_view_obj.btn_select_root.config(command=self.btn_select_root_click)
        self._fws_source_linker_view_obj.btn_select_dest.config(command=self.btn_select_dest_click)
        self._fws_source_linker_view_obj.btn_open_dest.config(command=self.btn_open_dest_click)
        self._fws_source_linker_view_obj.btn_copy.config(command=self.btn_copy_click)
        
        # ツリービューの展開時(ダミーノードを開いた時)のイベント
        self._fws_source_linker_view_obj.trv_files.bind("<<TreeviewOpen>>", self.trv_files_open)
        
        # エンターキーや選択でパス手入力反映
        self._fws_source_linker_view_obj.cbo_root_dir.bind("<Return>", self.cbo_root_dir_key_press)
        self._fws_source_linker_view_obj.cbo_root_dir.bind("<<ComboboxSelected>>", self.cbo_root_dir_key_press)
        
        # 更新ボタン
        self._fws_source_linker_view_obj.btn_reload_root.config(command=self.btn_reload_root_click)
        
        # ウィンドウクローズ
        self._fws_source_linker_view_obj.protocol("WM_DELETE_WINDOW", self.win_main_close)

    def _initialize_view(self) -> None:
        """
        Summary:
            画面の初期表示設定を行います。
        """
        config: dict = self._fws_source_linker_logic_obj.get_config()
        root_dir: str = config.get("root_dir", "")
        root_dir_history: list[str] = config.get("root_dir_history", [])
        dest_dir: str = config.get("dest_dir", "")
        dest_dir_history: list[str] = config.get("dest_dir_history", [])
        dest_sub_dir: str = config.get("dest_sub_dir", "")
        
        self._fws_source_linker_view_obj.cbo_root_dir["values"] = root_dir_history
        self._fws_source_linker_view_obj.cbo_root_dir.set(root_dir)
        
        self._fws_source_linker_view_obj.cbo_dest_dir["values"] = dest_dir_history
        self._fws_source_linker_view_obj.cbo_dest_dir.set(dest_dir)
        self._fws_source_linker_view_obj.ent_dest_sub_dir.insert(0, dest_sub_dir)
        
        if root_dir:
            self._update_tree(root_dir)
    # endregion
    
    # region Public Methods
    def start(self) -> None:
        """
        Summary:
            メインループを開始します。
        Args:
            なし
        Returns:
            None
        """
        self._fws_source_linker_view_obj.mainloop()

    def btn_select_root_click(self) -> None:
        """
        Summary:
            起点フォルダ選択ボタンクリックイベント。
        Description:
            フォルダ選択ダイアログを表示し、選択結果を入力欄に反映します。
        Args:
            なし
        Returns:
            None
        UserAction:
            起点フォルダ「参照...」ボタンクリック - フォルダ選択ダイアログが開き、選択後ツリーが更新される。
        """
        selected_dir: str = fws_dialog_utils.ask_open_dir(title="起点フォルダを選択", parent=self._fws_source_linker_view_obj)
        if selected_dir:
            self._fws_source_linker_view_obj.cbo_root_dir.set(selected_dir)
            self._update_tree(selected_dir)

    def btn_select_dest_click(self) -> None:
        """
        Summary:
            コピー先フォルダ選択ボタンクリックイベント。
        Description:
            フォルダ選択ダイアログを表示し、選択結果を入力欄に反映します。
        Args:
            なし
        Returns:
            None
        UserAction:
            コピー先「参照...」ボタンクリック - フォルダ選択ダイアログが開き、入力欄に反映される。
        """
        selected_dir: str = fws_dialog_utils.ask_open_dir(title="コピー先フォルダを選択", parent=self._fws_source_linker_view_obj)
        if selected_dir:
            self._fws_source_linker_view_obj.cbo_dest_dir.set(selected_dir)
            
            # 履歴の更新
            current_history = list(self._fws_source_linker_view_obj.cbo_dest_dir["values"])
            new_history = self._fws_source_linker_logic_obj.add_to_history(selected_dir, current_history)
            self._fws_source_linker_view_obj.cbo_dest_dir["values"] = new_history

    def btn_open_dest_click(self) -> None:
        """
        Summary:
            開くボタンクリックイベント。
        Description:
            コピー先ディレクトリをエクスプローラで開きます。
        Args:
            なし
        Returns:
            None
        UserAction:
            開くボタンクリック - フォルダが存在すればエクスプローラが起動する。
        """
        dest_base: str = self._fws_source_linker_view_obj.cbo_dest_dir.get()
        dest_sub: str = self._fws_source_linker_view_obj.ent_dest_sub_dir.get()
        
        if not dest_base:
            fws_dialog_utils.show_warning("警告", "コピー先のベースフォルダが指定されていません。", parent=self._fws_source_linker_view_obj)
            return
            
        dest_path: Path = Path(dest_base) / dest_sub if dest_sub else Path(dest_base)
        
        if not dest_path.exists() or not dest_path.is_dir():
            fws_dialog_utils.show_warning("警告", f"フォルダが存在しません。\n{dest_path}", parent=self._fws_source_linker_view_obj)
            return
            
        os.startfile(str(dest_path.resolve()))

    def cbo_root_dir_key_press(self, event: tk.Event = None) -> None:
        """
        Summary:
            起点フォルダ入力欄キー/選択イベント。
        Description:
            Enterキー押下や履歴選択でツリーを更新します。
        Args:
            event: tk.Event - キーイベント/選択イベント。
        Returns:
            None
        UserAction:
            Enterキー押下 - 入力されたパスの階層がツリーに表示される。
        """
        root_dir: str = self._fws_source_linker_view_obj.cbo_root_dir.get()
        if root_dir:
            self._update_tree(root_dir)

    def btn_reload_root_click(self) -> None:
        """
        Summary:
            更新ボタンクリックイベント。
        Description:
            入力されているパスでツリーを再読み込みします。
        Args:
            なし
        Returns:
            None
        UserAction:
            更新ボタンクリック - 入力パスの内容が再読み込みされる。
        """
        self.cbo_root_dir_key_press()

    def trv_files_open(self, event: tk.Event) -> None:
        """
        Summary:
            ツリービューノード展開イベント。
        Description:
            ダミーノードを削除し、子階層のアイテムを取得して追加します。
        Args:
            event: tk.Event - イベントオブジェクト。
        Returns:
            None
        UserAction:
            ツリーの「+」アイコンクリック - 子階層がロードされ展開される。
        """
        node_id: str = self._fws_source_linker_view_obj.trv_files.focus()
        children = self._fws_source_linker_view_obj.trv_files.get_children(node_id)
        if len(children) == 1 and self._fws_source_linker_view_obj.trv_files.item(children[0], "text") == "dummy":
            self._fws_source_linker_view_obj.trv_files.delete(children[0])
            path: str = self._fws_source_linker_view_obj.trv_files.item(node_id, "values")[0]
            self._insert_children(node_id, path)

    @fws_error_handler.with_error_handling(title="コピーエラー", ui_mode="tkinter")
    def btn_copy_click(self) -> None:
        """
        Summary:
            コピー実行ボタンクリックイベント。
        Description:
            選択されたアイテムをコピー先に複製・ショートカット生成します。
        Args:
            なし
        Returns:
            None
        UserAction:
            コピー実行ボタンクリック - コピーとショートカット生成が行われ、完了メッセージが表示される。
        """
        dest_base: str = self._fws_source_linker_view_obj.cbo_dest_dir.get()
        dest_sub: str = self._fws_source_linker_view_obj.ent_dest_sub_dir.get()
        
        if not dest_base:
            fws_dialog_utils.show_warning("警告", "コピー先のベースフォルダを指定してください。", parent=self._fws_source_linker_view_obj)
            return
            
        dest_path: Path = Path(dest_base) / dest_sub if dest_sub else Path(dest_base)
        dest_dir: str = str(dest_path.resolve())
            
        selected_ids = self._fws_source_linker_view_obj.trv_files.selection()
        if not selected_ids:
            fws_dialog_utils.show_warning("警告", "コピー対象を選択してください。", parent=self._fws_source_linker_view_obj)
            return
            
        items: list[str] = []
        for item_id in selected_ids:
            path: str = self._fws_source_linker_view_obj.trv_files.item(item_id, "values")[0]
            items.append(path)
            
        existing: list[str] = self._fws_source_linker_logic_obj.execute_copy(items, dest_dir)
        if existing:
            msg: str = f"以下のアイテムは既に存在します。上書きしますか？\n" + "\n".join(existing)
            if fws_dialog_utils.ask_yes_no("上書き確認", msg, parent=self._fws_source_linker_view_obj):
                self._fws_source_linker_logic_obj.execute_force_copy(existing, dest_dir)
        
        fws_dialog_utils.show_info("完了", "コピーおよびショートカットの作成が完了しました。", parent=self._fws_source_linker_view_obj)
        
        # 履歴追加
        current_history = list(self._fws_source_linker_view_obj.cbo_dest_dir["values"])
        new_history = self._fws_source_linker_logic_obj.add_to_history(dest_base, current_history)
        self._fws_source_linker_view_obj.cbo_dest_dir["values"] = new_history

    def chk_topmost_click(self) -> None:
        """
        Summary:
            最前面表示切り替えイベント。
        Description:
            チェックボックスの状態に応じて最前面表示を切り替えます。
        Args:
            なし
        Returns:
            None
        UserAction:
            「最前面に表示」チェックボックスクリック - 画面の最前面設定が切り替わる。
        """
        is_top = self._fws_source_linker_view_obj.var_topmost.get()
        fws_window_utils.set_window_topmost(self._fws_source_linker_view_obj, is_top)

    def scl_alpha_change(self, val: str = None) -> None:
        """
        Summary:
            透過度変更イベント。
        Description:
            スライダーの値に応じてウィンドウの透過度を変更します。
        Args:
            val: str - スライダーから渡される現在値（デフォルト None）。
        Returns:
            None
        UserAction:
            透過度スライダー操作 - 画面の透過度が変わる。
        """
        alpha = self._fws_source_linker_view_obj.var_alpha.get()
        fws_window_utils.set_window_alpha(self._fws_source_linker_view_obj, alpha)

    def win_main_close(self) -> None:
        """
        Summary:
            画面クローズイベント。
        Description:
            設定を保存してアプリケーションを終了します。
        Args:
            なし
        Returns:
            None
        UserAction:
            ウィンドウの「×」ボタンクリック - 設定が保存されアプリが終了する。
        """
        root_dir: str = self._fws_source_linker_view_obj.cbo_root_dir.get()
        root_dir_history: list[str] = list(self._fws_source_linker_view_obj.cbo_root_dir["values"])
        dest_dir: str = self._fws_source_linker_view_obj.cbo_dest_dir.get()
        dest_dir_history: list[str] = list(self._fws_source_linker_view_obj.cbo_dest_dir["values"])
        dest_sub_dir: str = self._fws_source_linker_view_obj.ent_dest_sub_dir.get()
        
        self._fws_source_linker_logic_obj.save_config(
            root_dir, root_dir_history, dest_dir, dest_dir_history, dest_sub_dir
        )
        self._fws_source_linker_view_obj.destroy()
    # endregion

    # region Private Methods
    def _update_tree(self, root_dir: str) -> None:
        """
        Summary:
            ツリービューの内容を更新します。
        Args:
            root_dir: str - 起点ディレクトリ。
        Returns:
            None
        """
        # 既存アイテムクリア
        for item in self._fws_source_linker_view_obj.trv_files.get_children():
            self._fws_source_linker_view_obj.trv_files.delete(item)
            
        self._insert_children("", root_dir)
        
        # 履歴更新
        current_history = list(self._fws_source_linker_view_obj.cbo_root_dir["values"])
        new_history = self._fws_source_linker_logic_obj.add_to_history(root_dir, current_history)
        self._fws_source_linker_view_obj.cbo_root_dir["values"] = new_history

    def _insert_children(self, parent_id: str, path: str) -> None:
        """
        Summary:
            ツリービューに子階層を追加します。
        Args:
            parent_id: str - 親ノードID。
            path: str - 対象ディレクトリパス。
        Returns:
            None
        """
        contents: list[tuple[str, str, str]] = self._fws_source_linker_logic_obj.get_directory_contents(path)
        for full_path, name, type_str in contents:
            node_id: str = self._fws_source_linker_view_obj.trv_files.insert(
                parent_id, "end", text=name, values=(full_path,)
            )
            if type_str == "dir":
                # 展開用にダミーノードを入れる
                self._fws_source_linker_view_obj.trv_files.insert(node_id, "end", text="dummy")
    # endregion
