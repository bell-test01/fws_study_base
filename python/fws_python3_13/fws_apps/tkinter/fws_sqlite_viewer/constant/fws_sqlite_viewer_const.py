"""
Summary:
    fws_sqlite_viewer アプリの定数定義モジュール。
Description:
    アプリ内で使用する不変の値を定義します。
Attachment:
    なし
"""
from pathlib import Path

# アプリケーションのルートディレクトリ（このファイルから見て3階層上）
APP_DIR: Path = Path(__file__).resolve().parent.parent
"""Path - アプリケーションのルートディレクトリ"""

# アプリケーションのバージョン情報
APP_VERSION: str = "1.6.2.0"
"""str - アプリケーションのバージョン情報"""

# デフォルトのデータ・出力ディレクトリ
DATA_DIR: Path = APP_DIR / "data"
"""Path - データファイル格納ディレクトリ"""
OUTPUT_DIR: Path = APP_DIR / "output"
"""Path - 出力ファイル格納ディレクトリ"""

# ファイル名関連
SESSION_FILE_NAME: str = "session.json"
"""str - セッション情報の保存ファイル名"""

# UI定数
WINDOW_TITLE: str = "DBBrowser SQLite - fws_sqlite_viewer"
"""str - メインウィンドウのタイトル"""
WINDOW_MIN_WIDTH: int = 600
"""int - ウィンドウの最小幅"""
WINDOW_MIN_HEIGHT: int = 400
"""int - ウィンドウの最小高さ"""
STATUS_MESSAGE_TIMEOUT_MS: int = 3000
"""int - ステータスバーの一時メッセージ表示時間（ミリ秒）"""
STATUS_MSG_READY: str = "Status: Ready"
"""str - ステータスバーの初期/待機メッセージ"""

# カラー設定
COLOR_EVEN_ROW: str = "#f0f0f0"
"""str - ストライプ行（偶数）の背景色"""
COLOR_ODD_ROW: str = "#ffffff"
"""str - ストライプ行（奇数）の背景色"""
