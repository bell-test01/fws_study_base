"""
Summary:
    fws_case_recorder アプリのメイン画面ビューモジュール。
Description:
    左右ペイン構成のUIレイアウトを構築します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk
from fws_apps.tkinter.fws_case_recorder.constant import fws_case_recorder_const

class FwsCaseRecorderView(tk.Tk):
    """
    Summary:
        メイン画面のビュークラス。
    Description:
        左ペイン（アクティブ記録）と右ペイン（履歴検索）を持つ2ペイン構成のUIを構築します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            UI部品を初期化し配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        super().__init__()

        self.title(f"{fws_case_recorder_const.WINDOW_TITLE} v{fws_case_recorder_const.APP_VERSION}")
        self.geometry(f"{fws_case_recorder_const.WINDOW_DEFAULT_WIDTH}x{fws_case_recorder_const.WINDOW_DEFAULT_HEIGHT}+0+0")
        self.minsize(fws_case_recorder_const.WINDOW_MIN_WIDTH, fws_case_recorder_const.WINDOW_MIN_HEIGHT)

        # フォント設定
        default_font = ("Meiryo UI", 7)
        self.option_add("*Font", default_font)
        style = ttk.Style()
        style.configure('.', font=default_font)
        style.configure('Left.TButton', anchor=tk.W)

        self._create_widgets()
    #endregion

    #region Private Methods
    def _create_widgets(self) -> None:
        """
        Summary:
            ウィジェットの生成と配置を行います。
        Description:
            メニューバー、左右ペイン、ステータスバーを構築します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._create_menu()
        self._create_main_paned_window()
        self._create_status_bar()

    def _create_menu(self) -> None:
        """
        Summary:
            メニューバーを作成します。
        Description:
            ツールメニュー（定型文管理）を配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.mnu_main: tk.Menu = tk.Menu(self)
        """tk.Menu - メインメニューバー"""
        self.mnu_tools: tk.Menu = tk.Menu(self.mnu_main, tearoff=0)
        """tk.Menu - ツールメニュー"""
        self.mnu_tools.add_command(label="定型文管理")
        self.mnu_main.add_cascade(label="ツール", menu=self.mnu_tools)
        self.config(menu=self.mnu_main)

    def _create_main_paned_window(self) -> None:
        """
        Summary:
            メインの左右ペインを作成します。
        Description:
            PanedWindowで左ペイン（記録）と右ペイン（検索）を構築します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.frm_main_paned: ttk.PanedWindow = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        """ttk.PanedWindow - メイン左右分割ペイン"""
        self.frm_main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._create_left_pane()
        self._create_right_pane()

    def _create_left_pane(self) -> None:
        """
        Summary:
            左ペイン（アクティブ記録エリア）を作成します。
        Description:
            上部に検索・ブロック作成エリア、下部にスクロール可能なブロックエリアを配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.frm_left_pane: ttk.Frame = ttk.Frame(self.frm_main_paned, width=fws_case_recorder_const.LEFT_PANE_MIN_WIDTH)
        """ttk.Frame - 左ペインフレーム"""
        self.frm_main_paned.add(self.frm_left_pane, weight=1)

        # 画面設定（最前面・透過度）エリア
        self.frm_settings: ttk.Frame = ttk.Frame(self.frm_left_pane)
        """ttk.Frame - 画面設定フレーム"""
        self.frm_settings.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 0))

        self.var_topmost: tk.BooleanVar = tk.BooleanVar(value=False)
        """tk.BooleanVar - 最前面固定フラグ"""
        self.chk_topmost: ttk.Checkbutton = ttk.Checkbutton(self.frm_settings, text="最前面固定", variable=self.var_topmost)
        """ttk.Checkbutton - 最前面固定チェックボックス"""
        self.chk_topmost.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(self.frm_settings, text="透過度:").pack(side=tk.LEFT)
        self.scl_alpha: ttk.Scale = ttk.Scale(self.frm_settings, from_=0.2, to=1.0, value=1.0, orient=tk.HORIZONTAL, length=100)
        """ttk.Scale - 透過度スライダー"""
        self.scl_alpha.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.frm_settings, text="時刻形式:").pack(side=tk.LEFT, padx=(10, 2))
        self.cmb_time_format: ttk.Combobox = ttk.Combobox(self.frm_settings, width=15, state="readonly")
        """ttk.Combobox - 時刻挿入フォーマット選択"""
        self.cmb_time_format["values"] = ("YYYY/MM/DD HH:MM", "YYYY/MM/DD", "HH:MM")
        self.cmb_time_format.current(0)
        self.cmb_time_format.pack(side=tk.LEFT, padx=(0, 5))

        # 上部: 検索・ブロック作成エリア
        self.frm_left_top: ttk.LabelFrame = ttk.LabelFrame(self.frm_left_pane, text="案件検索・ブロック作成")
        """ttk.LabelFrame - 左ペイン上部フレーム"""
        self.frm_left_top.pack(fill=tk.X, padx=5, pady=(5, 2))

        # 県域・ビル名の入力行
        frm_search_row: ttk.Frame = ttk.Frame(self.frm_left_top)
        """ttk.Frame - 検索入力行フレーム"""
        frm_search_row.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frm_search_row, text="県域:").pack(side=tk.LEFT, padx=(0, 2))
        self.ent_region: ttk.Entry = ttk.Entry(frm_search_row, width=8)
        """ttk.Entry - 県域入力フィールド"""
        self.ent_region.pack(side=tk.LEFT, padx=(0, 2))

        ttk.Label(frm_search_row, text="ビル名:").pack(side=tk.LEFT, padx=(0, 2))
        self.ent_building: ttk.Entry = ttk.Entry(frm_search_row, width=10)
        """ttk.Entry - ビル名入力フィールド"""
        self.ent_building.pack(side=tk.LEFT, padx=(0, 2))

        # 案件番号コンボボックスの行
        frm_case_row: ttk.Frame = ttk.Frame(self.frm_left_top)
        """ttk.Frame - 案件番号行フレーム"""
        frm_case_row.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frm_case_row, text="案件番号:").pack(side=tk.LEFT, padx=(0, 2))
        self.cmb_case_number: ttk.Combobox = ttk.Combobox(frm_case_row, width=15)
        """ttk.Combobox - 案件番号コンボボックス"""
        self.cmb_case_number.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_create_block: ttk.Button = ttk.Button(frm_case_row, text="作成", width=6)
        """ttk.Button - ブロック作成ボタン"""
        self.btn_create_block.pack(side=tk.LEFT)

        # 下部: スクロール可能なブロックエリア
        self.frm_left_bottom: ttk.LabelFrame = ttk.LabelFrame(self.frm_left_pane, text="アクティブ記録")
        """ttk.LabelFrame - 左ペイン下部フレーム"""
        self.frm_left_bottom.pack(fill=tk.BOTH, expand=True, padx=5, pady=(2, 5))

        self.cvs_blocks: tk.Canvas = tk.Canvas(self.frm_left_bottom)
        """tk.Canvas - ブロックエリアキャンバス"""
        self.frm_blocks_scrollbar: ttk.Scrollbar = ttk.Scrollbar(self.frm_left_bottom, orient=tk.VERTICAL, command=self.cvs_blocks.yview)
        """ttk.Scrollbar - ブロックエリアスクロールバー"""
        self.frm_blocks_container: ttk.Frame = ttk.Frame(self.cvs_blocks)
        """ttk.Frame - ブロック格納用コンテナフレーム"""

        self.frm_blocks_container.bind("<Configure>", lambda e: self.cvs_blocks.configure(scrollregion=self.cvs_blocks.bbox("all")))
        self.cvs_blocks_window = self.cvs_blocks.create_window((0, 0), window=self.frm_blocks_container, anchor="nw")
        
        self.cvs_blocks.configure(yscrollcommand=self.frm_blocks_scrollbar.set)

        self.frm_blocks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cvs_blocks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _create_right_pane(self) -> None:
        """
        Summary:
            右ペイン（履歴検索エリア）を作成します。
        Description:
            上部に検索エリア、下部にアコーディオン表示エリアを配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.frm_right_pane: ttk.Frame = ttk.Frame(self.frm_main_paned, width=fws_case_recorder_const.RIGHT_PANE_MIN_WIDTH)
        """ttk.Frame - 右ペインフレーム"""
        self.frm_main_paned.add(self.frm_right_pane, weight=1)

        # 上部: 検索エリア
        self.frm_right_top: ttk.LabelFrame = ttk.LabelFrame(self.frm_right_pane, text="履歴検索")
        """ttk.LabelFrame - 右ペイン上部フレーム"""
        self.frm_right_top.pack(fill=tk.X, padx=5, pady=(5, 2))

        frm_search_history_row1: ttk.Frame = ttk.Frame(self.frm_right_top)
        """ttk.Frame - 履歴検索入力行フレーム1"""
        frm_search_history_row1.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frm_search_history_row1, text="県域:").pack(side=tk.LEFT, padx=(0, 2))
        self.ent_search_region: ttk.Entry = ttk.Entry(frm_search_history_row1, width=8)
        """ttk.Entry - 履歴検索用県域入力フィールド"""
        self.ent_search_region.pack(side=tk.LEFT, padx=(0, 2))

        ttk.Label(frm_search_history_row1, text="ビル名:").pack(side=tk.LEFT, padx=(0, 2))
        self.ent_search_building: ttk.Entry = ttk.Entry(frm_search_history_row1, width=10)
        """ttk.Entry - 履歴検索用ビル名入力フィールド"""
        self.ent_search_building.pack(side=tk.LEFT, padx=(0, 2))

        frm_search_history_row2: ttk.Frame = ttk.Frame(self.frm_right_top)
        """ttk.Frame - 履歴検索入力行フレーム2"""
        frm_search_history_row2.pack(fill=tk.X, padx=5, pady=2)

        ttk.Label(frm_search_history_row2, text="案件番号:").pack(side=tk.LEFT, padx=(0, 2))
        self.cmb_search_case: ttk.Combobox = ttk.Combobox(frm_search_history_row2, width=20)
        """ttk.Combobox - 履歴検索用案件番号コンボボックス"""
        self.cmb_search_case.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        self.btn_search: ttk.Button = ttk.Button(frm_search_history_row2, text="更新", width=6)
        """ttk.Button - 検索(更新)ボタン"""
        self.btn_search.pack(side=tk.LEFT)

        # 下部: アコーディオン表示エリア
        self.frm_right_bottom: ttk.LabelFrame = ttk.LabelFrame(self.frm_right_pane, text="検索結果")
        """ttk.LabelFrame - 右ペイン下部フレーム"""
        self.frm_right_bottom.pack(fill=tk.BOTH, expand=True, padx=5, pady=(2, 5))

        self.cvs_history: tk.Canvas = tk.Canvas(self.frm_right_bottom)
        """tk.Canvas - 履歴表示キャンバス"""
        self.frm_history_scrollbar: ttk.Scrollbar = ttk.Scrollbar(self.frm_right_bottom, orient=tk.VERTICAL, command=self.cvs_history.yview)
        """ttk.Scrollbar - 履歴表示スクロールバー"""
        self.frm_history_container: ttk.Frame = ttk.Frame(self.cvs_history)
        """ttk.Frame - 履歴ブロック格納用コンテナフレーム"""

        self.frm_history_container.bind("<Configure>", lambda e: self.cvs_history.configure(scrollregion=self.cvs_history.bbox("all")))
        self.cvs_history_window = self.cvs_history.create_window((0, 0), window=self.frm_history_container, anchor="nw")
        
        self.cvs_history.configure(yscrollcommand=self.frm_history_scrollbar.set)

        self.frm_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cvs_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _create_status_bar(self) -> None:
        """
        Summary:
            ステータスバーを作成します。
        Description:
            画面下部にステータスメッセージを表示するラベルを配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.frm_status: ttk.Frame = ttk.Frame(self)
        """ttk.Frame - ステータスバーフレーム"""
        self.frm_status.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)

        self.lbl_status: ttk.Label = ttk.Label(self.frm_status, text=fws_case_recorder_const.STATUS_MSG_READY, anchor=tk.W)
        """ttk.Label - ステータスバーラベル"""
        self.lbl_status.pack(fill=tk.X, side=tk.LEFT)
    #endregion
