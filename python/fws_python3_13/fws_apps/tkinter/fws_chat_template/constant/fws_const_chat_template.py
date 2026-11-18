"""
Summary:
    fws_const_chat_template 定数定義および初期設定モジュール。
Description:
    fws_chat_template アプリ全体で使用する定数、パス管理変数、およびロガー・セッション・メッセージの初期設定関数を提供します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
from pathlib import Path
from typing import Any

from fws_lib.common import (
    fws_file_util,
    fws_json_util,
    fws_logger_util,
)
from fws_lib.database import fws_sqlite_util
from fws_lib.tkinter.views.logic import fws_logic_lib_event_exception_util
#endregion

#region constants
#------------------------------------------------------------------------------
# アプリケーション管理値
#------------------------------------------------------------------------------
APP_VERSION: str = "0.15.0.1"
"""str - アプリケーションバージョン"""
APP_NAME_ENGLISH: str = "fws_chat_template"
"""str - アプリケーション英語名称"""
FILE_NAME_INIT_DB_SQL: str = "init_db.sql"
"""str - データベース初期化SQLファイル名"""
APP_LOGGER: fws_logger_util.FwsLoggerUtil = fws_logger_util.FwsLoggerUtil()
"""fws_logger_util.FwsLoggerUtil - アプリケーション共通ロガーインスタンス"""
APP_EVENT_EXCEPTION: fws_logic_lib_event_exception_util.FwsLogicLibEventExceptionUtil = (
    fws_logic_lib_event_exception_util.FwsLogicLibEventExceptionUtil()
)
"""fws_logic_lib_event_exception_util.FwsLogicLibEventExceptionUtil - イベント例外ハンドリングデコレータインスタンス"""

APP_FONT_NAME: str = "Meiryo UI"
"""str - アプリケーション標準フォント名"""
DEFAULT_APP_FONT_SIZE: int = 9
"""int - アプリケーション標準フォントサイズ（デフォルト値）"""
MIN_APP_FONT_SIZE: int = 6
"""int - アプリケーション標準フォントサイズ（最小値）"""
MAX_APP_FONT_SIZE: int = 32
"""int - アプリケーション標準フォントサイズ（最大値）"""

DEFAULT_DESC_TEXT_HEIGHT: int = 20
"""int - Descriptionテキストエリアのデフォルト初期行数"""

VIEW_NAME_FWS_VIEW_CHAT_TEMPLATE: str = "fws_view_chat_template"
"""str - メイン画面ビュー識別名"""

#------------------------------------------------------------------------------
# メッセージキー定数
#------------------------------------------------------------------------------
MSG_STATUS_READY: str = "MSG_STATUS_READY"
"""str - 待機中ステータスメッセージID"""
MSG_STATUS_COMPARING: str = "MSG_STATUS_COMPARING"
"""str - WinMerge起動中ステータスメッセージID"""
MSG_ERR_WINMERGE_NOT_FOUND: str = "MSG_ERR_WINMERGE_NOT_FOUND"
"""str - WinMerge未検出エラーメッセージID"""
MSG_ERR_COMPARE_NO_DB_RECORD: str = "MSG_ERR_COMPARE_NO_DB_RECORD"
"""str - 比較対象DBレコード未存在エラーメッセージID"""
MSG_ERR_INVALID_FONT_SIZE: str = "MSG_ERR_INVALID_FONT_SIZE"
"""str - 不正フォントサイズ入力エラーメッセージID"""

#------------------------------------------------------------------------------
# パス管理変数
#------------------------------------------------------------------------------
DIR_PROJECT: Path = Path()
"""Path - プロジェクトルートディレクトリ"""
DIR_APP: Path = Path()
"""Path - アプリケーションルートディレクトリ"""
DIR_DB: Path = Path()
"""Path - データベース共通ディレクトリ"""
PATH_APP_DB_FILE: Path = Path()
"""Path - アプリケーション専用DBファイルパス"""
DIR_APP_DATA: Path = Path()
"""Path - アプリケーションデータディレクトリ"""
PATH_APP_SESSION_FILE: Path = Path()
"""Path - セッション設定ファイルパス"""
PATH_APP_MESSAGES_FILE: Path = Path()
"""Path - メッセージ設定ファイルパス"""
DIR_APP_OUTPUT: Path = Path()
"""Path - アプリケーション出力ディレクトリ"""
DIR_APP_TMP: Path = Path()
"""Path - アプリケーション一時ファイルディレクトリ"""
DIR_APP_LOG: Path = Path()
"""Path - アプリケーションログディレクトリ"""
PATH_APP_LOG_FILE: Path = Path()
"""Path - アプリケーション専用ログファイルパス"""

#------------------------------------------------------------------------------
# セッション設定キー定数
#------------------------------------------------------------------------------
SESSION_KEY_GEOMETRY: str = "geometry"
"""str - ウィンドウジオメトリのキー"""
DEFAULT_MAIN_GEOMETRY: str = "780x480"
"""str - メイン画面デフォルトジオメトリ"""
SESSION_KEY_FONT_SIZE: str = "font_size"
"""str - 画面フォントサイズのセッションキー"""
SESSION_KEY_WINMERGE_PATH: str = "winmerge_path"
"""str - WinMerge実行ファイルパスのセッションキー"""
DEFAULT_WINMERGE_PATH: str = "C:\\Program Files\\WinMerge\\WinMergeU.exe"
"""str - 64bit WinMergeデフォルトパス"""
DEFAULT_WINMERGE_PATH_X86: str = "C:\\Program Files (x86)\\WinMerge\\WinMergeU.exe"
"""str - 32bit WinMergeデフォルトパス"""
SESSION_DATA: dict[str, Any] = {}
"""dict[str, Any] - セッションデータメモリ保持用辞書"""

#------------------------------------------------------------------------------
# メッセージ管理辞書
#------------------------------------------------------------------------------
MESSAGES_DATA: dict[str, str] = {}
"""dict[str, str] - メッセージデータメモリ保持用辞書"""
#endregion

#region Public Methods
def initialize_application(project_dir: Path, app_dir: Path) -> None:
    """
    Summary:
        アプリケーションの全体初期化を実行します。
    Description:
        ルートディレクトリ設定、ロギング設定、イベント例外ハンドラ設定、セッションファイル読み込み、
        メッセージファイル読み込み、およびデータベース初期化を順次実行します。
    Args:
        project_dir: Path - プロジェクトのルートディレクトリパス。
        app_dir: Path - アプリケーションのルートディレクトリパス。
    Returns:
        None - 戻り値なし。
    """
    setup_app_dir(project_dir, app_dir)
    setup_logger()
    setup_event_exception()
    setup_session_file_data()
    setup_messages()
    _create_init_db_file()


def setup_app_dir(project_dir: Path, app_dir: Path) -> None:
    """
    Summary:
        アプリケーションのルートディレクトリおよび関連パスを設定します。
    Description:
        エントリーポイントから渡されたパスを基に各ディレクトリやファイルのパス管理変数を設定します。
    Args:
        project_dir: Path - プロジェクトのルートディレクトリパス。
        app_dir: Path - アプリケーションのルートディレクトリパス。
    Returns:
        None - 戻り値なし。
    """
    global DIR_PROJECT \
        ,DIR_APP \
        ,DIR_DB \
        ,PATH_APP_DB_FILE \
        ,DIR_APP_DATA \
        ,PATH_APP_SESSION_FILE \
        ,PATH_APP_MESSAGES_FILE \
        ,DIR_APP_OUTPUT,DIR_APP_TMP,DIR_APP_LOG \
        ,PATH_APP_LOG_FILE

    DIR_PROJECT = project_dir
    DIR_APP = app_dir

    DIR_DB = DIR_APP.parent.parent / "DB"
    PATH_APP_DB_FILE = DIR_DB / f"{APP_NAME_ENGLISH}.db"

    DIR_APP_DATA = DIR_APP / "data"
    PATH_APP_SESSION_FILE = DIR_APP_DATA / "session.json"
    PATH_APP_MESSAGES_FILE = DIR_APP_DATA / "messages.json"

    DIR_APP_OUTPUT = DIR_APP / "output"
    DIR_APP_TMP = DIR_APP_OUTPUT / "tmp"
    if not fws_file_util.is_dir(DIR_APP_TMP):
        fws_file_util.create_dir(DIR_APP_TMP)

    DIR_APP_LOG = DIR_APP / "log"
    PATH_APP_LOG_FILE = DIR_APP_LOG / f"{APP_NAME_ENGLISH}.log"


def setup_logger() -> None:
    """
    Summary:
        ロガーの初期設定を実行します。
    Description:
        ログディレクトリを作成し、アプリケーション用の共通ロガーを設定します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    if not fws_file_util.is_dir(DIR_APP_LOG):
        fws_file_util.create_dir(DIR_APP_LOG)
    global APP_LOGGER
    APP_LOGGER = fws_logger_util.FwsLoggerUtil(
        logger_name=APP_NAME_ENGLISH,
        log_file_path=PATH_APP_LOG_FILE,
        log_level=fws_logger_util.FwsLogLevelEnum.INFO,
        is_enable_console=True,
    )


