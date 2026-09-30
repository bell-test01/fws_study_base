"""
Summary:
    fws_source_linkerのメイン画面UI定義モジュールです。
Description:
    ウィンドウ、入力欄、Treeviewなどのウィジェットの配置を行います。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk, font

# app
from fws_apps.tkinter.fws_source_linker.constant import fws_source_linker_const


class FwsSourceLinkerView(tk.Tk):
    """
    Summary:
        メイン画面クラス。
    Description:
        起点ディレクトリ、コピー先ディレクトリの指定UI、および階層表示用Treeviewを配置します。
    """

    # region Constructor
    def __init__(self) -> None:
        """
        Summary:
            FwsSourceLinkerViewを初期化します。
        """
        super().__init__()
        
        self.title("fws_source_linker")
        self.geometry("800x600")
        
        # フォント設定
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family=fws_source_linker_const.UI_FONT_FAMILY, size=fws_source_linker_const.UI_FONT_SIZE)
        text_font = font.nametofont("TkTextFont")
        text_font.configure(family=fws_source_linker_const.UI_FONT_FAMILY, size=fws_source_linker_const.UI_FONT_SIZE)
        fixed_font = font.nametofont("TkFixedFont")
        fixed_font.configure(family=fws_source_linker_const.UI_FONT_FAMILY, size=fws_source_linker_const.UI_FONT_SIZE)
        
        style = ttk.Style()
        style.configure('.', font=(fws_source_linker_const.UI_FONT_FAMILY, fws_source_linker_const.UI_FONT_SIZE))
        
        # UIウィジェット
        self.frm_main = ttk.Frame(self, padding=10)
        self.frm_main.pack(fill=tk.BOTH, expand=True)
        
        # 設定(最前面/透過度)
        self.frm_settings = ttk.Frame(self.frm_main)
        self.frm_settings.pack(fill=tk.X, pady=(0, 5))
        
        self.var_topmost = tk.BooleanVar(value=fws_source_linker_const.UI_DEFAULT_TOPMOST)
        self.chk_topmost = ttk.Checkbutton(self.frm_settings, text="最前面に表示", variable=self.var_topmost)
        self.chk_topmost.pack(side=tk.LEFT)
        
        ttk.Label(self.frm_settings, text="透過度:").pack(side=tk.LEFT, padx=(15, 5))
        self.var_alpha = tk.DoubleVar(value=fws_source_linker_const.UI_DEFAULT_ALPHA)
        self.scl_alpha = ttk.Scale(
            self.frm_settings, 
            from_=fws_source_linker_const.UI_ALPHA_MIN, 
            to=fws_source_linker_const.UI_ALPHA_MAX, 
            variable=self.var_alpha, 
            orient=tk.HORIZONTAL
        )
        self.scl_alpha.pack(side=tk.LEFT)
        
        # 起点ディレクトリ
        self.frm_root = ttk.Frame(self.frm_main)
        self.frm_root.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(self.frm_root, text="コピー元フォルダ:").pack(side=tk.LEFT)
        
        self.btn_select_root = ttk.Button(self.frm_root, text="参照...")
        self.btn_select_root.pack(side=tk.LEFT)
        
        self.cbo_root_dir = ttk.Combobox(self.frm_root, width=50)
        self.cbo_root_dir.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.btn_reload_root = ttk.Button(self.frm_root, text="更新")
        self.btn_reload_root.pack(side=tk.LEFT)
        
        # コピー先ディレクトリ
        self.frm_dest = ttk.Frame(self.frm_main)
        self.frm_dest.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.frm_dest, text="コピー先フォルダ:").pack(side=tk.LEFT)
        
        self.btn_select_dest = ttk.Button(self.frm_dest, text="参照...")
        self.btn_select_dest.pack(side=tk.LEFT)
        
        self.cbo_dest_dir = ttk.Combobox(self.frm_dest, width=30)
        self.cbo_dest_dir.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 2))
        
        ttk.Label(self.frm_dest, text="\\").pack(side=tk.LEFT)
        
        self.ent_dest_sub_dir = ttk.Entry(self.frm_dest, width=15)
        self.ent_dest_sub_dir.pack(side=tk.LEFT, padx=(2, 5))
        
        self.btn_open_dest = ttk.Button(self.frm_dest, text="開く")
        self.btn_open_dest.pack(side=tk.LEFT)
        
        # ツリービュー (階層表示)
        self.frm_tree = ttk.Frame(self.frm_main)
        self.frm_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 複数選択可能(selectmode="extended")
        self.trv_files = ttk.Treeview(self.frm_tree, selectmode="extended", columns=("type",), show="tree")
        self.trv_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scr_tree = ttk.Scrollbar(self.frm_tree, orient="vertical", command=self.trv_files.yview)
        self.scr_tree.pack(side=tk.RIGHT, fill=tk.Y)
        self.trv_files.configure(yscrollcommand=self.scr_tree.set)
        
        # アクション
        self.frm_action = ttk.Frame(self.frm_main)
        self.frm_action.pack(fill=tk.X)
        self.btn_copy = ttk.Button(self.frm_action, text="コピー実行")
        self.btn_copy.pack(side=tk.RIGHT)
    # endregion
