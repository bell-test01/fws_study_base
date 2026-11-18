"""
Summary:
    機器情報テーブルおよび明細行コンポーネントモジュール。
Description:
    行追加・削除・データ取得・一括設定・保存ボタンを提供する専用コンポーネント FwsViewComponentChatTemplateDeviceTable、
    およびラック名、ホスト名、機種名、S/N、削除操作を備えた機器明細行の自律クラス FwsViewComponentChatTemplateDeviceRow を定義します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, Optional
#endregion

#region classes
class FwsViewComponentChatTemplateDeviceTable(ttk.Frame):
    """
    Summary:
        機器情報テーブルコンポーネントクラス。
    Description:
        ttk.Frame を継承し、上部ツールバー（行追加ボタン）、テーブルコンテナ（グリッド配置明細行）、
        および下部フッター（保存ボタン）を一体化した自律型GUIテーブルコンポーネントを提供します。
    """

    #region Constructor
    def __init__(
        self,
        parent: Any,
        model_candidates: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            機器情報テーブルの各ウィジェット（ツールバー、テーブルコンテナ、フッター）を初期化し、
            初期表示用の明細行を1行配置します。
        Args:
            parent: Any - 親ウィジェット。
            model_candidates: Optional[list[str]] - 機種名候補リスト（デフォルト None）。
            **kwargs: Any - ttk.Frame に渡す追加オプション。
        Returns:
            None - 戻り値なし。
        """
        super().__init__(parent, **kwargs)
        self.btn_add: ttk.Button
        """ttk.Button - 行追加ボタン"""
        self.btn_save: ttk.Button
        """ttk.Button - 保存ボタン"""
        self.sep_device: ttk.Separator
        """ttk.Separator - ツールバー下部セパレーター"""
        self.frm_rows: ttk.Frame
        """ttk.Frame - 明細行配置テーブルコンテナフレーム"""
        self.rows: list[FwsViewComponentChatTemplateDeviceRow] = []
        """list[FwsViewComponentChatTemplateDeviceRow] - 明細行インスタンス保持リスト"""
        self.model_candidates: list[str] = model_candidates if model_candidates is not None else []
        """list[str] - 機種名候補リスト"""
        self._row_counter: int = 1
        """int - グリッド行番号カウンタ"""
        self._on_save: Callable[[], None]
        """Callable[[], None] - 保存ボタン押下時コールバック"""

        self._init_layout()
        self.add_row()

    def _init_layout(self) -> None:
        """
        Summary:
            レイアウト初期化を行います。
        Description:
            上部ツールバー、セパレーター、テーブルグリッドコンテナ（タイトルヘッダー付き）、
            および下部フッター（保存ボタン）を配置します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        # 1. 上部ツールバー（行追加ボタン）
        frm_toolbar: ttk.Frame = ttk.Frame(self)
        frm_toolbar.pack(side=tk.TOP, fill=tk.X, padx=3, pady=(2, 4))
        self.btn_add = ttk.Button(
            frm_toolbar,
            text="行追加",
            width=8,
            command=self.add_row,
        )
        self.btn_add.pack(side=tk.LEFT)

        # 2. セパレーター
        self.sep_device = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.sep_device.pack(side=tk.TOP, fill=tk.X, padx=3, pady=(2, 6))

        # 3. テーブルコンテナ（タイトル行および明細行配置フレーム）
        self.frm_rows = ttk.Frame(self)
        self.frm_rows.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        self.frm_rows.columnconfigure(0, weight=1, uniform="device_cols")
        self.frm_rows.columnconfigure(1, weight=2, uniform="device_cols")
        self.frm_rows.columnconfigure(2, weight=1, uniform="device_cols")
        self.frm_rows.columnconfigure(3, weight=2, uniform="device_cols")
        self.frm_rows.columnconfigure(4, weight=0)

        # タイトル行（Row 0）
        lbl_hdr_rack: ttk.Label = ttk.Label(self.frm_rows, text="ラック名", anchor=tk.W)
        lbl_hdr_rack.grid(row=0, column=0, sticky="ew", padx=2, pady=(0, 4))
        lbl_hdr_hostname: ttk.Label = ttk.Label(self.frm_rows, text="ホスト名", anchor=tk.W)
        lbl_hdr_hostname.grid(row=0, column=1, sticky="ew", padx=2, pady=(0, 4))
        lbl_hdr_model: ttk.Label = ttk.Label(self.frm_rows, text="機種名", anchor=tk.W)
        lbl_hdr_model.grid(row=0, column=2, sticky="ew", padx=2, pady=(0, 4))
        lbl_hdr_serial: ttk.Label = ttk.Label(self.frm_rows, text="S/N", anchor=tk.W)
        lbl_hdr_serial.grid(row=0, column=3, sticky="ew", padx=2, pady=(0, 4))
        lbl_hdr_action: ttk.Label = ttk.Label(self.frm_rows, text="操作", anchor=tk.CENTER, width=6)
        lbl_hdr_action.grid(row=0, column=4, sticky="ew", padx=2, pady=(0, 4))

        # 4. 下部フッター（保存ボタン）
        frm_footer: ttk.Frame = ttk.Frame(self)
        frm_footer.pack(side=tk.TOP, fill=tk.X, padx=3, pady=(6, 2))
        self.btn_save = ttk.Button(frm_footer, text="保存", width=12, command=self._on_save_click)
        self.btn_save.pack(side=tk.RIGHT)
    #endregion

    #region Public Methods
    def set_callbacks(
        self,
        on_save: Callable[[], None],
    ) -> None:
        """
        Summary:
            各種イベントコールバックを設定します。
        Description:
            保存ボタン押下時に呼び出す外部コールバック関数を登録します。
        Args:
            on_save: Callable[[], None] - 保存ボタン押下時コールバック。
        Returns:
            None - 戻り値なし。
        """
        self._on_save = on_save

    def add_row(
        self,
        rack_name: str = "",
        hostname: str = "",
        model_name: str = "",
        serial_number: str = "",
    ) -> FwsViewComponentChatTemplateDeviceRow:
        """
        Summary:
            明細行を1行追加します。
        Description:
            FwsViewComponentChatTemplateDeviceRow インスタンスを生成してテーブルグリッドに配置し、
            明細行リストへ登録してそのインスタンスを返却します。
        Args:
            rack_name: str - 初期表示ラック名（デフォルト ""）。
            hostname: str - 初期表示ホスト名（デフォルト ""）。
            model_name: str - 初期選択機種名（デフォルト ""）。
            serial_number: str - 初期表示シリアル番号（デフォルト ""）。
        Returns:
            FwsViewComponentChatTemplateDeviceRow - 生成された明細行インスタンス。
        """
        row: FwsViewComponentChatTemplateDeviceRow = FwsViewComponentChatTemplateDeviceRow(
            table=self,
            current_row=self._row_counter,
            rack_name=rack_name,
            hostname=hostname,
            model_name=model_name,
            serial_number=serial_number,
        )
        self._row_counter += 1
        self.rows.append(row)
        return row

    def clear_rows(self) -> None:
        """
        Summary:
            明細行をすべてクリアします。
        Description:
            登録されている全行インスタンスの delete メソッドを呼び出してウィジェットを破棄し、
            明細行リストを空にします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        for row in list(self.rows):
            row.delete()
        self.rows.clear()

    def get_data(self) -> list[dict[str, str]]:
        """
        Summary:
            全明細行の入力データを取得します。
        Description:
            現在表示されている各明細行インスタンスの get_data を呼び出し、
            ホスト名、機種名、S/Nの辞書リストとして返却します。
        Args:
            なし
        Returns:
            list[dict[str, str]] - 明細行データ辞書リスト。
        """
        return [row.get_data() for row in self.rows]

    def set_data(self, data_list: list[dict[str, str]]) -> None:
        """
        Summary:
            明細行データを一括設定します。
        Description:
            現在の全明細行をクリアした上で、渡されたデータリストを基に明細行を再生成します。
        Args:
            data_list: list[dict[str, str]] - 設定する明細行データの辞書リスト。
        Returns:
            None - 戻り値なし。
        """
        self.clear_rows()
        for item in data_list:
            self.add_row(
                rack_name=item.get("rack_name", ""),
                hostname=item.get("hostname", ""),
                model_name=item.get("model_name", ""),
                serial_number=item.get("serial_number", ""),
            )

    def set_model_candidates(self, candidates: list[str]) -> None:
        """
        Summary:
            機器機種候補リストを設定・更新します。
        Description:
            内部の model_candidates を更新し、表示中の全明細行インスタンスの選択肢に即座に反映します。
        Args:
            candidates: list[str] - 設定する機種名文字列のリスト。
        Returns:
            None - 戻り値なし。
        """
        self.model_candidates = list(candidates)
        for row in self.rows:
            row.set_model_candidates(self.model_candidates)
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
    #endregion


