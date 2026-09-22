"""
Summary:
    fws_sqlite_viewer アプリのテーブル作成ダイアログ用イベントモジュール。
Description:
    新規テーブル作成用ダイアログのイベントバインドおよび作成ロジックを実行します。
Attachment:
    なし
"""
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional

from fws_apps.tkinter.fws_sqlite_viewer.views.view import fws_sqlite_viewer_create_table_view
from fws_apps.tkinter.fws_sqlite_viewer.views.logic import fws_sqlite_viewer_create_table_logic

class FwsSqliteViewerCreateTableEvent:
    """
    Summary:
        テーブル作成ダイアログのイベントハンドラクラス。
    Description:
        ダイアログの表示、入力値の検証、SQLの構築、および実行を行います。
    """

    def __init__(self, master: tk.Misc, alias: str, on_success_callback: Callable[[str], None]) -> None:
        """
        Summary:
            コンストラクタ。
        Args:
            master: tk.Misc - 親ウィジェット。
            alias: str - テーブルを作成する対象のDBエイリアス。
            on_success_callback: Callable[[str], None] - 作成成功時にSQLを渡すコールバック関数。
        """
        self.alias = alias
        self.logic = fws_sqlite_viewer_create_table_logic.FwsSqliteViewerCreateTableLogic()
        self.on_success_callback = on_success_callback
        
        self.view = fws_sqlite_viewer_create_table_view.FwsSqliteViewerCreateTableView(master, alias)
        self._bind_events()
        
        # 初期状態で1行追加しておく
        self._add_column_row()

    def _bind_events(self) -> None:
        """
        Summary:
            ボタンなどのイベントをバインドします。
        """
        self.view.btn_add_column.config(command=self._add_column_row)
        self.view.btn_cancel.config(command=self.view.destroy)
        self.view.btn_create.config(command=self._create_table)

    def _add_column_row(self) -> None:
        """
        Summary:
            新しいカラム行を追加し、削除ボタンのイベントをバインドします。
        """
        frm_row = self.view.add_column_row()
        btn_del = frm_row.widgets["btn_del"]
        btn_del.config(command=lambda row=frm_row: self.view.remove_column_row(row))

    def _create_table(self) -> None:
        """
        Summary:
            入力値を検証し、CREATE TABLE文を構築して実行します。
        """
        table_name = self.view.ent_table_name.get().strip()
        if not table_name:
            messagebox.showerror("Validation Error", "Table Name cannot be empty.", parent=self.view)
            return

        if not self.view.columns_frames:
            messagebox.showerror("Validation Error", "At least one column is required.", parent=self.view)
            return

        columns_def = []
        col_names_set = set()
        pk_count = 0

        for frm_row in self.view.columns_frames:
            widgets = frm_row.widgets
            
            c_name = widgets["name"].get().strip()
            if not c_name:
                messagebox.showerror("Validation Error", "Column Name cannot be empty.", parent=self.view)
                return
            if c_name.lower() in col_names_set:
                messagebox.showerror("Validation Error", f"Duplicate column name: '{c_name}'", parent=self.view)
                return
            col_names_set.add(c_name.lower())

            c_type = widgets["type"].get().strip()
            
            is_pk = widgets["pk"].get()
            if is_pk:
                pk_count += 1
                
            is_notnull = widgets["notnull"].get()
            
            c_default = widgets["default"].get().strip()

            # 構文の組み立て
            col_sql = f'"{c_name}" {c_type}' if c_type else f'"{c_name}"'
            if is_pk:
                col_sql += " PRIMARY KEY"
            if is_notnull:
                col_sql += " NOT NULL"
            if c_default:
                # デフォルト値が文字列として入力された場合のクォート処理は簡易的に行う。
                # 数値やキーワード（CURRENT_TIMESTAMP等）の場合はそのまま。
                # 安全のため、単一引用符が含まれていないか等の検証が必要だが、ここではSQL生成を優先。
                if c_default.upper() in ("NULL", "CURRENT_TIMESTAMP", "CURRENT_DATE", "CURRENT_TIME"):
                    col_sql += f" DEFAULT {c_default}"
                elif c_default.replace(".", "", 1).isdigit() or (c_default.startswith("-") and c_default[1:].replace(".", "", 1).isdigit()):
                    col_sql += f" DEFAULT {c_default}"
                else:
                    if not (c_default.startswith("'") and c_default.endswith("'")):
                        # シングルクォートで囲む
                        c_default_escaped = c_default.replace("'", "''")
                        col_sql += f" DEFAULT '{c_default_escaped}'"
                    else:
                        col_sql += f" DEFAULT {c_default}"

            columns_def.append(col_sql)

        if pk_count > 1:
            messagebox.showerror("Validation Error", "Multiple PRIMARY KEYs defined. Please define at most one.", parent=self.view)
            return

        try:
            # SQLを構築
            create_sql = self.logic.build_create_table_sql(table_name, self.alias, columns_def)
            
            # 成功したのでコールバックを呼んでSQLを親に渡し、自身を閉じる
            if self.on_success_callback:
                self.on_success_callback(create_sql)
                
            self.view.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create table:\n{e}", parent=self.view)
