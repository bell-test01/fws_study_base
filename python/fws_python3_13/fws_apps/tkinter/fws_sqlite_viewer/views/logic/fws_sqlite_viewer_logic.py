"""
Summary:
    fws_sqlite_viewer アプリのロジックモジュール。
Description:
    画面表示に関連する制御や値の変換処理を配置します。
Attachment:
    なし
"""
from typing import List, Dict
import re
from pathlib import Path
from fws_apps.tkinter.fws_sqlite_viewer.businesses.business import fws_sqlite_viewer_business
from fws_apps.tkinter.fws_sqlite_viewer.views.models import fws_sqlite_viewer_model_query_result
from fws_apps.tkinter.fws_sqlite_viewer.views.models import fws_sqlite_viewer_model_table_schema

class FwsSqliteViewerLogic:
    """
    Summary:
        ビューアーのロジッククラス。
    Description:
        ビジネスロジックを呼び出し、結果をView専用のModelに詰め替えて返します。UIコンポーネント(View)には依存しません。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            変数を初期化します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_sqlite_viewer_business_obj: fws_sqlite_viewer_business.FwsSqliteViewerBusiness = fws_sqlite_viewer_business.FwsSqliteViewerBusiness()
        """fws_sqlite_viewer_business.FwsSqliteViewerBusiness - ビジネスロジックオブジェクト"""
    #endregion

    #region Public Methods
    def load_db(self, db_path: str) -> Dict[str, Dict[str, List[str]]]:
        """
        Summary:
            DBに接続し、テーブルおよびビュー一覧を取得します。
        Args:
            db_path: str - DBファイルパス。
        Returns:
            Dict[str, Dict[str, List[str]]] - テーブルおよびビューの辞書。
        """
        self._fws_sqlite_viewer_business_obj.connect(db_path)
        return self._fws_sqlite_viewer_business_obj.get_tables()

    def run_query(self, sql: str) -> fws_sqlite_viewer_model_query_result.FwsSqliteViewerModelQueryResult:
        """
        Summary:
            入力されたSQLを実行し、結果をModelとして返します。
        Args:
            sql: str - 実行するSQL文字列。
        Returns:
            fws_sqlite_viewer_model_query_result.FwsSqliteViewerModelQueryResult - 実行結果Model。
        """
        entity = self._fws_sqlite_viewer_business_obj.execute_query(sql)
        return fws_sqlite_viewer_model_query_result.FwsSqliteViewerModelQueryResult(entity)

    def update_record(self, table_name: str, target_col: str, new_value: any, old_row_dict: dict) -> int:
        """
        Summary:
            指定されたテーブルの1レコードを更新します。
        Args:
            table_name: str - 更新対象のテーブル名。
            target_col: str - 更新するカラム名。
            new_value: any - 新しい値。
            old_row_dict: dict - 更新前レコードのカラム名と値の辞書。
        Returns:
            int - 更新された行数。
        """
        return self._fws_sqlite_viewer_business_obj.update_record(table_name, target_col, new_value, old_row_dict)

    def read_table_schema(self, table_name: str, alias: str = "main") -> List[fws_sqlite_viewer_model_table_schema.FwsSqliteViewerModelTableSchema]:
        """
        Summary:
            選択されたテーブルのスキーマをModelのリストとして取得します。
        Args:
            table_name: str - テーブル名。
            alias: str - データベースエイリアス。
        Returns:
            List[fws_sqlite_viewer_model_table_schema.FwsSqliteViewerModelTableSchema] - スキーマModelのリスト。
        """
        entities = self._fws_sqlite_viewer_business_obj.get_table_schema(table_name, alias)
        return [fws_sqlite_viewer_model_table_schema.FwsSqliteViewerModelTableSchema(e) for e in entities]

    def close_db(self) -> None:
        """
        Summary:
            DB接続をクローズします。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._fws_sqlite_viewer_business_obj.close()

    def get_tables(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Summary:
            現在のデータベースのテーブルおよびビュー一覧を再取得します。
        Args:
            なし
        Returns:
            Dict[str, Dict[str, List[str]]] - テーブルおよびビューの辞書。
        """
        return self._fws_sqlite_viewer_business_obj.get_tables()

    def attach_db(self, db_path: str, alias: str = None) -> str:
        """
        Summary:
            追加のDBをアタッチし、決定したエイリアス名を返します。
        Description:
            すでに同じDBファイルがアタッチされている場合はValueErrorを送出します。
        Args:
            db_path: str - DBファイルパス。
            alias: str - セッション復元時などに指定するエイリアス名。
        Returns:
            str - 実際にアタッチされたエイリアス名。
        """
        abs_db_path = Path(db_path).resolve()
        database_list = self.get_database_list()
        
        for seq, db_name, db_file in database_list:
            if db_file:
                if Path(db_file).resolve() == abs_db_path:
                    raise ValueError(f"Database already attached as '{db_name}'.")

        final_alias = alias
        if not final_alias:
            stem = abs_db_path.stem
            safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', stem)
            
            if not safe_name:
                safe_name = "db"
            elif safe_name[0].isdigit():
                safe_name = "db_" + safe_name
                
            existing_aliases = [name for seq, name, f in database_list]
            final_alias = safe_name
            counter = 1
            while final_alias in existing_aliases:
                final_alias = f"{safe_name}_{counter}"
                counter += 1

        self._fws_sqlite_viewer_business_obj.attach_db(db_path, final_alias)
        return final_alias

    def detach_db(self, alias: str) -> None:
        """
        Summary:
            アタッチされたDBをデタッチします。
        Args:
            alias: str - エイリアス
        """
        self._fws_sqlite_viewer_business_obj.detach_db(alias)

    def get_database_list(self) -> List[tuple]:
        """
        Summary:
            アタッチされているすべてのデータベースのリストを取得します。
        Returns:
            List[tuple] - PRAGMA database_list の実行結果のタプルリスト (seq, name, file)。
        """
        return self._fws_sqlite_viewer_business_obj.get_database_list()

    def is_connected(self) -> bool:
        """
        Summary:
            DBに接続されているかどうかを返します。
        Returns:
            bool - 接続されていればTrue、そうでなければFalse。
        """
        return self._fws_sqlite_viewer_business_obj.connection is not None

    def generate_recreate_script(self, table_name: str, alias: str = "main") -> str:
        """
        Summary:
            テーブル再作成スクリプトを生成します。
        Args:
            table_name: str - テーブル名。
            alias: str - データベースエイリアス。デフォルトは "main"。
        Returns:
            str - 生成されたSQLスクリプト。
        """
        schemas = self.read_table_schema(table_name, alias)
        if not schemas:
            return ""

        # カラム名のカンマ区切り文字列（データ移行のINSERT用）
        col_names = [schema.name for schema in schemas]
        col_name_str = ",\n    ".join(col_names)

        # sqlite_master から実際の DDL を取得
        table_ddl = self._fws_sqlite_viewer_business_obj.get_table_ddl(table_name, alias)
        # 関連するインデックス・トリガーの DDL を取得
        related_ddls = self._fws_sqlite_viewer_business_obj.get_related_ddl(table_name, alias)

        if not table_ddl:
            # 万が一取得できなかった場合のフォールバック（ここは空文字を返してエラーを防ぐか、あるいは...）
            return ""

        full_table_name = f"{alias}.{table_name}" if alias != "main" else table_name
        
        # エイリアス指定がある場合、DDL内のCREATE TABLE/INDEX/TRIGGERの直後にエイリアス名を挿入する
        if alias != "main":
            import re
            # CREATE [TEMP|UNIQUE] TABLE|INDEX|TRIGGER [IF NOT EXISTS] の後をキャプチャして置換
            pattern = re.compile(r'^(CREATE\s+(?:TEMP\s+|TEMPORARY\s+|UNIQUE\s+)?(?:TABLE|INDEX|TRIGGER)\s+(?:IF\s+NOT\s+EXISTS\s+)?)', re.IGNORECASE)
            table_ddl = pattern.sub(r'\1' + f'{alias}.', table_ddl, count=1)
            related_ddls = [pattern.sub(r'\1' + f'{alias}.', ddl, count=1) for ddl in related_ddls]

        # 関連DDLの結合
        related_ddl_str = "\n".join([f"{ddl};" for ddl in related_ddls])
        if related_ddl_str:
            related_ddl_str = "\n" + related_ddl_str + "\n"

        script = f"""BEGIN TRANSACTION;

DROP TABLE IF EXISTS temp.temp_{table_name};
CREATE TEMP TABLE temp_{table_name} AS 
SELECT * FROM {full_table_name};

DROP TABLE {full_table_name};
{table_ddl};{related_ddl_str}
INSERT INTO {full_table_name} 
SELECT
    {col_name_str}
FROM
    temp_{table_name};

COMMIT;"""
        return script
    #endregion
