"""
Summary:
    fws_lib 共通の文字列・データ操作モジュール。
Description:
    文字列の検証、日付・タイムスタンプ文字列の生成などの汎用処理を提供します。
Attachment:
    なし
"""
from typing import Optional
from datetime import datetime
from typing import Literal

DateTimeFormatType = Literal[
    # --- 日付＋時刻 ---
    "%Y-%m-%d %H:%M:%S",      # 例: 2026-10-26 02:15:30 (標準・DB・ログ用)
    "%Y/%m/%d %H:%M:%S",      # 例: 2026/10/26 02:15:30 (日本で一般的な表示形式)
    "%Y-%m-%dT%H:%M:%S",      # 例: 2026-10-26T02:15:30 (ISO 8601形式)
    "%Y-%m-%d %H:%M:%S.%f",   # 例: 2026-10-26 02:15:30.123456 (ミリ秒・詳細ログ用)
    # --- ファイル名・ID用（記号なし） ---
    "%Y%m%d_%H%M%S",          # 例: 20261026_021530 (バックアップ・ログファイル名用)
    "%Y%m%d%H%M%S",           # 例: 20261026021530 (14桁コンパクト形式)
    "%Y%m%d",                 # 例: 20261026 (日付のみコンパクト形式)
    # --- 日付のみ ---
    "%Y-%m-%d",               # 例: 2026-10-26 (ISO標準)
    "%Y/%m/%d",               # 例: 2026/10/26 (本プロジェクトの基準日フォーマット)
    # --- 時刻のみ ---
    "%H:%M:%S",               # 例: 02:15:30
    "%H%M%S",                 # 例: 021530
    # --- 日本語表記（表示・帳票用） ---
    "%Y年%m月%d日",           # 例: 2026年10月26日
    "%Y年%m月%d日 %H時%M分%S秒", # 例: 2026年10月26日 02時15分30秒
]

def is_empty_or_whitespace(text: Optional[str]) -> bool:
    """
    Summary:
        文字列が空、または空白文字のみで構成されているかを判定します。
    Description:
        入力が None の場合、または strip() の結果が空文字列の場合に True を返します。
    Args:
        text: Optional[str] - 判定対象の文字列。
    Returns:
        bool - 空または空白のみの場合は True、それ以外は False。
    """
    if text is None:
        return True
    return text.strip() == ""

def get_datetime_to_format_string(datetime_format_type:DateTimeFormatType,target_datetime:datetime = datetime.now()):
    """
    Summary:
        現在時刻を指定されたフォーマットの文字列として返します。
    Description:
        デフォルトでは '%Y-%m-%d %H:%M:%S' 形式で返します。
    Args:
        datetime_format_type: DateTimeFormatType - 日時フォーマットタイプ。
        target_datetime: datetime - 変換対象の日時。
    Returns:
        str - フォーマットされたタイムスタンプ文字列。
    """
    return target_datetime.strftime(datetime_format_type)