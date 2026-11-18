"""
Summary:
    アコーディオンブロックコンポーネントモジュール。
Description:
    開閉トグルボタンとタイトルラベルを備えたヘッダー、および折りたたみ可能なコンテンツコンテナを内包する
    アコーディオンブロックフレームを提供します。
Attachment:
    なし
"""
#region imports
import tkinter as tk
from tkinter import ttk
from typing import Any
#endregion

#region classes
class FwsViewComponentLibAccordionBlock(ttk.Frame):
    """
    Summary:
        アコーディオンブロッククラス。
    Description:
        ttk.Frame を継承し、ヘッダー（タイトルラベル、トグルボタン）とコンテンツコンテナを配置して、
        トグルボタン押下によるコンテンツ領域の表示・非表示を自律制御します。
    """

    #region Constructor
    def __init__(
        self,
        parent: Any,
        title: str = "",
        is_expanded: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            境界線および枠線スタイルを設定し、ヘッダーフレーム（トグルボタン、タイトル）とコンテンツ用コンテナを構築します。
        Args:
            parent: Any - 親ウィジェット。
            title: str - ヘッダーに表示するタイトル文字列（デフォルト ""）。
            is_expanded: bool - 初期展開状態フラグ（デフォルト True）。
            **kwargs: Any - ttk.Frame に渡す追加オプション。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent, relief=tk.SOLID, borderwidth=1, **kwargs)
        self.frm_header: ttk.Frame
        """ttk.Frame - ヘッダーフレーム"""
        self.frm_header_actions: ttk.Frame
        """ttk.Frame - ヘッダー右端アクションウィジェット配置用フレーム"""
        self.btn_toggle: ttk.Button
        """ttk.Button - 開閉トグルボタン"""
        self.lbl_title: ttk.Label
        """ttk.Label - ヘッダータイトルラベル"""
        self.container: ttk.Frame
        """ttk.Frame - 外部ウィジェット配置用コンテンツコンテナ"""
        self.is_expanded: bool = is_expanded
        """bool - コンテンツコンテナの展開状態フラグ"""

        self._init_layout(title)

    def _init_layout(self, title: str) -> None:
        """
        Summary:
            レイアウト初期化を行います。
        Description:
            ヘッダーフレーム（トグルボタン、タイトルラベル、右端アクション領域）およびコンテンツコンテナを配置します。
        Args:
            title: str - 表示するタイトル文字列。
        Returns:
            None - 戻り値なし。
        """
        self.frm_header = ttk.Frame(self)
        self.frm_header.pack(side=tk.TOP, fill=tk.X, padx=3, pady=3)

        self.btn_toggle = ttk.Button(
            self.frm_header,
            text="▼" if self.is_expanded else "▶",
            width=3,
            command=self.toggle,
        )
        self.btn_toggle.pack(side=tk.LEFT)

        self.lbl_title = ttk.Label(self.frm_header, text=title)
        self.lbl_title.pack(side=tk.LEFT, padx=5)

        self.frm_header_actions = ttk.Frame(self.frm_header)
        self.frm_header_actions.pack(side=tk.RIGHT)

        self.container = ttk.Frame(self)
        if self.is_expanded:
            self.container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
    #endregion

    #region Public Methods
    def toggle(self) -> None:
        """
        Summary:
            コンテンツコンテナの開閉（トグル）を行います。
        Description:
            現在の展開状態を反転し、コンテナの pack / pack_forget とトグルボタン表記（▼/▶）を自律的に切り替えます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        if self.is_expanded:
            self.container.pack_forget()
            self.btn_toggle.configure(text="▶")
            self.is_expanded = False
        else:
            self.container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
            self.btn_toggle.configure(text="▼")
            self.is_expanded = True
    #endregion
#endregion
