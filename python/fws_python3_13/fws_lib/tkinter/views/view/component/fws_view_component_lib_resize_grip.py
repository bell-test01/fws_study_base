"""
Summary:
    テキストウィジェット等用リサイズグリップコンポーネントモジュール。
Description:
    マウスドラッグ操作により対象ウィジェットの高さを動的に伸縮させるリサイズグリップフレームを提供します。
Attachment:
    なし
"""
#region imports
import tkinter as tk
from tkinter import ttk
from typing import Any
#endregion

#region classes
class FwsViewComponentLibResizeGrip(ttk.Frame):
    """
    Summary:
        リサイズグリップクラス。
    Description:
        ttk.Frame を継承し、水平セパレータとリサイズカーソルを表示して、
        ドラッグ操作に応じて対象ウィジェットの行数（height）を自律的に増減制御します。
    """

    #region Constructor
    def __init__(
        self,
        parent: Any,
        target_widget: Any,
        min_lines: int = 1,
        max_lines: int = 40,
        line_height_px: int = 18,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            対象ウィジェットおよび伸縮制約値を保持し、セパレータの配置とマウスドラッグイベントのバインドを行います。
        Args:
            parent: Any - 親ウィジェット。
            target_widget: Any - 高さリサイズ対象のウィジェット（configure(height=...) および cget('height') をサポートするオブジェクト）。
            min_lines: int - 最小許容行数（デフォルト 1）。
            max_lines: int - 最大許容行数（デフォルト 40）。
            line_height_px: int - 1行あたりのピクセル移動量（デフォルト 18）。
            **kwargs: Any - ttk.Frame に渡す追加オプション。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent, height=7, cursor="sb_v_double_arrow", **kwargs)
        self.sep_grip: ttk.Separator
        """ttk.Separator - リサイズグリップ表示用水平セパレータ"""
        self._target_widget: Any = target_widget
        """Any - リサイズ対象ウィジェット"""
        self._min_lines: int = min_lines
        """int - 最小行数"""
        self._max_lines: int = max_lines
        """int - 最大行数"""
        self._line_height_px: int = line_height_px
        """int - 1行のピクセル高"""
        self._drag_start_y: int = 0
        """int - ドラッグ開始時Y座標"""
        self._drag_start_height: int = 1
        """int - ドラッグ開始時の行数"""

        self._init_layout()
        self._bind_events()

    def _init_layout(self) -> None:
        """
        Summary:
            レイアウト初期化を行います。
        Description:
            内部に水平セパレータを全幅配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.sep_grip = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.sep_grip.pack(fill=tk.X, pady=2)

    def _bind_events(self) -> None:
        """
        Summary:
            イベントバインドを行います。
        Description:
            自身およびセパレータに対してマウス左ボタンドラッグイベントを設定します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        self.sep_grip.bind("<ButtonPress-1>", self._on_press)
        self.sep_grip.bind("<B1-Motion>", self._on_drag)
    #endregion

    #region Private Methods
    def _on_press(self, event: Any) -> None:
        """
        Summary:
            グリップ押下時のイベント処理を行います。
        Description:
            ドラッグ開始時のマウスY座標と対象ウィジェットの現在の高さを記録します。
        Args:
            event: Any - マウスイベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        self._drag_start_y = event.y_root
        try:
            self._drag_start_height = int(self._target_widget.cget("height"))
        except (ValueError, TypeError, tk.TclError):
            self._drag_start_height = self._min_lines

    def _on_drag(self, event: Any) -> None:
        """
        Summary:
            グリップドラッグ時のイベント処理を行います。
        Description:
            ドラッグ移動量（dy // line_height_px）に応じて対象ウィジェットの行数を動的に変更します。
        Args:
            event: Any - マウスイベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        dy: int = event.y_root - self._drag_start_y
        delta_lines: int = dy // self._line_height_px
        new_height: int = max(self._min_lines, min(self._max_lines, self._drag_start_height + delta_lines))
        self._target_widget.configure(height=new_height)
    #endregion
#endregion
