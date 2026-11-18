"""
Summary:
    外部プロセスおよびOS関連付け起動ユーティリティモジュール。
Description:
    subprocessによる非同期外部プロセス起動、os.startfileによるOS関連付け起動、
    およびWindowsエクスプローラによるパス・ファイル選択表示機能を提供します。
Attachment:
    なし
"""
#region imports
import os
from pathlib import Path
import subprocess
from typing import Optional
#endregion

#region Public Functions
def start_process(
    command_args: list[str],
    cwd: Optional[Path | str] = None,
) -> subprocess.Popen:
    """
    Summary:
        外部プロセスを非同期でバックグラウンド起動します。
    Description:
        指定されたコマンド引数リストを用いて、メインプロセスをブロックせずに
        非同期で外部プロセス（バックグラウンド起動）を開始します。
    Args:
        command_args: list[str] - 実行するコマンドおよび引数の文字列リスト。
        cwd: Optional[Path | str] - プロセスの作業ディレクトリ。省略時はNone。
    Returns:
        subprocess.Popen - 起動したプロセスのPopenオブジェクト。
    """
    working_dir: Optional[str] = str(cwd) if cwd is not None else None
    return subprocess.Popen(command_args, cwd=working_dir)


def open_by_os(target_path: Path | str) -> None:
    """
    Summary:
        指定されたパスをOS標準の関連付けアプリケーションで開きます。
    Description:
        os.startfile を呼び出し、拡張子に関連付けられた既定のソフトウェアで
        ファイルまたはディレクトリを開きます。
    Args:
        target_path: Path | str - 開く対象のファイルまたはディレクトリパス。
    Returns:
        None - 戻り値なし。
    """
    os.startfile(str(target_path))


def open_in_explorer(target_path: Path | str) -> None:
    """
    Summary:
        指定されたパスをWindowsエクスプローラで開きます。
    Description:
        対象パスがファイルの場合は /select オプションを付与して該当ファイルを選択状態で表示し、
        ディレクトリの場合はそのフォルダを展開してエクスプローラを開きます。
    Args:
        target_path: Path | str - エクスプローラで表示するファイルまたはディレクトリパス。
    Returns:
        None - 戻り値なし。
    """
    path_obj: Path = Path(target_path)
    if path_obj.is_file():
        subprocess.Popen(["explorer", f"/select,{str(path_obj)}"])
    else:
        subprocess.Popen(["explorer", str(path_obj)])
#endregion
