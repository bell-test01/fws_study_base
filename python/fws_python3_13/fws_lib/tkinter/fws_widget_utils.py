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
from typing import Union


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


