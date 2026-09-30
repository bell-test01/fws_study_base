"""
Summary:
    fws_source_linkerアプリの定数を定義するモジュールです。
Description:
    バージョン情報や固定文字列、ファイルパスなどの定数を一元管理します。
Attachment:
    なし
"""

# バージョン情報
APP_VERSION = "1.0.0.0"

# 設定ファイル関連
CONFIG_FILE_NAME = "fws_source_linker_config.json"
CONFIG_KEY_ROOT_DIR = "root_dir"
CONFIG_KEY_ROOT_DIR_HISTORY = "root_dir_history"
CONFIG_KEY_DEST_DIR = "dest_dir"
CONFIG_KEY_DEST_DIR_HISTORY = "dest_dir_history"
CONFIG_KEY_DEST_SUB_DIR = "dest_sub_dir"

# 履歴設定
MAX_HISTORY_COUNT = 10

# UI設定
UI_FONT_FAMILY = "Meiryo UI"
UI_FONT_SIZE = 7
UI_DEFAULT_TOPMOST = False
UI_DEFAULT_ALPHA = 1.0
UI_ALPHA_MIN = 0.1
UI_ALPHA_MAX = 1.0
