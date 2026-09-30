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

def generate_timestamp_string() -> str:
    """
    Summary:
        現在時刻からファイル名等に利用可能なタイムスタンプ文字列を生成します。
    Description:
        'YYYYMMDD_HHMMSS' 形式の現在時刻文字列を返します。
    Args:
        None
    Returns:
        str - 生成されたタイムスタンプ文字列。
    """
    now = datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")
