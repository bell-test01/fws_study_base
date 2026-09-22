"""
Summary:
    fws_sqlite_viewer アプリのテーブル作成ダイアログ用ロジックモジュール。
Description:
    新規テーブル作成用ダイアログのSQL構築やビジネスロジックの呼び出しを仲介します。
Attachment:
    なし
"""
from typing import List


class FwsSqliteViewerCreateTableLogic:
    """
    Summary:
        テーブル作成ダイアログ用のロジッククラス。
    Description:
        画面からの命令を受け取り、ビジネス層へ処理を依頼します。
    """

    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Args:
            なし
        """
        pass

    def build_create_table_sql(self, table_name: str, alias: str, columns_def: List[str]) -> str:
        """
        Summary:
            CREATE TABLE文を構築します。
        Args:
            table_name: str - 作成するテーブル名。
            alias: str - 対象のデータベースエイリアス。
            columns_def: List[str] - 各カラム定義のSQL文字列リスト。
        Returns:
            str - 構築されたSQL文字列。
        """
        columns_sql = ",\n    ".join(columns_def)
        
        if alias == "main":
            create_sql = f'CREATE TABLE "{table_name}" (\n    {columns_sql}\n);'
        else:
            create_sql = f'CREATE TABLE "{alias}"."{table_name}" (\n    {columns_sql}\n);'

        return create_sql