class FwsViewComponentChatTemplateDeviceRow:
    """
    Summary:
        機器情報テーブル明細行クラス。
    Description:
        テーブル内の1行分のウィジェット（ラック名Entry、ホスト名Entry、機種名Combobox、S/N Entry、削除Button）を管理し、
        データの取得、機種名候補の動的更新、および自身の破棄（self.delete）を自律的に行います。
    """

    #region Constructor
    def __init__(
        self,
        table: FwsViewComponentChatTemplateDeviceTable,
        current_row: int,
        rack_name: str = "",
        hostname: str = "",
        model_name: str = "",
        serial_number: str = "",
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            1行分のウィジェットを生成・初期化し、親テーブルのグリッド行に配置します。
            削除ボタン押下時のコマンドとして自身の delete メソッドを設定します。
        Args:
            table: FwsViewComponentChatTemplateDeviceTable - 所属する親テーブルインスタンス。
            current_row: int - グリッド配置先の行番号。
            rack_name: str - 初期表示ラック名（デフォルト ""）。
            hostname: str - 初期表示ホスト名（デフォルト ""）。
            model_name: str - 初期選択機種名（デフォルト ""）。
            serial_number: str - 初期表示シリアル番号（デフォルト ""）。
        Returns:
            None - 戻り値なし。
        """
        self.table: FwsViewComponentChatTemplateDeviceTable = table
        """FwsViewComponentChatTemplateDeviceTable - 所属する親テーブルインスタンス"""
        self.current_row: int = current_row
        """int - 配置先のグリッド行番号"""
        self.ent_rack_name: ttk.Entry = ttk.Entry(table.frm_rows)
        """ttk.Entry - ラック名入力テキストボックス"""
        self.ent_hostname: ttk.Entry = ttk.Entry(table.frm_rows)
        """ttk.Entry - ホスト名入力テキストボックス"""
        self.cmb_model: ttk.Combobox = ttk.Combobox(
            table.frm_rows,
            values=table.model_candidates,
        )
        """ttk.Combobox - 機種名選択コンボボックス"""
        self.ent_serial: ttk.Entry = ttk.Entry(table.frm_rows)
        """ttk.Entry - シリアル番号入力テキストボックス"""
        self.btn_delete: ttk.Button = ttk.Button(
            table.frm_rows,
            text="削除",
            width=6,
            command=self.delete,
        )
        """ttk.Button - 明細行削除ボタン"""

        self.ent_rack_name.insert(0, rack_name)
        self.ent_hostname.insert(0, hostname)
        self.cmb_model.set(model_name)
        self.ent_serial.insert(0, serial_number)

        self.ent_rack_name.grid(row=current_row, column=0, sticky="ew", padx=2, pady=2)
        self.ent_hostname.grid(row=current_row, column=1, sticky="ew", padx=2, pady=2)
        self.cmb_model.grid(row=current_row, column=2, sticky="ew", padx=2, pady=2)
        self.ent_serial.grid(row=current_row, column=3, sticky="ew", padx=2, pady=2)
        self.btn_delete.grid(row=current_row, column=4, sticky="ew", padx=2, pady=2)
    #endregion

    #region Public Methods
    def delete(self) -> None:
        """
        Summary:
            明細行を破棄します。
        Description:
            自身が保持する全ウィジェットを破棄し、親テーブルの rows リストから自身を除外します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self.ent_rack_name.destroy()
        self.ent_hostname.destroy()
        self.cmb_model.destroy()
        self.ent_serial.destroy()
        self.btn_delete.destroy()
        if self in self.table.rows:
            self.table.rows.remove(self)

    def get_data(self) -> dict[str, str]:
        """
        Summary:
            明細行の入力データを取得します。
        Description:
            ラック名、ホスト名、機種名、S/Nの各入力値の前後の空白を除去して辞書形式で返却します。
        Args:
            なし
        Returns:
            dict[str, str] - 明細行データ辞書（rack_name, hostname, model_name, serial_number）。
        """
        return {
            "rack_name": str(self.ent_rack_name.get()).strip(),
            "hostname": str(self.ent_hostname.get()).strip(),
            "model_name": str(self.cmb_model.get()).strip(),
            "serial_number": str(self.ent_serial.get()).strip(),
        }

    def set_model_candidates(self, candidates: list[str]) -> None:
        """
        Summary:
            機種名候補リストを更新します。
        Description:
            コンボボックスの選択肢（values）を最新の候補リストで更新します。
        Args:
            candidates: list[str] - 設定する機種名候補文字列リスト。
        Returns:
            None - 戻り値なし。
        """
        self.cmb_model.configure(values=candidates)
    #endregion
#endregion
