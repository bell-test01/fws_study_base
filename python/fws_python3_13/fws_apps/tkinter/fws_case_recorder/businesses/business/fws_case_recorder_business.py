"""
Summary:
    fws_case_recorder アプリのビジネスロジックモジュール。
Description:
    SQLiteデータベースへのCRUD操作および曖昧検索を提供します。
Attachment:
    なし
"""
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fws_apps.tkinter.fws_case_recorder.constant import fws_case_recorder_const
from fws_apps.tkinter.fws_case_recorder.businesses.entity import fws_case_recorder_entity_record
from fws_apps.tkinter.fws_case_recorder.businesses.entity import fws_case_recorder_entity_template

class FwsCaseRecorderBusiness:
    """
    Summary:
        ビジネスロジッククラス。
    Description:
        データベースの初期化、案件記録および定型文のCRUD操作、曖昧検索を提供します。
    """

    #region Constructor
    def __init__(self) -> None:
        """
        Summary:
            コンストラクタ。
        Description:
            データベースの初期化を行います。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._db_path: Path = fws_case_recorder_const.DB_PATH
        """Path - データベースファイルパス"""
        self._initialize_database()

    def _initialize_database(self) -> None:
        """
        Summary:
            データベースを初期化します。
        Description:
            DBディレクトリが存在しない場合は作成し、DDLファイルを読み込んでテーブルを作成します。
        Args:
            なし
        Returns:
            None - 戻り値なし。
        """
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        ddl_path: Path = fws_case_recorder_const.DDL_PATH
        """Path - DDLファイルパス"""
        if not ddl_path.exists():
            raise FileNotFoundError(f"DDLファイルが見つかりません: {ddl_path}")
        ddl_content: str = ddl_path.read_text(encoding="utf-8")
        """str - DDLファイル内容"""
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            connection.executescript(ddl_content)
            connection.commit()
    #endregion

    #region Public Methods
    def insert_record(self, fws_case_recorder_entity_record_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord) -> int:
        """
        Summary:
            案件記録をデータベースに挿入します。
        Description:
            案件記録エンティティの内容をcase_recordsテーブルに保存し、採番されたIDを返却します。
        Args:
            fws_case_recorder_entity_record_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord - 挿入する案件記録エンティティ。
        Returns:
            int - 挿入されたレコードのID。
        """
        current_time: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        """str - 現在日時文字列"""
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute(
                "INSERT INTO case_records (region, building, case_number, record_time, content, created_at, updated_at, is_editing) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    fws_case_recorder_entity_record_obj.region,
                    fws_case_recorder_entity_record_obj.building,
                    fws_case_recorder_entity_record_obj.case_number,
                    fws_case_recorder_entity_record_obj.record_time,
                    fws_case_recorder_entity_record_obj.content,
                    current_time,
                    current_time,
                    fws_case_recorder_entity_record_obj.is_editing
                )
            )
            connection.commit()
            inserted_id: int = cursor.lastrowid
            """int - 挿入されたレコードID"""
            return inserted_id

    def update_record(self, fws_case_recorder_entity_record_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord) -> None:
        """
        Summary:
            案件記録を更新します。
        Description:
            指定されたIDの案件記録を更新します。
        Args:
            fws_case_recorder_entity_record_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord - 更新する案件記録エンティティ。
        Returns:
            None - 戻り値なし。
        """
        current_time: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        """str - 現在日時文字列"""
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute(
                "UPDATE case_records SET region = ?, building = ?, case_number = ?, "
                "record_time = ?, content = ?, updated_at = ? WHERE id = ?",
                (
                    fws_case_recorder_entity_record_obj.region,
                    fws_case_recorder_entity_record_obj.building,
                    fws_case_recorder_entity_record_obj.case_number,
                    fws_case_recorder_entity_record_obj.record_time,
                    fws_case_recorder_entity_record_obj.content,
                    current_time,
                    fws_case_recorder_entity_record_obj.record_id
                )
            )
            connection.commit()

    def update_editing_status(self, record_id: int, is_editing: int) -> None:
        """
        Summary:
            指定レコードの編集中フラグを更新します。
        Description:
            指定したレコードのis_editingカラムを指定値で更新します。
        Args:
            record_id: int - 更新対象のレコードID。
            is_editing: int - 編集中フラグの値。
        Returns:
            None - 戻り値なし。
        """
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute("UPDATE case_records SET is_editing = ? WHERE id = ?", (is_editing, record_id))
            connection.commit()

    def delete_record(self, record_id: int) -> None:
        """
        Summary:
            案件記録を削除します。
        Description:
            指定されたIDの案件記録をcase_recordsテーブルから削除します。
        Args:
            record_id: int - 削除するレコードのID。
        Returns:
            None - 戻り値なし。
        """
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute("DELETE FROM case_records WHERE id = ?", (record_id,))
            connection.commit()

    def search_records(self, case_number: str, region: str = "", building: str = "") -> List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord]:
        """
        Summary:
            条件（案件番号・県域・ビル名）で案件記録を検索します。
        Description:
            指定された条件で部分一致検索を行い、案件記録を取得します。
        Args:
            case_number: str - 検索する案件番号。
            region: str - 検索する県域。
            building: str - 検索するビル名。
        Returns:
            List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord] - 検索結果のエンティティリスト。
        """
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            connection.row_factory = sqlite3.Row
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            query = "SELECT id, region, building, case_number, record_time, content, created_at, updated_at, is_editing FROM case_records WHERE 1=1"
            params = []
            if case_number:
                query += " AND case_number LIKE ?"
                params.append(f"%{case_number}%")
            if region:
                query += " AND region LIKE ?"
                params.append(f"%{region}%")
            if building:
                query += " AND building LIKE ?"
                params.append(f"%{building}%")
            query += " ORDER BY record_time DESC"

            cursor.execute(query, params)
            rows: List[sqlite3.Row] = cursor.fetchall()
            """List[sqlite3.Row] - 検索結果行"""
            result_list: List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord] = []
            """List[FwsCaseRecorderEntityRecord] - 変換後のエンティティリスト"""
            for row in rows:
                result_list.append(self._convert_row_to_record_entity(row))
            return result_list

    def fetch_active_records(self) -> List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord]:
        """
        Summary:
            編集中（is_editing=1）の案件記録を取得します。
        Description:
            is_editingが1のレコードを取得し、エンティティリストとして返却します。
        Args:
            なし
        Returns:
            List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord] - 編集中エンティティリスト。
        """
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            connection.row_factory = sqlite3.Row
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute("SELECT id, region, building, case_number, record_time, content, created_at, updated_at, is_editing FROM case_records WHERE is_editing = 1 ORDER BY record_time DESC")
            rows: List[sqlite3.Row] = cursor.fetchall()
            """List[sqlite3.Row] - 検索結果行"""
            result_list: List[fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord] = []
            """List[FwsCaseRecorderEntityRecord] - 変換後のエンティティリスト"""
            for row in rows:
                result_list.append(self._convert_row_to_record_entity(row))
            return result_list

    def search_case_numbers_by_region_building(self, region: str, building: str) -> List[str]:
        """
        Summary:
            県域とビル名による案件番号の曖昧検索を行います。
        Description:
            県域とビル名の組み合わせでLIKE検索を行い、該当する案件番号の重複なしリストを返却します。
        Args:
            region: str - 県域（部分一致検索）。
            building: str - ビル名（部分一致検索）。
        Returns:
            List[str] - 該当する案件番号のリスト（重複なし）。
        """
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            query: str = "SELECT DISTINCT case_number FROM case_records WHERE 1=1"
            """str - 検索クエリ"""
            params: list = []
            """list - クエリパラメータ"""
            if region:
                query += " AND region LIKE ?"
                params.append(f"%{region}%")
            if building:
                query += " AND building LIKE ?"
                params.append(f"%{building}%")
            query += " ORDER BY case_number"
            cursor.execute(query, params)
            rows: List[tuple] = cursor.fetchall()
            """List[tuple] - 検索結果行"""
            case_number_list: List[str] = [row[0] for row in rows if row[0]]
            """List[str] - 案件番号リスト"""
            return case_number_list

    def fetch_all_templates(self) -> List[fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate]:
        """
        Summary:
            全定型文を取得します。
        Description:
            templatesテーブルから全件を取得してエンティティリストとして返却します。
        Args:
            なし
        Returns:
            List[fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate] - 定型文エンティティのリスト。
        """
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            connection.row_factory = sqlite3.Row
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute(
                "SELECT id, title, content, created_at, updated_at FROM templates ORDER BY title"
            )
            rows: List[sqlite3.Row] = cursor.fetchall()
            """List[sqlite3.Row] - 検索結果行"""
            result_list: List[fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate] = []
            """List[FwsCaseRecorderEntityTemplate] - 変換後のエンティティリスト"""
            for row in rows:
                result_list.append(self._convert_row_to_template_entity(row))
            return result_list

    def insert_template(self, fws_case_recorder_entity_template_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate) -> int:
        """
        Summary:
            定型文をデータベースに挿入します。
        Description:
            定型文エンティティの内容をtemplatesテーブルに保存し、採番されたIDを返却します。
        Args:
            fws_case_recorder_entity_template_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate - 挿入する定型文エンティティ。
        Returns:
            int - 挿入されたレコードのID。
        """
        current_time: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        """str - 現在日時文字列"""
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute(
                "INSERT INTO templates (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (
                    fws_case_recorder_entity_template_obj.title,
                    fws_case_recorder_entity_template_obj.content,
                    current_time,
                    current_time
                )
            )
            connection.commit()
            inserted_id: int = cursor.lastrowid
            """int - 挿入されたレコードID"""
            return inserted_id

    def update_template(self, fws_case_recorder_entity_template_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate) -> None:
        """
        Summary:
            定型文を更新します。
        Description:
            指定されたIDの定型文を更新します。
        Args:
            fws_case_recorder_entity_template_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate - 更新する定型文エンティティ。
        Returns:
            None - 戻り値なし。
        """
        current_time: str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        """str - 現在日時文字列"""
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute(
                "UPDATE templates SET title = ?, content = ?, updated_at = ? WHERE id = ?",
                (
                    fws_case_recorder_entity_template_obj.title,
                    fws_case_recorder_entity_template_obj.content,
                    current_time,
                    fws_case_recorder_entity_template_obj.template_id
                )
            )
            connection.commit()

    def delete_template(self, template_id: int) -> None:
        """
        Summary:
            定型文を削除します。
        Description:
            指定されたIDの定型文をtemplatesテーブルから削除します。
        Args:
            template_id: int - 削除する定型文のID。
        Returns:
            None - 戻り値なし。
        """
        with closing(sqlite3.connect(str(self._db_path))) as connection:
            """sqlite3.Connection - データベース接続"""
            cursor: sqlite3.Cursor = connection.cursor()
            """sqlite3.Cursor - カーソル"""
            cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))
            connection.commit()
    #endregion

    #region Private Methods

    def _convert_row_to_record_entity(self, row: sqlite3.Row) -> fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord:
        """
        Summary:
            データベース行を案件記録エンティティに変換します。
        Description:
            sqlite3.Rowオブジェクトからエンティティオブジェクトを生成します。
        Args:
            row: sqlite3.Row - データベースの行データ。
        Returns:
            fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord - 変換後のエンティティ。
        """
        fws_case_recorder_entity_record_obj: fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord = fws_case_recorder_entity_record.FwsCaseRecorderEntityRecord()
        """FwsCaseRecorderEntityRecord - 案件記録エンティティ"""
        fws_case_recorder_entity_record_obj.record_id = row["id"]
        fws_case_recorder_entity_record_obj.region = row["region"] or ""
        fws_case_recorder_entity_record_obj.building = row["building"] or ""
        fws_case_recorder_entity_record_obj.case_number = row["case_number"] or ""
        fws_case_recorder_entity_record_obj.record_time = row["record_time"] or ""
        fws_case_recorder_entity_record_obj.content = row["content"] or ""
        fws_case_recorder_entity_record_obj.created_at = row["created_at"] or ""
        fws_case_recorder_entity_record_obj.updated_at = row["updated_at"] or ""
        
        # is_editing カラムが存在するかチェック（古いDBだとカラムがない場合があるため）
        try:
            fws_case_recorder_entity_record_obj.is_editing = row["is_editing"]
        except IndexError:
            fws_case_recorder_entity_record_obj.is_editing = 0

        return fws_case_recorder_entity_record_obj

    def _convert_row_to_template_entity(self, row: sqlite3.Row) -> fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate:
        """
        Summary:
            データベース行を定型文エンティティに変換します。
        Description:
            sqlite3.Rowオブジェクトからエンティティオブジェクトを生成します。
        Args:
            row: sqlite3.Row - データベースの行データ。
        Returns:
            fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate - 変換後のエンティティ。
        """
        fws_case_recorder_entity_template_obj: fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate = fws_case_recorder_entity_template.FwsCaseRecorderEntityTemplate()
        """FwsCaseRecorderEntityTemplate - 定型文エンティティ"""
        fws_case_recorder_entity_template_obj.template_id = row["id"]
        fws_case_recorder_entity_template_obj.title = row["title"] or ""
        fws_case_recorder_entity_template_obj.content = row["content"] or ""
        fws_case_recorder_entity_template_obj.created_at = row["created_at"] or ""
        fws_case_recorder_entity_template_obj.updated_at = row["updated_at"] or ""
        return fws_case_recorder_entity_template_obj
    #endregion
