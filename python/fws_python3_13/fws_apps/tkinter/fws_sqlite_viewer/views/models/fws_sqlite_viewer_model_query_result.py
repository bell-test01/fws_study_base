"""
Summary:
    クエリ実行結果のModel。
Description:
    Logic層からEvent層(UI)へ渡される表示用データ構造です。
Attachment:
    なし
"""
from typing import List, Tuple, Any, Optional
from fws_apps.tkinter.fws_sqlite_viewer.businesses.entity import fws_sqlite_viewer_entity_query_result

class FwsSqliteViewerModelQueryResult:
    """
    Summary:
        クエリ実行結果を保持するViewModelクラス。
    """

    #region Constructor
    def __init__(self, entity: fws_sqlite_viewer_entity_query_result.FwsSqliteViewerEntityQueryResult = None) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            Entityからデータを詰め替えます。
        Args:
            entity: fws_sqlite_viewer_entity_query_result.FwsSqliteViewerEntityQueryResult - データ元となるEntity
        Returns:
            None - 戻り値なし。
        """
        if entity:
            self.columns: List[str] = entity.columns
            self.rows: List[Tuple[Any, ...]] = entity.rows
            self.rowcount: int = entity.rowcount
            self.error_message: Optional[str] = entity.error_message
            self.execution_time_ms: float = entity.execution_time_ms
            self.execution_history: List[Tuple[str, int]] = entity.execution_history
            self.executed_select_sql: str = getattr(entity, 'executed_select_sql', "")
        else:
            self.columns: List[str] = []
            self.rows: List[Tuple[Any, ...]] = []
            self.rowcount: int = -1
            self.error_message: Optional[str] = None
            self.execution_time_ms: float = 0.0
            self.execution_history: List[Tuple[str, int]] = []
            self.executed_select_sql: str = ""
    #endregion

    #region Public Methods
    @property
    def is_success(self) -> bool:
        """
        Summary:
            クエリが成功したかどうかを返します。
        Returns:
            bool - 成功時はTrue、エラー時はFalse。
        """
        return self.error_message is None
    #endregion
