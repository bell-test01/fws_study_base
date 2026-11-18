"""
Summary:
    Tkinterのウィジェット操作に関するユーティリティモジュール。
Description:
    テキストエリアのスクロール、入力補助など、
    各ウィジェットに対する共通操作を提供します。
Attachment:
    なし
"""

import tkinter as tk
from tkinter import ttk
from typing import Any, Optional, Union


def scroll_to_bottom(text_widget: tk.Text) -> None:
    """
    Summary:
        テキストウィジェットを末尾までスクロールします。
    Description:
        チャットやログ表示など、最新の行を表示させたい場合に使用します。
    Args:
        text_widget: tk.Text - 対象のテキストウィジェット。
    Returns:
        None - 戻り値なし。
    """
    text_widget.see(tk.END)

def insert_text_at_cursor(text_widget: tk.Text, insert_text: str) -> None:
    """
    Summary:
        テキストウィジェットの現在のカーソル位置に文字列を挿入します。
    Description:
        記号や定型文などをカーソル位置に入力する際に使用します。
    Args:
        text_widget: tk.Text - 対象のテキストウィジェット。
        insert_text: str - 挿入する文字列。
    Returns:
        None - 戻り値なし。
    """
    text_widget.insert(tk.INSERT, insert_text)

def clear_text_widget(text_widget: tk.Text) -> None:
    """
    Summary:
        テキストウィジェットの内容をすべて消去します。
    Description:
        テキストウィジェット内の文字列をクリアします。
    Args:
        text_widget: tk.Text - 対象のテキストウィジェット。
    Returns:
        None - 戻り値なし。
    """
    text_widget.delete("1.0", tk.END)

def get_all_text(text_widget: tk.Text) -> str:
    """
    Summary:
        テキストウィジェット内のすべての文字列を取得します。
    Description:
        テキストウィジェットに入力されている全テキストを取得して返します。末尾の改行は除外されます。
    Args:
        text_widget: tk.Text - 対象のテキストウィジェット。
    Returns:
        str - 取得した文字列。
    """
    return text_widget.get("1.0", "end-1c")

def set_state(widget: Union[tk.Widget, ttk.Widget], is_enabled: bool) -> None:
    """
    Summary:
        ウィジェットの活性/非活性状態を切り替えます。
    Description:
        is_enabled が True の場合は 'normal'、False の場合は 'disabled' に設定します。
    Args:
        widget: Union[tk.Widget, ttk.Widget] - 対象のウィジェット。
        is_enabled: bool - 活性化する場合は True。
    Returns:
        None - 戻り値なし。
    """
    state = "normal" if is_enabled else "disabled"
    widget["state"] = state

def clear_treeview(treeview: ttk.Treeview) -> None:
    """
    Summary:
        Treeview の全行データを消去します。
    Description:
        Treeview に登録されているすべての子アイテムを削除します。
    Args:
        treeview: ttk.Treeview - 対象の Treeview ウィジェット。
    Returns:
        None - 戻り値なし。
    """
    treeview.delete(*treeview.get_children())

def update_combobox(combobox: ttk.Combobox, values: list) -> None:
    """
    Summary:
        Combobox の選択肢を更新します。
    Description:
        Combobox の既存の値をクリアし、新しいリストをセットします。
    Args:
        combobox: ttk.Combobox - 対象の Combobox ウィジェット。
        values: list - セットする新しい選択肢のリスト。
    Returns:
        None - 戻り値なし。
    """
    combobox.set("")
    combobox["values"] = values

def get_treeview_selected_items(treeview: ttk.Treeview) -> list[dict]:
    """
    Summary:
        Treeview で現在選択されている行のデータをすべて取得します。
    Description:
        選択されている各行の item(iid) の戻り値（辞書）をリストにまとめて返します。
    Args:
        treeview: ttk.Treeview - 対象の Treeview ウィジェット。
    Returns:
        list[dict] - 選択行のデータ辞書のリスト。
    """
    selected_iids = treeview.selection()
    return [treeview.item(iid) for iid in selected_iids]

