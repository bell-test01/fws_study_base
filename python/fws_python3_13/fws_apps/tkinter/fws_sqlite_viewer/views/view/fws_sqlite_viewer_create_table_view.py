"""
Summary:
    fws_sqlite_viewer アプリのテーブル作成ダイアログのビューモジュール。
Description:
    新規テーブル作成用ダイアログのUIレイアウトを構築します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk
from typing import List

class FwsSqliteViewerCreateTableView(tk.Toplevel):
    """
    Summary:
        テーブル作成ダイアログのビュークラス。
    Description:
        テーブル名入力、カラム定義リスト、追加・削除ボタン、作成・キャンセルボタンを配置します。
    """

    def __init__(self, master: tk.Misc, alias: str) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            UI部品を初期化し配置します。
        Args:
            master: tk.Misc - 親ウィジェット。
            alias: str - 対象のデータベースエイリアス。
        """
        super().__init__(master)
        
        self.title(f"Create New Table [{alias}]")
        self.minsize(500, 300)
        self.transient(master)
        self.grab_set()

        self.columns_frames: List[ttk.Frame] = []
        self._create_widgets()

    def _create_widgets(self) -> None:
        """
        Summary:
            ウィジェットの生成と配置を行います。
        """
        # メインフレーム
        frm_main = ttk.Frame(self)
        frm_main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # テーブル名エリア
        frm_top = ttk.Frame(frm_main)
        frm_top.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frm_top, text="Table Name:").pack(side=tk.LEFT, padx=(0, 5))
        self.ent_table_name = ttk.Entry(frm_top)
        self.ent_table_name.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # カラム一覧エリア (CanvasとScrollbarを使ったスクロール可能フレーム)
        frm_middle = ttk.LabelFrame(frm_main, text="Columns")
        frm_middle.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # ヘッダー行
        frm_header = ttk.Frame(frm_middle)
        frm_header.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(frm_header, text="Name", width=15).pack(side=tk.LEFT, padx=2)
        ttk.Label(frm_header, text="Type", width=12).pack(side=tk.LEFT, padx=2)
        ttk.Label(frm_header, text="PK", width=4).pack(side=tk.LEFT, padx=2)
        ttk.Label(frm_header, text="Not Null", width=8).pack(side=tk.LEFT, padx=2)
        ttk.Label(frm_header, text="Default", width=10).pack(side=tk.LEFT, padx=2)

        # スクロールエリア構築
        self.canvas = tk.Canvas(frm_middle, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(frm_middle, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.frm_columns = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frm_columns, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.frm_columns.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ボタンエリア (カラム追加、作成、キャンセル)
        frm_bottom = ttk.Frame(frm_main)
        frm_bottom.pack(fill=tk.X)

        self.btn_add_column = ttk.Button(frm_bottom, text="Add Column")
        self.btn_add_column.pack(side=tk.LEFT)

        self.btn_cancel = ttk.Button(frm_bottom, text="Cancel")
        self.btn_cancel.pack(side=tk.RIGHT, padx=(5, 0))

        self.btn_create = ttk.Button(frm_bottom, text="Create")
        self.btn_create.pack(side=tk.RIGHT)

    def add_column_row(self) -> ttk.Frame:
        """
        Summary:
            新しいカラム入力用の行を追加し、そのフレームを返します。
        Returns:
            ttk.Frame - 追加された行のフレーム。
        """
        frm_row = ttk.Frame(self.frm_columns)
        frm_row.pack(fill=tk.X, padx=5, pady=2)

        # Name
        ent_name = ttk.Entry(frm_row, width=15)
        ent_name.pack(side=tk.LEFT, padx=2)
        
        # Type
        cb_type = ttk.Combobox(frm_row, values=["INTEGER", "TEXT", "REAL", "BLOB", "NUMERIC"], width=10)
        cb_type.pack(side=tk.LEFT, padx=2)
        
        # PK
        var_pk = tk.BooleanVar()
        chk_pk = ttk.Checkbutton(frm_row, variable=var_pk, width=4)
        chk_pk.pack(side=tk.LEFT, padx=2)
        
        # Not Null
        var_notnull = tk.BooleanVar()
        chk_notnull = ttk.Checkbutton(frm_row, variable=var_notnull, width=8)
        chk_notnull.pack(side=tk.LEFT, padx=2)
        
        # Default
        ent_default = ttk.Entry(frm_row, width=10)
        ent_default.pack(side=tk.LEFT, padx=2)

        # Delete Button
        btn_del = ttk.Button(frm_row, text="Del", width=4)
        btn_del.pack(side=tk.LEFT, padx=2)

        # ウィジェットの参照を保存しておく（イベント側で値を取得するため）
        frm_row.widgets = {
            "name": ent_name,
            "type": cb_type,
            "pk": var_pk,
            "notnull": var_notnull,
            "default": ent_default,
            "btn_del": btn_del
        }

        self.columns_frames.append(frm_row)
        return frm_row

    def remove_column_row(self, frm_row: ttk.Frame) -> None:
        """
        Summary:
            指定されたカラム行を削除します。
        Args:
            frm_row: ttk.Frame - 削除対象の行フレーム。
        """
        if frm_row in self.columns_frames:
            self.columns_frames.remove(frm_row)
        frm_row.destroy()
        # スクロール領域の更新を促す
        self.update_idletasks()
