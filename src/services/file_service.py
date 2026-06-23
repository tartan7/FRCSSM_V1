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

class FileService:
    """ファイル操作の共通サービス"""

    def __init__(self):
        self.current_path = None
        self.vix_path = None
        self._load_paths()

    def _load_paths(self) -> None:
        """config.ini の [Paths] セクションからパス設定を読み込む"""
        try:
            parser = configparser.RawConfigParser()
            parser.read(config.CONFIG_INI, encoding='UTF-8')

            # basepath が未設定またはフォルダが存在しない場合は BASE_PATH で初期化
            basepath = parser.get('Paths', 'basepath', fallback='').strip()
            if not basepath or not os.path.isdir(basepath):
                basepath = config.BASE_PATH
                os.makedirs(basepath, exist_ok=True)
                if not parser.has_section('Paths'):
                    parser.add_section('Paths')
                parser.set('Paths', 'basepath', basepath)
                with open(config.CONFIG_INI, 'w', encoding='UTF-8') as f:
                    parser.write(f)

            self.current_path = parser.get('Paths', 'current_path', fallback='').strip() or None
            self.vix_path = parser.get('Paths', 'vix_path', fallback='').strip() or None
        except Exception as e:
            print(f"Error reading {config.CONFIG_INI}: {str(e)}")

    def save_paths(self, current_path: str, vix_path: Optional[str] = None) -> None:
        """パス設定を config.ini の [Paths] セクションに保存する"""
        try:
            if vix_path is None and self.vix_path:
                vix_path = self.vix_path

            parser = configparser.RawConfigParser()
            parser.read(config.CONFIG_INI, encoding='UTF-8')
            if not parser.has_section('Paths'):
                parser.add_section('Paths')
            parser.set('Paths', 'current_path', current_path)
            parser.set('Paths', 'vix_path', vix_path or '')

            with open(config.CONFIG_INI, 'w', encoding='UTF-8') as f:
                parser.write(f)

            self.current_path = current_path
            if vix_path:
                self.vix_path = vix_path

        except Exception as e:
            print(f"Error writing to {config.CONFIG_INI}: {str(e)}")
    
    def get_basepath(self) -> str:
        """config.ini の basepath を取得。未設定なら config.BASE_PATH を返す。"""
        try:
            parser = configparser.RawConfigParser()
            parser.read(config.CONFIG_INI, encoding='UTF-8')
            bp = parser.get('Paths', 'basepath', fallback='').strip()
            return bp if bp else config.BASE_PATH
        except Exception:
            return config.BASE_PATH

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