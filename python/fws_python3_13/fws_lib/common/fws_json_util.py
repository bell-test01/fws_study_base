"""
Summary:
    fws_lib 共通のJSON操作ユーティリティモジュール。
Description:
    JSON 形式のファイル読み込み、書き出し、部分更新、デフォルト補完等の操作を提供します。
Attachment:
    なし
"""
import json
from pathlib import Path
from typing import Dict, Any, Union
from fws_lib.constant import fws_lib_const
from fws_lib.common import fws_file_util

def load_json(path: str|Path) -> Dict[str, Any]:
    """
    Summary:
        JSON ファイルを読み込み、辞書として返します。
    Description:
        指定されたファイルからJSONデータをパースし、辞書型で返します。存在しない場合は空の辞書を返します。
    Args:
        path: str|Path - 対象のファイルパス。
    Returns:
        Dict[str, Any] - パースされた JSON データ。ファイルが存在しない場合は空の辞書。
    """
    if not fws_file_util.is_exists_path(path):
        return {}
        
    try:
        content = fws_file_util.read_text_all(path,'utf-8')
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"{fws_lib_const.ERROR_PREFIX} Failed to parse JSON at {path}: {e}")
    except OSError as e:
        raise OSError(f"{fws_lib_const.ERROR_PREFIX} Failed to read file at {path}: {e}")

def save_json(path:str|Path, data: Dict[str, Any], indent: int = 4) -> None:
    """
    Summary:
        辞書データを JSON ファイルとして保存します。
    Description:
        与えられた辞書データをJSON形式で整形し、ファイルに書き出します。
    Args:
        path: Union[str, Path] - 保存先のファイルパス。
        data: Dict[str, Any] - 保存するデータ。
        indent: int - JSON のインデント (デフォルト: 4)。
    Returns:
        None - 戻り値なし。
    """
    content = json.dumps(data, indent=indent, ensure_ascii=False)
    try:
        fws_file_util.write_text_all(path, content)
    except OSError as e:
        raise OSError(f"{fws_lib_const.ERROR_PREFIX} Failed to write file at {path}: {e}")

def update_json_value(path: str|Path, key: str, value: Any, indent: int = 4) -> None:
    """
    Summary:
        JSONファイルの特定のキーの値を更新します。
    Description:
        既存のJSONを読み込み、指定されたキーの値を上書き（または追加）して保存します。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
        key: str - 更新するキー。
        value: Any - 設定する値。
        indent: int - JSON のインデント (デフォルト: 4)。
    Returns:
        None - 戻り値なし。
    """
    data = load_json(path)
    data[key] = value
    save_json(path, data, indent)
