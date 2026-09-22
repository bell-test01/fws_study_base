"""
Summary:
    テーブルスキーマのEntity。
Description:
    Business層からLogic層へ渡されるスキーマ情報のデータ構造です。
Attachment:
    なし
"""

class FwsSqliteViewerEntityTableSchema:
    """
    Summary:
        テーブルの各カラムスキーマ情報を保持するEntityクラス。
    """

    #region Constructor
    def __init__(self, cid: int, name: str, type_name: str, notnull: int, dflt_value: str, pk: int) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            PRAGMA table_info で取得した情報を格納します。
        Args:
            cid: int - カラムID
            name: str - カラム名
            type_name: str - データ型
            notnull: int - NOT NULL制約 (1: true, 0: false)
            dflt_value: str - デフォルト値
            pk: int - プライマリキー (1以上: true, 0: false)
        Returns:
            None - 戻り値なし。
        """
        self.cid: int = cid
        """int - カラムID"""
        
        self.name: str = name
        """str - カラム名"""
        
        self.type_name: str = type_name
        """str - データ型"""
        
        self.notnull: int = notnull
        """int - NOT NULL制約"""
        
        self.dflt_value: str = dflt_value
        """str - デフォルト値"""
        
        self.pk: int = pk
        """int - プライマリキー"""
    #endregion
