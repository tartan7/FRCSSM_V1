"""
ファイル操作サービス
ファイルとディレクトリの操作を統一管理
"""
import os
import shutil
import glob
import re
import configparser
from typing import List, Dict, Optional
import config
from utils.drive_utils import is_removable_drive

class FileService:
    """ファイル操作の共通サービス

    basepath はUSBメモリ運用とPCインストール運用の2パターンを
    config.ini の [Paths] basepath_usb / basepath_fixed に別々に保存する。
    起動しているドライブがリムーバブルメディアかどうかで自動的にどちらを使うか判定するため、
    USBメモリのドライブレターがPCによって変わっても再設定が不要になる。
    """

    def __init__(self):
        self.basepath = None
        self.current_path = None
        self.vix_path = None
        self._load_paths()

    def _current_mode(self) -> str:
        """アプリの実行場所のドライブ種別から動作モードを判定する"""
        return 'usb' if is_removable_drive(config.APP_ROOT) else 'fixed'

    def _basepath_key(self) -> str:
        return 'basepath_usb' if self._current_mode() == 'usb' else 'basepath_fixed'

    def _resolve_stored_path(self, stored: str) -> Optional[str]:
        """config.ini に保存された文字列を絶対パスに解決する。
        相対パス表記（USBメモリ運用でドライブレターに依存しないように保存されたもの）は
        APP_ROOT（実行ファイルの現在の場所＝現在のドライブレター）を基準に解決する。"""
        if not stored:
            return None
        if os.path.isabs(stored):
            return os.path.normpath(stored)
        return os.path.normpath(os.path.join(config.APP_ROOT, stored))

    def _relativize_if_possible(self, target: str) -> str:
        """target を APP_ROOT からの相対パスに変換できれば変換する。
        別ドライブ等で変換できない場合は絶対パスのまま返す。"""
        try:
            return os.path.relpath(target, config.APP_ROOT)
        except ValueError:
            return os.path.normpath(target)

    def _load_paths(self) -> None:
        """config.ini の [Paths] セクションからパス設定を読み込む"""
        try:
            parser = configparser.RawConfigParser()
            parser.read(config.CONFIG_INI, encoding='UTF-8')

            stored_basepath = parser.get('Paths', self._basepath_key(), fallback='').strip()
            if not stored_basepath:
                # 旧形式（basepath 単一キー）からの移行フォールバック
                stored_basepath = parser.get('Paths', 'basepath', fallback='').strip()
            self.basepath = self._resolve_stored_path(stored_basepath)

            stored_current = parser.get('Paths', 'current_path', fallback='').strip()
            if stored_current and self.basepath and not os.path.isabs(stored_current):
                self.current_path = os.path.normpath(os.path.join(self.basepath, stored_current))
            else:
                self.current_path = stored_current or None

            self.vix_path = parser.get('Paths', 'vix_path', fallback='').strip() or None
        except Exception as e:
            print(f"Error reading {config.CONFIG_INI}: {str(e)}")

    def save_initial_config(self, basepath: str, vix_path: str = '') -> None:
        """初回セットアップ: config.ini を新規生成する"""
        try:
            key = self._basepath_key()
            other_key = 'basepath_fixed' if key == 'basepath_usb' else 'basepath_usb'
            stored_basepath = self._relativize_if_possible(basepath) if key == 'basepath_usb' else basepath

            parser = configparser.RawConfigParser()
            parser.add_section('Paths')
            parser.set('Paths', key, stored_basepath)
            parser.set('Paths', other_key, '')
            parser.set('Paths', 'current_path', '')
            parser.set('Paths', 'vix_path', vix_path)
            parser.add_section('Excel')
            parser.set('Excel', 'booka', config.XLBOOK_A)
            parser.set('Excel', 'bookb', config.XLBOOK_B)
            parser.set('Excel', 'bookc', config.XLBOOK_C)
            parser.add_section('App')
            parser.set('App', 'log_retention_days', '30')
            parser.set('App', 'memory_threshold_mb', '500')
            with open(config.CONFIG_INI, 'w', encoding='UTF-8') as f:
                parser.write(f)
            self.basepath = self._resolve_stored_path(stored_basepath)
            self.vix_path = vix_path or None
        except Exception as e:
            print(f"Error writing initial config: {str(e)}")

    def save_paths(self, current_path: str, vix_path: Optional[str] = None) -> None:
        """パス設定を config.ini の [Paths] セクションに保存する"""
        try:
            if vix_path is None and self.vix_path:
                vix_path = self.vix_path

            basepath = self.basepath or self.get_basepath()
            stored_current = current_path
            if basepath:
                try:
                    rel = os.path.relpath(current_path, basepath)
                    if not rel.startswith('..'):
                        stored_current = rel
                except ValueError:
                    pass

            parser = configparser.RawConfigParser()
            parser.read(config.CONFIG_INI, encoding='UTF-8')
            if not parser.has_section('Paths'):
                parser.add_section('Paths')
            parser.set('Paths', 'current_path', stored_current)
            parser.set('Paths', 'vix_path', vix_path or '')

            with open(config.CONFIG_INI, 'w', encoding='UTF-8') as f:
                parser.write(f)

            self.current_path = current_path
            if vix_path:
                self.vix_path = vix_path

        except Exception as e:
            print(f"Error writing to {config.CONFIG_INI}: {str(e)}")

    def get_basepath(self) -> str:
        """basepath を取得。未設定なら config.BASE_PATH を返す。
        basepath は「終了分」フォルダそのものを指す（初回セットアップで選択）。
        """
        self._load_paths()
        return self.basepath or config.BASE_PATH

    def get_template_path(self) -> str:
        """テンプレートフォルダ（初期テンプレート/最新）のパスを返す。
        basepath（終了分）の親ディレクトリ配下にある想定。
        例: C:/inte_dir/終了分 → C:/inte_dir/初期テンプレート/最新
        """
        basepath = self.get_basepath()
        parent = os.path.dirname(os.path.normpath(basepath))
        return os.path.join(parent, config.TPATH1, config.TPATH2)

    def has_basepath_configured(self) -> bool:
        """config.ini に有効な basepath（実在するフォルダ）が設定済みか判定する"""
        self._load_paths()
        return bool(self.basepath) and os.path.isdir(self.basepath)

    def get_current_path(self) -> str:
        """現在のパスを取得。複数コントローラーが別インスタンスを持つため毎回 config.ini を再読込する。"""
        self._load_paths()
        return self.current_path or ""
    
    def get_vix_path(self) -> str:
        """VIXパスを取得"""
        return self.vix_path or ""
    
    def create_directory(self, path: str) -> bool:
        """ディレクトリを作成"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"ディレクトリ作成エラー: {str(e)}")
            return False

    def create_case_folder(self, template_path: str, dest_path: str) -> None:
        """テンプレートフォルダをコピーして案件フォルダを新規作成する。

        Raises:
            FileNotFoundError: テンプレートが存在しない
            FileExistsError: 作成先が既に存在する
            ValueError: パスが不正
        """
        template_path = os.path.normpath(template_path.strip()) if template_path else ''
        dest_path = os.path.normpath(dest_path.strip()) if dest_path else ''
        if not template_path or not dest_path or dest_path in ('.', ''):
            raise ValueError("テンプレートまたは作成先パスが不正です")
        if not os.path.isdir(template_path):
            raise FileNotFoundError(f"テンプレートフォルダがありません:\n{template_path}")
        if os.path.exists(dest_path):
            raise FileExistsError(f"既に存在します:\n{dest_path}")
        parent = os.path.dirname(dest_path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        shutil.copytree(template_path, dest_path)

    def create_folder_structure(self, base_path: str, folder_name: str) -> Dict[str, bool]:
        """フォルダ構造を作成"""
        results = {}
        folders = [
            "初期テンプレート",
            "最新",
            "終了分",
            "CD用"
        ]
        
        for folder in folders:
            full_path = os.path.join(base_path, folder_name, folder)
            results[folder] = self.create_directory(full_path)
        
        return results
    
    def copy_file(self, src: str, dst: str) -> bool:
        """ファイルをコピー"""
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:
            print(f"ファイルコピーエラー: {str(e)}")
            return False
    
    def move_file(self, src: str, dst: str) -> bool:
        """ファイルを移動"""
        try:
            shutil.move(src, dst)
            return True
        except Exception as e:
            print(f"ファイル移動エラー: {str(e)}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """ファイルを削除"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"ファイル削除エラー: {str(e)}")
            return False
    
    def find_files(self, pattern: str, directory: str = None) -> List[str]:
        """パターンに一致するファイルを検索"""
        if directory is None:
            directory = self.get_current_path()
        
        try:
            search_pattern = os.path.join(directory, pattern)
            return glob.glob(search_pattern)
        except Exception as e:
            print(f"ファイル検索エラー: {str(e)}")
            return []
    
    def get_file_size(self, file_path: str) -> int:
        """ファイルサイズを取得"""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            print(f"ファイルサイズ取得エラー: {str(e)}")
            return 0
    
    def file_exists(self, file_path: str) -> bool:
        """ファイルが存在するかチェック"""
        return os.path.exists(file_path)
    
    def directory_exists(self, dir_path: str) -> bool:
        """ディレクトリが存在するかチェック"""
        return os.path.isdir(dir_path)
    
    def get_directory_contents(self, dir_path: str) -> List[str]:
        """ディレクトリの内容を取得"""
        try:
            return os.listdir(dir_path)
        except Exception as e:
            print(f"ディレクトリ内容取得エラー: {str(e)}")
            return []
    
    def extract_family_name(self, path: str) -> str:
        """パスから遺族名を抽出"""
        try:
            path_parts = path.split("\\\\")
            folder_name = path_parts[-1]
            # 数字とカンマを除去
            pattern = r'[A-Za-z0-9,]'
            family_name = re.sub(pattern, '', folder_name)
            return family_name
        except Exception as e:
            print(f"遺族名抽出エラー: {str(e)}")
            return ""
    
    def get_relative_path(self, full_path: str, base_path: str = None) -> str:
        """相対パスを取得"""
        if base_path is None:
            base_path = self.get_current_path()
        
        try:
            return os.path.relpath(full_path, base_path)
        except Exception as e:
            print(f"相対パス取得エラー: {str(e)}")
            return full_path
    
    def normalize_path(self, path: str) -> str:
        """パスを正規化"""
        return os.path.normpath(path)
    
    def join_paths(self, *paths) -> str:
        """パスを結合"""
        return os.path.join(*paths)
    
    def get_file_extension(self, file_path: str) -> str:
        """ファイル拡張子を取得"""
        return os.path.splitext(file_path)[1]
    
    def get_file_name(self, file_path: str) -> str:
        """ファイル名を取得"""
        return os.path.basename(file_path)
    
    def get_directory_name(self, file_path: str) -> str:
        """ディレクトリ名を取得"""
        return os.path.dirname(file_path)