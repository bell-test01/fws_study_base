"""
Summary:
    fws_lib パッケージ全体の定数モジュール。
Description:
    各アプリから横断的に参照されるライブラリ全体のバージョン情報や、
    共通の定数値（もしあれば）を一元管理します。
Attachment:
    なし
"""

#region constants
APP_VERSION: str = "1.8.1.0"
"""str - アプリケーション/ライブラリバージョン"""

LIB_VERSION: str = APP_VERSION
"""str - ライブラリバージョン（APP_VERSIONのエイリアス）"""

ENCODING_TYPE_UTF_8: str = "utf-8"
"""str - デフォルトのファイルエンコーディング"""

DEFAULT_ENCODING: str = ENCODING_TYPE_UTF_8
"""str - デフォルトエンコーディング（ENCODING_TYPE_UTF_8のエイリアス）"""

ERROR_PREFIX: str = "[FWS_LIB_ERROR]"
"""str - 共通エラーメッセージのプレフィックス"""
#endregion