def insert_treeview_items(treeview: ttk.Treeview, items_list: list[list]) -> None:
    """
    Summary:
        複数のデータを一括で Treeview に挿入します。
    Description:
        提供された値のリストを Treeview の末尾に追加します。
    Args:
        treeview: ttk.Treeview - 対象の Treeview ウィジェット。
        items_list: list[list] - 挿入する行データのリスト（各行の表示値のリスト）。
    Returns:
        None - 戻り値なし。
    """
    for values in items_list:
        treeview.insert("", tk.END, values=values)

def has_focus(widget: Union[tk.Widget, ttk.Widget]) -> bool:
    """
    Summary:
        ウィジェットにフォーカスが当たっているかを判定します。
    Description:
        対象のウィジェットが現在フォーカスを持っている場合に True を返します。
    Args:
        widget: Union[tk.Widget, ttk.Widget] - 対象のウィジェット。
    Returns:
        bool - フォーカスがある場合は True。
    """
    return widget.focus_displayof() == widget


def enable_mousewheel_scroll_chain(target_window: tk.Misc) -> None:
    """
    Summary:
        指定ウィンドウ全体に、ホバー要素優先および祖先スクロールコンテナ自動検出のマウスホイール連動をバインドします。
    Description:
        マウスポインタ直下のウィジェットから親方向（祖先）へツリーを探索し、
        Textウィジェットの端到達時伝播および直近の親Canvasの自動スクロールを実行します。
    Args:
        target_window: tk.Misc - イベントをバインドする対象ウィンドウまたはウィジェット。
    Returns:
        None - 戻り値なし。
    """
    def _find_ancestor_text(widget: Any) -> Optional[tk.Text]:
        curr: Any = widget
        while curr is not None:
            if isinstance(curr, tk.Text):
                return curr
            curr = getattr(curr, "master", None)
        return None

    def _find_ancestor_canvas(widget: Any) -> Optional[tk.Canvas]:
        curr: Any = widget
        while curr is not None:
            if isinstance(curr, tk.Canvas):
                return curr
            curr = getattr(curr, "master", None)
        return None

    def _on_mousewheel(event: Any) -> Optional[str]:
        if not hasattr(event, "delta") or event.delta == 0:
            return None
        scroll_units: int = int(-1 * (event.delta / 120))
        target_widget: Any = None
        try:
            target_widget = event.widget.winfo_containing(event.x_root, event.y_root)
        except Exception:
            target_widget = getattr(event, "widget", None)
        if target_widget is None:
            return None

        # 優先度1: target_widget またはその祖先が tk.Text の場合
        text_widget = _find_ancestor_text(target_widget)
        if text_widget is not None:
            try:
                top, bottom = text_widget.yview()
                if scroll_units < 0 and top <= 0.001:
                    # 上端到達: 親方向のCanvasへバブリング伝播
                    parent_canvas = _find_ancestor_canvas(getattr(text_widget, "master", None))
                    if parent_canvas is not None:
                        parent_canvas.yview_scroll(scroll_units, "units")
                elif scroll_units > 0 and bottom >= 0.999:
                    # 下端到達: 親方向のCanvasへバブリング伝播
                    parent_canvas = _find_ancestor_canvas(getattr(text_widget, "master", None))
                    if parent_canvas is not None:
                        parent_canvas.yview_scroll(scroll_units, "units")
                else:
                    text_widget.yview_scroll(scroll_units, "units")
                return "break"
            except Exception:
                pass

        # 優先度2: target_widget の祖先にある tk.Canvas を自動探索
        canvas_widget = _find_ancestor_canvas(target_widget)
        if canvas_widget is not None:
            try:
                canvas_widget.yview_scroll(scroll_units, "units")
                return "break"
            except Exception:
                pass

        return None

    target_window.bind_all("<MouseWheel>", _on_mousewheel)



