"""
Summary:
    テンプレート構成からファイルやディレクトリを生成するコアロジックモジュール。
Description:
    GUI/CLI の標準テンプレートや、git_structure.txt などの構造定義ファイルから
    ディレクトリおよび空ファイル群を生成する役割を持ちます。
Attachment:
    docs_fws_apps_template_generator/final_specification.md
"""
import fnmatch
import re
from pathlib import Path

from constant import fws_apps_template_generator_const as const


class FwsAppsTemplateGeneratorCore:
    """
    Summary:
        ファイルおよびディレクトリ構成の自動生成を行うコアクラス。
    Description:
        定数に定義されたテンプレート構成（GUI/CLI）、または
        git_structure.txt などのツリー構造ファイルからパスを読み取り、
        指定された出力先ディレクトリに実体（空ファイル/ディレクトリ）を作成します。
    """
    # region Constructor
    def __init__(self, output_path: str, app_name: str, template_type: str = "gui", ignore_file: str | None = None) -> None:
        """
        Summary:
            クラスの初期化を行います。
        Args:
            output_path: str - 出力先ディレクトリのパス。
            app_name: str - アプリケーション名。
            template_type: str - テンプレートの種類 ("gui" または "cli")。
            ignore_file: str | None - 除外リストファイルのパス。
        Returns:
            None - 戻り値なし。
        """
        self.output_path = Path(output_path).resolve()
        self.app_name = app_name
        self.template_type: str = template_type
        
        self.exclude_list: list[str] = []
        if ignore_file:
            ignore_path = Path(ignore_file).resolve()
            if ignore_path.exists():
                with open(ignore_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.exclude_list.append(line)
    # endregion

    # region Public Methods
    def generate_from_template(self) -> None:
        """
        Summary:
            定数 (const) に定義されたテンプレートからファイル構成を生成します。
        Description:
            インスタンス生成時に指定された `template_type` (gui または cli) に応じて
            展開する構成を切り替え、プレースホルダー `{app_name}` を置換しながら出力します。
        Args:
            None
        Returns:
            None - 戻り値なし。
        """
        if self.template_type == "cli":
            template: list[str] = const.CLI_TEMPLATE_STRUCTURE
        else:
            template: list[str] = const.GUI_TEMPLATE_STRUCTURE

        print(f"Generating {self.template_type} template for {self.app_name} at {self.output_path}")

        for item in template:
            # プレースホルダーを置換
            rel_path: str = item.replace("{app_name}", self.app_name)
            
            if self._is_excluded(rel_path):
                # ファイル自体は除外するが、親ディレクトリが除外対象でなければ作成する
                target_path: Path = self.output_path / rel_path
                if not rel_path.endswith('/'):
                    parent_rel = str(Path(rel_path).parent).replace('\\', '/')
                    if parent_rel != "." and not self._is_excluded(parent_rel):
                        if not target_path.parent.exists():
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            print(f"Created directory: {target_path.parent}")
                continue

            full_path: Path = self.output_path / rel_path

            if rel_path.endswith("/"):
                # ディレクトリ
                full_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {full_path}")
            else:
                # ファイル
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.touch(exist_ok=True)
                print(f"Created file: {full_path}")

    def generate_from_structure_file(self, file_path: str) -> None:
        """
        Summary:
            フラットなパスリスト形式のテキストファイルからファイル構成を生成します。
        Description:
            git_structure.txt などの形式で書かれた相対パス一覧を読み取り、
            ディレクトリおよびファイル構成を生成します。
        Args:
            file_path: str - 読み込む構造定義ファイルのパス。
        Returns:
            None - 戻り値なし。
        """
        structure_file: Path = Path(file_path).resolve()
        if not structure_file.exists():
            raise FileNotFoundError(f"Structure file not found: {structure_file}")
            
        print(f"Generating from structure file {structure_file} at {self.output_path}")

        with open(structure_file, 'r', encoding='utf-8') as f:
            lines: list[str] = f.readlines()

        for line in lines:
            line = line.rstrip('\n').strip()
            if not line:
                continue

            current_path: Path = self.output_path / line

            # 除外判定
            # ルートパスからの相対パスで判定する
            try:
                rel_from_root = current_path.relative_to(self.output_path)
                rel_path_str = str(rel_from_root).replace('\\', '/')
                if self._is_excluded(rel_path_str):
                    # ファイル自体は除外するが、親ディレクトリが除外対象でなければ作成する
                    if not line.endswith('/'):
                        parent_rel = str(Path(rel_path_str).parent).replace('\\', '/')
                        if parent_rel != "." and not self._is_excluded(parent_rel):
                            if not current_path.parent.exists():
                                current_path.parent.mkdir(parents=True, exist_ok=True)
                                print(f"Created directory: {current_path.parent}")
                    continue
            except ValueError:
                pass

            if line.endswith('/'):
                current_path.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {current_path}")
            else:
                current_path.parent.mkdir(parents=True, exist_ok=True)
                current_path.touch(exist_ok=True)
                print(f"Created file: {current_path}")
    # endregion

    # region Private Methods
    def _is_excluded(self, path_str: str) -> bool:
        """
        Summary:
            除外リストに含まれるパスかどうかを判定します。
        Description:
            設定された除外パターンとパスを比較します。
            パス全体とのパターンマッチ、およびパスの各構成要素とのマッチを行います。
        Args:
            path_str: str - 判定対象の相対パス。
        Returns:
            bool - 除外対象であれば True、そうでなければ False。
        """
        path = Path(path_str)
        path_str_fwd = str(path).replace('\\', '/')
        
        for exclude in self.exclude_list:
            exclude = exclude.strip()
            if not exclude:
                continue

            # 1. フルパス（相対パス）としてのマッチング
            if fnmatch.fnmatch(path_str_fwd, exclude):
                return True
                
            # 2. パスの各構成要素に対するマッチング
            clean_exclude = exclude.strip('/')
            for part in path.parts:
                if fnmatch.fnmatch(part, clean_exclude):
                    return True

        return False
    # endregion
