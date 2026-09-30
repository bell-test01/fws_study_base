import logging
import os

# シングルトンロガーインスタンス
_logger = None

def setup_logger(log_file_path="app.log", level=logging.INFO):
    """
    アプリケーション用のロガーを初期化・取得する
    """
    global _logger
    if _logger is not None:
        return _logger

    # ログファイルのディレクトリが存在しない場合は作成
    log_dir = os.path.dirname(log_file_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    _logger = logging.getLogger("fws_app_logger")
    _logger.setLevel(level)
    
    # 既存のハンドラがある場合はクリア（二重出力を防ぐ）
    if _logger.hasHandlers():
        _logger.handlers.clear()

    # ファイルハンドラ（追記モード）
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(level)
    
    # フォーマッタ
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    _logger.addHandler(file_handler)
    
    return _logger

def get_logger():
    """
    初期化済みのロガーを取得する。
    未初期化の場合はデフォルト設定で初期化して返す。
    """
    if _logger is None:
        return setup_logger()
    return _logger
