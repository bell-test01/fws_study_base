"""
Summary:
    FWSロギングおよび未捕捉例外ハンドリング統合ユーティリティモジュール。
Description:
    ファイル出力（UTF-8追記対応）およびコンソール出力をサポートする軽量ロガー、
    アプリ全体への自動ロギング一括適用窓口（enable_auto_log）、
    およびCLI・スレッド・Tkinter未捕捉例外グローバルハンドラ（setup_global_exception_handler）を提供します。
Attachment:
    なし
"""
#region imports
from enum import StrEnum
import functools
import importlib
import inspect
import logging
from pathlib import Path
import sys
import threading
import traceback
from types import ModuleType, TracebackType
from typing import Any, Optional, Union
#endregion

#region constants
WRAPS_FUNC_KEY: str = "_is_wrap_output_start_end_log"
#endregion

#region enum
class FwsLogLevelEnum(StrEnum):
    """
    Summary:
        ロギングレベル列挙型クラス。
    Description:
        FwsLoggerUtil で指定可能なログレベルの定数文字列を提供します。
        StrEnum を継承しているため、文字列としてもそのまま利用可能です。
    """
    DEBUG = "DEBUG"
    """str - デバッグレベル（詳細情報）"""
    INFO = "INFO"
    """str - 情報レベル（通常動作ログ）"""
    WARNING = "WARNING"
    """str - 警告レベル（注意が必要な事象）"""
    ERROR = "ERROR"
    """str - エラーレベル（処理の失敗）"""
    CRITICAL = "CRITICAL"
    """str - 致命的エラーレベル（システム停止等）"""
#endregion

