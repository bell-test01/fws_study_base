"""
Summary:
    fws_source_linkerのエントリーポイントです。
Description:
    Eventクラスをインスタンス化してアプリケーションを起動します。
Attachment:
    なし
"""
import sys
from pathlib import Path

app_dir: Path = Path(__file__).resolve().parent
"""Path - アプリケーションディレクトリ"""
project_root: Path = app_dir.parent.parent.parent
"""Path - プロジェクトルートディレクトリ"""
sys.path.append(str(project_root))

from fws_apps.tkinter.fws_source_linker.views.event import fws_source_linker_event


def main() -> None:
    """
    Summary:
        メイン処理。
    Description:
        Eventオブジェクトを作成し、起動します。
    Args:
        なし
    Returns:
        None
    """
    fws_source_linker_event_obj: fws_source_linker_event.FwsSourceLinkerEvent = fws_source_linker_event.FwsSourceLinkerEvent()
    fws_source_linker_event_obj.start()


if __name__ == "__main__":
    main()