def setup_event_exception() -> None:
    """
    Summary:
        イベント例外ハンドラの初期設定を実行します。
    Description:
        ロガーとアプリケーション名をイベント例外ハンドラに紐付けます。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    global APP_EVENT_EXCEPTION
    APP_EVENT_EXCEPTION = fws_logic_lib_event_exception_util.FwsLogicLibEventExceptionUtil(
        fws_logger_util_obj=APP_LOGGER,
    )


def setup_session_file_data() -> None:
    """
    Summary:
        セッション設定ファイルを読み込みます。
    Description:
        session.json を読み込み、メモリ上の SESSION_DATA に展開します。
        ファイルが存在しない場合は空のファイルを作成します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    global SESSION_DATA
    if not fws_file_util.is_file(PATH_APP_SESSION_FILE):
        if not fws_file_util.is_dir(DIR_APP_DATA):
            fws_file_util.create_dir(DIR_APP_DATA)
        fws_json_util.save_json(PATH_APP_SESSION_FILE, {})
    SESSION_DATA = fws_json_util.load_json(PATH_APP_SESSION_FILE)


def setup_messages() -> None:
    """
    Summary:
        メッセージ設定ファイルを読み込みます。
    Description:
        messages.json を読み込み、メモリ上の MESSAGES_DATA に展開します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    global MESSAGES_DATA
    if fws_file_util.is_file(PATH_APP_MESSAGES_FILE):
        MESSAGES_DATA = fws_json_util.load_json(PATH_APP_MESSAGES_FILE)
    else:
        MESSAGES_DATA = {}


def get_message(message_key: str) -> str:
    """
    Summary:
        メッセージキーに対応する文言を取得します。
    Description:
        MESSAGES_DATA からメッセージ文字列を取得し、未定義の場合はキー名をそのまま返却します。
    Args:
        message_key: str - メッセージキー。
    Returns:
        str - メッセージ文言。
    """
    return MESSAGES_DATA.get(message_key, message_key)


def save_session_file_data() -> None:
    """
    Summary:
        現在のセッションデータをファイルへ保存します。
    Description:
        メモリ上に保持されている SESSION_DATA の辞書内容を session.json ファイルへ書き出します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    fws_json_util.save_json(PATH_APP_SESSION_FILE, SESSION_DATA)


