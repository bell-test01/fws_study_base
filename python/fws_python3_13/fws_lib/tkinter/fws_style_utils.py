"""
Summary:
    Tkinterのスタイル・テーマ操作に関するユーティリティモジュール。
Description:
    フォント設定やカラーテーマなど、
    アプリ全体の外観を制御する共通操作を提供します。
Attachment:
    なし
"""

import tkinter as tk
from tkinter import ttk

def apply_default_font(font_name: str = "Meiryo UI", font_size: int = 9) -> None:
    """
    Summary:
        アプリケーション全体のデフォルトフォントを設定します。
    Description:
        ttk.Styleを使用して、すべてのttkウィジェットの標準フォントを一括で変更します。
        ルートウィンドウ作成後に呼び出してください。
    Args:
        font_name: str - フォント名。デフォルトは "Meiryo UI"。
        font_size: int - フォントサイズ。デフォルトは 9。
    Returns:
        None - 戻り値なし。
    """
    style = ttk.Style()
    default_font = (font_name, font_size)
    
    # 標準設定として適用
    style.configure(".", font=default_font)

def apply_theme(theme_name: str) -> bool:
    """
    Summary:
        ttkのテーマを変更します。
    Description:
        利用可能なテーマ（"clam", "alt", "default", "classic"など）をアプリ全体に適用します。
    Args:
        theme_name: str - 適用するテーマ名。
    Returns:
        bool - テーマの適用に成功した場合は True、テーマが存在しない場合は False。
    """
    style = ttk.Style()
    if theme_name in style.theme_names():
        style.theme_use(theme_name)
        return True
    return False

