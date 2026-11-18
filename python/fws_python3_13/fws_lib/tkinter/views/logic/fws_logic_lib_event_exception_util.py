"""
Summary:
    Tkinter GUIアプリケーション向けイベント例外ハンドリングロジックモジュール。
Description:
    TkinterのEvent層メソッド（ボタンクリックやウィンドウ操作などのイベントハンドラ）における
    try-except例外捕捉、ロガーへのスタックトレース出力、
    およびエラーダイアログ（fws_view_lib_dialog_utils.show_error）表示を共通化するデコレータクラスを提供します。
Attachment:
    なし
"""
#region imports
import functools
import tkinter as tk
import traceback
from typing import Any, Callable

from fws_lib.common import fws_logger_util
from fws_lib.tkinter.views.view import fws_view_lib_dialog_utils
#endregion

#region classes
class FwsLogicLibEventExceptionUtil:
    """
    Summary:
        Tkinterイベント例外ハンドリングデコレータクラス。
    Description:
        イベントハンドラメソッドに @catch_exception デコレータを付与することで、
        メソッド実行中に発生した予期せぬ例外を捕捉し、エラーログ出力と
        親ウィンドウ（操作画面）にかぶせたエラーダイアログ表示を行います。
    """

    #region Constructor
    def __init__(
        self,
        fws_logger_util_obj: fws_logger_util.FwsLoggerUtil = fws_logger_util.FwsLoggerUtil(),
        error_dialog_title: str = "例外エラー",
    ) -> None:
        """
        Summary:
            イベント例外ハンドリングユーティリティを初期化します。
        Description:
            エラーログ出力用の FwsLoggerUtil インスタンスと、
            例外捕捉時に表示するエラーダイアログのタイトル文字列を保持します。
        Args:
            fws_logger_util_obj: fws_logger_util.FwsLoggerUtil - エラー出力用ロガーインスタンス（デフォルト: FwsLoggerUtil()）。
            error_dialog_title: str - エラーダイアログのタイトル文字列（デフォルト: "例外エラー"）。
        Returns:
            None - 戻り値なし。
        """
        self._fws_logger_util_obj: fws_logger_util.FwsLoggerUtil = fws_logger_util_obj
        """fws_logger_util.FwsLoggerUtil - エラー出力用ロガーインスタンス"""
        self._error_dialog_title: str = error_dialog_title
        """str - エラーダイアログのタイトル文字列"""
    #endregion

    #region Public Methods
    def catch_exception(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Summary:
            イベントメソッドの例外を捕捉してログ出力およびダイアログ表示を行うデコレータです。
        Description:
            対象関数を functools.wraps でラップし、実行時の例外ハンドリングを
            _execute_with_exception_handling メソッドへ委譲します。
        Args:
            func: Callable[..., Any] - デコレート対象のイベントメソッド。
        Returns:
            Callable[..., Any] - 例外捕捉処理が付与されたラッパー関数。
        """
        @functools.wraps(func)
        def _wraps_catch_exception(*args: object, **kwargs: Any) -> Any:
            return self._execute_with_exception_handling(func, *args, **kwargs)

        return _wraps_catch_exception
    #endregion

    #region Private Methods
    def _execute_with_exception_handling(
        self,
        orig_func: Callable[..., Any],
        *args: object,
        **kwargs: Any,
    ) -> Any:
        """
        Summary:
            例外ハンドリングを伴って元関数を実行します。
        Description:
            元関数（orig_func）を実行し、Exception が発生した場合はスタックトレースを取得します。
            保持しているロガーの output_error でログ出力した後、
            fws_view_lib_dialog_utils.show_error で親ウィンドウにかぶせたエラーダイアログを表示し、None を返します。
        Args:
            orig_func: Callable[..., Any] - 実行対象の元関数オブジェクト。
            *args: object - 可変長位置引数。
            **kwargs: Any - 可変長キーワード引数。
        Returns:
            Any - 元関数の戻り値（例外発生時は None）。
        """
        try:
            return orig_func(*args, **kwargs)
        except Exception as exc:
            error_details: str = traceback.format_exc().rstrip()
            func_name: str = getattr(
                orig_func,
                "__qualname__",
                getattr(orig_func, "__name__", "unknown"),
            )
            self._fws_logger_util_obj.output_error(
                f"[EVENT_EXCEPTION] {func_name} - {type(exc).__name__}: {exc}\n{error_details}"
            )

            error_summary: str = (
                "例外エラーが発生しました。\n"
                "エンジニアに報告してください。\n"
                f"・{type(exc).__name__}: {exc}"
            )
            parent_window: Any = self._resolve_parent_window(args)
            fws_view_lib_dialog_utils.show_error(
                self._error_dialog_title,
                error_summary,
                parent=parent_window,
            )
            return None

    def _resolve_parent_window(self, args: tuple[object, ...]) -> Any:
        """
        Summary:
            イベントメソッドの引数からダイアログ表示用の親ウィンドウを解決します。
        Description:
            先頭引数（Eventクラスのselfインスタンス等）が tk.Widget であればそれを返し、
            インスタンス属性内に tk.Tk または tk.Toplevel（Viewインスタンス）が保持されていればそれを返します。
            いずれにも該当しない場合は tk._default_root を返します。
        Args:
            args: tuple[object, ...] - イベントメソッドに渡された位置引数タプル。
        Returns:
            Any - 解決された親ウィンドウオブジェクト（未検出時は None）。
        """
        if args:
            first_arg: object = args[0]
            if isinstance(first_arg, tk.Widget):
                return first_arg
            if hasattr(first_arg, "__dict__"):
                for attr_value in vars(first_arg).values():
                    if isinstance(attr_value, (tk.Tk, tk.Toplevel)):
                        return attr_value

        return getattr(tk, "_default_root", None)
    #endregion
#endregion
