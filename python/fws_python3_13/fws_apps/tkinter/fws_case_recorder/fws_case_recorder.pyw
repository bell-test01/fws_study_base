"""
Summary:
    fws_case_recorder アプリのエントリーポイント。
Description:
    システムパスを追加し、アプリケーションのイベントクラスを起動します。
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

from fws_apps.tkinter.fws_case_recorder.views.event import fws_case_recorder_event

def main() -> None:
    """
    Summary:
        アプリケーションのメイン処理。
    Description:
        イベントクラスをインスタンス化してメインループを開始します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    try:
        fws_case_recorder_event_obj: fws_case_recorder_event.FwsCaseRecorderEvent = fws_case_recorder_event.FwsCaseRecorderEvent()
        """fws_case_recorder_event.FwsCaseRecorderEvent - イベントオブジェクト"""
        fws_case_recorder_event_obj.start()
    except Exception as e:
        """Exception - 実行時に発生した例外オブジェクト"""
        print(f"Fatal error in application: {e}")

if __name__ == "__main__":
    main()
