"""
Summary:
    SQLite データベース操作モジュール。
Description:
    SQLite の接続管理、基本CRUD処理を行います。
"""
#region Imports
from pathlib import Path
import sqlite3
from typing import (
                Any 
                ,Dict 
                ,List 
                ,Sequence 
                ,Self
                ,Mapping
            )

#endregion

#region Type
# SQLiteが直接扱える値の型 (None, int/bool, float, str, bytes)
type SqliteValue = int | float | str | bytes | None
"""
Summary:
    SQLiteが直接扱える値の型
Description:
    SQLiteが直接扱える値の型を定義します。
    None, int, float, str, bytes
"""

# パラメータ全体の型 (タプル・リストなどのSequence、または名前付き辞書Mapping)
type SqliteParams = Sequence[SqliteValue] | Mapping[str, SqliteValue]
"""
Summary:
    SQLiteのパラメータ全体の型
Description:
    SQLiteのパラメータ全体の型を定義します。
    タプル・リストなどのSequence、または名前付き辞書Mapping
"""
#endregion

#region class
class FwsSqliteUtil:
    """
    Summary:
        SQLiteデータベースの操作を提供するクラス。
    Description:
        特になし。
    """
    #region Constructor
    def __init__(self,main_db_path:str|Path,attache_db_paths:Dict[str,str|Path] | None = None):
        """
        Summary:
            FwsSqliteUtilのコンストラクタ。
        Args:
            main_db_path (str|Path): メインDBのパス。
            attache_db_paths (Dict[str,str|Path] | None): アタッチDBのエイリアス名とDBパスの辞書。
        Returns:
            None - 戻り値なし。
        Description:
            コネクションを作成し、sql実行可能のクラスを作成する。
        """
        #----------------------------------------------------------------------
        #DBコネクション取得
        #----------------------------------------------------------------------
        #メインDBのコネクションを取得する。
        self._connection_obj:sqlite3.Connection = self._create_connection(str(main_db_path))

        #----------------------------------------------------------------------
        #DBコネクション設定
        #----------------------------------------------------------------------
        #行ファクトリを設定する。
        self._connection_obj.row_factory = sqlite3.Row
        
        #アタッチ対象DBの有無を確認する。
        if attache_db_paths is not None:
            #アタッチ対象DBがあった場合、アタッチを実行する。
            self._attach_database(attache_db_paths)

    def _create_connection(self,db_path:str) -> sqlite3.Connection:
        """
        Summary:
            コネクションを作成し返却する。
        Args:
            db_path (str): メインDBのファイルパス。
        Returns:
            sqlite3.Connection - コネクション。
        Description:
            特になし。
        """
        return sqlite3.connect(db_path)

    def _attach_database(self,attache_db_paths:Dict[str,str|Path]) -> None:
        """
        Summary:
            アタッチ対象DBをアタッチする。
        Args:
            attache_db_paths (Dict[str,str]): アタッチ対象DBのエイリアス名とDBパスの辞書。
        Returns:
            None - 戻り値なし。
        Description:
            特になし。
        """
        sql_text:str = "ATTACH DATABASE ? AS ?"
        for schema_name,db_path in attache_db_paths.items():
            self.execute_non_query(sql_text,(str(db_path), schema_name))
        
    #endregion

    #region ContextManager
    def __enter__(self) -> Self:
        """
        Summary:
            コンテキストマネージャーのエントリーポイント。
        Args:
            None - 引数なし。
        Returns:
            Self - self。
        Description:
            コンテキストマネージャーの開始時に呼び出され、selfを返却する。
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Summary:
            コンテキストマネージャーのエンドポイント。
        Args:
            exc_type - 例外型。
            exc_val - 例外値。
            exc_tb - 例外トレースバック。
        Returns:
            None - 戻り値なし。
        Description:
            コンテキストマネージャーの終了時に呼び出され、DBコネクションをクローズする。
            正常終了の場合はコミットし、異常終了の場合はロールバックする。
        """
        #実行結果の判定を実施する。
        if exc_type is None:
            #正常終了の場合コミット
            self._connection_obj.commit()
        else:
            #異常終了の場合ロールバック
            self._connection_obj.rollback()
        
        #コネクション切断
        self._connection_obj.close()

    #endregion

    #region PublicMethod  
    def execute_non_query(self,sql_text:str,params:SqliteParams | None = None) -> int:
        """
        Summary:
            SQL(insert,update,delete,create,attach等)を実行し、影響を受けた行数を返却する。
        Args:
            sql_text (str): SQL文。
            params (SqliteParams | None): SQL文のパラメータ。
        Returns:
            int - 影響を受けた行数。
        Description:
            特になし。
        """
        try:
            #パラメータ存在確認をする。
            if params is None:
                #存在しない場合、初期値を設定する。
                params = ()

            #SQLを実行し、影響を受けた行数を返却する。
            return self._connection_obj.cursor().execute(sql_text,params).rowcount

        except sqlite3.Error as e:
            raise

    def execute_scalar(self,sql_text:str,params:SqliteParams | None = None) -> Any:
        """
        Summary:
            SQLを実行し、結果の1列目の1行目を返却する。
        Args:
            sql_text (str): SQL文。
            params (SqliteParams | None): SQL文のパラメータ。
        Returns:
            Any - 結果の1列目の1行目。
        Description:
            特になし。
        """
        try:
            #パラメータ存在確認をする。
            if params is None:
                #存在しない場合、初期値を設定する。
                params = ()

            #SQLを実行し、結果の1列目の1行目を返却する。
            return self._connection_obj.cursor().execute(sql_text,params).fetchone()[0]

        except sqlite3.Error as e:
            raise
        
    def execute_fetch_all(self,sql_text:str,params:SqliteParams | None = None) -> List[Dict[str,Any]]:
        #todo
        try:
            #パラメータ存在確認をする。
            if params is None:
                #存在しない場合、初期値を設定する。
                params = ()

            #SQLを実行し、全件取得する。
            return self._connection_obj.cursor().execute(sql_text,params).fetchall()
            #sql_result_rows:List[sqlite3.Row] = self._connection_obj.cursor().execute(sql_text,params).fetchall()
            #return [dict(sql_result_row) for sql_result_row in sql_result_rows]
        
        except sqlite3.Error as e:
            raise    

    def execute_script(self,sql_text:str) -> None:
        """
        Summary:
            SQLスクリプトを実行する。
        Args:
            sql_text (str): SQLスクリプト。
        Returns:
            None - 戻り値なし。
        Description:
            特になし。
        """
        try:
            self._connection_obj.cursor().executescript(sql_text)
        except sqlite3.Error as e:
            raise

    #endregion

#endregion