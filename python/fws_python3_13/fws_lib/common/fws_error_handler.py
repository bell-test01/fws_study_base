import functools
import traceback
import tkinter
import tkinter.messagebox
import sys
from fws_lib.common.fws_logger import get_logger

def with_error_handling(title="エラー", ui_mode="tkinter"):
    """
    関数・メソッドで発生した例外をキャッチし、ログへの詳細出力と
    指定したUIへの概要表示を自動で行うデコレータ。
    
    Args:
        title (str): メッセージのタイトル。
        ui_mode (str): "tkinter" の場合はメッセージボックスを表示。
                       "console" の場合は標準エラー出力に表示。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = get_logger()
                
                # 詳細なスタックトレースをログ出力
                error_details = traceback.format_exc()
                logger.error(f"Error in {func.__name__}:\n{error_details}")
                
                # エラーの簡易概要
                error_summary = f"{type(e).__name__}: {str(e)}"
                
                if ui_mode == "tkinter":
                    try:
                        # Tkinter環境が有効か確認し、メッセージボックスを表示
                        tkinter.messagebox.showerror(title, error_summary)
                    except Exception:
                        # Tkinterが利用できない場合はフォールバックとしてコンソールに出力
                        print(f"[{title}] {error_summary}", file=sys.stderr)
                elif ui_mode == "console":
                    print(f"[{title}] {error_summary}", file=sys.stderr)
        return wrapper
    return decorator
