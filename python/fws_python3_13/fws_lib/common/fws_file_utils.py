"""
Summary:
    fws_lib 共通のファイルシステムユーティリティ。
Description:
    ファイルやディレクトリの操作に関する便利なラッパー関数を提供します。
Attachment:
    なし
"""
import shutil
from pathlib import Path
from typing import Union
from fws_lib.constant import fws_lib_const

def ensure_dir(path: Union[str, Path]) -> None:
    """
    Summary:
        指定されたディレクトリが存在しない場合、作成します。
    Description:
        親ディレクトリも含めてディレクトリ構造を作成します。
    Args:
        path: Union[str, Path] - 対象のディレクトリパス。
    Returns:
        None - 戻り値なし。
    """
    Path(path).mkdir(parents=True, exist_ok=True)

def read_text(path: Union[str, Path], encoding: str = fws_lib_const.DEFAULT_ENCODING) -> str:
    """
    Summary:
        テキストファイルを読み込みます。
    Description:
        指定されたエンコーディングでファイルを読み込み、文字列として返します。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
        encoding: str - エンコーディング (デフォルト: UTF-8)。
    Returns:
        str - 読み込んだファイルの内容。
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"{fws_lib_const.ERROR_PREFIX} File not found: {path}")
    return p.read_text(encoding=encoding)

def write_text(path: Union[str, Path], content: str, encoding: str = fws_lib_const.DEFAULT_ENCODING) -> None:
    """
    Summary:
        テキストファイルに内容を書き込みます。
    Description:
        親ディレクトリが存在しない場合は自動作成し、指定された文字列をファイルに書き込みます。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
        content: str - 書き込む内容。
        encoding: str - エンコーディング (デフォルト: UTF-8)。
    Returns:
        None - 戻り値なし。
    """
    p = Path(path)
    ensure_dir(p.parent)
    p.write_text(content, encoding=encoding)

def get_absolute_path(path: Union[str, Path]) -> str:
    """
    Summary:
        相対パスを絶対パスに変換します。
    Description:
        与えられたパスをシステムの絶対パスに変換し、文字列として返します。
    Args:
        path: Union[str, Path] - 対象のファイルまたはディレクトリのパス。
    Returns:
        str - 絶対パスの文字列。
    """
    return str(Path(path).resolve())

def get_file_name(path: Union[str, Path], with_extension: bool = True) -> str:
    """
    Summary:
        パス文字列からファイル名を抽出します。
    Description:
        with_extension が True の場合は拡張子付き、False の場合は拡張子なしのファイル名を返します。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
        with_extension: bool - 拡張子を含める場合は True (デフォルト: True)。
    Returns:
        str - 抽出されたファイル名。
    """
    p = Path(path)
    return p.name if with_extension else p.stem

def change_extension(path: Union[str, Path], new_extension: str) -> str:
    """
    Summary:
        ファイルパスの拡張子を変更します。
    Description:
        対象のファイルパスの拡張子を指定したものに置き換えた新しいパス文字列を返します。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
        new_extension: str - 新しい拡張子（例: ".json"）。
    Returns:
        str - 拡張子が変更されたパス文字列。
    """
    if not new_extension.startswith("."):
        new_extension = f".{new_extension}"
    return str(Path(path).with_suffix(new_extension))

def copy_file(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
    """
    Summary:
        ファイルをコピーします。
    Description:
        shutil.copy2 を使用してファイルをメタデータと共にコピーします。
    Args:
        src_path: Union[str, Path] - コピー元のファイルパス。
        dst_path: Union[str, Path] - コピー先のファイルパス。
    Returns:
        None - 戻り値なし。
    """
    shutil.copy2(src_path, dst_path)

def move_file(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
    """
    Summary:
        ファイルを移動またはリネームします。
    Description:
        shutil.move を使用してファイルを移動します。
    Args:
        src_path: Union[str, Path] - 移動元のファイルパス。
        dst_path: Union[str, Path] - 移動先のファイルパス。
    Returns:
        None - 戻り値なし。
    """
    shutil.move(src_path, dst_path)

def read_lines(path: Union[str, Path], skip_empty: bool = True) -> list[str]:
    """
    Summary:
        テキストファイルを読み込み、行ごとのリストを返します。
    Description:
        ファイルを読み込み、各行の末尾の改行文字を削除したリストを返します。
        skip_empty が True の場合は、空白のみの行を除外します。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
        skip_empty: bool - 空行を除外する場合は True。
    Returns:
        list[str] - 行のリスト。
    """
    content = read_text(path)
    lines = content.splitlines()
    if skip_empty:
        return [line for line in lines if line.strip()]
    return lines


