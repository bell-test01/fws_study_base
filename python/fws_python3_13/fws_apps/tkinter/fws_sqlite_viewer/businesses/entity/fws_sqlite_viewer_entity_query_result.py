"""
Summary:
    クエリ実行結果のEntity。
Description:
    Business層からLogic層へ渡される純粋なDBアクセス結果のデータ構造です。
Attachment:
    なし
"""
from typing import List, Tuple, Any, Optional

class FwsSqliteViewerEntityQueryResult:
    """
    Summary:
        クエリ実行結果を保持するEntityクラス。
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
        self.columns: List[str] = []
        """List[str] - カラム名のリスト"""
        
        self.rows: List[Tuple[Any, ...]] = []
        """List[Tuple[Any, ...]] - 取得されたデータ行のリスト"""
        
        self.rowcount: int = -1
        """int - 影響を受けた行数（INSERT/UPDATE時など）"""
        
        self.error_message: Optional[str] = None
        """Optional[str] - エラー発生時のメッセージ"""
        
        self.execution_time_ms: float = 0.0
        """float - 実行にかかった時間（ミリ秒）"""
        
        self.execution_history: List[Tuple[str, int]] = []
        """List[Tuple[str, int]] - 複数クエリ実行時の履歴（クエリ文字列と処理件数のタプル）"""

        self.executed_select_sql: str = ""
        """str - 最後に実行され結果セットを返したSELECT文"""
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
