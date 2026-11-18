"""
Summary:
    fws_chat_template アプリケーションのエントリーポイント。
Description:
    システムパスを解決し、環境設定およびセッション初期化を行った後、メイン画面イベントクラスを起動します。
Attachment:
    docs_fws_chat_template/implementation_plan.md
"""
#region imports
import sys
from pathlib import Path
#------------------------------------------------------------------------------
# 自作モジュールインポート設定（パス解決）
#------------------------------------------------------------------------------
app_dir: Path = Path(__file__).resolve().parent
"""Path - アプリケーションルートディレクトリ"""
project_root_dir: Path = app_dir.parent.parent.parent
"""Path - プロジェクトルートディレクトリ"""
sys.path.append(str(project_root_dir))
#------------------------------------------------------------------------------
# 自作モジュールインポート
#------------------------------------------------------------------------------
from fws_apps.tkinter.fws_chat_template.constant import fws_const_chat_template
# アプリケーション初期設定実施
fws_const_chat_template.initialize_application(project_root_dir, app_dir)
from fws_apps.tkinter.fws_chat_template.views.event import fws_event_chat_template
#endregion

#region entry_point
def main() -> None:
    """
    Summary:
        アプリケーションのメイン処理を実行します。
    Description:
        メイン画面イベントクラスをインスタンス化し、アプリケーションを起動します。
    Args:
        なし
    Returns:
        None - 戻り値なし。
    """
    # アプリケーション起動
    fws_event_chat_template_obj: fws_event_chat_template.FwsEventChatTemplate = fws_event_chat_template.FwsEventChatTemplate()
    fws_event_chat_template_obj.start()
#endregion

if __name__ == "__main__":
    main()
