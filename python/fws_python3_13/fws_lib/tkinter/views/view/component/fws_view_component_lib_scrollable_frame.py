"""
Summary:
    スクロール可能フレームコンポーネントモジュール。
Description:
    内部に Canvas と縦スクロールバーを内包し、子要素のサイズ変化に応じて
    スクロール領域を自動追従するスクロール可能フレームを提供します。
Attachment:
    なし
"""
#region imports
import tkinter as tk
from tkinter import ttk
from typing import Any

from fws_lib.tkinter.util import fws_util_lib_widget
#endregion

#region classes
class FwsViewComponentLibScrollableFrame(ttk.Frame):
    """
    Summary:
        スクロール可能フレームクラス。
    Description:
        ttk.Frame を継承し、Canvas と垂直スクロールバーを grid 配置して、
        コンテンツフレームの動的サイズ変更や親幅レスポンシブ追従、マウスホイール連動スクロールを自律制御します。
    """

    #region Constructor
    def __init__(self, parent: Any, **kwargs: Any) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            Canvasおよび垂直スクロールバーを初期化し、内部コンテンツフレームの生成とリサイズイベントのバインドを行います。
        Args:
            parent: Any - 親ウィジェット。
            **kwargs: Any - ttk.Frame に渡す追加オプション。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent, **kwargs)
        self.content_frame: ttk.Frame
        """ttk.Frame - 外部ウィジェット配置用コンテンツフレーム"""
        self._cvs_scroll: tk.Canvas
        """tk.Canvas - 内部スクロールキャンバス"""
        self._scb_v: ttk.Scrollbar
        """ttk.Scrollbar - 垂直スクロールバー"""
        self._cvs_window_id: int
        """int - キャンバス内に作成したコンテンツフレームのウィンドウID"""

        self._init_layout()
        self._bind_events()

    def _init_layout(self) -> None:
        """
        Summary:
            レイアウト初期化を行います。
        Description:
            grid の伸縮設定を行い、Canvas、垂直スクロールバー、およびコンテンツフレームを配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._scb_v = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._cvs_scroll = tk.Canvas(
            self,
            highlightthickness=0,
            yscrollcommand=self._scb_v.set,
        )
        self._scb_v.configure(command=self._cvs_scroll.yview)

        self._cvs_scroll.grid(row=0, column=0, sticky="nsew")
        self._scb_v.grid(row=0, column=1, sticky="ns")

        self.content_frame = ttk.Frame(self._cvs_scroll)
        self._cvs_window_id = self._cvs_scroll.create_window(
            (0, 0),
            window=self.content_frame,
            anchor=tk.NW,
        )

    def _bind_events(self) -> None:
        """
        Summary:
            イベントバインドを行います。
        Description:
            コンテンツフレームの <Configure>・<Unmap> イベント、Canvasの <Configure>・<Expose> イベント、
            ならびにマウスホイールスクロールチェーンを設定します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.content_frame.bind("<Configure>", self._on_content_configure)
        self.content_frame.bind("<Unmap>", self._on_content_configure)
        self._cvs_scroll.bind("<Configure>", self._on_canvas_configure)
        self._cvs_scroll.bind("<Expose>", self._on_content_configure)
        fws_util_lib_widget.enable_mousewheel_scroll_chain(self)
    #endregion

    #region Public Methods
    def yview(self, *args: Any) -> Any:
        """
        Summary:
            垂直スクロールバー設定または位置取得を行います。
        Description:
            内部の Canvas.yview メソッドに処理を委譲します。
        Args:
            *args: Any - 可変長引数。
        Returns:
            Any - スクロール位置情報またはNone。
        """
        return self._cvs_scroll.yview(*args)

    def yview_moveto(self, fraction: float) -> None:
        """
        Summary:
            キャンバスの垂直スクロール位置を移動します。
        Description:
            内部の Canvas.yview_moveto メソッドに処理を委譲します。
        Args:
            fraction: float - 移動先位置（0.0〜1.0）。
        Returns:
            None - 戻り値なし。
        """
        self._cvs_scroll.yview_moveto(fraction)
    #endregion

    #region Private Methods
    def _on_content_configure(self, event: Any) -> None:
        """
        Summary:
            コンテンツフレームのリサイズおよび状態変化イベント処理を行います。
        Description:
            子ウィジェット追加・折りたたみ等によるコンテンツサイズや表示状態の変化に応じて、
            Canvasのスクロール領域（scrollregion）および表示位置を同期します。
        Args:
            event: Any - イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        self._sync_scrollregion()

    def _on_canvas_configure(self, event: Any) -> None:
        """
        Summary:
            Canvasのリサイズイベント処理を行います。
        Description:
            Canvasの横幅変更に追従してコンテンツフレームの幅を更新し、スクロール領域を同期します。
            縦幅は内部ウィジェットの自動計算（シュリンクラップ）に委ねるため明示指定しません。
        Args:
            event: Any - イベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        self._cvs_scroll.itemconfig(
            self._cvs_window_id,
            width=event.width,
        )
        self._sync_scrollregion()

    def _sync_scrollregion(self) -> None:
        """
        Summary:
            Canvasのスクロール領域と表示位置を同期します。
        Description:
            Canvas全体の境界ボックス（bbox）と現在の scrollregion を比較し、
            差分がある場合のみ scrollregion を更新します。
            また、コンテンツ高さがCanvas高さ以下に収まっている状態で表示位置が先頭からずれている場合は先頭へ補正します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        bbox: tuple[int, int, int, int] | None = self._cvs_scroll.bbox("all")
        if bbox is None:
            return
        target_scrollregion: str = f"{bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}"
        if str(self._cvs_scroll.cget("scrollregion")) != target_scrollregion:
            self._cvs_scroll.configure(scrollregion=bbox)
        canvas_h: int = self._cvs_scroll.winfo_height()
        if canvas_h > 1 and (bbox[3] - bbox[1]) <= canvas_h and self._cvs_scroll.canvasy(0) != 0.0:
            self._cvs_scroll.yview_moveto(0.0)
    #endregion
#endregion
