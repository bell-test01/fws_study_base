"""
Summary:
    fws_lib 共通の設定（Config）および履歴管理モジュール。
Description:
    JSON などの形式で設定データや履歴データをシリアライズ/デシリアライズします。
Attachment:
    なし
"""
import json
from pathlib import Path
from typing import Dict, Any, Union
from fws_lib.constant import fws_lib_const
from fws_lib.common import fws_file_utils

def load_json(path: Union[str, Path]) -> Dict[str, Any]:
    """
    Summary:
        JSON ファイルを読み込み、辞書として返します。
    Description:
        指定されたファイルからJSONデータをパースし、辞書型で返します。存在しない場合は空の辞書を返します。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
    Returns:
        Dict[str, Any] - パースされた JSON データ。ファイルが存在しない場合は空の辞書。
    """
    p = Path(path)
    if not p.exists():
        return {}
        
    try:
        content = fws_file_utils.read_text(p)
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"{fws_lib_const.ERROR_PREFIX} Failed to parse JSON at {path}: {e}")

def save_json(path: Union[str, Path], data: Dict[str, Any], indent: int = 4) -> None:
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
    fws_file_utils.write_text(path, content)

def update_json_value(path: Union[str, Path], key: str, value: Any, indent: int = 4) -> None:
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

def load_json_with_default(path: Union[str, Path], default_data: Dict[str, Any], indent: int = 4) -> Dict[str, Any]:
    """
    Summary:
        JSONファイルを読み込み、不足しているキーをデフォルト値で補完します。
    Description:
        ファイルが存在しない場合、またはキーが不足している場合に default_data の内容で補完し、その状態を保存して返します。
    Args:
        path: Union[str, Path] - 対象のファイルパス。
        default_data: Dict[str, Any] - デフォルト値の辞書。
        indent: int - JSON のインデント (デフォルト: 4)。
    Returns:
        Dict[str, Any] - 補完された JSON データ。
    """
    p = Path(path)
    if not p.exists():
        save_json(p, default_data, indent)
        return default_data.copy()
    
    current_data = load_json(p)
    is_updated = False
    
    for key, value in default_data.items():
        if key not in current_data:
            current_data[key] = value
            is_updated = True
            
    if is_updated:
        save_json(p, current_data, indent)
        
    return current_data
