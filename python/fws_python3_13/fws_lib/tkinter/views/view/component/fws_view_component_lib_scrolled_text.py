"""
Summary:
    スクロール付きテキストウィジェットコンポーネントモジュール。
Description:
    内部に tk.Text と縦・横スクロールバーを grid で交差配置し、
    主要なテキスト操作メソッドを委譲する複合テキストコンポーネントを提供します。
Attachment:
    なし
"""
#region imports
import tkinter as tk
from tkinter import ttk
from typing import Any
#endregion

#region classes
class FwsViewComponentLibScrolledText(ttk.Frame):
    """
    Summary:
        スクロール付きテキストウィジェットクラス。
    Description:
        ttk.Frame を継承し、内部に tk.Text と縦・横スクロールバーを OS標準の交差レイアウトで配置します。
        get, insert, delete, configure, cget, focus_set 等のメソッドを内部 Text ウィジェットへ委譲します。
    """

    #region Constructor
    def __init__(self, parent: Any, **kwargs: Any) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            undo や wrap などの Text オプションを抽出し、内部 Text ウィジェットおよびスクロールバーを構築・連携配置します。
        Args:
            parent: Any - 親ウィジェット。
            **kwargs: Any - tk.Text に渡す追加オプション（undo, wrap, font, height 等）。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent)
        self.text_widget: tk.Text
        """tk.Text - 内部テキストウィジェット本体"""
        self.scb_v: ttk.Scrollbar
        """ttk.Scrollbar - 垂直スクロールバー"""
        self.scb_h: ttk.Scrollbar
        """ttk.Scrollbar - 水平スクロールバー"""

        self._init_layout(**kwargs)

    def _init_layout(self, **kwargs: Any) -> None:
        """
        Summary:
            レイアウト初期化を行います。
        Description:
            内部 Text ウィジェットと縦横スクロールバーを生成し、交差 grid 配置およびスクロール連動を設定します。
        Args:
            **kwargs: Any - tk.Text 生成オプション。
        Returns:
            None - 戻り値なし。
        """
        undo: bool = kwargs.pop("undo", True)
        wrap: str = kwargs.pop("wrap", tk.NONE)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.text_widget = tk.Text(self, undo=undo, wrap=wrap, **kwargs)
        self.scb_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scb_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        self.text_widget.configure(yscrollcommand=self.scb_v.set, xscrollcommand=self.scb_h.set)

        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.scb_v.grid(row=0, column=1, sticky="ns")
        self.scb_h.grid(row=1, column=0, sticky="ew")
    #endregion

    #region Public Methods
    def get(self, *args: Any, **kwargs: Any) -> Any:
        """
        Summary:
            テキストウィジェットから文字列を取得します。
        Description:
            内部の Text.get メソッドに処理を委譲します。
        Args:
            *args: Any - 可変長引数（例: "1.0", tk.END 等）。
            **kwargs: Any - キーワード引数。
        Returns:
            Any - 取得したテキスト。
        """
        return self.text_widget.get(*args, **kwargs)

    def insert(self, *args: Any, **kwargs: Any) -> Any:
        """
        Summary:
            テキストウィジェットに文字列を挿入します。
        Description:
            内部の Text.insert メソッドに処理を委譲します。
        Args:
            *args: Any - 可変長引数（例: tk.INSERT, "文字列" 等）。
            **kwargs: Any - キーワード引数。
        Returns:
            Any - 戻り値。
        """
        return self.text_widget.insert(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Any:
        """
        Summary:
            テキストウィジェットから文字列を削除します。
        Description:
            内部の Text.delete メソッドに処理を委譲します。
        Args:
            *args: Any - 可変長引数（例: "1.0", tk.END 等）。
            **kwargs: Any - キーワード引数。
        Returns:
            Any - 戻り値。
        """
        return self.text_widget.delete(*args, **kwargs)

    def configure(self, cnf: Any = None, **kwargs: Any) -> Any:
        """
        Summary:
            テキストウィジェットの設定属性を変更または取得します。
        Description:
            内部の Text.configure メソッドに処理を委譲します。
        Args:
            cnf: Any - 設定辞書（省略可）。
            **kwargs: Any - 設定キーワード引数。
        Returns:
            Any - 設定情報またはNone。
        """
        return self.text_widget.configure(cnf, **kwargs)

    config = configure

    def cget(self, key: str) -> Any:
        """
        Summary:
            テキストウィジェットの設定属性値を取得します。
        Description:
            内部の Text.cget メソッドに処理を委譲します。
        Args:
            key: str - 設定キー名。
        Returns:
            Any - 設定値。
        """
        return self.text_widget.cget(key)

    def focus_set(self) -> None:
        """
        Summary:
            テキストウィジェットにフォーカスを設定します。
        Description:
            内部の Text.focus_set メソッドに処理を委譲します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.text_widget.focus_set()

    def see(self, index: Any) -> None:
        """
        Summary:
            指定インデックスのテキストを表示領域内にスクロールします。
        Description:
            内部の Text.see メソッドに処理を委譲します。
        Args:
            index: Any - 表示対象の位置。
        Returns:
            None - 戻り値なし。
        """
        self.text_widget.see(index)
    #endregion
#endregion
