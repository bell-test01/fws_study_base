"""
Summary:
    fws_case_recorder アプリの定数定義モジュール。
Description:
    アプリ内で使用する不変の値を定義します。
Attachment:
    なし
"""
from pathlib import Path

# アプリケーションのルートディレクトリ（このファイルから見て2階層上）
APP_DIR: Path = Path(__file__).resolve().parent.parent
"""Path - アプリケーションのルートディレクトリ"""

# プロジェクトルートディレクトリ（fws_python3_13）
PROJECT_ROOT: Path = APP_DIR.parent.parent.parent
"""Path - プロジェクトルートディレクトリ"""

# アプリケーションのバージョン情報
APP_VERSION: str = "1.4.1.0"
"""str - アプリケーションのバージョン情報"""

# データベース関連
DB_DIR: Path = APP_DIR.parent.parent / "DB"
"""Path - DBファイル格納ディレクトリ（fws_apps/DB/）"""
DB_FILE_NAME: str = "fws_case_recorder.db"
"""str - データベースファイル名"""
DB_PATH: Path = DB_DIR / DB_FILE_NAME
"""Path - データベースファイルのフルパス"""

# DDLファイル関連
DATA_DIR: Path = APP_DIR / "data"
"""Path - データファイル格納ディレクトリ"""
DDL_FILE_NAME: str = "fws_case_recorder_ddl.sql"
"""str - DDLファイル名"""
DDL_PATH: Path = DATA_DIR / DDL_FILE_NAME
"""Path - DDLファイルのフルパス"""

# UI定数
WINDOW_TITLE: str = "案件記録 - fws_case_recorder"
"""str - メインウィンドウのタイトル"""
WINDOW_MIN_WIDTH: int = 400
"""int - ウィンドウの最小幅"""
WINDOW_MIN_HEIGHT: int = 250
"""int - ウィンドウの最小高さ"""
WINDOW_DEFAULT_WIDTH: int = 480
"""int - ウィンドウのデフォルト幅"""
WINDOW_DEFAULT_HEIGHT: int = 270
"""int - ウィンドウのデフォルト高さ"""

# ステータスバー
STATUS_MESSAGE_TIMEOUT_MS: int = 3000
"""int - ステータスバーの一時メッセージ表示時間（ミリ秒）"""
STATUS_MSG_READY: str = "Status: Ready"
"""str - ステータスバーの初期/待機メッセージ"""

# 入力補助記号
SYMBOL_ARROW_RIGHT: str = "→"
"""str - 右矢印記号"""
SYMBOL_ARROW_LEFT: str = "←"
"""str - 左矢印記号"""
SYMBOL_QUOTE_LINE: str = "-------------------------"
"""str - 引用線記号"""

# ペイン比率
LEFT_PANE_MIN_WIDTH: int = 200
"""int - 左ペインの最小幅"""
RIGHT_PANE_MIN_WIDTH: int = 150
"""int - 右ペインの最小幅"""
