"""
Summary:
    時系列ブロックおよびタスクカードコンポーネントモジュール。
Description:
    タスクカード群およびソートツールバーを統括管理する自律型コンテナ FwsViewComponentChatTemplateTimelineBlock と、
    時系列タスクカード FwsViewComponentChatTemplateTimelineCard を定義します。
    また、各チェック項目に動的配置される補足UI（FwsTimelineExtraUiBase, FwsTimelineExtraUiOnsiteCall,
    FwsTimelineExtraUiTextOnly, FwsTimelineExtraUiHostCombo, FwsTimelineExtraUiTextTransform,
    FwsTimelineExtraUiDynamicSelector, FwsTimelineExtraUiDeviceSwap）を同居集約して提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from __future__ import annotations

from datetime import datetime
import json
import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Optional

from fws_lib.tkinter.views.view.component import (
    fws_view_component_lib_accordion_block,
    fws_view_component_lib_resize_grip,
    fws_view_component_lib_scrollable_frame,
    fws_view_component_lib_scrolled_text,
)
#endregion

#region classes
class FwsViewComponentChatTemplateTimelineBlock(ttk.Frame):
    """
    Summary:
        時系列ブロック親コンポーネントクラス。
    Description:
        ttk.Frame を継承し、上部並び替えツールバー、スクロールフレーム、
        プレースホルダーラベル、および時系列タスクカード群（FwsViewComponentChatTemplateTimelineCard）の生成・追加・削除・データ集約を自律統括します。
    """

    #region Constructor
    def __init__(self, parent: tk.Widget, **kwargs: Any) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            基底 ttk.Frame を初期化し、ツールバー、スクロール枠、プレースホルダーを生成・配置します。
        Args:
            parent: tk.Widget - 親ウィジェット。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent, **kwargs)

        self.cards: list[FwsViewComponentChatTemplateTimelineCard] = []
        """list[FwsViewComponentChatTemplateTimelineCard] - 内包する時系列タスクカード保持リスト"""
        self.frm_sort_bar: ttk.Frame
        """ttk.Frame - 上部並び替えツールバーフレーム"""
        self.lbl_sort_order: ttk.Label
        """ttk.Label - 並び替えラベル"""
        self.cmb_sort_order: ttk.Combobox
        """ttk.Combobox - 並び替え選択コンボボックス"""
        self.btn_refresh_sort: ttk.Button
        """ttk.Button - ソートリフレッシュボタン"""
        self.scr_timeline: fws_view_component_lib_scrollable_frame.FwsViewComponentLibScrollableFrame
        """fws_view_component_lib_scrollable_frame.FwsViewComponentLibScrollableFrame - 時系列タスクカード表示用スクロールフレーム"""
        self.lbl_placeholder: ttk.Label
        """ttk.Label - タスクカード未追加時のプレースホルダーラベル"""
        self._on_refresh_sort: Callable[[], None]
        """Callable[[], None] - ソートリフレッシュボタン押下時コールバック"""
        self._on_delete: Callable[[FwsViewComponentChatTemplateTimelineCard], None]
        """Callable[[FwsViewComponentChatTemplateTimelineCard], None] - カード削除時コールバック"""
        self._on_check_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None]
        """Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None] - チェック状態変更時コールバック"""
        self._on_extra_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None]
        """Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None] - 補足UI変更時コールバック"""
        self._on_memo_change: Callable[[FwsViewComponentChatTemplateTimelineCard, str], None]
        """Callable[[FwsViewComponentChatTemplateTimelineCard, str], None] - メモ変更時コールバック"""
        self._on_complete_change: Callable[[FwsViewComponentChatTemplateTimelineCard], None]
        """Callable[[FwsViewComponentChatTemplateTimelineCard], None] - 完了状態変更時コールバック"""
        self._device_provider: Callable[[], list[dict[str, str]]]
        """Callable[[], list[dict[str, str]]] - 機器情報プロバイダ関数"""

        self._init_layout()

    def _init_layout(self) -> None:
        """
        Summary:
            レイアウト初期化を行います。
        Description:
            上部ソートバー、スクロールフレーム、および初期プレースホルダーラベルを配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # 1. 上部ツールバー（ソートバー）
        self.frm_sort_bar = ttk.Frame(self)
        self.frm_sort_bar.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        self.lbl_sort_order = ttk.Label(self.frm_sort_bar, text="並び替え:")
        self.lbl_sort_order.pack(side=tk.LEFT, padx=(0, 5))

        self.cmb_sort_order = ttk.Combobox(
            self.frm_sort_bar,
            state="readonly",
            values=["時系列順", "作業分類順"],
            width=12,
        )
        self.cmb_sort_order.set("時系列順")
        self.cmb_sort_order.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_refresh_sort = ttk.Button(self.frm_sort_bar, text="リフレッシュ", width=10, command=self._on_refresh_sort_click)
        self.btn_refresh_sort.pack(side=tk.LEFT)

        # 2. スクロール可能フレーム
        self.scr_timeline = fws_view_component_lib_scrollable_frame.FwsViewComponentLibScrollableFrame(self)
        self.scr_timeline.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 3. プレースホルダーラベル
        self.lbl_placeholder = ttk.Label(
            self.scr_timeline.content_frame,
            text="（時系列タスクカード表示領域: メニューダブルクリックでここに追加されます）",
        )
        self.lbl_placeholder.pack(anchor=tk.NW, padx=10, pady=10)
    #endregion

    #region Public Methods
    def set_callbacks(
        self,
        on_refresh_sort: Callable[[], None],
        on_delete: Callable[[FwsViewComponentChatTemplateTimelineCard], None],
        on_check_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None],
        on_extra_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None],
        on_memo_change: Callable[[FwsViewComponentChatTemplateTimelineCard, str], None],
        on_complete_change: Callable[[FwsViewComponentChatTemplateTimelineCard], None],
        device_provider: Callable[[], list[dict[str, str]]],
    ) -> None:
        """
        Summary:
            時系列ブロックおよび配下カードの各種コールバック・プロバイダを設定します。
        Description:
            リフレッシュボタン押下時コールバック、カード内イベント用コールバック群、
            および補足UI用の機器情報プロバイダ関数をブロック単位で一括登録します。
        Args:
            on_refresh_sort: Callable[[], None] - ソートリフレッシュ押下時コールバック。
            on_delete: Callable[[FwsViewComponentChatTemplateTimelineCard], None] - カード削除時コールバック。
            on_check_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None] - チェック変更時コールバック。
            on_extra_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None] - 補足UI変更時コールバック。
            on_memo_change: Callable[[FwsViewComponentChatTemplateTimelineCard, str], None] - メモ変更時コールバック。
            on_complete_change: Callable[[FwsViewComponentChatTemplateTimelineCard], None] - 完了変更時コールバック。
            device_provider: Callable[[], list[dict[str, str]]] - 機器情報プロバイダ関数。
        Returns:
            None - 戻り値なし。
        """
        self._on_refresh_sort = on_refresh_sort
        self._on_delete = on_delete
        self._on_check_change = on_check_change
        self._on_extra_change = on_extra_change
        self._on_memo_change = on_memo_change
        self._on_complete_change = on_complete_change
        self._device_provider = device_provider

    def add_card(
        self,
        task_time: str,
        category_name: str,
        task_name: str,
        task_template_id: str = "",
        item_number: int = 0,
        checklist_items: Optional[list[dict[str, Any]]] = None,
        memo: str = "",
    ) -> FwsViewComponentChatTemplateTimelineCard:
        """
        Summary:
            時系列タスクカードを生成・追加します。
        Description:
            FwsViewComponentChatTemplateTimelineCard インスタンスを生成してスクロール枠内に pack 配置し、
            set_callbacks で登録された各種コールバックおよび device_provider を自動引き継ぎした上で、
            カードリストへの登録、破棄イベントのバインド、プレースホルダーの非表示、
            および最下部への自動スクロールを自律的に行います。
        Args:
            task_time: str - 作業時刻（例: "14:30"）。
            category_name: str - 作業分類名。
            task_name: str - 作業項目名。
            task_template_id: str - タスクテンプレートID（例: "T0001"）。
            item_number: int - タスク連番（デフォルト: 0）。
            checklist_items: Optional[list[dict[str, Any]]] - チェックリスト初期項目リスト。
            memo: str - 初期メモ文字列。
        Returns:
            FwsViewComponentChatTemplateTimelineCard - 生成された時系列タスクカードインスタンス。
        """
        card: FwsViewComponentChatTemplateTimelineCard = FwsViewComponentChatTemplateTimelineCard(
            master=self.scr_timeline.content_frame,
            task_time=task_time,
            category_name=category_name,
            task_name=task_name,
            task_template_id=task_template_id,
            item_number=item_number,
            checklist_items=checklist_items,
            memo=memo,
            on_delete=self._on_delete,
            on_check_change=self._on_check_change,
            on_extra_change=self._on_extra_change,
            on_memo_change=self._on_memo_change,
            on_complete_change=self._on_complete_change,
            device_provider=self._device_provider,
        )
        card.bind("<Destroy>", lambda e, c=card: self._on_card_destroyed(c))
        card.pack(side=tk.TOP, fill=tk.X, padx=5, pady=3)
        self.cards.append(card)

        self.lbl_placeholder.pack_forget()
        self.update_idletasks()
        self.scr_timeline.yview_moveto(1.0)
        return card

    def clear_cards(self) -> None:
        """
        Summary:
            全タスクカードを破棄・クリアします。
        Description:
            保持している全 FwsViewComponentChatTemplateTimelineCard の delete メソッドを呼び出して破棄し、
            カード管理リストを空にしてプレースホルダーを再表示します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        for card in list(self.cards):
            card.delete()
        self.cards.clear()
        self.lbl_placeholder.pack(anchor=tk.NW, padx=10, pady=10)

    def set_cards_data(
        self,
        cards_data: list[dict[str, Any]],
    ) -> None:
        """
        Summary:
            時系列タスクカードデータを一括設定・復元します。
        Description:
            現在のカードをクリアした上で、渡されたカードデータリストを基にカードを再生成します。
            各カードの完了状態（is_completed）も正しく復元します。
        Args:
            cards_data: list[dict[str, Any]] - 設定するカードデータの辞書リスト。
        Returns:
            None - 戻り値なし。
        """
        self.clear_cards()
        for item in cards_data:
            card: FwsViewComponentChatTemplateTimelineCard = self.add_card(
                task_time=str(item.get("task_time", "")),
                category_name=str(item.get("category_name", "")),
                task_name=str(item.get("task_name", "")),
                task_template_id=str(item.get("task_template_id", "")),
                item_number=int(item.get("item_number", 0)),
                checklist_items=item.get("check_items", []),
                memo=str(item.get("memo", "")),
            )
            if item.get("is_completed", False):
                card.set_completed(True)

    def sort_cards(self, order: str) -> None:
        """
        Summary:
            時系列タスクカードの並び替え・再描画を行います。
        Description:
            指定されたソート順序に従ってカード群の再配置を行います。
            現在はUI配置先行実装に伴うスタブ処理（将来のDB/データモデル連携時に本格実装予定）です。
        Args:
            order: str - 並び替え順序名（例: "時系列順", "作業分類順"）。
        Returns:
            None - 戻り値なし。
        """
        # 現在はUI配置先行実装に伴うスタブ処理であるため、何もしない（Pass）
        pass
    #endregion

    #region Private Methods
    def _on_refresh_sort_click(self) -> None:
        """
        Summary:
            ソートリフレッシュボタン押下時の内部ラッパー処理を行います。
        Description:
            登録されている _on_refresh_sort コールバックを呼び出します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._on_refresh_sort()

    def _on_card_destroyed(self, card: FwsViewComponentChatTemplateTimelineCard) -> None:
        """
        Summary:
            タスクカード破棄時の自律内部後処理を行います。
        Description:
            管理リストからカードを除外します。残カード数が0件になった場合はプレースホルダーラベルを再表示します。
            ウィンドウ破棄中のエラーをガードします。
        Args:
            card: FwsViewComponentChatTemplateTimelineCard - 破棄されたタスクカードインスタンス。
        Returns:
            None - 戻り値なし。
        """
        if card in self.cards:
            self.cards.remove(card)

        try:
            if not self.lbl_placeholder.winfo_exists():
                return
        except Exception:
            return

        if len(self.cards) == 0:
            self.lbl_placeholder.pack(anchor=tk.NW, padx=10, pady=10)
    #endregion