#region classes
class FwsLoggerUtil:
    """
    Summary:
        FWSロギングユーティリティクラス。
    Description:
        logging.Loggerをラップし、UTF-8ファイルハンドラ（FileHandler）および
        コンソールハンドラ（標準エラー出力）へのログ出力を提供します。
        動詞始まりのログ出力メソッド（output_info, output_warning, output_error,
        output_debug, output_critical）、アプリ全体への自動ロギング一括適用窓口（enable_auto_log）、
        およびCLI・ワーカースレッド・Tkinterの未捕捉例外自動ロギング（setup_global_exception_handler）を備えます。
    """

    #region Constructor
    def __init__(
        self,
        logger_name: str = "",
        log_file_path: Path = Path(),
        log_level: FwsLogLevelEnum = FwsLogLevelEnum.INFO,
        is_enable_console: bool = False,
    ) -> None:
        """
        Summary:
            ロガーインスタンスを初期化し、ファイルおよびコンソールハンドラを設定します。
        Description:
            指定されたログファイルパスへのファイル追記出力および
            コンソール（標準エラー出力）へのハンドラを設定します。
            既存のハンドラが登録されている場合は重複を防ぐためクリアします。
        Args:
            logger_name: str - ロガーの識別名（デフォルト: ""）。
            log_file_path: Path - ログファイルの出力先パス（デフォルト: Path()、空パスの場合はファイル出力なし）。
            log_level: FwsLogLevelEnum - ロギングレベル（デフォルト: FwsLogLevelEnum.INFO）。
            is_enable_console: bool - コンソール（sys.stderr）出力の有効フラグ（デフォルト: False）。
        Returns:
            None - 戻り値なし。
        """
        self._logger: logging.Logger = logging.getLogger(logger_name)
        """logging.Logger - 内部標準ロガーインスタンス"""

        if self._logger.hasHandlers():
            self._logger.handlers.clear()

        self._logger.setLevel(log_level)
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s\t[%(levelname)s]\t[%(threadName)s]\t%(name)s\t%(message)s"
        )

        # ファイルパス指定判定
        if log_file_path != Path():
            target_path: Path = Path(log_file_path)
            if target_path.parent and not target_path.parent.exists():
                target_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler: logging.FileHandler = logging.FileHandler(
                filename=str(target_path),
                mode="a",
                encoding="utf-8",
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

        # コンソール出力判定
        if is_enable_console:
            console_handler: logging.StreamHandler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)
    #endregion

    #region Public Methods
    def output_info(self, msg: object, *args: object, **kwargs: Any) -> None:
        """
        Summary:
            INFOレベルのログを出力します。
        Description:
            通常動作情報メッセージを指定フォーマットでログに出力します。
        Args:
            msg: object - ログメッセージ。
            *args: object - 可変長引数。
            **kwargs: Any - キーワード引数。
        Returns:
            None - 戻り値なし。
        """
        self._logger.info(msg, *args, **kwargs)

    def output_warning(self, msg: object, *args: object, **kwargs: Any) -> None:
        """
        Summary:
            WARNINGレベルのログを出力します。
        Description:
            警告メッセージを指定フォーマットでログに出力します。
        Args:
            msg: object - ログメッセージ。
            *args: object - 可変長引数。
            **kwargs: Any - キーワード引数。
        Returns:
            None - 戻り値なし。
        """
        self._logger.warning(msg, *args, **kwargs)

    def output_error(self, msg: object, *args: object, **kwargs: Any) -> None:
        """
        Summary:
            ERRORレベルのログを出力します。
        Description:
            エラー発生メッセージを指定フォーマットでログに出力します。
        Args:
            msg: object - ログメッセージ。
            *args: object - 可変長引数。
            **kwargs: Any - キーワード引数。
        Returns:
            None - 戻り値なし。
        """
        self._logger.error(msg, *args, **kwargs)

    def output_debug(self, msg: object, *args: object, **kwargs: Any) -> None:
        """
        Summary:
            DEBUGレベルのログを出力します。
        Description:
            開発・デバッグ用詳細メッセージを指定フォーマットでログに出力します。
        Args:
            msg: object - ログメッセージ。
            *args: object - 可変長引数。
            **kwargs: Any - キーワード引数。
        Returns:
            None - 戻り値なし。
        """
        self._logger.debug(msg, *args, **kwargs)

    def output_critical(self, msg: object, *args: object, **kwargs: Any) -> None:
        """
        Summary:
            CRITICALレベルのログを出力します。
        Description:
            致命的エラーメッセージを指定フォーマットでログに出力します。
        Args:
            msg: object - ログメッセージ。
            *args: object - 可変長引数。
            **kwargs: Any - キーワード引数。
        Returns:
            None - 戻り値なし。
        """
        self._logger.critical(msg, *args, **kwargs)



