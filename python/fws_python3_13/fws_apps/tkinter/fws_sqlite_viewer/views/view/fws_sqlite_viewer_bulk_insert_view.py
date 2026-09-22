"""
Summary:
    バルクインサート設定ダイアログのViewモジュール。
Description:
    Toplevelを用いたダイアログのGUI定義を行います。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk

class FwsSqliteViewerBulkInsertView:
    """
    Summary:
        バルクインサート設定ダイアログのViewクラス。
    Description:
        入力ソース選択、ファイルパス/テキストデータ入力、オプション設定、実行ボタンなどを配置します。
    """

    #region Constructor
    def __init__(self, parent: tk.Widget, table_name: str) -> None:
        """
        Summary:
            コンストラクタ。
        Args:
            parent: tk.Widget - 親ウィジェット
            table_name: str - 対象テーブル名
        """
        self.dlg = tk.Toplevel(parent)
        self.dlg.title(f"Bulk Insert to {table_name}")
        self.dlg.geometry("600x400")
        self.dlg.transient(parent)
        self.dlg.grab_set()

        # Input Source (Radio)
        self.frm_source = ttk.LabelFrame(self.dlg, text="Input Source")
        self.frm_source.pack(fill=tk.X, padx=10, pady=5)
        
        self.var_source = tk.StringVar(value="file")
        self.rb_file = ttk.Radiobutton(self.frm_source, text="File (CSV/TSV)", variable=self.var_source, value="file")
        self.rb_text = ttk.Radiobutton(self.frm_source, text="Text (Clipboard)", variable=self.var_source, value="text")
        self.rb_file.pack(side=tk.LEFT, padx=5, pady=5)
        self.rb_text.pack(side=tk.LEFT, padx=5, pady=5)

        # File Input
        self.frm_file = ttk.Frame(self.dlg)
        self.frm_file.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(self.frm_file, text="File Path:").pack(side=tk.LEFT)
        self.var_filepath = tk.StringVar()
        self.ent_filepath = ttk.Entry(self.frm_file, textvariable=self.var_filepath)
        self.ent_filepath.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.btn_browse = ttk.Button(self.frm_file, text="Browse...")
        self.btn_browse.pack(side=tk.LEFT)

        # Text Input
        self.frm_text = ttk.LabelFrame(self.dlg, text="Text Data")
        self.frm_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.txt_data = tk.Text(self.frm_text, height=10)
        self.txt_data.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Options
        self.frm_options = ttk.LabelFrame(self.dlg, text="Options")
        self.frm_options.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.frm_options, text="Delimiter:").pack(side=tk.LEFT, padx=5)
        self.var_delimiter = tk.StringVar(value=", (Comma)")
        self.cb_delimiter = ttk.Combobox(self.frm_options, textvariable=self.var_delimiter, values=[", (Comma)", "\\t (Tab)"], state="readonly", width=15)
        self.cb_delimiter.pack(side=tk.LEFT, padx=5)
        
        self.var_header = tk.BooleanVar(value=True)
        self.chk_header = ttk.Checkbutton(self.frm_options, text="First row is header", variable=self.var_header)
        self.chk_header.pack(side=tk.LEFT, padx=20)

        # Execute/Cancel Buttons
        self.frm_buttons = ttk.Frame(self.dlg)
        self.frm_buttons.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_execute = ttk.Button(self.frm_buttons, text="Execute")
        self.btn_execute.pack(side=tk.RIGHT, padx=5)
        self.btn_cancel = ttk.Button(self.frm_buttons, text="Cancel", command=self.dlg.destroy)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)
    #endregion
