"""
Summary:
    テーブルスキーマのModel。
Description:
    Logic層からEvent層(UI)へ渡されるスキーマ情報のデータ構造です。
Attachment:
    なし
"""
from fws_apps.tkinter.fws_sqlite_viewer.businesses.entity import fws_sqlite_viewer_entity_table_schema

class FwsSqliteViewerModelTableSchema:
    """
    Summary:
        テーブルの各カラムスキーマ情報を保持するViewModelクラス。
    """

    #region Constructor
    def __init__(self, entity: fws_sqlite_viewer_entity_table_schema.FwsSqliteViewerEntityTableSchema) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            Entityからデータを詰め替えます。
        Args:
            entity: fws_sqlite_viewer_entity_table_schema.FwsSqliteViewerEntityTableSchema - データ元となるEntity
        Returns:
            None - 戻り値なし。
        """
        self.cid: int = entity.cid
        """int - カラムID"""
        
        self.name: str = entity.name
        """str - カラム名"""
        
        self.type_name: str = entity.type_name
        """str - データ型"""
        
        self.notnull: int = entity.notnull
        """int - NOT NULL制約"""
        
        self.dflt_value: str = entity.dflt_value
        """str - デフォルト値"""
        
        self.pk: int = entity.pk
        """int - プライマリキー"""
    #endregion