class FwsViewComponentChatTemplateTimelineCard(ttk.Frame):
    """
    Summary:
        時系列タスクカードコンポーネントクラス。
    Description:
        ttk.Frame を継承し、FwsViewComponentLibAccordionBlock を内包して開閉可能なヘッダー部（アクション領域に削除ボタン）、
        チェックリストとメモの左右分割ボディ部、作業完了トグルボタンを含むフッター部、
        およびメモ伸縮用リサイズグリップを配置・自律制御します。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        task_time: str,
        category_name: str,
        task_name: str,
        on_delete: Callable[[FwsViewComponentChatTemplateTimelineCard], None],
        on_check_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None],
        on_extra_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None],
        on_memo_change: Callable[[FwsViewComponentChatTemplateTimelineCard, str], None],
        on_complete_change: Callable[[FwsViewComponentChatTemplateTimelineCard], None],
        device_provider: Callable[[], list[dict[str, str]]],
        task_template_id: str = "",
        item_number: int = 0,
        checklist_items: Optional[list[dict[str, Any]]] = None,
        memo: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            基底 ttk.Frame を初期化し、内部に FwsViewComponentLibAccordionBlock を内包配置した上で、
            ヘッダーアクション部、詳細ペイン、フッター、リサイズグリップウィジェットを生成・配置します。
        Args:
            master: tk.Widget - 親ウィジェット。
            task_time: str - 作業時刻（例: "14:30"）。
            category_name: str - 作業分類名。
            task_name: str - 作業項目名。
            on_delete: Callable[[FwsViewComponentChatTemplateTimelineCard], None] - 削除時コールバック。
            on_check_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None] - チェック状態変更時コールバック。
            on_extra_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None] - 補足UI変更時コールバック。
            on_memo_change: Callable[[FwsViewComponentChatTemplateTimelineCard, str], None] - メモ変更時コールバック。
            on_complete_change: Callable[[FwsViewComponentChatTemplateTimelineCard], None] - 完了状態変更時コールバック。
            device_provider: Callable[[], list[dict[str, str]]] - 機器情報プロバイダ関数。
            task_template_id: str - タスクテンプレートID（例: "T0001"）。
            item_number: int - タスク連番（デフォルト: 0）。
            checklist_items: Optional[list[dict[str, Any]]] - チェックリスト初期項目リスト。
            memo: str - 初期メモ文字列。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master, **kwargs)

        self.item_number: int = item_number
        """int - タスク連番"""
        self.task_time: str = task_time
        """str - 作業時刻文字列"""
        self.category_name: str = category_name
        """str - 作業分類名"""
        self.task_name: str = task_name
        """str - 作業項目名"""
        self.task_template_id: str = task_template_id
        """str - タスクテンプレートID"""
        self.is_completed: bool = False
        """bool - 作業完了状態フラグ"""
        self.check_items: list[dict[str, Any]] = []
        """list[dict[str, Any]] - チェックリスト項目情報リスト"""
        self.on_delete: Callable[[FwsViewComponentChatTemplateTimelineCard], None] = on_delete
        """Callable[[FwsViewComponentChatTemplateTimelineCard], None] - 削除時通知コールバック"""
        self.on_check_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None] = on_check_change
        """Callable[[FwsViewComponentChatTemplateTimelineCard, int, bool], None] - チェック状態変更時通知コールバック"""
        self.on_extra_change: Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None] = on_extra_change
        """Callable[[FwsViewComponentChatTemplateTimelineCard, int, dict[str, Any]], None] - 補足UI変更時通知コールバック"""
        self.on_memo_change: Callable[[FwsViewComponentChatTemplateTimelineCard, str], None] = on_memo_change
        """Callable[[FwsViewComponentChatTemplateTimelineCard, str], None] - メモ変更時通知コールバック"""
        self.on_complete_change: Callable[[FwsViewComponentChatTemplateTimelineCard], None] = on_complete_change
        """Callable[[FwsViewComponentChatTemplateTimelineCard], None] - 完了状態変更時通知コールバック"""
        self.device_provider: Callable[[], list[dict[str, str]]] = device_provider
        """Callable[[], list[dict[str, str]]] - 機器情報プロバイダ関数"""

        self.blk_accordion: fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock
        """fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock - 内包アコーディオンブロックウィジェット"""
        self.btn_delete: ttk.Button
        """ttk.Button - 削除ボタン"""
        self.paned_body: ttk.PanedWindow
        """ttk.PanedWindow - 左右分割ペインウィンドウ"""
        self.frm_checklist: ttk.Frame
        """ttk.Frame - 左側チェックリストフレーム"""
        self.frm_memo: ttk.Frame
        """ttk.Frame - 右側メモフレーム"""
        self.txt_memo: fws_view_component_lib_scrolled_text.FwsViewComponentLibScrolledText
        """fws_view_component_lib_scrolled_text.FwsViewComponentLibScrolledText - メモ入力用スクロールテキスト"""
        self.frm_footer: ttk.Frame
        """ttk.Frame - フッターフレーム"""
        self.btn_complete: ttk.Button
        """ttk.Button - 作業完了トグルボタン"""
        self.grp_memo: fws_view_component_lib_resize_grip.FwsViewComponentLibResizeGrip
        """fws_view_component_lib_resize_grip.FwsViewComponentLibResizeGrip - メモ領域用リサイズグリップ"""

        self._create_widgets(checklist_items, memo)

    def _create_widgets(
        self,
        checklist_items: Optional[list[dict[str, Any]]],
        memo: str,
    ) -> None:
        """
        Summary:
            タスクカード内の追加ウィジェットを生成し配置します。
        Description:
            内部に FwsViewComponentLibAccordionBlock を内包配置し、ヘッダーアクション部への削除ボタン配置、
            コンテンツコンテナ内への左右分割ペイン（チェックリスト・メモ）、
            フッター部（完了ボタン）、およびメモ用リサイズグリップを順に構築します。
        Args:
            checklist_items: Optional[list[dict[str, Any]]] - チェックリスト初期項目リスト。
            memo: str - 初期メモ文字列。
        Returns:
            None - 戻り値なし。
        """
        # 1. 自身の直下に FwsViewComponentLibAccordionBlock を配置（内包）
        self.blk_accordion = fws_view_component_lib_accordion_block.FwsViewComponentLibAccordionBlock(
            self,
            title=f"[{self.task_time}] {self.category_name} - {self.task_name}",
            is_expanded=True,
        )
        self.blk_accordion.pack(fill=tk.BOTH, expand=True)

        # 2. アコーディオンのヘッダー右側アクション領域に削除ボタンを配置
        self.btn_delete = ttk.Button(
            self.blk_accordion.frm_header_actions,
            text="削除",
            width=6,
            command=self._on_delete_click,
        )
        self.btn_delete.pack(side=tk.RIGHT)

        # 3. アコーディオンのコンテンツコンテナ内に左右分割ペインを配置
        self.paned_body = ttk.PanedWindow(self.blk_accordion.container, orient=tk.HORIZONTAL)
        self.paned_body.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 左ペイン: チェックリスト
        self.frm_checklist = ttk.Frame(self.paned_body, padding=5)
        raw_items: list[dict[str, Any]] = checklist_items if checklist_items is not None else []
        for item in raw_items:
            display_text: str = str(item.get("display_text", ""))
            append_text: str = str(item.get("append_text", ""))
            extra_builder: str = str(item.get("extra_builder", ""))
            extra_data_val: Any = item.get("extra_data", "")
            item_seq: int = int(item.get("item_seq", 1))
            var: tk.BooleanVar = tk.BooleanVar(value=bool(item.get("is_checked", False)))

            initial_extra_data: dict[str, Any] = {}
            if isinstance(extra_data_val, str) and extra_data_val.strip():
                try:
                    initial_extra_data = json.loads(extra_data_val)
                except Exception:
                    initial_extra_data = {}
            elif isinstance(extra_data_val, dict):
                initial_extra_data = extra_data_val

            extra_ui: Optional[FwsTimelineExtraUiBase] = None
            if extra_builder == "device_swap":
                lbl_title = ttk.Label(self.frm_checklist, text=f"・ {display_text}")
                lbl_title.pack(anchor=tk.W, pady=2)

                ui_cls = EXTRA_UI_REGISTRY[extra_builder]
                extra_ui = ui_cls(
                    self.frm_checklist,
                    initial_data=initial_extra_data,
                    on_change=lambda seq=item_seq: self._on_extra_ui_change(seq),
                    report_var=var,
                    on_report_toggle=lambda seq=item_seq, v=var: self._on_check_toggle(seq, v),
                    device_provider=self.device_provider,
                )
                extra_ui.pack(fill=tk.X, padx=(10, 0), pady=(0, 4))
                chk_widget: tk.Widget = lbl_title
            else:
                chk: ttk.Checkbutton = ttk.Checkbutton(
                    self.frm_checklist,
                    text=display_text,
                    variable=var,
                )
                chk.configure(command=lambda seq=item_seq, v=var: self._on_check_toggle(seq, v))
                chk.pack(anchor=tk.W, pady=2)
                chk_widget = chk

                if extra_builder in EXTRA_UI_REGISTRY:
                    ui_cls = EXTRA_UI_REGISTRY[extra_builder]
                    extra_ui = ui_cls(
                        self.frm_checklist,
                        initial_data=initial_extra_data,
                        on_change=lambda seq=item_seq: self._on_extra_ui_change(seq),
                        device_provider=self.device_provider,
                    )
                    extra_ui.pack(fill=tk.X, padx=(20, 0), pady=(0, 4))

            self.check_items.append(
                {
                    "checklist_template_id": str(item.get("checklist_template_id", "")),
                    "task_template_id": str(item.get("task_template_id", "")),
                    "item_seq": item_seq,
                    "display_text": display_text,
                    "append_text": append_text,
                    "extra_builder": extra_builder,
                    "extra_ui": extra_ui,
                    "var": var,
                    "chk_widget": chk_widget,
                }
            )

        self.paned_body.add(self.frm_checklist, weight=1)

        # 右ペイン: メモ
        self.frm_memo = ttk.Frame(self.paned_body, padding=5)
        self.txt_memo = fws_view_component_lib_scrolled_text.FwsViewComponentLibScrolledText(self.frm_memo, height=6, wrap=tk.NONE)
        self.txt_memo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        if memo:
            self.txt_memo.insert("1.0", memo)
        self.txt_memo.bind("<FocusOut>", self._on_memo_focus_out)

        self.paned_body.add(self.frm_memo, weight=1)

        # 4. フッターフレーム
        self.frm_footer = ttk.Frame(self.blk_accordion.container)
        self.frm_footer.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 0))

        self.btn_complete = ttk.Button(
            self.frm_footer,
            text="作業完了",
            command=self._on_toggle_complete,
        )
        self.btn_complete.pack(side=tk.RIGHT)

        # 5. リサイズグリップ（最下部）
        self.grp_memo = fws_view_component_lib_resize_grip.FwsViewComponentLibResizeGrip(self.blk_accordion.container, target_widget=self.txt_memo)
        self.grp_memo.pack(side=tk.TOP, fill=tk.X, pady=(2, 0))
    #endregion

    #region Public Methods
    def delete(self) -> None:
        """
        Summary:
            カード自身を破棄します。
        Description:
            自身のウィジェット（内包するアコーディオンブロックを含む）を破棄（destroy）します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.destroy()

    def set_completed(self, is_completed: bool) -> None:
        """
        Summary:
            作業完了状態を設定し、ボタン表示を更新します。
        Description:
            完了フラグを指定された真偽値に更新し、ボタンの表示テキストを「作業完了解除」または「作業完了」に切り替えます。
            完了時はアコーディオンを自動で折りたたみ、解除時は自動で展開します。
        Args:
            is_completed: bool - 作業完了状態。
        Returns:
            None - 戻り値なし。
        """
        self.is_completed = is_completed
        self.btn_complete.configure(text="作業完了解除" if is_completed else "作業完了")
        if self.is_completed:
            if self.blk_accordion.is_expanded:
                self.blk_accordion.toggle()
        else:
            if not self.blk_accordion.is_expanded:
                self.blk_accordion.toggle()

    def get_check_item(self, item_seq: int) -> Optional[dict[str, Any]]:
        """
        Summary:
            指定された連番のチェック項目情報を取得します。
        Description:
            保持している check_items リストから item_seq が一致する辞書を検索して返却します。
        Args:
            item_seq: int - チェック項目連番。
        Returns:
            Optional[dict[str, Any]] - チェック項目情報辞書、未検出時はNone。
        """
        for item in self.check_items:
            if item["item_seq"] == item_seq:
                return item
        return None

    def get_formatted_append_text(self, item_seq: int, now_time_str: str) -> str:
        """
        Summary:
            チェック項目に対するメモ追記用整形文字列を取得します。
        Description:
            該当項目に補足UIが存在する場合はその format_memo_text を呼び出し、
            存在しない場合は "[HH:MM] append_text" 形式の文字列を生成して返却します。
        Args:
            item_seq: int - チェック項目連番。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        chk_info = self.get_check_item(item_seq)
        if not chk_info:
            return ""
        base_text: str = str(chk_info.get("append_text", ""))
        extra_ui = chk_info.get("extra_ui")
        if extra_ui is not None:
            return extra_ui.format_memo_text(base_text, now_time_str)
        return f"[{now_time_str}] {base_text}"

    def append_memo_text(self, append_line: str) -> str:
        """
        Summary:
            メモテキストエリアの末尾に整形文字列を自動追記します。
        Description:
            既存のメモ本文の末尾に改行を挟んで指定文字列を追記し、追記後のメモ全文を返却します。
        Args:
            append_line: str - 追記する文字列。
        Returns:
            str - 追記後のメモ本文全文。
        """
        current_memo: str = str(self.txt_memo.get("1.0", tk.END)).rstrip("\r\n")
        if current_memo:
            new_memo: str = f"{current_memo}\n{append_line}"
        else:
            new_memo = append_line
        self.txt_memo.delete("1.0", tk.END)
        self.txt_memo.insert("1.0", new_memo)
        return new_memo
    #endregion

    #region Private Methods
    def _on_delete_click(self) -> None:
        """
        Summary:
            削除ボタン押下時のイベント処理を行います。
        Description:
            設定されている削除コールバックを呼び出した上で、自身を破棄（delete）します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.on_delete(self)
        self.delete()

    def _on_check_toggle(self, item_seq: int, var: tk.BooleanVar) -> None:
        """
        Summary:
            チェックリスト項目のチェック状態トグル処理を行います。
        Description:
            チェック状態変更コールバックに自身、item_seq、およびチェック真偽値を渡して呼び出します。
        Args:
            item_seq: int - チェック項目連番。
            var: tk.BooleanVar - チェック状態変数。
        Returns:
            None - 戻り値なし。
        """
        self.on_check_change(self, item_seq, bool(var.get()))

    def _on_extra_ui_change(self, item_seq: int) -> None:
        """
        Summary:
            補足UI変更時のイベント処理を行います。
        Description:
            該当項目の補足UIからデータを取得し、on_extra_change コールバックを呼び出します。
        Args:
            item_seq: int - チェック項目連番。
        Returns:
            None - 戻り値なし。
        """
        chk_info = self.get_check_item(item_seq)
        if chk_info and chk_info.get("extra_ui"):
            data = chk_info["extra_ui"].get_data()
            self.on_extra_change(self, item_seq, data)

    def _on_memo_focus_out(self, event: Any = None) -> None:
        """
        Summary:
            メモ入力欄フォーカスアウト時のイベント処理を行います。
        Description:
            メモ変更コールバックに自身および現在のメモ文字列を渡して呼び出します。
        Args:
            event: Any - イベントオブジェクト（省略時はNone）。
        Returns:
            None - 戻り値なし。
        """
        memo_text: str = str(self.txt_memo.get("1.0", tk.END)).rstrip("\r\n")
        self.on_memo_change(self, memo_text)

    def _on_toggle_complete(self) -> None:
        """
        Summary:
            作業完了トグル処理を行います。
        Description:
            自身の完了フラグを反転させてボタン表示を更新し、完了状態変更コールバックに自身を渡して呼び出します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.set_completed(not self.is_completed)
        self.on_complete_change(self)
    #endregion


class FwsTimelineExtraUiBase(ttk.Frame):
    """
    Summary:
        時系列チェックリスト補足UI基底クラス。
    Description:
        ttk.Frame を継承し、各補足入力UIの共通インターフェースおよびフォーカスアウト変更通知コールバックを管理します。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        initial_data: dict[str, Any],
        on_change: Optional[Callable[[], None]] = None,
        device_provider: Optional[Callable[[], list[dict[str, str]]]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            基底 ttk.Frame を初期化し、初期データ、変更通知コールバック、および機器情報プロバイダを保持します。
        Args:
            master: tk.Widget - 親ウィジェット。
            initial_data: dict[str, Any] - 初期入力データ辞書。
            on_change: Optional[Callable[[], None]] - フォーカスアウト等の入力変更通知コールバック。
            device_provider: Optional[Callable[[], list[dict[str, str]]]] - 機器情報レコード一覧取得プロバイダ関数。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master, **kwargs)
        self.on_change: Optional[Callable[[], None]] = on_change
        """Optional[Callable[[], None]] - 入力変更通知コールバック"""
        self.device_provider: Optional[Callable[[], list[dict[str, str]]]] = device_provider
        """Optional[Callable[[], list[dict[str, str]]]] - 機器情報プロバイダ関数"""
    #endregion

    #region Public Methods
    def get_data(self) -> dict[str, Any]:
        """
        Summary:
            UIの入力データを辞書形式で取得します。
        Description:
            サブクラスでオーバーライドして各入力ウィジェットの値を辞書として返却します。
        Args:
            なし
        Returns:
            dict[str, Any] - 入力データ辞書。
        """
        return {}

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Summary:
            辞書データをUI入力欄に反映します。
        Description:
            サブクラスでオーバーライドして渡された辞書の値を各入力ウィジェットに設定します。
        Args:
            data: dict[str, Any] - 設定対象データ辞書。
        Returns:
            None - 戻り値なし。
        """
        pass

    def format_memo_text(self, base_text: str, now_time_str: str) -> str:
        """
        Summary:
            メモ自動追記用の整形文字列を生成します。
        Description:
            サブクラスでオーバーライドして現在時刻、ベース文言および入力値に応じた整形文字列を返却します。
        Args:
            base_text: str - ベースとなるappend_text。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        return f"[{now_time_str}] {base_text}"
    #endregion

    #region Private Methods
    def _notify_change(self) -> None:
        """
        Summary:
            入力値変更（FocusOut等）を外部へ通知します。
        Description:
            設定されている on_change コールバックを呼び出します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        if self.on_change is not None:
            self.on_change()

    def _get_device_hostnames(self) -> list[str]:
        """
        Summary:
            機器情報プロバイダから一意なホスト名一覧を取得します。
        Description:
            device_provider から機器レコード一覧を取得し、空文字を除外した上で昇順ソート済みの一意リストを返却します。
        Args:
            なし
        Returns:
            list[str] - 一意かつ昇順ソート済みのホスト名一覧。
        """
        if self.device_provider is None:
            return []
        records: list[dict[str, str]] = self.device_provider()
        return sorted(list(set(r.get("hostname", "") for r in records if r.get("hostname"))))
    #endregion


class FwsTimelineExtraUiOnsiteCall(FwsTimelineExtraUiBase):
    """
    Summary:
        「オンサイトへ電話連絡実施」専用補足入力UIクラス。
    Description:
        電話実施者、サービスセンタ、電話受領者のEntry入力欄および複数行連絡事項（Text）を提供し、
        値の取得・設定およびメモ追記用文字列の整形を行います。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        initial_data: dict[str, Any],
        on_change: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            インデント付きフレーム内に各入力項目（実施者、連絡先、受領者、連絡事項）を配置し、
            FocusOutイベントをバインドして初期データを反映します。
        Args:
            master: tk.Widget - 親ウィジェット。
            initial_data: dict[str, Any] - 初期入力データ辞書。
            on_change: Optional[Callable[[], None]] - 入力変更通知コールバック。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master, initial_data=initial_data, on_change=on_change, padding=(15, 2, 0, 4), **kwargs)

        self.ent_operator: ttk.Entry
        """ttk.Entry - 電話実施者入力欄"""
        self.ent_center: ttk.Entry
        """ttk.Entry - 電話先サービスセンタ入力欄"""
        self.ent_receiver: ttk.Entry
        """ttk.Entry - 電話受領者入力欄"""
        self.txt_notes: tk.Text
        """tk.Text - 複数行連絡事項入力欄"""

        self._create_widgets()
        if initial_data:
            self.set_data(initial_data)

    def _create_widgets(self) -> None:
        """
        Summary:
            入力ウィジェットを生成・配置します。
        Description:
            実施者、連絡先、受領者のEntryおよび連絡事項のTextウィジェットをgrid配置し、
            各ウィジェットに <FocusOut> イベントをバインドします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        lbl_operator = ttk.Label(self, text="実施者:")
        lbl_operator.grid(row=0, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_operator = ttk.Entry(self, width=16)
        self.ent_operator.grid(row=0, column=1, sticky=tk.W, pady=1)
        self.ent_operator.bind("<FocusOut>", lambda e: self._notify_change())

        lbl_center = ttk.Label(self, text="連絡先:")
        lbl_center.grid(row=1, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_center = ttk.Entry(self, width=16)
        self.ent_center.grid(row=1, column=1, sticky=tk.W, pady=1)
        self.ent_center.bind("<FocusOut>", lambda e: self._notify_change())

        lbl_receiver = ttk.Label(self, text="受領者:")
        lbl_receiver.grid(row=2, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_receiver = ttk.Entry(self, width=16)
        self.ent_receiver.grid(row=2, column=1, sticky=tk.W, pady=1)
        self.ent_receiver.bind("<FocusOut>", lambda e: self._notify_change())

        lbl_notes = ttk.Label(self, text="連絡事項:")
        lbl_notes.grid(row=3, column=0, sticky=tk.NW, padx=(0, 4), pady=1)
        self.txt_notes = tk.Text(self, height=3, width=20, wrap=tk.NONE, undo=True)
        self.txt_notes.grid(row=3, column=1, sticky=tk.W, pady=1)
        self.txt_notes.bind("<FocusOut>", lambda e: self._notify_change())
    #endregion

    #region Public Methods
    def get_data(self) -> dict[str, Any]:
        """
        Summary:
            入力データを辞書形式で取得します。
        Description:
            実施者、連絡先、受領者、および連絡事項の各文字列を取得して辞書を返却します。
        Args:
            なし
        Returns:
            dict[str, Any] - 入力データ辞書。
        """
        return {
            "operator": self.ent_operator.get().strip(),
            "center": self.ent_center.get().strip(),
            "receiver": self.ent_receiver.get().strip(),
            "notes": self.txt_notes.get("1.0", "end-1c").rstrip("\r\n"),
        }

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Summary:
            辞書データを入力ウィジェットに反映します。
        Description:
            渡された辞書から各項目の値を抽出し、EntryおよびTextへ設定します。
        Args:
            data: dict[str, Any] - 設定対象データ辞書。
        Returns:
            None - 戻り値なし。
        """
        self.ent_operator.delete(0, tk.END)
        self.ent_operator.insert(0, str(data.get("operator", "")))
        self.ent_center.delete(0, tk.END)
        self.ent_center.insert(0, str(data.get("center", "")))
        self.ent_receiver.delete(0, tk.END)
        self.ent_receiver.insert(0, str(data.get("receiver", "")))
        self.txt_notes.delete("1.0", tk.END)
        notes = data.get("notes", "")
        if notes:
            self.txt_notes.insert("1.0", str(notes))

    def format_memo_text(self, base_text: str, now_time_str: str) -> str:
        """
        Summary:
            メモ自動追記用の整形文字列を生成します。
        Description:
            現在時刻付きベース文言、NOC/実施者 ⇒ 連絡先/受領者 行、および連絡事項（存在する場合）を改行結合して返却します。
        Args:
            base_text: str - ベースとなるappend_text。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        data: dict[str, Any] = self.get_data()
        lines: list[str] = [f"[{now_time_str}] {base_text}"]
        lines.append(f"NOC/{data.get('operator', '')} ⇒ {data.get('center', '')}/{data.get('receiver', '')}")
        notes: str = data.get("notes", "")
        if notes:
            lines.append(notes)
        return "\n".join(lines)
    #endregion


class FwsTimelineExtraUiTextOnly(FwsTimelineExtraUiBase):
    """
    Summary:
        テキストのみ（複数行）の補足入力UIクラス。
    Description:
        複数行テキストエリアを提供し、入力値の取得・設定およびメモ追記用文字列の整形を行います。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        initial_data: dict[str, Any],
        on_change: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            インデント付きフレーム内に複数行テキストエリアを配置し、初期データを反映します。
        Args:
            master: tk.Widget - 親ウィジェット。
            initial_data: dict[str, Any] - 初期入力データ辞書。
            on_change: Optional[Callable[[], None]] - 入力変更通知コールバック。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master, initial_data=initial_data, on_change=on_change, padding=(15, 2, 0, 4), **kwargs)

        self.txt_content: tk.Text
        """tk.Text - 複数行テキスト入力エリア"""

        self._create_widgets()
        if initial_data:
            self.set_data(initial_data)

    def _create_widgets(self) -> None:
        """
        Summary:
            入力ウィジェットを生成・配置します。
        Description:
            複数行Textウィジェットを生成して配置し、<FocusOut> イベントをバインドします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.txt_content = tk.Text(self, height=3, width=22, wrap=tk.NONE, undo=True)
        self.txt_content.pack(anchor=tk.W, pady=1)
        self.txt_content.bind("<FocusOut>", lambda e: self._notify_change())
    #endregion

    #region Public Methods
    def get_data(self) -> dict[str, Any]:
        """
        Summary:
            入力データを辞書形式で取得します。
        Description:
            テキストエリアの全文字列を取得して辞書を返却します。
        Args:
            なし
        Returns:
            dict[str, Any] - 入力データ辞書。
        """
        return {
            "text": self.txt_content.get("1.0", "end-1c").rstrip("\r\n"),
        }

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Summary:
            辞書データを入力ウィジェットに反映します。
        Description:
            渡された辞書から text の値を抽出し、Textウィジェットへ設定します。
        Args:
            data: dict[str, Any] - 設定対象データ辞書。
        Returns:
            None - 戻り値なし。
        """
        self.txt_content.delete("1.0", tk.END)
        text_val: Any = data.get("text", "")
        if text_val:
            self.txt_content.insert("1.0", str(text_val))

    def format_memo_text(self, base_text: str, now_time_str: str) -> str:
        """
        Summary:
            メモ自動追記用の整形文字列を生成します。
        Description:
            テキストが存在する場合はベース文言の直下に改行して追記し、空の場合はベース文言のみを返却します。
        Args:
            base_text: str - ベースとなるappend_text。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        data: dict[str, Any] = self.get_data()
        text: str = str(data.get("text", ""))
        if text:
            return f"[{now_time_str}] {base_text}\n{text}"
        return f"[{now_time_str}] {base_text}"
    #endregion


class FwsTimelineExtraUiHostCombo(FwsTimelineExtraUiBase):
    """
    Summary:
        ホスト名選択コンボボックス補足UIクラス。
    Description:
        画面左ペインの機器テーブルに入力されているホスト名一覧をドロップダウン選択する補足UIを提供します。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        initial_data: dict[str, Any],
        on_change: Optional[Callable[[], None]] = None,
        device_provider: Optional[Callable[[], list[dict[str, str]]]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            機器情報プロバイダ関数を基底クラスへ引き渡し、LabelとComboboxを配置して初期データを反映します。
        Args:
            master: tk.Widget - 親ウィジェット。
            initial_data: dict[str, Any] - 初期入力データ辞書。
            on_change: Optional[Callable[[], None]] - 入力変更通知コールバック。
            device_provider: Optional[Callable[[], list[dict[str, str]]]] - 機器情報レコード取得関数。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(
            master,
            initial_data=initial_data,
            on_change=on_change,
            device_provider=device_provider,
            padding=(15, 2, 0, 4),
            **kwargs,
        )

        self.cmb_host: ttk.Combobox
        """ttk.Combobox - ホスト名選択コンボボックス"""

        self._create_widgets()
        if initial_data:
            self.set_data(initial_data)

    def _create_widgets(self) -> None:
        """
        Summary:
            入力ウィジェットを生成・配置します。
        Description:
            LabelおよびComboboxウィジェットをgrid配置し、展開時イベントやFocusOutイベントをバインドします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        lbl_host = ttk.Label(self, text="ホスト名:")
        lbl_host.grid(row=0, column=0, sticky=tk.W, padx=(0, 4), pady=1)

        self.cmb_host = ttk.Combobox(self, width=18, postcommand=self._on_post_command)
        self.cmb_host.grid(row=0, column=1, sticky=tk.W, pady=1)
        self.cmb_host.bind("<FocusOut>", lambda e: self._notify_change())
        self.cmb_host.bind("<<ComboboxSelected>>", lambda e: self._notify_change())
    #endregion

    #region Public Methods
    def get_data(self) -> dict[str, Any]:
        """
        Summary:
            入力データを辞書形式で取得します。
        Description:
            選択されたホスト名文字列を取得して辞書を返却します。
        Args:
            なし
        Returns:
            dict[str, Any] - 入力データ辞書。
        """
        return {
            "hostname": self.cmb_host.get().strip(),
        }

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Summary:
            辞書データを入力ウィジェットに反映します。
        Description:
            渡された辞書から hostname の値を抽出し、Comboboxへ設定します。
        Args:
            data: dict[str, Any] - 設定対象データ辞書。
        Returns:
            None - 戻り値なし。
        """
        self.cmb_host.set(str(data.get("hostname", "")))

    def format_memo_text(self, base_text: str, now_time_str: str) -> str:
        """
        Summary:
            メモ自動追記用の整形文字列を生成します。
        Description:
            ホスト名が選択されていれば対象ホスト情報を付加して返却します。
        Args:
            base_text: str - ベースとなるappend_text。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        data: dict[str, Any] = self.get_data()
        hostname: str = str(data.get("hostname", ""))
        if hostname:
            return f"[{now_time_str}] {base_text} (対象ホスト: {hostname})"
        return f"[{now_time_str}] {base_text}"
    #endregion

    #region Private Methods
    def _on_post_command(self) -> None:
        """
        Summary:
            コンボボックス展開時の最新ホスト名一覧取得処理を行います。
        Description:
            保持している device_provider から最新ホスト名候補を一意かつソート済みで取得してコンボボックスへ反映します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        if self.device_provider is not None:
            candidates: list[str] = self._get_device_hostnames()
            self.cmb_host.configure(values=candidates)
    #endregion


class FwsTimelineExtraUiTextTransform(FwsTimelineExtraUiBase):
    """
    Summary:
        テキスト連動加工補足UIクラス。
    Description:
        入力テキストをチェックボックス押下により連動加工（大文字化・プレフィックス付与）して出力する補足UIを提供します。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        initial_data: dict[str, Any],
        on_change: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            入力Entry、加工チェックボックス、出力Entryを配置し、初期データを反映します。
        Args:
            master: tk.Widget - 親ウィジェット。
            initial_data: dict[str, Any] - 初期入力データ辞書。
            on_change: Optional[Callable[[], None]] - 入力変更通知コールバック。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master, initial_data=initial_data, on_change=on_change, padding=(15, 2, 0, 4), **kwargs)

        self.ent_source: ttk.Entry
        """ttk.Entry - 入力テキスト欄"""
        self.var_transform: tk.BooleanVar
        """tk.BooleanVar - 加工適用チェック状態変数"""
        self.chk_transform: ttk.Checkbutton
        """ttk.Checkbutton - 加工適用チェックボタン"""
        self.ent_target: ttk.Entry
        """ttk.Entry - 加工結果出力欄"""

        self._create_widgets()
        if initial_data:
            self.set_data(initial_data)

    def _create_widgets(self) -> None:
        """
        Summary:
            入力ウィジェットを生成・配置します。
        Description:
            入力Entry、連動加工用Checkbutton、加工結果Entryをgrid配置し、イベントを設定します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        lbl_source = ttk.Label(self, text="入力テキスト:")
        lbl_source.grid(row=0, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_source = ttk.Entry(self, width=22)
        self.ent_source.grid(row=0, column=1, sticky=tk.W, pady=1)
        self.ent_source.bind("<FocusOut>", self._on_source_focus_out)

        self.var_transform = tk.BooleanVar(value=False)
        self.chk_transform = ttk.Checkbutton(
            self,
            text="加工適用 (大文字化)",
            variable=self.var_transform,
            command=self._on_transform_toggle,
        )
        self.chk_transform.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=1)

        lbl_target = ttk.Label(self, text="加工結果:")
        lbl_target.grid(row=2, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_target = ttk.Entry(self, width=22)
        self.ent_target.grid(row=2, column=1, sticky=tk.W, pady=1)
        self.ent_target.bind("<FocusOut>", lambda e: self._notify_change())
    #endregion

    #region Public Methods
    def get_data(self) -> dict[str, Any]:
        """
        Summary:
            入力データを辞書形式で取得します。
        Description:
            入力テキスト、加工フラグ、加工結果テキストを取得して辞書を返却します。
        Args:
            なし
        Returns:
            dict[str, Any] - 入力データ辞書。
        """
        return {
            "source_text": self.ent_source.get().strip(),
            "is_transformed": bool(self.var_transform.get()),
            "target_text": self.ent_target.get().strip(),
        }

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Summary:
            辞書データを入力ウィジェットに反映します。
        Description:
            渡された辞書から各項目の値を抽出し、ウィジェットへ設定します。
        Args:
            data: dict[str, Any] - 設定対象データ辞書。
        Returns:
            None - 戻り値なし。
        """
        self.ent_source.delete(0, tk.END)
        self.ent_source.insert(0, str(data.get("source_text", "")))
        self.var_transform.set(bool(data.get("is_transformed", False)))
        self.ent_target.delete(0, tk.END)
        self.ent_target.insert(0, str(data.get("target_text", "")))

    def format_memo_text(self, base_text: str, now_time_str: str) -> str:
        """
        Summary:
            メモ自動追記用の整形文字列を生成します。
        Description:
            加工結果テキストが存在する場合はベース文言の直下に改行して追記し返却します。
        Args:
            base_text: str - ベースとなるappend_text。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        data: dict[str, Any] = self.get_data()
        target_text: str = str(data.get("target_text", ""))
        if target_text:
            return f"[{now_time_str}] {base_text}\n{target_text}"
        return f"[{now_time_str}] {base_text}"
    #endregion

    #region Private Methods
    def _on_transform_toggle(self) -> None:
        """
        Summary:
            加工適用チェックボックストグル時の連動処理を行います。
        Description:
            先頭で加工結果欄をクリアし、チェックONかつ入力テキストが存在する場合のみ大文字化して加工結果欄へ出力します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.ent_target.delete(0, tk.END)
        src: str = self.ent_source.get().strip()
        if self.var_transform.get() and src:
            self.ent_target.insert(0, f"[PROCESSED] {src.upper()}")
        self._notify_change()

    def _on_source_focus_out(self, event: Optional[tk.Event] = None) -> None:
        """
        Summary:
            入力テキストのフォーカス喪失時処理を行います。
        Description:
            加工トグル処理（_on_transform_toggle）を呼び出して加工結果を再計算・反映します。
        Args:
            event: Optional[tk.Event] - Tkinterイベントオブジェクト。
        Returns:
            None - 戻り値なし。
        """
        self._on_transform_toggle()
    #endregion


class FwsTimelineExtraUiDynamicSelector(FwsTimelineExtraUiBase):
    """
    Summary:
        動的アイテム切替補足UIクラス。
    Description:
        コンボボックス・オプションチェックボックス・切替ボタンにより、コンテナ内のウィジェットを動的に切替・配置します。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        initial_data: dict[str, Any],
        on_change: Optional[Callable[[], None]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            モード選択・オプション部・動的ウィジェットコンテナを配置し、初期データを反映します。
        Args:
            master: tk.Widget - 親ウィジェット。
            initial_data: dict[str, Any] - 初期入力データ辞書。
            on_change: Optional[Callable[[], None]] - 入力変更通知コールバック。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(master, initial_data=initial_data, on_change=on_change, padding=(15, 2, 0, 4), **kwargs)

        self.cmb_mode: ttk.Combobox
        """ttk.Combobox - モード選択コンボボックス"""
        self.var_opt1: tk.BooleanVar
        """tk.BooleanVar - オプション1チェック状態変数"""
        self.chk_opt1: ttk.Checkbutton
        """ttk.Checkbutton - オプション1チェックボタン"""
        self.var_opt2: tk.BooleanVar
        """tk.BooleanVar - タイムスタンプ付与チェック状態変数"""
        self.chk_opt2: ttk.Checkbutton
        """ttk.Checkbutton - タイムスタンプ付与チェックボタン"""
        self.btn_switch: ttk.Button
        """ttk.Button - アイテム切替・反映ボタン"""
        self.frm_dynamic_container: ttk.Frame
        """ttk.Frame - 動的ウィジェット配置用コンテナフレーム"""
        self._current_dynamic_widget: Optional[tk.Widget] = None
        """Optional[tk.Widget] - 現在生成されている動的ウィジェット"""

        self._create_widgets()
        if initial_data:
            self.set_data(initial_data)

    def _create_widgets(self) -> None:
        """
        Summary:
            入力ウィジェットを生成・配置します。
        Description:
            モードコンボ、オプションチェックボックス、切替ボタン、動的コンテナを配置し、初期UIを生成します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        frm_ctrl = ttk.Frame(self)
        frm_ctrl.pack(fill=tk.X, pady=1)

        lbl_mode = ttk.Label(frm_ctrl, text="モード:")
        lbl_mode.pack(side=tk.LEFT, padx=(0, 2))
        self.cmb_mode = ttk.Combobox(frm_ctrl, state="readonly", values=["モードA", "モードB", "モードC"], width=10)
        self.cmb_mode.set("モードA")
        self.cmb_mode.pack(side=tk.LEFT, padx=(0, 4))

        self.var_opt1 = tk.BooleanVar(value=False)
        self.chk_opt1 = ttk.Checkbutton(frm_ctrl, text="詳細オプション1", variable=self.var_opt1)
        self.chk_opt1.pack(side=tk.LEFT, padx=(0, 4))

        self.var_opt2 = tk.BooleanVar(value=False)
        self.chk_opt2 = ttk.Checkbutton(frm_ctrl, text="タイムスタンプ付与", variable=self.var_opt2)
        self.chk_opt2.pack(side=tk.LEFT, padx=(0, 4))

        self.btn_switch = ttk.Button(frm_ctrl, text="アイテム切替 / 反映", width=16, command=self._on_switch_click)
        self.btn_switch.pack(side=tk.LEFT)

        self.frm_dynamic_container = ttk.Frame(self)
        self.frm_dynamic_container.pack(fill=tk.X, pady=(2, 0))

        self._switch_dynamic_ui()
    #endregion

    #region Public Methods
    def get_data(self) -> dict[str, Any]:
        """
        Summary:
            入力データを辞書形式で取得します。
        Description:
            モード、各オプション、動的ウィジェットの現在文字列を取得して辞書を返却します。
        Args:
            なし
        Returns:
            dict[str, Any] - 入力データ辞書。
        """
        return {
            "mode": self.cmb_mode.get(),
            "opt1": bool(self.var_opt1.get()),
            "opt2": bool(self.var_opt2.get()),
            "dynamic_value": self._get_dynamic_value(),
        }

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Summary:
            辞書データを入力ウィジェットに反映します。
        Description:
            モード、各オプションを反映後、動的コンテナ内ウィジェットを再生成して値を設定します。
        Args:
            data: dict[str, Any] - 設定対象データ辞書。
        Returns:
            None - 戻り値なし。
        """
        mode: str = str(data.get("mode", "モードA"))
        if mode in ["モードA", "モードB", "モードC"]:
            self.cmb_mode.set(mode)
        self.var_opt1.set(bool(data.get("opt1", False)))
        self.var_opt2.set(bool(data.get("opt2", False)))
        dyn_val: str = str(data.get("dynamic_value", ""))
        self._switch_dynamic_ui(initial_value=dyn_val)

    def format_memo_text(self, base_text: str, now_time_str: str) -> str:
        """
        Summary:
            メモ自動追記用の整形文字列を生成します。
        Description:
            モード、有効オプション名、および動的入力値をフォーマットした文字列を返却します。
        Args:
            base_text: str - ベースとなるappend_text。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        mode: str = self.cmb_mode.get()
        dyn_val: str = self._get_dynamic_value()
        opts: list[str] = []
        if self.var_opt1.get():
            opts.append("オプション1")
        if self.var_opt2.get():
            opts.append("タイムスタンプ")
        opt_str: str = f" ({', '.join(opts)})" if opts else ""
        val_str: str = f" : {dyn_val}" if dyn_val else ""
        return f"[{now_time_str}] {base_text} [{mode}]{opt_str}{val_str}"
    #endregion

    #region Private Methods
    def _on_switch_click(self) -> None:
        """
        Summary:
            アイテム切替・反映ボタン押下時の処理を行います。
        Description:
            コンテナ内ウィジェットを再生成し、変更通知を発火します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._switch_dynamic_ui()
        self._notify_change()

    def _switch_dynamic_ui(self, initial_value: str = "") -> None:
        """
        Summary:
            動的ウィジェットの生成・切替を行います。
        Description:
            モード（A: Entry, B: Label, C: Text）およびタイムスタンプオプションに応じてウィジェットを再構築します。
        Args:
            initial_value: str - 初期設定文字列。
        Returns:
            None - 戻り値なし。
        """
        for child in self.frm_dynamic_container.winfo_children():
            child.destroy()

        mode: str = self.cmb_mode.get()
        has_timestamp: bool = bool(self.var_opt2.get())
        time_prefix: str = f"[{datetime.now().strftime('%H:%M')}] " if has_timestamp else ""

        if mode == "モードA":
            ent = ttk.Entry(self.frm_dynamic_container, width=22)
            ent.pack(anchor=tk.W, pady=1)
            if initial_value:
                ent.insert(0, initial_value)
            elif has_timestamp:
                ent.insert(0, time_prefix)
            ent.bind("<FocusOut>", lambda e: self._notify_change())
            self._current_dynamic_widget = ent
        elif mode == "モードB":
            lbl_text: str = "【固定表示】モードB 稼働中"
            if has_timestamp:
                lbl_text = f"{time_prefix}{lbl_text}"
            lbl = ttk.Label(self.frm_dynamic_container, text=lbl_text)
            lbl.pack(anchor=tk.W, pady=1)
            self._current_dynamic_widget = lbl
        else:
            txt = tk.Text(self.frm_dynamic_container, height=2, width=22, undo=True, wrap=tk.NONE)
            txt.pack(anchor=tk.W, pady=1)
            if initial_value:
                txt.insert("1.0", initial_value)
            elif has_timestamp:
                txt.insert("1.0", time_prefix)
            txt.bind("<FocusOut>", lambda e: self._notify_change())
            self._current_dynamic_widget = txt

    def _get_dynamic_value(self) -> str:
        """
        Summary:
            現在の動的ウィジェットから値を取得します。
        Description:
            Entry, Label, Text の種別に応じて文字列を取得して返却します。
        Args:
            なし
        Returns:
            str - 入力または表示文字列。
        """
        if isinstance(self._current_dynamic_widget, ttk.Entry):
            return self._current_dynamic_widget.get().strip()
        if isinstance(self._current_dynamic_widget, ttk.Label):
            return self._current_dynamic_widget.cget("text").strip()
        if isinstance(self._current_dynamic_widget, tk.Text):
            return self._current_dynamic_widget.get("1.0", "end-1c").rstrip("\r\n")
        return ""
    #endregion


class FwsTimelineExtraUiDeviceSwap(FwsTimelineExtraUiBase):
    """
    Summary:
        機器交換（抜去・搭載）補足入力UIクラス。
    Description:
        現場での機器交換作業において、抜去後および搭載のホスト名・型番・S/Nの入力・自動補完、
        報告用テキストの動的整形、スキップ切替、および親カードチェック状態と連動する報告実施チェックボタンを提供します。
    """

    #region Constructor
    def __init__(
        self,
        master: tk.Widget,
        initial_data: dict[str, Any],
        on_change: Optional[Callable[[], None]] = None,
        report_var: Optional[tk.BooleanVar] = None,
        on_report_toggle: Optional[Callable[[], None]] = None,
        device_provider: Optional[Callable[[], list[dict[str, str]]]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            スキップ制御、抜去機器情報、搭載機器情報、報告用テキスト、報告実施チェックボックスを配置し、
            初期データを反映します。
        Args:
            master: tk.Widget - 親ウィジェット。
            initial_data: dict[str, Any] - 初期入力データ辞書。
            on_change: Optional[Callable[[], None]] - 入力変更通知コールバック。
            report_var: Optional[tk.BooleanVar] - 親カードのチェック状態変数（省略時は新規生成）。
            on_report_toggle: Optional[Callable[[], None]] - 報告実施チェック押下時の親カード通知コールバック。
            device_provider: Optional[Callable[[], list[dict[str, str]]]] - 機器情報取得関数。
            **kwargs: Any - ttk.Frame へ渡す追加引数。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(
            master,
            initial_data=initial_data,
            on_change=on_change,
            device_provider=device_provider,
            padding=(15, 2, 0, 4),
            **kwargs,
        )

        self.report_var: tk.BooleanVar = report_var if report_var is not None else tk.BooleanVar(value=False)
        """tk.BooleanVar - 報告実施チェック状態変数"""
        self.on_report_toggle: Optional[Callable[[], None]] = on_report_toggle
        """Optional[Callable[[], None]] - 報告実施トグル通知コールバック"""

        self.var_skip: tk.BooleanVar = tk.BooleanVar(value=False)
        """tk.BooleanVar - スキップチェック状態変数"""
        self.chk_skip: ttk.Checkbutton
        """ttk.Checkbutton - 当該項目スキップチェックボタン"""
        self.cmb_remove_host: ttk.Combobox
        """ttk.Combobox - 抜去後ホスト名選択コンボボックス"""
        self.ent_remove_model: ttk.Entry
        """ttk.Entry - 抜去後型番入力欄"""
        self.ent_remove_serial: ttk.Entry
        """ttk.Entry - 抜去後S/N入力欄"""
        self.cmb_install_host: ttk.Combobox
        """ttk.Combobox - 搭載ホスト名選択コンボボックス"""
        self.ent_install_model: ttk.Entry
        """ttk.Entry - 搭載型番入力欄"""
        self.ent_install_serial: ttk.Entry
        """ttk.Entry - 搭載S/N入力欄"""
        self.txt_report: tk.Text
        """tk.Text - 報告用テキストエリア"""
        self.chk_report: ttk.Checkbutton
        """ttk.Checkbutton - 報告実施チェックボタン"""

        self._create_widgets()
        if initial_data:
            self.set_data(initial_data)

    def _create_widgets(self) -> None:
        """
        Summary:
            入力ウィジェットを生成・配置します。
        Description:
            スキップチェック、抜去グループ、搭載グループ、報告テキスト、報告実施チェックをgrid配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # 1. スキップ制御
        self.chk_skip = ttk.Checkbutton(
            self,
            text="当該項目をskipする",
            variable=self.var_skip,
            command=self._on_skip_toggle,
        )
        self.chk_skip.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 2))

        # 2. 抜去機器情報
        lbl_remove_host = ttk.Label(self, text="抜去後ホスト名:")
        lbl_remove_host.grid(row=1, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.cmb_remove_host = ttk.Combobox(self, width=18, postcommand=self._on_post_command)
        self.cmb_remove_host.grid(row=1, column=1, sticky=tk.W, pady=1)
        self.cmb_remove_host.bind("<<ComboboxSelected>>", lambda e: self._on_host_selected("remove"))
        self.cmb_remove_host.bind("<FocusOut>", lambda e: self._on_field_focus_out())

        lbl_remove_model = ttk.Label(self, text="型番:")
        lbl_remove_model.grid(row=2, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_remove_model = ttk.Entry(self, width=18)
        self.ent_remove_model.grid(row=2, column=1, sticky=tk.W, pady=1)
        self.ent_remove_model.bind("<FocusOut>", lambda e: self._on_field_focus_out())

        lbl_remove_serial = ttk.Label(self, text="S/N:")
        lbl_remove_serial.grid(row=3, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_remove_serial = ttk.Entry(self, width=18)
        self.ent_remove_serial.grid(row=3, column=1, sticky=tk.W, pady=1)
        self.ent_remove_serial.bind("<FocusOut>", lambda e: self._on_field_focus_out())

        # 3. 搭載機器情報
        lbl_install_host = ttk.Label(self, text="搭載ホスト名:")
        lbl_install_host.grid(row=4, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.cmb_install_host = ttk.Combobox(self, width=18, postcommand=self._on_post_command)
        self.cmb_install_host.grid(row=4, column=1, sticky=tk.W, pady=1)
        self.cmb_install_host.bind("<<ComboboxSelected>>", lambda e: self._on_host_selected("install"))
        self.cmb_install_host.bind("<FocusOut>", lambda e: self._on_field_focus_out())

        lbl_install_model = ttk.Label(self, text="型番:")
        lbl_install_model.grid(row=5, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_install_model = ttk.Entry(self, width=18)
        self.ent_install_model.grid(row=5, column=1, sticky=tk.W, pady=1)
        self.ent_install_model.bind("<FocusOut>", lambda e: self._on_field_focus_out())

        lbl_install_serial = ttk.Label(self, text="S/N:")
        lbl_install_serial.grid(row=6, column=0, sticky=tk.W, padx=(0, 4), pady=1)
        self.ent_install_serial = ttk.Entry(self, width=18)
        self.ent_install_serial.grid(row=6, column=1, sticky=tk.W, pady=1)
        self.ent_install_serial.bind("<FocusOut>", lambda e: self._on_field_focus_out())

        # 4. 報告用テキスト
        lbl_report = ttk.Label(self, text="報告用テキスト:")
        lbl_report.grid(row=7, column=0, sticky=tk.NW, padx=(0, 4), pady=1)
        self.txt_report = tk.Text(self, height=3, width=24, wrap=tk.NONE, undo=True, background="white", foreground="black")
        self.txt_report.grid(row=7, column=1, sticky=tk.W, pady=1)
        self.txt_report.bind("<FocusOut>", lambda e: self._notify_change())

        # 5. 報告実施チェック
        self.chk_report = ttk.Checkbutton(
            self,
            text="報告を実施",
            variable=self.report_var,
            command=self._on_report_toggle,
        )
        self.chk_report.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(2, 0))
    #endregion

    #region Public Methods
    def get_data(self) -> dict[str, Any]:
        """
        Summary:
            入力データを辞書形式で取得します。
        Description:
            スキップフラグ、抜去情報、搭載情報、報告テキストを取得して辞書を返却します。
        Args:
            なし
        Returns:
            dict[str, Any] - 入力データ辞書。
        """
        return {
            "is_skip": bool(self.var_skip.get()),
            "remove_host": self.cmb_remove_host.get().strip(),
            "remove_model": self.ent_remove_model.get().strip(),
            "remove_serial": self.ent_remove_serial.get().strip(),
            "install_host": self.cmb_install_host.get().strip(),
            "install_model": self.ent_install_model.get().strip(),
            "install_serial": self.ent_install_serial.get().strip(),
            "report_text": self.txt_report.get("1.0", "end-1c").rstrip("\r\n"),
        }

    def set_data(self, data: dict[str, Any]) -> None:
        """
        Summary:
            辞書データを入力ウィジェットに反映します。
        Description:
            渡された辞書から各項目の値を抽出し、ウィジェットへ設定してスキップ状態を同期します。
        Args:
            data: dict[str, Any] - 設定対象データ辞書。
        Returns:
            None - 戻り値なし。
        """
        self.var_skip.set(bool(data.get("is_skip", False)))
        self.cmb_remove_host.set(str(data.get("remove_host", "")))
        self.ent_remove_model.delete(0, tk.END)
        self.ent_remove_model.insert(0, str(data.get("remove_model", "")))
        self.ent_remove_serial.delete(0, tk.END)
        self.ent_remove_serial.insert(0, str(data.get("remove_serial", "")))
        self.cmb_install_host.set(str(data.get("install_host", "")))
        self.ent_install_model.delete(0, tk.END)
        self.ent_install_model.insert(0, str(data.get("install_model", "")))
        self.ent_install_serial.delete(0, tk.END)
        self.ent_install_serial.insert(0, str(data.get("install_serial", "")))

        self.txt_report.configure(state="normal")
        self.txt_report.delete("1.0", tk.END)
        report_text: Any = data.get("report_text", "")
        if report_text:
            self.txt_report.insert("1.0", str(report_text))

        self._on_skip_toggle()

    def format_memo_text(self, base_text: str, now_time_str: str) -> str:
        """
        Summary:
            メモ自動追記用の整形文字列を生成します。
        Description:
            現在時刻付きベース文言を返却します（親メモ欄に "[HH:MM] 工程終了" を追記）。
        Args:
            base_text: str - ベースとなるappend_text。
            now_time_str: str - 現在時刻文字列（例: "14:30"）。
        Returns:
            str - メモ追記用整形文字列。
        """
        return f"[{now_time_str}] {base_text}"
    #endregion

    #region Private Methods
    def _on_skip_toggle(self) -> None:
        """
        Summary:
            スキップチェックボックストグル時の連動処理を行います。
        Description:
            スキップ状態に応じて直下の全入力ウィジェットの活性/非活性状態および背景色・文字色を切り替え、変更を通知します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        is_skip: bool = bool(self.var_skip.get())
        state_val: str = "disabled" if is_skip else "normal"
        self.cmb_remove_host.configure(state=state_val)
        self.ent_remove_model.configure(state=state_val)
        self.ent_remove_serial.configure(state=state_val)
        self.cmb_install_host.configure(state=state_val)
        self.ent_install_model.configure(state=state_val)
        self.ent_install_serial.configure(state=state_val)
        if is_skip:
            self.txt_report.configure(state="disabled", background="#f0f0f0", foreground="#6d6d6d")
        else:
            self.txt_report.configure(state="normal", background="white", foreground="black")
        self.chk_report.configure(state=state_val)
        self._notify_change()

    def _on_post_command(self) -> None:
        """
        Summary:
            コンボボックス展開時の最新ホスト名一覧取得処理を行います。
        Description:
            基底クラスの _get_device_hostnames を通じて一意なホスト名候補を取得し、コンボボックスへ設定します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        if self.device_provider is not None:
            hostnames: list[str] = self._get_device_hostnames()
            self.cmb_remove_host.configure(values=hostnames)
            self.cmb_install_host.configure(values=hostnames)

    def _on_host_selected(self, target: str) -> None:
        """
        Summary:
            ホスト名選択時の連動処理を行います。
        Description:
            選択されたホスト名に対応する機器レコードから型番およびS/Nを各Entryに自動補完し、報告用テキストを更新します。
        Args:
            target: str - 対象機器区分（"remove" または "install"）。
        Returns:
            None - 戻り値なし。
        """
        selected_host: str = (
            self.cmb_remove_host.get().strip() if target == "remove" else self.cmb_install_host.get().strip()
        )
        if self.device_provider is not None and selected_host:
            records = self.device_provider()
            for r in records:
                if r.get("hostname") == selected_host:
                    if target == "remove":
                        if r.get("model_name"):
                            self.ent_remove_model.delete(0, tk.END)
                            self.ent_remove_model.insert(0, r["model_name"])
                        if r.get("serial_number"):
                            self.ent_remove_serial.delete(0, tk.END)
                            self.ent_remove_serial.insert(0, r["serial_number"])
                    else:
                        if r.get("model_name"):
                            self.ent_install_model.delete(0, tk.END)
                            self.ent_install_model.insert(0, r["model_name"])
                        if r.get("serial_number"):
                            self.ent_install_serial.delete(0, tk.END)
                            self.ent_install_serial.insert(0, r["serial_number"])
                    break
        self._update_report_text()
        self._notify_change()

    def _on_field_focus_out(self) -> None:
        """
        Summary:
            入力フィールドフォーカス喪失時の処理を行います。
        Description:
            報告用テキストを自動整形・反映し、変更通知を発火します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._update_report_text()
        self._notify_change()

    def _update_report_text(self) -> None:
        """
        Summary:
            報告用テキストを各入力項目の値から自動整形して反映します。
        Description:
            {remove_host}/{remove_model}/{remove_serial}\n{install_host}/{install_model}/{install_serial}
            の形式で整形したテキストを txt_report に設定します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        rem_host: str = self.cmb_remove_host.get().strip()
        rem_model: str = self.ent_remove_model.get().strip()
        rem_serial: str = self.ent_remove_serial.get().strip()
        ins_host: str = self.cmb_install_host.get().strip()
        ins_model: str = self.ent_install_model.get().strip()
        ins_serial: str = self.ent_install_serial.get().strip()
        line1: str = f"{rem_host}/{rem_model}/{rem_serial}"
        line2: str = f"{ins_host}/{ins_model}/{ins_serial}"
        formatted_text: str = f"{line1}\n{line2}"

        is_skip: bool = bool(self.var_skip.get())
        if is_skip:
            self.txt_report.configure(state="normal")
        self.txt_report.delete("1.0", tk.END)
        self.txt_report.insert("1.0", formatted_text)
        if is_skip:
            self.txt_report.configure(state="disabled", background="#f0f0f0", foreground="#6d6d6d")
        else:
            self.txt_report.configure(state="normal", background="white", foreground="black")

    def _on_report_toggle(self) -> None:
        """
        Summary:
            報告実施チェックボックストグル時の処理を行います。
        Description:
            設定されている on_report_toggle コールバックを呼び出し、親カードのチェック処理を発火します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        if self.on_report_toggle is not None:
            self.on_report_toggle()
    #endregion


# 補足UIクラスレジストリ辞書
EXTRA_UI_REGISTRY: dict[str, type[FwsTimelineExtraUiBase]] = {
    "onsite_call": FwsTimelineExtraUiOnsiteCall,
    "text_only": FwsTimelineExtraUiTextOnly,
    "host_combo": FwsTimelineExtraUiHostCombo,
    "text_transform": FwsTimelineExtraUiTextTransform,
    "dynamic_selector": FwsTimelineExtraUiDynamicSelector,
    "device_swap": FwsTimelineExtraUiDeviceSwap,
}
#endregion
