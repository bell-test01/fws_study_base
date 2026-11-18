"""
Summary:
    Tkinter の汎用ユーティリティモジュール。
Description:
    ウィンドウジオメトリの保存・復元、Treeview構築などの共通処理を提供します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk
from typing import Tuple

def save_geometry(window: tk.Tk) -> str:
    """
    Summary:
        ウィンドウの現在のジオメトリからサイズ（幅x高さ）を取得し保存します。位置情報は破棄します。
    """
    geom = window.geometry()
    return geom.split('+')[0]

def restore_geometry(window: tk.Tk, geometry_str: str) -> None:
    """
    Summary:
        ウィンドウのサイズ（幅x高さ）を適用して復元します。
    """
    if geometry_str:
        size_only = geometry_str.split('+')[0]
        window.geometry(size_only)

def create_scrollable_treeview(parent: tk.Widget) -> Tuple[ttk.Treeview, ttk.Scrollbar, ttk.Scrollbar]:
    """
    Summary:
        縦横スクロールバー付きの Treeview を構築します。
    Returns:
        Tuple[ttk.Treeview, ttk.Scrollbar, ttk.Scrollbar] - Treeviewと縦・横スクロールバーのタプル
    """
    tree = ttk.Treeview(parent)
    
    vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
    
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    return tree, vsb, hsb