def load_window_geometry(window_key: str) -> str:
    """
    Summary:
        ウィンドウサイズをセッションデータから取得します。
    Description:
        指定された画面キーのサイズを取得し、未設定の場合はデフォルト値（DEFAULT_MAIN_GEOMETRY）を返却します。
    Args:
        window_key: str - 画面識別キー。
    Returns:
        str - 復元対象のジオメトリ文字列。
    """
    geometry_dict: dict[str, Any] = SESSION_DATA.get(SESSION_KEY_GEOMETRY, {})
    return str(geometry_dict.get(window_key, DEFAULT_MAIN_GEOMETRY))


def save_window_geometry(window_key: str, window_width: int, window_height: int) -> None:
    """
    Summary:
        ウィンドウサイズをセッションファイルへ保存します。
    Description:
        指定された画面キーに対応するウィンドウサイズ（幅x高さ）をセッションデータに記録し、session.json を更新します。
    Args:
        window_key: str - 画面識別キー。
        window_width: int - ウィンドウの幅。
        window_height: int - ウィンドウの高さ。
    Returns:
        None - 戻り値なし。
    """
    if SESSION_KEY_GEOMETRY not in SESSION_DATA:
        SESSION_DATA[SESSION_KEY_GEOMETRY] = {}
    SESSION_DATA[SESSION_KEY_GEOMETRY][window_key] = f"{window_width}x{window_height}"
    save_session_file_data()


