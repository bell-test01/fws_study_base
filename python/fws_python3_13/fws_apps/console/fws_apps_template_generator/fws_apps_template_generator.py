"""
Summary:
    FWSアプリテンプレートジェネレータのエントリポイントモジュール。
Description:
    コマンドライン引数をパースし、FwsAppsTemplateGeneratorCoreを呼び出して、ファイル・フォルダ構成を自動生成します。
Attachment:
    docs_fws_apps_template_generator/final_specification.md
"""
import argparse
import sys
from pathlib import Path

from core.fws_apps_template_generator_core import FwsAppsTemplateGeneratorCore


def main():
    """
    Summary:
        fws_apps_template_generator のエントリポイントメソッド。
    Description:
        コマンドライン引数をパースし、指定された条件に基づいてfwsプロジェクトのファイル構成を生成します。
    Args:
        None
    Returns:
        None - 戻り値なし。
    """
    # ヘルプメッセージや使用例を見やすくするための設定
    description_text: str = (
        "=========================================\n"
        " FWS Apps Template Generator\n"
        "=========================================\n"
        "fwsプロジェクトのファイル・フォルダ構成を自動生成するツールです。\n"
        "GUI/CLIのテンプレート展開、または git_structure.txt からの生成をサポートします。"
    )
    epilog_text: str = (
        "【使用例】\n"
        "  # GUIテンプレートを使ってアプリを生成する場合\n"
        "  python fws_apps_template_generator.py -p ./my_new_app -n my_new_app\n\n"
        "  # CLIテンプレートを使ってアプリを生成する場合\n"
        "  python fws_apps_template_generator.py -p ./my_cli_app -n my_cli_app -t cli\n\n"
        "  # git_structure.txt から構成を生成する場合\n"
        "  python fws_apps_template_generator.py -p ./custom_app -n custom_app -f ./git_structure.txt"
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=description_text,
        epilog=epilog_text,
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-p", "--path", help="出力先ディレクトリのルートパス")
    parser.add_argument("-n", "--app-name", help="アプリケーション名（例: fws_sample_app）")
    parser.add_argument("-f", "--file", help="読み込む構造定義ファイル (git_structure.txt等)")
    parser.add_argument("-t", "--type", choices=["gui", "cli"], help="生成するテンプレートの種類 (デフォルト: gui)")

    args: argparse.Namespace = parser.parse_args()

    out_path_str: str | None = args.path
    app_name_str: str | None = args.app_name
    template_type: str | None = args.type
    structure_file: str | None = args.file

    # 引数が不足している場合は対話式に入力させる
    if not structure_file and not template_type:
        structure_file = input("読み込む構造定義ファイル(git_structure.txt等)のパスを入力してください（使用しない場合は空のままEnter）: ").strip(' "\'')
        if not structure_file:
            mode = input("生成モードを選択してください (1: GUIテンプレート, 2: CLIテンプレート): ").strip()
            if mode == "2":
                template_type = "cli"
            else:
                if mode != "1":
                    print("無効な選択です。デフォルトのGUIテンプレートを使用します。")
                template_type = "gui"

    if not template_type:
        template_type = "gui"

    if not out_path_str:
        out_path_str = input("出力先ディレクトリのルートパスを入力してください: ").strip(' "\'')

    # 構造定義ファイルを使用しない場合のみ、アプリケーション名を聞く
    if not structure_file and not app_name_str:
        app_name_str = input("アプリケーション名を入力してください（例: fws_sample_app）: ").strip()

    if not app_name_str:
        app_name_str = ""

    if not out_path_str or (not structure_file and not app_name_str):
        print("出力先ディレクトリは必須です。（テンプレート生成の場合はアプリケーション名も必須です）", file=sys.stderr)
        input("\nEnterキーを押して終了してください...")
        sys.exit(1)

    # 出力先パスの検証と作成
    output_path: Path = Path(out_path_str).resolve()
    if not output_path.exists():
        print(f"Creating output root directory: {output_path}")
        output_path.mkdir(parents=True, exist_ok=True)

    # data/.templateignore が存在するか確認
    ignore_file_path: str | None = None
    script_dir: Path = Path(__file__).parent.resolve()
    default_ignore_file: Path = script_dir / "data" / ".templateignore"
    if default_ignore_file.exists() and default_ignore_file.is_file():
        ignore_file_path = str(default_ignore_file)

    fws_apps_template_generator_core_obj: FwsAppsTemplateGeneratorCore = FwsAppsTemplateGeneratorCore(
        output_path=str(output_path),
        app_name=app_name_str,
        template_type=template_type,
        ignore_file=ignore_file_path
    )

    try:
        if structure_file:
            fws_apps_template_generator_core_obj.generate_from_structure_file(structure_file)
        else:
            fws_apps_template_generator_core_obj.generate_from_template()
        print("Generation completed successfully.")
        input("\n処理が完了しました。Enterキーを押して終了してください...")
    except Exception as e:
        print(f"Error during generation: {e}", file=sys.stderr)
        input("\nエラーが発生しました。Enterキーを押して終了してください...")
        sys.exit(1)


if __name__ == "__main__":
    main()
