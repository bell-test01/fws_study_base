"""
Summary:
    fws_lib Tkinter アプリ用のダイアログユーティリティ。
Description:
    tkinter.messagebox や filedialog のよく使う処理をラップして提供します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from typing import Optional
from pathlib import Path

class FwsCustomDialog(tk.Toplevel):
    """
    親ウィンドウの中央に表示するためのカスタムダイアログクラス。
    """
    def __init__(self, parent: tk.Widget, title: str, message: str, dialog_type: str = "info") -> None:
        super().__init__(parent)
        self.title(title)
        self.result = False
        
        self.transient(parent)
        self.grab_set()
        
        # アイコンのパス設定
        current_dir = Path(__file__).resolve().parent
        icons_dir = current_dir / "assets" / "icons"
        
        icon_map = {
            "info": "info.png",
            "error": "error.png",
            "warning": "warning.png",
            "yes_no": "question.png",
            "ok_cancel": "question.png"
        }
        icon_filename = icon_map.get(dialog_type, "info.png")
        icon_path = icons_dir / icon_filename
            
        # UI構築
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)
        
        frm_top = ttk.Frame(frm)
        frm_top.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 画像ファイルが存在すれば読み込んで表示
        self.icon_image = None
        if icon_path.exists():
            try:
                self.icon_image = tk.PhotoImage(file=str(icon_path))
                lbl_icon = ttk.Label(frm_top, image=self.icon_image)
            except Exception:
                lbl_icon = ttk.Label(frm_top)
        else:
            lbl_icon = ttk.Label(frm_top)
            
        lbl_icon.pack(side=tk.LEFT, padx=(0, 15))
        
        lbl_text = ttk.Label(frm_top, text=message, justify=tk.LEFT)
        lbl_text.pack(side=tk.LEFT)
        
        frm_btn = ttk.Frame(frm)
        frm_btn.pack()
        
        if dialog_type == "yes_no":
            btn_yes = ttk.Button(frm_btn, text="はい", width=10, command=self._on_yes)
            btn_yes.pack(side=tk.LEFT, padx=5)
            btn_no = ttk.Button(frm_btn, text="いいえ", width=10, command=self._on_no)
            btn_no.pack(side=tk.LEFT, padx=5)
        elif dialog_type == "ok_cancel":
            btn_ok = ttk.Button(frm_btn, text="OK", width=10, command=self._on_yes)
            btn_ok.pack(side=tk.LEFT, padx=5)
            btn_cancel = ttk.Button(frm_btn, text="キャンセル", width=10, command=self._on_no)
            btn_cancel.pack(side=tk.LEFT, padx=5)
        else:
            btn_ok = ttk.Button(frm_btn, text="OK", width=10, command=self._on_yes)
            btn_ok.pack()
            
        self.update_idletasks()
        
        w = self.winfo_width()
        h = self.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")
        
        self.protocol("WM_DELETE_WINDOW", self._on_no)
        self.wait_window(self)
        
    def _on_yes(self):
        self.result = True
        self.destroy()
        
    def _on_no(self):
        self.result = False
        self.destroy()

def show_info(title: str, message: str, parent: Optional[tk.Widget] = None) -> None:
    """
    Summary:
        情報ダイアログを表示します。
    Description:
        tkinterのmessageboxを用いて情報メッセージを表示します。
    Args:
        title: str - ダイアログのタイトル。
        message: str - 表示するメッセージ。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        None - 戻り値なし。
    """
    if parent:
        FwsCustomDialog(parent, title, message, "info")
    else:
        messagebox.showinfo(title, message)

def show_error(title: str, message: str, parent: Optional[tk.Widget] = None) -> None:
    """
    Summary:
        エラーダイアログを表示します。
    Description:
        tkinterのmessageboxを用いてエラーメッセージを表示します。
    Args:
        title: str - ダイアログのタイトル。
        message: str - 表示するメッセージ。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        None - 戻り値なし。
    """
    if parent:
        FwsCustomDialog(parent, title, message, "error")
    else:
        messagebox.showerror(title, message)

def show_warning(title: str, message: str, parent: Optional[tk.Widget] = None) -> None:
    """
    Summary:
        警告ダイアログを表示します。
    Description:
        tkinterのmessageboxを用いて警告メッセージを表示します。
    Args:
        title: str - ダイアログのタイトル。
        message: str - 表示するメッセージ。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        None - 戻り値なし。
    """
    if parent:
        FwsCustomDialog(parent, title, message, "warning")
    else:
        messagebox.showwarning(title, message)

def ask_yes_no(title: str, message: str, parent: Optional[tk.Widget] = None) -> bool:
    """
    Summary:
        「はい/いいえ」を確認するダイアログを表示します。
    Description:
        ユーザーにYes/Noの選択を促します。
    Args:
        title: str - ダイアログのタイトル。
        message: str - 表示するメッセージ。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        bool - 「はい」を選択した場合は True、それ以外は False。
    """
    if parent:
        dlg = FwsCustomDialog(parent, title, message, "yes_no")
        return dlg.result
    else:
        return messagebox.askyesno(title, message)

def ask_open_file(title: str, filetypes: tuple, initialdir: Optional[str] = None, parent: Optional[tk.Widget] = None) -> str:
    """
    Summary:
        ファイルを開くダイアログを表示します。
    Description:
        指定された条件でファイル選択ダイアログを表示し、選択されたパスを返します。
    Args:
        title: str - ダイアログのタイトル。
        filetypes: tuple - 選択可能なファイル形式のタプル。
        initialdir: Optional[str] - 初期ディレクトリ。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        str - 選択されたファイルのパス。キャンセルされた場合は空文字。
    """
    options = {"title": title, "filetypes": filetypes}
    if initialdir:
        options["initialdir"] = initialdir
    if parent:
        options["parent"] = parent
    
    path = filedialog.askopenfilename(**options)
    return path if path else ""

def ask_open_dir(title: str, initialdir: Optional[str] = None, parent: Optional[tk.Widget] = None) -> str:
    """
    Summary:
        ディレクトリを選択するダイアログを表示します。
    Description:
        ディレクトリ選択ダイアログを表示し、選択されたパスを返します。
    Args:
        title: str - ダイアログのタイトル。
        initialdir: Optional[str] - 初期ディレクトリ。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        str - 選択されたディレクトリのパス。キャンセルされた場合は空文字。
    """
    options = {"title": title}
    if initialdir:
        options["initialdir"] = initialdir
    if parent:
        options["parent"] = parent
        
    path = filedialog.askdirectory(**options)
    return path if path else ""

def ask_save_as_file(title: str, filetypes: tuple, initialdir: Optional[str] = None, defaultextension: str = "", parent: Optional[tk.Widget] = None) -> str:
    """
    Summary:
        名前を付けて保存するファイルダイアログを表示します。
    Description:
        保存先ファイルのパスを選択するダイアログを表示し、選択されたパスを返します。
    Args:
        title: str - ダイアログのタイトル。
        filetypes: tuple - 選択可能なファイル形式のタプル。
        initialdir: Optional[str] - 初期ディレクトリ。
        defaultextension: str - デフォルトの拡張子（例: ".json"）。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        str - 選択されたファイルのパス。キャンセルされた場合は空文字。
    """
    options = {"title": title, "filetypes": filetypes, "defaultextension": defaultextension}
    if initialdir:
        options["initialdir"] = initialdir
    if parent:
        options["parent"] = parent
    
    path = filedialog.asksaveasfilename(**options)
    return path if path else ""

def ask_ok_cancel(title: str, message: str, parent: Optional[tk.Widget] = None) -> bool:
    """
    Summary:
        「OK/キャンセル」を確認するダイアログを表示します。
    Description:
        ユーザーにOK/Cancelの選択を促します。処理を続行してよいかの確認等に使用します。
    Args:
        title: str - ダイアログのタイトル。
        message: str - 表示するメッセージ。
        parent: Optional[tk.Widget] - 親ウィンドウ。指定すると中央に表示されます。
    Returns:
        bool - 「OK」を選択した場合は True、それ以外は False。
    """
    if parent:
        dlg = FwsCustomDialog(parent, title, message, "ok_cancel")
        return dlg.result
    else:
        return messagebox.askokcancel(title, message)

