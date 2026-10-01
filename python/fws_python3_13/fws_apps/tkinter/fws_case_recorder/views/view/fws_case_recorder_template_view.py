"""
Summary:
    fws_case_recorder アプリの定型文管理画面ビューモジュール。
Description:
    定型文のCRUD操作を行う簡素なダイアログUIを構築します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk

class FwsCaseRecorderTemplateView(tk.Toplevel):
    """
    Summary:
        定型文管理画面のビュークラス。
    Description:
        定型文の一覧表示と追加・編集・削除を行うダイアログを構築します。
    """

    #region Constructor
    def __init__(self, master: tk.Tk, width: int = 600, height: int = 500) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            親ウィンドウを指定してダイアログを初期化し、UI部品を配置します。
        Args:
            master: tk.Tk - 親ウィンドウ。
            width: int - ウィンドウの幅（デフォルト600）。
            height: int - ウィンドウの高さ（デフォルト500）。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master)

        self.title("定型文管理")
        master.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() - width) // 2
        y = master.winfo_y() + (master.winfo_height() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(500, 400)
        self.transient(master)

        self._create_widgets()
    #endregion

    #region Private Methods
    def _create_widgets(self) -> None:
        """
        Summary:
            ウィジェットの生成と配置を行います。
        Description:
            一覧表示エリア、入力エリア、操作ボタンを構築します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # 一覧表示エリア
        self.frm_list: ttk.LabelFrame = ttk.LabelFrame(self, text="定型文一覧")
        """ttk.LabelFrame - 一覧エリアフレーム"""
        self.frm_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.trv_templates: ttk.Treeview = ttk.Treeview(self.frm_list, columns=("title", "content"), show="headings", height=8)
        """ttk.Treeview - 定型文一覧ツリービュー"""
        self.trv_templates.heading("title", text="タイトル")
        self.trv_templates.heading("content", text="本文")
        self.trv_templates.column("title", width=150)
        self.trv_templates.column("content", width=350)

        frm_trv_scroll: ttk.Scrollbar = ttk.Scrollbar(self.frm_list, orient=tk.VERTICAL, command=self.trv_templates.yview)
        """ttk.Scrollbar - ツリービュースクロールバー"""
        self.trv_templates.configure(yscrollcommand=frm_trv_scroll.set)
        self.trv_templates.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frm_trv_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # 入力エリア
        self.frm_input: ttk.LabelFrame = ttk.LabelFrame(self, text="入力")
        """ttk.LabelFrame - 入力エリアフレーム"""
        self.frm_input.pack(fill=tk.X, padx=10, pady=5)

        frm_title_row: ttk.Frame = ttk.Frame(self.frm_input)
        """ttk.Frame - タイトル行フレーム"""
        frm_title_row.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(frm_title_row, text="タイトル:").pack(side=tk.LEFT, padx=(0, 5))
        self.ent_template_title: ttk.Entry = ttk.Entry(frm_title_row)
        """ttk.Entry - タイトル入力フィールド"""
        self.ent_template_title.pack(side=tk.LEFT, fill=tk.X, expand=True)

        frm_content_row: ttk.Frame = ttk.Frame(self.frm_input)
        """ttk.Frame - 本文行フレーム"""
        frm_content_row.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(frm_content_row, text="本文:").pack(side=tk.LEFT, padx=(0, 5), anchor=tk.N)
        self.txt_template_content: tk.Text = tk.Text(frm_content_row, height=4, undo=True)
        """tk.Text - 本文入力テキストエリア"""
        self.txt_template_content.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 操作ボタンエリア
        self.frm_buttons: ttk.Frame = ttk.Frame(self)
        """ttk.Frame - ボタンエリアフレーム"""
        self.frm_buttons.pack(fill=tk.X, padx=10, pady=(5, 10))

        self.btn_template_add: ttk.Button = ttk.Button(self.frm_buttons, text="追加")
        """ttk.Button - 追加ボタン"""
        self.btn_template_add.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_template_update: ttk.Button = ttk.Button(self.frm_buttons, text="更新")
        """ttk.Button - 更新ボタン"""
        self.btn_template_update.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_template_delete: ttk.Button = ttk.Button(self.frm_buttons, text="削除")
        """ttk.Button - 削除ボタン"""
        self.btn_template_delete.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_template_close: ttk.Button = ttk.Button(self.frm_buttons, text="閉じる")
        """ttk.Button - 閉じるボタン"""
        self.btn_template_close.pack(side=tk.RIGHT)
    #endregion