#-------------------------------------------------------
#以下は、実装中のロジック
#-------------------------------------------------------
    def enable_auto_log(
        self,
        app_path: Path,
        project_root: Path,
        log_internal: bool = False,
    ) -> None:
        """
        Summary:
            指定されたアプリケーションディレクトリ配下の全モジュール・全関数・全クラスに対して自動ロギングを一括適用します。
        Description:
            project_root から app_path.parent までのプレフィックス文字列（mod_prefix）を事前に算出した上で、
            app_path 配下のすべての Python ファイル（*.py、__init__.py は除外）について
            project_root 基準の相対パスから完全修飾モジュール名（mod_name）を生成し、importlib.import_module でインポートします。
            あわせて mod_name から mod_prefix を除去してアプリ名始まりのモジュール名（app_mod_name）を生成し、
            取得した各サブモジュールに対して _wrap_module を呼び出し、モジュール直下関数および
            自モジュール内クラスメソッドに自動ロギングを適用します。
        Args:
            app_path: Path - アプリケーションのルートディレクトリパス。
            project_root: Path - プロジェクトのルートディレクトリパス。
            log_internal: bool - アンダースコア始まりの内部関数・内部メソッドをログ対象に含めるフラグ（デフォルト: False）。
        Returns:
            None - 戻り値なし。
        """
        prefix_parts: tuple[str, ...] = (
            app_path.resolve().parent.relative_to(project_root.resolve()).parts
        )
        mod_prefix: str = ".".join(prefix_parts) + "." if prefix_parts else ""

        # プロジェクトルートと紐付けたモジュール名を生成してインポート
        # app_pathより再帰的に*.pyファイルを検索
        for py_file in sorted(app_path.rglob("*.py")):
            # __init__.pyファイル判定
            if py_file.name == "__init__.py":
                # __init__.pyファイルはインポートしない
                continue

            # モジュール名生成
            rel_path: Path = py_file.resolve().relative_to(project_root.resolve())
            mod_name: str = ".".join(rel_path.with_suffix("").parts)
            app_mod_name: str = mod_name.removeprefix(mod_prefix)
            # モジュールのインポートを実行し、インポートオブジェクトを取得
            submodule: ModuleType = importlib.import_module(mod_name)
            # インポートをしたモジュール内の関数に自動ロギングを適用
            self._wrap_module(submodule, app_mod_name, log_internal=log_internal)

    def setup_global_exception_handler(self) -> None:
        """
        Summary:
            未捕捉例外（クラッシュ時）を自動捕捉してログ出力するグローバルハンドラを設定します。
        Description:
            sys.excepthook、threading.excepthook、および tkinter.Tk.report_callback_exception にカスタムハンドラを登録し、
            アプリケーション内（CLI/メイン処理、マルチスレッド処理、GUIイベントコールバック）で
            キャッチされずに漏れた例外を本ロガーの出力先（ファイル・コンソール）へ
            完全なスタックトレース付きで [CRITICAL] ログとして自動記録します。
            KeyboardInterrupt は通常中断とみなしログ出力を行わずに元のハンドラへ委譲します。
            ログ記録後は元のハンドラを呼び出して Python および Tkinter の標準挙動を維持します。
            tkinter が利用できない環境では ImportError を安全に無視します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        original_sys_excepthook: Any = sys.excepthook
        original_threading_excepthook: Any = threading.excepthook

        def _handle_uncaught_exception(
            exc_type: type[BaseException],
            exc_value: BaseException,
            exc_traceback: Optional[TracebackType],
        ) -> None:
            if issubclass(exc_type, KeyboardInterrupt):
                original_sys_excepthook(exc_type, exc_value, exc_traceback)
                return

            formatted_tb: list[str] = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            tb_text: str = "".join(formatted_tb).rstrip()
            self.output_critical(
                f"[UNCAUGHT_EXCEPTION] {exc_type.__name__}: {exc_value}\n{tb_text}"
            )
            original_sys_excepthook(exc_type, exc_value, exc_traceback)

        def _handle_threading_exception(args: threading.ExceptHookArgs) -> None:
            if args.exc_type is not None and issubclass(args.exc_type, KeyboardInterrupt):
                original_threading_excepthook(args)
                return

            formatted_tb: list[str] = traceback.format_exception(
                args.exc_type, args.exc_value, args.exc_traceback
            )
            tb_text: str = "".join(formatted_tb).rstrip()
            thread_name: str = args.thread.name if args.thread else "UnknownThread"
            exc_name: str = (
                args.exc_type.__name__ if args.exc_type is not None else "Exception"
            )
            self.output_critical(
                f"[UNCAUGHT_THREAD_EXCEPTION] [{thread_name}] {exc_name}: {args.exc_value}\n{tb_text}"
            )
            original_threading_excepthook(args)

        sys.excepthook = _handle_uncaught_exception
        threading.excepthook = _handle_threading_exception

        # 3. Tkinter GUIコールバックの未捕捉例外ハンドラ（GUI操作時のエラーをキャッチ）
        try:
            import tkinter as tk

            original_tk_report: Any = tk.Tk.report_callback_exception

            def _handle_tk_exception(
                self_tk: Any,
                exc_type: type[BaseException],
                exc_value: BaseException,
                exc_traceback: Optional[TracebackType],
            ) -> None:
                if issubclass(exc_type, KeyboardInterrupt):
                    original_tk_report(self_tk, exc_type, exc_value, exc_traceback)
                    return

                formatted_tb: list[str] = traceback.format_exception(
                    exc_type, exc_value, exc_traceback
                )
                tb_text: str = "".join(formatted_tb).rstrip()
                self.output_critical(
                    f"[UNCAUGHT_TKINTER_EXCEPTION] {exc_type.__name__}: {exc_value}\n{tb_text}"
                )
                original_tk_report(self_tk, exc_type, exc_value, exc_traceback)

            tk.Tk.report_callback_exception = _handle_tk_exception
        except ImportError:
            pass
    #endregion

    #region Private Methods
    def _wrap_module(
        self,
        submodule: ModuleType,
        app_mod_name: str,
        log_internal: bool = False,
    ) -> None:
        """
        Summary:
            モジュール直下の関数群および自モジュール内で定義されたクラスのメソッド群に自動ロギングラッパーを適用します。
        Description:
            モジュール自身に対して app_mod_name を渡して _wrap_attributes を呼び出しモジュール直下のトップレベル関数群をラップした後、
            自モジュール内で定義された各クラス（getattr(attr_value, "__module__", None) == submodule.__name__）に対しても
            app_mod_name を渡して _wrap_attributes を呼び出しメソッド群をラップします。
        Args:
            submodule: ModuleType - 自動ロギングを適用する対象モジュール。
            app_mod_name: str - アプリ名から始まるログ表示用モジュール名。
            log_internal: bool - アンダースコア始まりの内部関数・内部メソッドをログ対象に含めるフラグ（デフォルト: False）。
        Returns:
            None - 戻り値なし。
        """
        # 1. モジュール直下の関数をラップ
        self._wrap_attributes(submodule, app_mod_name, log_internal=log_internal)

        # 2. 自モジュール内で定義されたクラスのメソッドをラップ
        for _, attr_value in inspect.getmembers(submodule, inspect.isclass):
            if getattr(attr_value, "__module__", None) == submodule.__name__:
                self._wrap_attributes(
                    attr_value,
                    app_mod_name,
                    log_internal=log_internal,
                )

    def _wrap_attributes(
        self,
        target: Union[ModuleType, type],
        app_mod_name: str,
        log_internal: bool = False,
    ) -> None:
        """
        Summary:
            対象（モジュールまたはクラス）の属性を走査し、安全判定を通過した関数・メソッドに自動ロギングラッパーを適用します。
        Description:
            vars(target) を走査し、特殊関数・ダンダーメソッド（__...__）、内部関数・メソッド（log_internal=False時の_...）、
            property ディスクリプタ、モジュール走査時の外部インポート関数（__module__ 不一致）、
            二重ラップ防止フラグ WRAPS_FUNC_KEY を検証します。
            安全判定を通過した対象に対し、モジュール直下関数の場合は「{app_mod_name}.{attr_name}」、
            クラスメソッドの場合は「{app_mod_name}.{target.__name__}.{attr_name}」の形式で qualname を生成します。
            classmethod / staticmethod はアンラップして再ラップし、_generate_wraps_func を適用して setattr で差し替えます。
        Args:
            target: Union[ModuleType, type] - 自動ロギングを適用する対象モジュールまたはクラス。
            app_mod_name: str - アプリ名から始まるログ表示用モジュール名。
            log_internal: bool - アンダースコア始まりの内部関数・内部メソッドをログ対象に含めるフラグ（デフォルト: False）。
        Returns:
            None - 戻り値なし。
        """
        is_module: bool = isinstance(target, ModuleType)

        for attr_name, attr_value in list(vars(target).items()):
            # 特殊メソッド・関数の除外（ダンダー: __repr__ 等）
            # __init__ は対象とするため、条件分岐の先頭で除外判定を行わない
            if attr_name != "__init__" and (attr_name.startswith("__") and attr_name.endswith("__")):
                continue

            # 内部メソッド・関数の除外判定
            #if not log_internal and attr_name.startswith("_"):
            #    continue

            # property ディスクリプタの保護
            if isinstance(attr_value, property):
                continue

            is_classmethod: bool = isinstance(attr_value, classmethod)
            is_staticmethod: bool = isinstance(attr_value, staticmethod)

            target_func: Any = attr_value
            if is_classmethod or is_staticmethod:
                target_func = attr_value.__func__

            # 通常の関数オブジェクトであることを確認
            if not callable(target_func) or not inspect.isfunction(target_func):
                continue

            # モジュール走査時の外部インポート関数除外判定
            if is_module and getattr(target_func, "__module__", None) != target.__name__:
                continue

            # 二重ラップ防止
            if getattr(target_func, WRAPS_FUNC_KEY, False):
                continue

            # 元の関数を _generate_wraps_func でラップする
            if is_module:
                qualname: str = f"{app_mod_name}.{attr_name}"
            else:
                qualname = f"{app_mod_name}.{target.__name__}.{attr_name}"
            wrapped_func: Any = self._generate_wraps_func(target_func, qualname)

            # 元の関数を上書き保存する（classmethod / staticmethod は再ラップ）
            if is_classmethod:
                setattr(target, attr_name, classmethod(wrapped_func))
            elif is_staticmethod:
                setattr(target, attr_name, staticmethod(wrapped_func))
            else:
                setattr(target, attr_name, wrapped_func)

    def _generate_wraps_func(self, orig_func: Any, qualname: str) -> Any:
        """
        Summary:
            ログ機能付き関数を生成します。
        Description:
            functools.wraps により元関数のメタデータを保持した関数（_wraps_output_start_end_log）を生成します。
            内部の処理は独立した実行メソッド（output_start_end_log_wrapper）へ委譲し、
            二重ラップ防止フラグ（WRAPS_FUNC_KEY = True）を設定します。
        Args:
            orig_func: Any - ラップ対象の元関数オブジェクト。
            qualname: str - 呼び出し対象の修飾名。
        Returns:
            Any - 生成されたログ機能付き関数。
        """
        @functools.wraps(orig_func)
        def _wraps_output_start_end_log(*args: object, **kwargs: Any) -> Any:
            return self.output_start_end_log_wrapper(orig_func, qualname, *args, **kwargs)

        setattr(_wraps_output_start_end_log, WRAPS_FUNC_KEY, True)
        return _wraps_output_start_end_log
    #endregion

    #region Wraps Method
    def output_start_end_log_wrapper(
        self,
        orig_func: Any,
        qualname: str,
        *args: object,
        **kwargs: Any,
    ) -> Any:
        """
        Summary:
            トレースログを出力しながら元関数を実行する独立メソッドです。
        Description:
            関数実行開始時に [START] を記録し、元関数を実行して正常終了時に [END] を記録します。
            例外発生時には [ERROR] ログを記録した上で例外を再送出（re-raise）します。
            独立したdefとして定義されているため、IDEでのブレークポイントが100%確実に機能します。
        Args:
            orig_func: Any - 実行対象の元関数オブジェクト。
            qualname: str - 呼び出し対象の修飾名。
            *args: object - 可変長引数。
            **kwargs: Any - キーワード引数。
        Returns:
            Any - 元関数の実行結果。
        """
        self.output_info(f"[START]\t{qualname}")
        try:
            result: Any = orig_func(*args, **kwargs)
            self.output_info(f"[END  ]\t{qualname}")
            return result
        except Exception as e:
            self.output_error(f"[ERROR]\t{qualname}: {e}")
            raise
    #endregion

#endregion
