"""
Summary:
    メイン画面ビューモジュール。
Description:
    fws_chat_template アプリケーションのメイン画面UIウィジェット生成およびレイアウト配置を行います。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

from fws_lib.tkinter.views.view.component import (
    fws_view_component_lib_accordion_block,
    fws_view_component_lib_scrollable_frame,
)

from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
from fws_apps.tkinter.fws_chat_template.views.view.component import (
    fws_view_component_chat_template_description_block,
    fws_view_component_chat_template_device_table,
    fws_view_component_chat_template_timeline_block,
)
#endregion

#region classes
class FwsViewChatTemplate(tk.Tk):
    """
    Summary:
        メイン画面ビュークラス。
    Description:
        tk.Tk を継承し、最上面固定・透過度設定フレーム、全幅ステータスバー、
        チケット番号・県域・ビル名入力フォーム、および専用コンポーネント化されたスクロール対応の
        基本情報エリア（Descriptionブロック、拡張領域）を含むメイン画面UIを構築します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            親クラス（tk.Tk）の初期化、ウィンドウ属性設定、およびウィジェットの生成と配置を行います。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        super().__init__()
        self.var_topmost: tk.BooleanVar
        """tk.BooleanVar - 最前面固定フラグ"""
        self.chk_topmost: ttk.Checkbutton
        """ttk.Checkbutton - 最前面固定チェックボックス"""
        self.scl_alpha: ttk.Scale
        """ttk.Scale - 透過度スライダー"""
        self.lbl_status: ttk.Label
        """ttk.Label - ステータスバーラベル"""
        self.app_font: tkfont.Font
        """tkfont.Font - アプリケーション標準名前付きフォント"""
        self.cmb_ticket_number: ttk.Combobox
        """ttk.Combobox - チケット番号コンボボックス"""
        self.cmb_prefecture: ttk.Combobox
        """ttk.Combobox - 県域コンボボックス"""
        self.cmb_building_name: ttk.Combobox
        """ttk.Combobox - ビル名コンボボックス"""
        self.btn_delete: ttk.Button
        """ttk.Button - チケット削除ボタン"""
        self.btn_unlock: ttk.Button
        """ttk.Button - 入力キーロック解除ボタン"""
        self.scr_base_data: fws_view_component_lib_scrollable_frame.FwsViewComponentLibScrollableFrame
        """fws_view_component_lib_scrollable_frame.FwsViewComponentLibScrollableFrame - 基本情報エリア用スクロール可能フレーム"""
        self.blk_desc: fws_view_component_chat_template_description_block.FwsViewComponentChatTemplateDescriptionBlock
        """fws_view_component_chat_template_description_block.FwsViewComponentChatTemplateDescriptionBlock - Descriptionコンポーネント"""
        self.blk_device: fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock
        """fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock - 機器情報アコーディオンブロック"""
        self.tbl_device: fws_view_component_chat_template_device_table.FwsViewComponentChatTemplateDeviceTable
        """fws_view_component_chat_template_device_table.FwsViewComponentChatTemplateDeviceTable - 機器情報テーブルコンポーネント"""
        self.nbk_right: ttk.Notebook
        """ttk.Notebook - 右ペイン用ノートブック"""
        self.paned_timeline: ttk.PanedWindow
        """ttk.PanedWindow - 時系列タブ内左右分割ペインウィンドウ"""
        self.cmb_work_category: ttk.Combobox
        """ttk.Combobox - 作業分類選択コンボボックス"""
        self.lst_timeline_menu: tk.Listbox
        """tk.Listbox - 作業メニュー一覧リストボックス"""
        self.scb_timeline_menu_v: ttk.Scrollbar
        """ttk.Scrollbar - 作業メニュー一覧縦スクロールバー"""
        self.blk_timeline: fws_view_component_chat_template_timeline_block.FwsViewComponentChatTemplateTimelineBlock
        """fws_view_component_chat_template_timeline_block.FwsViewComponentChatTemplateTimelineBlock - 時系列親コンポーネント"""
        self.menu_task_items: list[dict[str, str]] = []
        """list[dict[str, str]] - 現在リストボックスに表示中のタスクメニュー項目情報リスト"""
        self.ent_winmerge_path: ttk.Entry
        """ttk.Entry - WinMergeパス設定入力欄"""
        self.ent_font_size: ttk.Entry
        """ttk.Entry - フォントサイズ設定入力欄"""

        self._init_screen()
        self._create_widgets()

    def _init_screen(self) -> None:
        """
        Summary:
            画面の基本属性を初期化します。
        Description:
            ウィンドウタイトル、セッションから復元したフォントサイズ、および復元したウィンドウサイズを設定します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # 画面タイトル設定
        self.title(f"{fws_const_chat_template.APP_NAME_ENGLISH} v{fws_const_chat_template.APP_VERSION}")

        # フォント設定（session.json から復元）
        self.app_font = tkfont.Font(
            family=fws_const_chat_template.APP_FONT_NAME,
            size=fws_const_chat_template.load_font_size(),
        )
        self.option_add("*Font", self.app_font)
        style: ttk.Style = ttk.Style()
        style.configure(".", font=self.app_font)

        # 画面サイズ設定（幅x高さのみ復元、表示座標はOS標準動作に委譲）
        self.geometry(fws_const_chat_template.load_window_geometry(fws_const_chat_template.VIEW_NAME_FWS_VIEW_CHAT_TEMPLATE))

    def _create_widgets(self) -> None:
        """
        Summary:
            画面上のウィジェットを生成し配置します。
        Description:
            最上部に最前面固定・透過度制御フレーム、ステータスバーを全幅配置し、
            メインエリア（左ペイン）に検索キーフォーム、スクロール可能フレーム、アコーディオン、テキスト、
            ボタン群、リサイズグリップ、将来拡張ダミー領域を配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # 最前面固定・透過度制御フレーム（画面最上部に全幅配置）
        _frm_window_settings: ttk.Frame = ttk.Frame(self)
        _frm_window_settings.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 0))

        self.var_topmost = tk.BooleanVar(value=False)
        self.chk_topmost = ttk.Checkbutton(
            _frm_window_settings,
            text="最前面固定",
            variable=self.var_topmost,
        )
        self.chk_topmost.pack(side=tk.LEFT, padx=(0, 10))

        self.scl_alpha = ttk.Scale(
            _frm_window_settings,
            from_=0.2,
            to=1.0,
            value=1.0,
            orient=tk.HORIZONTAL,
            length=120,
        )
        self.scl_alpha.pack(side=tk.LEFT, padx=5)

        # ステータスバー（設定フレーム直下に全幅配置）
        _frm_status_msg: ttk.Frame = ttk.Frame(self)
        _frm_status_msg.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(3, 5))
        self.lbl_status = ttk.Label(
            _frm_status_msg,
            text=fws_const_chat_template.get_message(fws_const_chat_template.MSG_STATUS_READY),
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 3),
        )
        self.lbl_status.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(3, 5))

        # オペレーションウィンドウのメインフレーム
        _frm_operation: ttk.Frame = ttk.Frame(self)
        _frm_operation.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=(3, 5))

        # 左右分割ペインウィンドウ（ステータスバー直下に配置）
        _paned_operation: ttk.PanedWindow = ttk.PanedWindow(_frm_operation, orient=tk.HORIZONTAL)
        _paned_operation.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # 左ペイン（メインエリア）
        _frm_left: ttk.Frame = ttk.Frame(
            _paned_operation,
            padding=5,
            relief=tk.SOLID,
            borderwidth=1,
        )

        #-------------------------------------------------------
        # 検索キー入力フォームフレーム（上部配置）
        #-------------------------------------------------------
        _frm_input_key: ttk.Frame = ttk.Frame(_frm_left)
        _frm_input_key.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        _frm_input_key.columnconfigure(0, weight=1)
        _frm_input_key.columnconfigure(1, weight=1)

        # チケット番号（2列結合して全幅配置）
        lbl_ticket_number: ttk.Label = ttk.Label(_frm_input_key, text="チケット番号:")
        lbl_ticket_number.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 2))
        self.cmb_ticket_number = ttk.Combobox(_frm_input_key)
        self.cmb_ticket_number.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(0, 5))

        # 県域（左側: 0列目）
        lbl_prefecture: ttk.Label = ttk.Label(_frm_input_key, text="県域:")
        lbl_prefecture.grid(row=2, column=0, sticky=tk.W, pady=(0, 2))
        self.cmb_prefecture = ttk.Combobox(_frm_input_key)
        self.cmb_prefecture.grid(row=3, column=0, sticky=tk.EW, padx=(0, 5))

        # ビル名（右側: 1列目）
        lbl_building_name: ttk.Label = ttk.Label(_frm_input_key, text="ビル名:")
        lbl_building_name.grid(row=2, column=1, sticky=tk.W, pady=(0, 2))
        self.cmb_building_name = ttk.Combobox(_frm_input_key)
        self.cmb_building_name.grid(row=3, column=1, sticky=tk.EW)

        # 削除ボタン（県域コンボボックスの左下: row=4, column=0）
        self.btn_delete = ttk.Button(
            _frm_input_key,
            text="削除",
            state=tk.DISABLED,
        )
        self.btn_delete.grid(row=4, column=0, sticky=tk.W, pady=(4, 0))

        # ロック解除ボタン（ビル名コンボボックスの右下: row=4, column=1）
        self.btn_unlock = ttk.Button(
            _frm_input_key,
            text="ロック解除",
            state=tk.DISABLED,
        )
        self.btn_unlock.grid(row=4, column=1, sticky=tk.E, pady=(4, 0))

        #-------------------------------------------------------
        # 基本情報入力エリア（スクロール可能フレーム）
        #-------------------------------------------------------
        self.scr_base_data = fws_view_component_lib_scrollable_frame.FwsViewComponentLibScrollableFrame(_frm_left)
        self.scr_base_data.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=(2, 0))

        # Descriptionコンポーネント
        self.blk_desc = fws_view_component_chat_template_description_block.FwsViewComponentChatTemplateDescriptionBlock(self.scr_base_data.content_frame)
        self.blk_desc.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(2, 0))

        # 機器情報アコーディオンブロック
        self.blk_device = fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock(
            self.scr_base_data.content_frame,
            title="機器情報:",
            is_expanded=False,
        )
        self.blk_device.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 5))

        # 機器情報テーブルコンポーネント（配置するだけ！）
        self.tbl_device = fws_view_component_chat_template_device_table.FwsViewComponentChatTemplateDeviceTable(self.blk_device.container)
        self.tbl_device.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        _paned_operation.add(_frm_left, weight=1)

        # 右ペイン（サブエリア: ノートブック）
        _frm_right: ttk.Frame = ttk.Frame(
            _paned_operation,
            padding=5,
            relief=tk.SOLID,
            borderwidth=1,
        )

        self.nbk_right = ttk.Notebook(_frm_right)
        self.nbk_right.pack(fill=tk.BOTH, expand=True)

        # タブ1: 「時系列」タブ
        frm_tab_timeline: ttk.Frame = ttk.Frame(self.nbk_right, padding=5)
        self.nbk_right.add(frm_tab_timeline, text="時系列")

        self.paned_timeline = ttk.PanedWindow(frm_tab_timeline, orient=tk.HORIZONTAL)
        self.paned_timeline.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 時系列タブ - 左側（作業分類・メニュー選択）
        frm_timeline_left: ttk.Frame = ttk.Frame(
            self.paned_timeline,
            padding=5,
            relief=tk.SOLID,
            borderwidth=1,
        )
        lbl_work_category: ttk.Label = ttk.Label(frm_timeline_left, text="作業分類:")
        lbl_work_category.pack(anchor=tk.W, pady=(0, 2))
        self.cmb_work_category = ttk.Combobox(frm_timeline_left, state="readonly", values=[])
        self.cmb_work_category.pack(fill=tk.X, pady=(0, 5))

        lbl_timeline_menu: ttk.Label = ttk.Label(frm_timeline_left, text="メニュー（ダブルクリックで追加）:")
        lbl_timeline_menu.pack(anchor=tk.W, pady=(0, 2))

        frm_menu_container: ttk.Frame = ttk.Frame(frm_timeline_left)
        frm_menu_container.pack(fill=tk.BOTH, expand=True)

        self.scb_timeline_menu_v = ttk.Scrollbar(frm_menu_container, orient=tk.VERTICAL)
        self.lst_timeline_menu = tk.Listbox(
            frm_menu_container,
            exportselection=False,
            selectmode=tk.SINGLE,
            yscrollcommand=self.scb_timeline_menu_v.set,
        )
        self.scb_timeline_menu_v.configure(command=self.lst_timeline_menu.yview)
        self.scb_timeline_menu_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.lst_timeline_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.paned_timeline.add(frm_timeline_left, weight=1)

        # 時系列タブ - 右側（時系列ブロックコンポーネント配置）
        self.blk_timeline = fws_view_component_chat_template_timeline_block.FwsViewComponentChatTemplateTimelineBlock(
            self.paned_timeline,
            padding=5,
            relief=tk.SOLID,
            borderwidth=1,
        )
        self.paned_timeline.add(self.blk_timeline, weight=2)

        # タブ2: 「設定」タブ
        frm_tab_settings: ttk.Frame = ttk.Frame(self.nbk_right, padding=10)
        self.nbk_right.add(frm_tab_settings, text="設定")

        lbl_winmerge_path: ttk.Label = ttk.Label(frm_tab_settings, text="WinMerge パス:")
        lbl_winmerge_path.pack(anchor=tk.W, pady=(0, 2))
        self.ent_winmerge_path = ttk.Entry(frm_tab_settings)
        self.ent_winmerge_path.pack(fill=tk.X, pady=(0, 10))

        lbl_font_size: ttk.Label = ttk.Label(frm_tab_settings, text="フォントサイズ:")
        lbl_font_size.pack(anchor=tk.W, pady=(0, 2))
        self.ent_font_size = ttk.Entry(frm_tab_settings)
        self.ent_font_size.pack(fill=tk.X, pady=(0, 10))

        # 初期表示タブ設定
        self.nbk_right.select(frm_tab_timeline)

        _paned_operation.add(_frm_right, weight=1)
    #endregion
#endregion
