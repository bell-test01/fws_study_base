"""
Summary:
    fws_source_linkerのコア業務ロジックを実行するモジュールです。
Description:
    ショートカットの生成、ファイルコピーなどのバックエンド処理を担います。
Attachment:
    なし
"""
import shutil
import subprocess
from pathlib import Path

# fws_lib
from fws_lib.common import fws_config_manager, fws_file_utils

# app
from fws_apps.tkinter.fws_source_linker.businesses.entity import fws_source_linker_entity_config
from fws_apps.tkinter.fws_source_linker.constant import fws_source_linker_const


class FwsSourceLinkerBusiness:
    """
    Summary:
        ファイルコピーおよびショートカット生成を行うビジネスクラスです。
    Description:
        設定の読み書き、実体ファイルのコピー処理、PowerShell経由での.lnk生成を行います。
    """

    # region Constructor
    def __init__(self) -> None:
        """
        Summary:
            FwsSourceLinkerBusinessを初期化します。
        """
        app_dir: Path = Path(__file__).resolve().parent.parent.parent
        self._config_path: Path = app_dir / "data" / fws_source_linker_const.CONFIG_FILE_NAME
        fws_file_utils.ensure_dir(self._config_path.parent)
    # endregion

    # region Public Methods
    def get_config(self) -> fws_source_linker_entity_config.FwsSourceLinkerEntityConfig:
        """
        Summary:
            設定情報を取得します。
        Args:
            なし
        Returns:
            fws_source_linker_entity_config.FwsSourceLinkerEntityConfig - 設定情報を格納したEntity。
        """
        config: dict = fws_config_manager.load_json(self._config_path)
        entity = fws_source_linker_entity_config.FwsSourceLinkerEntityConfig(
            root_dir=config.get(fws_source_linker_const.CONFIG_KEY_ROOT_DIR, ""),
            root_dir_history=config.get(fws_source_linker_const.CONFIG_KEY_ROOT_DIR_HISTORY, []),
            dest_dir=config.get(fws_source_linker_const.CONFIG_KEY_DEST_DIR, ""),
            dest_dir_history=config.get(fws_source_linker_const.CONFIG_KEY_DEST_DIR_HISTORY, []),
            dest_sub_dir=config.get(fws_source_linker_const.CONFIG_KEY_DEST_SUB_DIR, "")
        )
        return entity

    def save_config(self, entity: fws_source_linker_entity_config.FwsSourceLinkerEntityConfig) -> None:
        """
        Summary:
            設定情報を保存します。
        Args:
            entity: fws_source_linker_entity_config.FwsSourceLinkerEntityConfig - 保存する設定情報Entity。
        Returns:
            None
        """
        config: dict = {
            fws_source_linker_const.CONFIG_KEY_ROOT_DIR: entity.root_dir,
            fws_source_linker_const.CONFIG_KEY_ROOT_DIR_HISTORY: entity.root_dir_history,
            fws_source_linker_const.CONFIG_KEY_DEST_DIR: entity.dest_dir,
            fws_source_linker_const.CONFIG_KEY_DEST_DIR_HISTORY: entity.dest_dir_history,
            fws_source_linker_const.CONFIG_KEY_DEST_SUB_DIR: entity.dest_sub_dir
        }
        fws_config_manager.save_json(self._config_path, config)

    def create_shortcut(self, target_path: str, dest_dir: str) -> None:
        """
        Summary:
            指定されたパスへのショートカットを生成します。
        Args:
            target_path: str - リンク先の元のパス（ファイルまたはフォルダ）。
            dest_dir: str - ショートカットを配置するディレクトリパス。
        Returns:
            None
        """
        target_path_obj: Path = Path(target_path)
        
        # ファイルの場合は親フォルダへのリンクにする
        if target_path_obj.is_file():
            link_target: str = str(target_path_obj.parent.resolve())
            shortcut_name: str = f"【原本】{target_path_obj.parent.name}.lnk"
        else:
            link_target: str = str(target_path_obj.resolve())
            shortcut_name: str = f"【原本】{target_path_obj.name}.lnk"

        shortcut_path: Path = Path(dest_dir) / shortcut_name
        
        # PowerShellからWScript.Shell経由で作成
        ps_script: str = f"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
        $Shortcut.TargetPath = '{link_target}'
        $Shortcut.Save()
        """
        subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)

    def copy_items(self, items: list[str], dest_dir: str) -> list[str]:
        """
        Summary:
            指定されたファイル・フォルダをコピー先に複製し、ショートカットを生成します。
        Args:
            items: list[str] - コピー元のパスリスト。
            dest_dir: str - コピー先のディレクトリパス。
        Returns:
            list[str] - 既に存在するアイテムのパスリスト。上書き確認用。
        """
        dest_path: Path = Path(dest_dir)
        fws_file_utils.ensure_dir(dest_path)
        
        existing_items: list[str] = []
        for item in items:
            src_path: Path = Path(item)
            dst_path: Path = dest_path / src_path.name
            if dst_path.exists():
                existing_items.append(item)
        
        # 競合のないアイテムはそのままコピー
        for item in items:
            if item not in existing_items:
                self._do_copy(item, str(dest_path))
                self.create_shortcut(item, str(dest_path))
        
        return existing_items

    def force_copy_items(self, items: list[str], dest_dir: str) -> None:
        """
        Summary:
            指定されたアイテムを強制的に上書きコピーします。
        Args:
            items: list[str] - コピー元のパスリスト。
            dest_dir: str - コピー先のディレクトリパス。
        Returns:
            None
        """
        for item in items:
            self._do_copy(item, dest_dir)
            self.create_shortcut(item, dest_dir)
    # endregion

    # region Private Methods
    def _do_copy(self, src_path: str, dest_dir: str) -> None:
        """
        Summary:
            実際のコピー処理を行います。
        Args:
            src_path: str - コピー元のパス。
            dest_dir: str - コピー先のディレクトリ。
        Returns:
            None
        """
        src: Path = Path(src_path)
        dst: Path = Path(dest_dir) / src.name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            fws_file_utils.copy_file(src, dst)
    # endregion
