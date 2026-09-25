"""
Summary:
    定型文データのエンティティモジュール。
Description:
    データベースの templates テーブルに対応するデータ構造を定義します。
Attachment:
    なし
"""
from typing import Optional

class FwsCaseRecorderEntityTemplate:
    """
    Summary:
        定型文エンティティクラス。
    Description:
        1件の定型文データを保持します。DBテーブル構造に対応します。
    """

    #region Constructor
    def __init__(self, template_id: Optional[int] = None, title: str = "", content: str = "", created_at: str = "", updated_at: str = "") -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            各フィールドを初期化します。
        Args:
            template_id: Optional[int] - テンプレートID。
            title: str - 定型文タイトル。
            content: str - 定型文本文。
            created_at: str - 作成日時。
            updated_at: str - 更新日時。
        Returns:
            None - 戻り値なし。
        """
        self.template_id: Optional[int] = template_id
        """Optional[int] - テンプレートID（AUTOINCREMENT）"""
        self.title: str = title
        """str - 定型文タイトル（選択リスト表示用）"""
        self.content: str = content
        """str - 定型文本文"""
        self.created_at: str = created_at
        """str - 作成日時"""
        self.updated_at: str = updated_at
        """str - 更新日時"""
    #endregion