def load_font_size() -> int:
    """
    Summary:
        セッションデータから画面フォントサイズを取得します。
    Description:
        session.json に保存されている font_size を取得します。
        未設定または正の範囲外（MIN_APP_FONT_SIZE未満またはMAX_APP_FONT_SIZE超過）の場合はデフォルト値を返却します。
    Args:
        なし
    Returns:
        int - フォントサイズ。
    """
    raw_size: Any = SESSION_DATA.get(SESSION_KEY_FONT_SIZE)
    if raw_size is not None:
        try:
            size_int: int = int(raw_size)
            if MIN_APP_FONT_SIZE <= size_int <= MAX_APP_FONT_SIZE:
                return size_int
        except (ValueError, TypeError):
            pass
    return DEFAULT_APP_FONT_SIZE


def save_font_size(font_size: int) -> None:
    """
    Summary:
        フォントサイズをセッションファイルへ保存します。
    Description:
        指定されたフォントサイズをセッションデータに記録し、session.json を更新します。
    Args:
        font_size: int - 保存するフォントサイズ。
    Returns:
        None - 戻り値なし。
    """
    SESSION_DATA[SESSION_KEY_FONT_SIZE] = font_size
    save_session_file_data()


def save_winmerge_path(winmerge_path: str) -> None:
    """
    Summary:
        WinMergeの実行ファイルパスをセッションファイルへ保存します。
    Description:
        指定されたWinMergeパス文字列をセッションデータに記録し、session.json を更新します。
    Args:
        winmerge_path: str - 保存するWinMerge実行ファイルパス。
    Returns:
        None - 戻り値なし。
    """
    SESSION_DATA[SESSION_KEY_WINMERGE_PATH] = winmerge_path.strip()
    save_session_file_data()


def load_winmerge_path() -> str:
    """
    Summary:
        セッションデータからWinMerge実行ファイルパスを取得します。
    Description:
        session.json に保存されている winmerge_path を取得します。
        未設定または空文字の場合はデフォルトパス（DEFAULT_WINMERGE_PATH）を返却します。
    Args:
        なし
    Returns:
        str - WinMerge実行ファイルパス。
    """
    saved_path: str = str(SESSION_DATA.get(SESSION_KEY_WINMERGE_PATH, "")).strip()
    return saved_path if saved_path else DEFAULT_WINMERGE_PATH


def get_winmerge_path() -> Path:
    """
    Summary:
        WinMergeの実行ファイルパスを取得します。
    Description:
        session.json に保存されている winmerge_path を最優先で取得します。
        未設定または存在しない場合は、標準の64bitインストール先、次いで32bitインストール先を確認し、
        実在するパスを返却します。いずれも見つからない場合はデフォルトパスを返却します。
    Args:
        なし
    Returns:
        Path - WinMerge実行ファイルのパス。
    """
    saved_path_str: str = str(SESSION_DATA.get(SESSION_KEY_WINMERGE_PATH, "")).strip()
    if saved_path_str:
        saved_path: Path = Path(saved_path_str)
        if fws_file_util.is_file(saved_path):
            return saved_path

    path_64: Path = Path(DEFAULT_WINMERGE_PATH)
    if fws_file_util.is_file(path_64):
        return path_64

    path_x86: Path = Path(DEFAULT_WINMERGE_PATH_X86)
    if fws_file_util.is_file(path_x86):
        return path_x86

    return path_64

#endregion

#region Private Methods
def _create_init_db_file() -> None:
    """
    Summary:
        初期データベースファイルを生成し初期化SQLを実行します。
    Description:
        DBディレクトリとDBファイルを生成・初期化し、data/init_db.sql を読み込んでテーブルスキーマ構築および初期マスタデータを投入します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    sql_path: Path = DIR_APP_DATA / FILE_NAME_INIT_DB_SQL
    if not fws_file_util.is_file(sql_path):
        return

    if not fws_file_util.is_dir(DIR_DB):
        fws_file_util.create_dir(DIR_DB)

    if not fws_file_util.is_file(PATH_APP_DB_FILE):
        fws_file_util.create_empty_file(PATH_APP_DB_FILE)

    sql_text: str = fws_file_util.read_text_all(sql_path)
    with fws_sqlite_util.FwsSqliteUtil(PATH_APP_DB_FILE) as fws_sqlite_util_obj:
        fws_sqlite_util_obj.execute_script(sql_text)

#endregion
