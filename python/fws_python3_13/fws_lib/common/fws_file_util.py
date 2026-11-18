"""
Summary:
    fws_lib 共通のファイルシステムユーティリティ。
Description:
    ファイルやディレクトリの操作に関する便利なラッパー関数を提供します。
Attachment:
    なし
"""
import shutil
import os
from pathlib import Path
from typing import Literal
EncodingType = Literal[
    "utf-8",
    "utf-8-sig",
    "cp932",
    "shift_jis",
    "euc-jp",
]


#-------------------------------------------
#textutliMethodを作成するときに使いたい要素、
#WriteMode = Literal["w", "a", "write", "append"]
#-------------------------------------------

#region PablicMethod
def is_exists_path(target_path:str|Path) -> bool:
    """
    Summary:
        指定されたパス（ファイルまたはディレクトリ）が存在するか検証する
    Description:
        指定されたパスが存在する場合、Trueを返す。存在しない場合は False を返す。
    Args:
        target_path: str|Path - 検証対象のパス（文字列またはPathオブジェクト）
    Returns:
        bool - 存在していれば True、存在しない（または権限不足等でアクセス不能な）場合は False
    """
    return Path(target_path).exists()

def is_file(target_file_path:str|Path) -> bool:
    """
    Summary:
        指定されたパスがファイルであるか検証する
    Description:
        指定されたパスがファイルである場合、Trueを返す。それ以外は False を返す。
    Args:
        target_file_path: str|Path - 検証対象のパス（文字列またはPathオブジェクト）
    Returns:
        bool - ファイルであれば True、それ以外は False
    """
    return Path(target_file_path).is_file()

def is_dir(target_dir_path:str|Path) -> bool:
    """
    Summary:
        指定されたパスがディレクトリであるか検証する
    Description:
        指定されたパスがディレクトリである場合、Trueを返す。それ以外は False を返す。
    Args:
        target_dir_path: str|Path - 検証対象のパス（文字列またはPathオブジェクト）
    Returns:
        bool - ディレクトリであれば True、それ以外は False
    """
    return Path(target_dir_path).is_dir()

def get_absolute_path(target_path:str|Path) -> str:
    """
    Summary:
        指定されたパスを絶対パスに変換する
    Args:
        target_path: str|Path - 対象のパス（文字列またはPathオブジェクト）
    Returns:
        str - 絶対パスの文字列
    """
    return str(Path(target_path).resolve())

def get_file_name(target_file_path:str|Path,is_with_extension:bool=True) -> str:
    """
    Summary:
        指定されたパスからファイル名を取得する
    Args:
        target_file_path: str|Path - 対象のファイルパス（文字列またはPathオブジェクト）
        is_with_extension: bool - 拡張子を含むかどうか
    Returns:
        str - ファイル名
    """
    file_name:str = ""
    #拡張子取得有無判定を実施する。
    if is_with_extension:
        #拡張子取得ありの場合、拡張子含めて返す。
        file_name = Path(target_file_path).name
    else:
        #拡張子取得なしの場合、拡張子を除いて返す。
        file_name = Path(target_file_path).stem

    return file_name

def read_text_all(target_file_path:str|Path,encoding_type:EncodingType="utf-8") -> str:
    """
    Summary:
        指定されたパスのファイルをテキストとして全て読み込む
    Args:
        target_file_path: str|Path - 対象のファイルパス（文字列またはPathオブジェクト）
    Returns:
        str - ファイルの内容
    Description:
        指定されたパスのファイルをテキストとして全て読み込む。
    """
    return Path(target_file_path).read_text(encoding_type)

def write_text_all(target_file_path:str|Path,text:str,encoding_type:EncodingType="utf-8") -> None:
    """
    Summary:
        指定されたパスにテキストを書き込む
    Args:
        target_file_path: str|Path - 対象のファイルパス（文字列またはPathオブジェクト）
        text: str - 書き込む内容
    Returns:
        None - 戻り値なし。
    Description:
        指定されたパスにテキストを書き込む。
    """
    Path(target_file_path).write_text(text,encoding_type)

def copy_file(source_file_path:str|Path,destination_file_path:str|Path)-> None:
    """
    Summary:
        指定されたパスのファイルをコピーする
    Args:
        source_file_path: str|Path - コピー元のファイルパス（文字列またはPathオブジェクト）
        destination_file_path: str|Path - コピー先のファイルパス（文字列またはPathオブジェクト）
    Returns:
        None - 戻り値なし。
    Description:
        指定されたパスのファイルをコピーする。
    """
    shutil.copy2(source_file_path, destination_file_path)

def move_file(source_file_path:str|Path,destination_file_path:str|Path)-> None:
    """
    Summary:
        指定されたパスのファイルを移動する
    Args:
        source_file_path: str|Path - 移動元のファイルパス（文字列またはPathオブジェクト）
        destination_file_path: str|Path - 移動先のファイルパス（文字列またはPathオブジェクト）
    Returns:
        None - 戻り値なし。
    Description:
        指定されたパスのファイルを移動する。
    """
    shutil.move(source_file_path, destination_file_path)

def execute_file_or_dir_for_win(target_file_path: str | Path) -> bool:
    """
    Summary:
        OSの関連付けに従ってファイルを既定のアプリケーションで実行（オープン）する
    Args:
        target_file_path: str|Path - 対象のファイルパス（文字列またはPathオブジェクト）
    Returns:
        bool - True(ファイル実行を試みる)/False(実行失敗)
    """
    if not is_exists_path(target_file_path):
        return False

    os.startfile(get_absolute_path(target_file_path))
    return True

def create_dir(target_dir_path:str|Path,is_create_parents:bool=True,is_exist_ok:bool = True)-> None:
    """
    Summary:
        指定されたパスにディレクトリを作成する
    Args:
        target_dir_path: str|Path - ディレクトリパス（文字列またはPathオブジェクト）
        is_create_parents: bool - 親ディレクトリが存在しない場合に作成するかどうか
        is_exist_ok: bool - ディレクトリが既に存在する場合にエラーとしないかどうか
    Returns:
        None - 戻り値なし。
    Description:
        指定されたパスにディレクトリを作成する。
        親ディレクトリが存在しない場合は、親ディレクトリも作成する（is_create_parents=Trueの場合）
        ディレクトリが既に存在する場合、エラーとしない（is_exist_ok=Trueの場合）
    """
    Path(target_dir_path).mkdir(parents=is_create_parents,exist_ok=is_exist_ok)

def create_empty_file(target_file_path:str|Path)-> None:
    """
    Summary:
        指定されたパスに空のファイルを作成する
    Args:
        target_file_path: str|Path - ファイルパス（文字列またはPathオブジェクト）
    Returns:
        None - 戻り値なし。
    Description:
        指定されたパスに空のファイルを作成する。
    """
    Path(target_file_path).touch(exist_ok=True)

def string_to_path(target_path:str) -> Path:
    """
    Summary:
        文字列またはPathオブジェクトを、前後のクォーテーションや空白を除去して安全な Path に変換します。
    Args:
        target_path: str - 対象のパス
    Returns:
        Path - 正規化された Path オブジェクト
    """    
    # 前後の空白、ダブルクォーテーション、シングルクォーテーションを除去
    cleaned_str = str(target_path).strip().strip('"\'')
    return Path(cleaned_str)

#endregion PablicMethod

