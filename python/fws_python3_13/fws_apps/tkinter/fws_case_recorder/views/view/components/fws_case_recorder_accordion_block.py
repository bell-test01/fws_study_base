"""
Summary:
    fws_case_recorder アプリのアコーディオンブロックコンポーネント。
Description:
    案件入力および履歴表示で使用されるアコーディオン形式の共通UIコンポーネントです。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import ttk
from typing import Any

class FwsCaseRecorderAccordionBlock(ttk.Frame):
    """
    Summary:
        アコーディオンブロックコンポーネント。
    Description:
        県域、ビル名、案件番号、時間、ツールバー、テキストエリアを持つブロックを生成します。
    """

    def __init__(
        self,
        master: tk.Widget,
        block_id: int,
        region: str,
        building: str,
        case_number: str,
        record_time: str,
        content: str,
        display_header: str,
        is_active_mode: bool,
        **kwargs: Any
    ) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            アコーディオンブロック内の各種ウィジェットを初期化・配置します。
        Args:
            master: tk.Widget - 親ウィジェット。
            block_id: int - レコードID。
            region: str - 初期表示する県域。
            building: str - 初期表示するビル名。
            case_number: str - 初期表示する案件番号。
            record_time: str - 初期表示する時間。
            content: str - 初期表示するテキスト内容。
            display_header: str - ヘッダーに表示するテキスト。
            is_active_mode: bool - アクティブ記録用（左ペイン）の場合はTrue。
            **kwargs: Any - その他のFrameオプション。
        """
        super().__init__(master, **kwargs)
        
        self.block_id: int = block_id
        self.is_active_mode: bool = is_active_mode
        self.display_header: str = display_header
        
        self.is_expanded: tk.BooleanVar = tk.BooleanVar(value=is_active_mode)
        
        # ヘッダー
        self.frm_header: ttk.Frame = ttk.Frame(self)
        self.frm_header.pack(fill=tk.X)
        
        # コンテンツフレーム
        self.frm_content: ttk.LabelFrame = ttk.LabelFrame(self, text="") if is_active_mode else ttk.Frame(self)
        
        icon = "▼" if self.is_expanded.get() else "▶"
        self.btn_header: ttk.Button = ttk.Button(
            self.frm_header if is_active_mode else self,
            text=f"{icon} {self.display_header}",
            style="Left.TButton"
        )
        if is_active_mode:
            self.btn_header.pack(fill=tk.X)
            self.frm_content.pack(fill=tk.X)
        else:
            self.btn_header.pack(fill=tk.X)
        
        # 1行目: 県域・ビル名
        frm_row1: ttk.Frame = ttk.Frame(self.frm_content)
        frm_row1.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frm_row1, text="県域:").pack(side=tk.LEFT, padx=(0, 2))
        self.ent_region: ttk.Entry = ttk.Entry(frm_row1, width=8)
        self.ent_region.pack(side=tk.LEFT, padx=(0, 2))
        self.ent_region.insert(0, region)
        
        ttk.Label(frm_row1, text="ビル名:").pack(side=tk.LEFT, padx=(0, 2))
        self.ent_building: ttk.Entry = ttk.Entry(frm_row1, width=10)
        self.ent_building.pack(side=tk.LEFT, padx=(0, 2))
        self.ent_building.insert(0, building)
        
        # 2行目: 案件番号・時間
        frm_row2: ttk.Frame = ttk.Frame(self.frm_content)
        frm_row2.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(frm_row2, text="案件番号:").pack(side=tk.LEFT, padx=(0, 2))
        self.cmb_case_number: ttk.Combobox = ttk.Combobox(frm_row2, width=15)
        self.cmb_case_number.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        self.cmb_case_number.set(case_number)
        self.input_case = self.cmb_case_number
        ttk.Label(frm_row2, text="時間:").pack(side=tk.LEFT, padx=(0, 2))
        self.ent_record_time: ttk.Entry = ttk.Entry(frm_row2, width=15)
        self.ent_record_time.pack(side=tk.LEFT)
        self.ent_record_time.insert(0, record_time)
        
        if is_active_mode:
            self.var_time_check: tk.BooleanVar = tk.BooleanVar(value=False)
            self.chk_time: ttk.Checkbutton = ttk.Checkbutton(
                frm_row2, 
                text="更新", 
                variable=self.var_time_check
            )
            self.chk_time.pack(side=tk.LEFT, padx=(2, 8))
            
        # 3行目: ツールバー
        self.frm_toolbar: ttk.Frame = ttk.Frame(self.frm_content)
        self.frm_toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        self.btn_arrow_r: ttk.Button = ttk.Button(self.frm_toolbar, text="→", width=3)
        self.btn_arrow_r.pack(side=tk.LEFT, padx=(0, 2))
        
        self.btn_arrow_l: ttk.Button = ttk.Button(self.frm_toolbar, text="←", width=3)
        self.btn_arrow_l.pack(side=tk.LEFT, padx=(0, 2))
        
        self.btn_quote: ttk.Button = ttk.Button(self.frm_toolbar, text="---", width=4)
        self.btn_quote.pack(side=tk.LEFT, padx=(0, 2))
        
        self.btn_tmpl: ttk.Button = ttk.Button(self.frm_toolbar, text="定型文▼", width=7)
        self.btn_tmpl.pack(side=tk.LEFT, padx=(0, 2))
        
        self.btn_time: ttk.Button = ttk.Button(self.frm_toolbar, text="時刻挿入", width=8)
        self.btn_time.pack(side=tk.LEFT, padx=(0, 2))
        
        # 4行目: テキストエリア (折り返しなし + 縦横スクロールバー)
        height = 8 if is_active_mode else 6
        
        self.frm_text_container = ttk.Frame(self.frm_content)
        self.frm_text_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=(2, 0))
        
        self.txt_content: tk.Text = tk.Text(self.frm_text_container, height=height, undo=True, wrap="none")
        
        self.scr_content_y = ttk.Scrollbar(self.frm_text_container, orient=tk.VERTICAL, command=self.txt_content.yview)
        self.scr_content_x = ttk.Scrollbar(self.frm_text_container, orient=tk.HORIZONTAL, command=self.txt_content.xview)
        
        self.txt_content.configure(yscrollcommand=self.scr_content_y.set, xscrollcommand=self.scr_content_x.set)
        
        self.scr_content_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scr_content_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.txt_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # リサイズ用グリップ（つまみ）
        self.frm_resize_grip = tk.Frame(self.frm_content, height=4, cursor="sb_v_double_arrow", bg="gray")
        self.frm_resize_grip.pack(fill=tk.X, padx=5, pady=(0, 2))
        
        self.resize_start_y: int = 0
        self.resize_start_height: int = 0
        
        self.txt_content.insert("1.0", content)
        
        # 5行目: ボタン配置用コンテナ
        self.frm_buttons: ttk.Frame = ttk.Frame(self.frm_content)
        self.frm_buttons.pack(fill=tk.X, padx=5, pady=(2, 5))



    def update_header_text(self, new_text: str) -> None:
        """ヘッダーのテキストを更新します。"""
        self.display_header = new_text
        icon = "▼" if self.is_expanded.get() else "▶"
        self.btn_header.config(text=f"{icon} {self.display_header}")
