"""
Summary:
    バルクインサートのLogicモジュール。
Description:
    Business層を呼び出し、データ挿入を実行します。
Attachment:
    なし
"""
from fws_apps.tkinter.fws_sqlite_viewer.businesses.business import fws_sqlite_viewer_business

class FwsSqliteViewerBulkInsertLogic:
    """
    Summary:
        バルクインサートのLogicクラス。
    """
    
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Args:
            なし
        """
        pass

    def validate_input(self, data: str, is_file: bool) -> tuple[bool, str]:
        """
        Summary:
            入力データのバリデーションを行います。
        Args:
            data: str - ファイルパスまたはテキストデータ
            is_file: bool - ファイルかどうか
        Returns:
            tuple[bool, str] - (検証結果, エラーメッセージ)
        """
        if not data:
            if is_file:
                return False, "Please select a file."
            else:
                return False, "Please input text data."
        return True, ""

    def bulk_insert(self, main_logic, table_name: str, alias: str, data: str, is_file: bool, delimiter: str, has_header: bool) -> int:
        """
        Summary:
            メインのLogic経由でBusiness層を呼び出し、バルクインサートを実行します。
        Args:
            main_logic: FwsSqliteViewerLogic - データベース接続を持つメインのロジックオブジェクト
            table_name: str - 挿入先テーブル名
            alias: str - 対象DBエイリアス
            data: str - ファイルパスまたはテキストデータ
            is_file: bool - dataがファイルパスかどうか
            delimiter: str - 区切り文字
            has_header: bool - ヘッダー行の有無
        Returns:
            int - 挿入された行数
        """
        return main_logic._fws_sqlite_viewer_business_obj.bulk_insert(
            table_name=table_name,
            alias=alias,
            data=data,
            is_file=is_file,
            delimiter=delimiter,
            has_header=has_header
        )

