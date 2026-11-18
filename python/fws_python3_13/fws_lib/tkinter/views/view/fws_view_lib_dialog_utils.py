"""
Summary:
    fws_lib Tkinter アプリ用のダイアログユーティリティモジュール。
Description:
    tkinter.messagebox や filedialog のよく使う処理をラップして提供します。
Attachment:
    なし
"""
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from typing import Optional


def _get_icon_image(dialog_type: str) -> Optional[tk.PhotoImage]:
    """
    Summary:
        ダイアログ種別に応じたアイコン画像を読み込んで返します。
    Description:
        dialog_type に対応するアイコン画像（tk.PhotoImage）を読み込んで返します。
        ファイルが存在しない場合や画像の読み込みに失敗した場合は None を返します。
    Args:
        dialog_type: str - ダイアログ種別（"info", "error", "warning", "question", "yes_no", "ok_cancel" 等）。
    Returns:
        Optional[tk.PhotoImage] - アイコン画像オブジェクト。取得できない場合は None。
    """
    icons_dir: Path = Path(__file__).resolve().parent / "icons"
    icon_map: dict[str, str] = {
        "info": "info.png",
        "error": "error.png",
        "warning": "warning.png",
        "question": "question.png",
        "yes_no": "question.png",
        "ok_cancel": "question.png",
    }
    icon_filename: str = icon_map.get(dialog_type, "info.png")
    icon_path: Path = icons_dir / icon_filename

    if icon_path.exists():
        try:
            return tk.PhotoImage(file=str(icon_path))
        except Exception:
            return None
    return None


class FwsViewLibCustomDialog(tk.Toplevel):
    """
    Summary:
        親ウィンドウの中央に表示するためのカスタムダイアログクラス。
    Description:
        親ウィンドウの中央にモーダルダイアログを表示し、メッセージと確認ボタンを提供します。
    """

    #region Constructor
    def __init__(self, parent: tk.Widget, title: str, message: str, dialog_type: str = "info") -> None:
        """
        Summary:
            カスタムダイアログの初期化を行います。
        Description:
            親ウィンドウの中央にモーダルダイアログを構築・表示し、ユーザーの応答を待ち受けます。
        Args:
            parent: tk.Widget - 親ウィンドウ。
            title: str - ダイアログのタイトル。
            message: str - 表示するメッセージ。
            dialog_type: str - ダイアログ種別（"info", "error", "warning", "question", "yes_no", "ok_cancel" 等）。デフォルトは "info"。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent)
        self.title(title)
        self.result: bool = False
        """bool - ダイアログの押下結果（はい/OKならTrue、いいえ/キャンセルならFalse）"""

        self.transient(parent)
        self.grab_set()

        # UI構築
        frm: ttk.Frame = ttk.Frame(self, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)

        frm_top: ttk.Frame = ttk.Frame(frm)
        frm_top.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # 画像ファイルが存在すれば読み込んで表示
        self.icon_image: Optional[tk.PhotoImage] = _get_icon_image(dialog_type)
        """Optional[tk.PhotoImage] - ダイアログアイコン画像オブジェクト"""
        lbl_icon: ttk.Label
        if self.icon_image is not None:
            lbl_icon = ttk.Label(frm_top, image=self.icon_image)
        else:
            lbl_icon = ttk.Label(frm_top)

        lbl_icon.pack(side=tk.LEFT, padx=(0, 15))

        lbl_text: ttk.Label = ttk.Label(frm_top, text=message, justify=tk.LEFT)
        lbl_text.pack(side=tk.LEFT)

        frm_btn: ttk.Frame = ttk.Frame(frm)
        frm_btn.pack()

        if dialog_type == "yes_no":
            btn_yes: ttk.Button = ttk.Button(frm_btn, text="はい", width=10, command=self._on_yes)
            btn_yes.pack(side=tk.LEFT, padx=5)
            btn_no: ttk.Button = ttk.Button(frm_btn, text="いいえ", width=10, command=self._on_no)
            btn_no.pack(side=tk.LEFT, padx=5)
        elif dialog_type == "ok_cancel":
            btn_ok: ttk.Button = ttk.Button(frm_btn, text="OK", width=10, command=self._on_yes)
            btn_ok.pack(side=tk.LEFT, padx=5)
            btn_cancel: ttk.Button = ttk.Button(frm_btn, text="キャンセル", width=10, command=self._on_no)
            btn_cancel.pack(side=tk.LEFT, padx=5)
        else:
            btn_ok: ttk.Button = ttk.Button(frm_btn, text="OK", width=10, command=self._on_yes)
            btn_ok.pack()

        self.update_idletasks()

        w: int = self.winfo_width()
        h: int = self.winfo_height()
        px: int = parent.winfo_rootx()
        py: int = parent.winfo_rooty()
        pw: int = parent.winfo_width()
        ph: int = parent.winfo_height()

        x: int = px + (pw - w) // 2
        y: int = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self._on_no)
        self.wait_window(self)
    #endregion

    #region Private Methods
    def _on_yes(self) -> None:
        """
        Summary:
            肯定応答（はい / OK）時の内部処理を行います。
        Description:
            ダイアログ結果を True に設定し、ダイアログウィンドウを破棄します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.result = True
        self.destroy()

    def _on_no(self) -> None:
        """
        Summary:
            否定応答（いいえ / キャンセル / 閉じる）時の内部処理を行います。
        Description:
            ダイアログ結果を False に設定し、ダイアログウィンドウを破棄します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.result = False
        self.destroy()
    #endregion


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
        FwsViewLibCustomDialog(parent, title, message, "info")
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
        FwsViewLibCustomDialog(parent, title, message, "error")
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
        FwsViewLibCustomDialog(parent, title, message, "warning")
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
        dlg = FwsViewLibCustomDialog(parent, title, message, "yes_no")
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
        dlg = FwsViewLibCustomDialog(parent, title, message, "ok_cancel")
        return dlg.result
    else:
        return messagebox.askokcancel(title, message)
