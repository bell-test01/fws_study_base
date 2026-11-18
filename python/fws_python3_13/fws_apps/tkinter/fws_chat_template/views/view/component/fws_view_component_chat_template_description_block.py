"""
Summary:
    Description領域コンポーネントモジュール。
Description:
    チケット詳細テキストエリア、比較・保存ボタン、アコーディオン開閉、
    およびリサイズグリップを一体化した専用コンポーネント FwsViewComponentChatTemplateDescriptionBlock を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

from fws_lib.tkinter.views.view.component import (
    fws_view_component_lib_accordion_block,
    fws_view_component_lib_resize_grip,
    fws_view_component_lib_scrolled_text,
)

from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
#endregion

#region classes
class FwsViewComponentChatTemplateDescriptionBlock(ttk.Frame):
    """
    Summary:
        Description領域コンポーネントクラス。
    Description:
        ttk.Frame を継承し、FwsViewComponentLibAccordionBlock を内包してチケット詳細テキストエリア（FwsViewComponentLibScrolledText）、
        比較・保存ボタンフレーム、および上下リサイズグリップ（FwsViewComponentLibResizeGrip）を一体化してカプセル化します。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        title: str = "Description:",
        height: int = fws_const_chat_template.DEFAULT_DESC_TEXT_HEIGHT,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            親ウィジェット上に基底フレームを初期化し、内部に FwsViewComponentLibAccordionBlock を内包配置した上で、
            テキストエリア、ボタン群、リサイズグリップを生成・配置します。
        Args:
            master: tk.Widget - 親ウィジェット。
            title: str - アコーディオンヘッダーに表示するタイトル（デフォルト "Description:"）。
            height: int - テキストエリアの初期行数（デフォルト DEFAULT_DESC_TEXT_HEIGHT）。
            **kwargs: Any - ttk.Frame に渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master, **kwargs)

        self.blk_accordion: fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock
        """fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock - Descriptionアコーディオンブロック"""
        self.txt_description: fws_view_component_lib_scrolled_text.FwsViewComponentLibScrolledText
        """fws_view_component_lib_scrolled_text.FwsViewComponentLibScrolledText - チケット詳細スクロール付きテキストエリア"""
        self.btn_compare: ttk.Button
        """ttk.Button - 差分比較ボタン"""
        self.btn_save: ttk.Button
        """ttk.Button - 保存ボタン"""
        self.grp_desc: fws_view_component_lib_resize_grip.FwsViewComponentLibResizeGrip
        """fws_view_component_lib_resize_grip.FwsViewComponentLibResizeGrip - Descriptionリサイズグリップ"""
        self._on_save: Callable[[], None]
        """Callable[[], None] - 保存ボタン押下時コールバック"""
        self._on_compare: Callable[[], None]
        """Callable[[], None] - 比較ボタン押下時コールバック"""

        self._init_layout(title, height)

    def _init_layout(self, title: str, height: int) -> None:
        """
        Summary:
            コンポーネントの内部レイアウトを初期化します。
        Description:
            FwsViewComponentLibAccordionBlock を展開状態で配置し、その container 内に FwsViewComponentLibScrolledText、
            ボタンフレーム（比較・保存）、および FwsViewComponentLibResizeGrip を順次配置します。
        Args:
            title: str - アコーディオンヘッダーのタイトル。
            height: int - テキストエリアの初期行数。
        Returns:
            None - 戻り値なし。
        """
        # 1. アコーディオンブロック配置
        self.blk_accordion = fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock(self, title=title, is_expanded=True)
        self.blk_accordion.pack(fill=tk.BOTH, expand=True)

        # 2. コンテナ内に各ウィジェットを順次配置
        # 2-1. スクロール付きテキストエリア
        self.txt_description = fws_view_component_lib_scrolled_text.FwsViewComponentLibScrolledText(
            self.blk_accordion.container,
            height=height,
            wrap=tk.NONE,
        )
        self.txt_description.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 2-2. ボタンフレーム（比較、保存）
        frm_desc_buttons: ttk.Frame = ttk.Frame(self.blk_accordion.container)
        frm_desc_buttons.pack(side=tk.TOP, fill=tk.X, padx=3, pady=(5, 2))
        self.btn_compare = ttk.Button(frm_desc_buttons, text="比較", width=12, command=self._on_compare_click)
        self.btn_compare.pack(side=tk.LEFT, padx=(0, 5))
        self.btn_save = ttk.Button(frm_desc_buttons, text="保存", width=12, command=self._on_save_click)
        self.btn_save.pack(side=tk.RIGHT, padx=(5, 0))

        # 2-3. リサイズグリップ
        self.grp_desc = fws_view_component_lib_resize_grip.FwsViewComponentLibResizeGrip(
            self.blk_accordion.container,
            target_widget=self.txt_description,
        )
        self.grp_desc.pack(side=tk.TOP, fill=tk.X, pady=(2, 0))
    #endregion

    #region Public Methods
    def set_callbacks(
        self,
        on_save: Callable[[], None],
        on_compare: Callable[[], None],
    ) -> None:
        """
        Summary:
            各種イベントコールバックを設定します。
        Description:
            保存ボタンおよび比較ボタン押下時に呼び出す外部コールバック関数を登録します。
        Args:
            on_save: Callable[[], None] - 保存ボタン押下時コールバック。
            on_compare: Callable[[], None] - 比較ボタン押下時コールバック。
        Returns:
            None - 戻り値なし。
        """
        self._on_save = on_save
        self._on_compare = on_compare

    def get_text(self) -> str:
        """
        Summary:
            テキスト内容を取得します。
        Description:
            テキストエリアの全文字列を取得し、末尾の改行コードを除去して返却します。
        Args:
            なし
        Returns:
            str - テキストエリアの文字列。
        """
        return str(self.txt_description.get("1.0", tk.END)).rstrip("\r\n")

    def set_text(self, text: str) -> None:
        """
        Summary:
            テキスト内容を設定します。
        Description:
            既存のテキスト内容をクリアし、指定された文字列を挿入します。
        Args:
            text: str - 設定するテキスト文字列。
        Returns:
            None - 戻り値なし。
        """
        self.clear_text()
        self.txt_description.insert("1.0", text)

    def clear_text(self) -> None:
        """
        Summary:
            テキスト内容をクリアします。
        Description:
            テキストエリアの内容を先頭から末尾まで全削除します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.txt_description.delete("1.0", tk.END)

    def toggle(self) -> None:
        """
        Summary:
            アコーディオンの開閉を切り替えます。
        Description:
            内包する FwsViewComponentLibAccordionBlock の toggle メソッドを呼び出し、開閉状態を切り替えます。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.blk_accordion.toggle()
    #endregion

    #region Private Methods
    def _on_save_click(self) -> None:
        """
        Summary:
            保存ボタン押下時の内部ラッパー処理を行います。
        Description:
            登録されている _on_save コールバックを呼び出します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._on_save()

    def _on_compare_click(self) -> None:
        """
        Summary:
            比較ボタン押下時の内部ラッパー処理を行います。
        Description:
            登録されている _on_compare コールバックを呼び出します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._on_compare()
    #endregion
#endregion
