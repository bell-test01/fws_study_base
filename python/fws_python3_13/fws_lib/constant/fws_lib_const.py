"""
Summary:
    fws_lib パッケージ全体の定数モジュール。
Description:
    各アプリから横断的に参照されるライブラリ全体のバージョン情報や、
    共通の定数値（もしあれば）を一元管理します。
Attachment:
    なし
"""

"""str - ライブラリのバージョン情報 (Major.Minor.Patch.Revision)"""
LIB_VERSION: str = "1.1.0.0"

"""str - デフォルトのファイルエンコーディング"""
DEFAULT_ENCODING: str = "utf-8"

"""str - 共通エラーメッセージのプレフィックス"""
ERROR_PREFIX: str = "[FWS_LIB_ERROR]"
