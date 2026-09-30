"""
Summary:
    Tkinterのウィンドウ操作に関するユーティリティモジュール。
Description:
    ウィンドウの最前面表示、透過度設定、中央配置など、
    Tkinterのウィンドウ(TkまたはToplevel)に対する共通操作を提供します。
Attachment:
    なし
"""

import tkinter as tk
from typing import Union

def set_window_topmost(window: Union[tk.Tk, tk.Toplevel], is_topmost: bool) -> None:
    """
    Summary:
        ウィンドウの最前面表示設定を切り替えます。
    Description:
        指定されたウィンドウの最前面表示(topmost)属性を、is_topmostの値に応じて設定します。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
        is_topmost: bool - Trueの場合は最前面に固定し、Falseの場合は解除します。
    Returns:
        None - 戻り値なし。
    """
    window.attributes("-topmost", is_topmost)

def set_window_alpha(window: Union[tk.Tk, tk.Toplevel], alpha: float) -> None:
    """
    Summary:
        ウィンドウの透過度を設定します。
    Description:
        指定されたウィンドウの透過度(alpha)属性を設定します。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
        alpha: float - 透過度 (0.0: 完全に透明 ～ 1.0: 完全に不透明)。
    Returns:
        None - 戻り値なし。
    """
    window.attributes("-alpha", alpha)

def center_window(window: Union[tk.Tk, tk.Toplevel], width: int, height: int) -> None:
    """
    Summary:
        ウィンドウを画面の中央に配置します。
    Description:
        指定された幅と高さで、ウィンドウをディスプレイの水平・垂直方向の中央に配置します。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
        width: int - ウィンドウの幅 (ピクセル)。
        height: int - ウィンドウの高さ (ピクセル)。
    Returns:
        None - 戻り値なし。
    """
    # 画面の幅と高さを取得
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 中央に配置するためのX, Y座標を計算
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)

    # ジオメトリを設定
    window.geometry(f"{width}x{height}+{x}+{y}")

def maximize_window(window: Union[tk.Tk, tk.Toplevel]) -> None:
    """
    Summary:
        ウィンドウを最大化します。
    Description:
        ウィンドウをディスプレイの最大サイズに設定します（ズーム）。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
    Returns:
        None - 戻り値なし。
    """
    window.state("zoomed")

def bring_to_front(window: Union[tk.Tk, tk.Toplevel]) -> None:
    """
    Summary:
        ウィンドウを最前面にアクティブ化します。
    Description:
        他のウィンドウの後ろに隠れているウィンドウを前に出し、フォーカスを当てます。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
    Returns:
        None - 戻り値なし。
    """
    window.lift()
    window.focus_force()

def set_min_size(window: Union[tk.Tk, tk.Toplevel], width: int, height: int) -> None:
    """
    Summary:
        ウィンドウの最小サイズを設定します。
    Description:
        ウィンドウがこれ以上小さくならないように最小の幅と高さを制限します。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
        width: int - 最小の幅 (ピクセル)。
        height: int - 最小の高さ (ピクセル)。
    Returns:
        None - 戻り値なし。
    """
    window.minsize(width, height)

def toggle_fullscreen(window: Union[tk.Tk, tk.Toplevel], is_fullscreen: bool) -> None:
    """
    Summary:
        ウィンドウのフルスクリーン表示を切り替えます。
    Description:
        is_fullscreen が True の場合はフルスクリーン化し、False の場合は解除します。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
        is_fullscreen: bool - フルスクリーンにする場合は True。
    Returns:
        None - 戻り値なし。
    """
    window.attributes("-fullscreen", is_fullscreen)

def bind_escape_to_close(window: Union[tk.Tk, tk.Toplevel]) -> None:
    """
    Summary:
        Escapeキーでウィンドウを閉じるイベントをバインドします。
    Description:
        ウィンドウ上でEscapeキーが押下された際に、ウィンドウを破棄(destroy)するように設定します。
    Args:
        window: Union[tk.Tk, tk.Toplevel] - 対象のウィンドウオブジェクト。
    Returns:
        None - 戻り値なし。
    """
    window.bind("<Escape>", lambda e: window.destroy())

