"""
データサービス
データアクセス層の統一管理
"""
from typing import Dict, List, Any, Optional
from services.excel_service import ExcelService
from services.file_service import FileService
from services.validation_service import ValidationService
from services.operations_service import OperationsService
from models.flower_model import FlowerModel
from models.condolence_model import CondolenceModel
from models.offering_model import OfferingModel
from models.incense_model import IncenseModel

class DataService:
    """データアクセスの共通サービス"""

    def __init__(self):
        self.excel_service = ExcelService()
        self.file_service = FileService()
        self.validation_service = ValidationService()
        self.operations_service = OperationsService(self.excel_service, self.file_service)
        # FileService が読み込んだ作業パスを ExcelService に注入
        self.excel_service.set_cpath(self.file_service.get_current_path())
    
    # 香典データ関連
    def get_koden_data(self, row: int) -> Dict[str, Any]:
        """香典データを取得"""
        try:
            return self.excel_service.read_koden_data(row)
        except Exception as e:
            print(f"香典データ取得エラー: {str(e)}")
            return {}
    
    def save_koden_data(self, row: int, data: Dict[str, Any]) -> bool:
        """香典データを保存"""
        try:
            # バリデーション
            errors = self.validation_service.validate_koden_data(data)
            if errors:
                print(f"バリデーションエラー: {self.validation_service.get_validation_summary(errors)}")
                return False
            
            # データを正規化
            normalized_data = self._normalize_koden_data(data)
            
            # Excelに保存
            self.excel_service.update_koden_data(row, normalized_data)
            return True
        except Exception as e:
            print(f"香典データ保存エラー: {str(e)}")
            return False
    
    def _normalize_koden_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """香典データを正規化"""
        normalized = {}
        
        if 'name' in data and data['name']:
            normalized['name'] = self.validation_service.normalize_text(data['name'])
            # フリガナを自動生成
            normalized['furigana'] = self.validation_service.convert_to_furigana(data['name'])
        
        if 'address' in data and data['address']:
            normalized['address'] = self.validation_service.normalize_text(data['address'])
        
        if 'price' in data:
            normalized['price'] = data['price']
        
        if 'receipt' in data:
            normalized['receipt'] = bool(data['receipt'])
        
        if 'check' in data:
            normalized['check'] = bool(data['check'])
        
        return normalized
    
    # 葬儀データ関連
    def get_funeral_data(self) -> Dict[str, Any]:
        """葬儀データを取得"""
        try:
            # 実装は既存のfunc1の関数を呼び出す
            # ここでは例として空の辞書を返す
            return {}
        except Exception as e:
            print(f"葬儀データ取得エラー: {str(e)}")
            return {}
    
    def save_funeral_data(self, data: Dict[str, Any]) -> bool:
        """葬儀データを保存"""
        try:
            # バリデーション
            errors = self.validation_service.validate_funeral_data(data)
            if errors:
                print(f"バリデーションエラー: {self.validation_service.get_validation_summary(errors)}")
                return False
            
            # データを正規化
            normalized_data = self._normalize_funeral_data(data)
            
            # 実装は既存のfunc1の関数を呼び出す
            # ここでは例としてTrueを返す
            return True
        except Exception as e:
            print(f"葬儀データ保存エラー: {str(e)}")
            return False
    
    def _normalize_funeral_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """葬儀データを正規化"""
        normalized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                normalized[key] = self.validation_service.normalize_text(value)
            else:
                normalized[key] = value
        
        return normalized
    
    # 施工状況データ関連
    def get_construction_data(self) -> List[Dict[str, Any]]:
        """施工状況データを取得"""
        try:
            # 実装は既存のfunc1の関数を呼び出す
            # ここでは例として空のリストを返す
            return []
        except Exception as e:
            print(f"施工状況データ取得エラー: {str(e)}")
            return []
    
    def save_construction_data(self, data: Dict[str, Any]) -> bool:
        """施工状況データを保存"""
        try:
            # バリデーション
            errors = self.validation_service.validate_construction_data(data)
            if errors:
                print(f"バリデーションエラー: {self.validation_service.get_validation_summary(errors)}")
                return False
            
            # 実装は既存のfunc1の関数を呼び出す
            return True
        except Exception as e:
            print(f"施工状況データ保存エラー: {str(e)}")
            return False
    
    # 供物データ関連
    def get_offering_data(self) -> List[Dict[str, Any]]:
        """供物データを取得"""
        try:
            # 実装は既存のfunc1の関数を呼び出す
            return []
        except Exception as e:
            print(f"供物データ取得エラー: {str(e)}")
            return []
    
    def save_offering_data(self, data: Dict[str, Any]) -> bool:
        """供物データを保存"""
        try:
            # バリデーション
            errors = self.validation_service.validate_offering_data(data)
            if errors:
                print(f"バリデーションエラー: {self.validation_service.get_validation_summary(errors)}")
                return False
            
            # 実装は既存のfunc1の関数を呼び出す
            return True
        except Exception as e:
            print(f"供物データ保存エラー: {str(e)}")
            return False
    
    # 焼香順データ関連
    def get_incense_data(self) -> List[Dict[str, Any]]:
        """焼香順データを取得"""
        try:
            # 実装は既存のfunc1の関数を呼び出す
            return []
        except Exception as e:
            print(f"焼香順データ取得エラー: {str(e)}")
            return []
    
    def save_incense_data(self, data: Dict[str, Any]) -> bool:
        """焼香順データを保存"""
        try:
            # 実装は既存のfunc1の関数を呼び出す
            return True
        except Exception as e:
            print(f"焼香順データ保存エラー: {str(e)}")
            return False
    
    # 供花料データ関連
    def get_flower_data(self, row: int = None) -> List[FlowerModel]:
        """供花料データを取得"""
        try:
            if row is not None:
                # 特定の行のデータを取得
                data = self.excel_service.read_flower_data(row)
                if data:
                    flower = FlowerModel()
                    flower.from_excel_row(data)
                    return [flower]
            else:
                # 全データを取得
                all_data = self.excel_service.read_all_flower_data()
                flowers = []
                for data in all_data:
                    flower = FlowerModel()
                    flower.from_excel_row(data)
                    flowers.append(flower)
                return flowers
            return []
        except Exception as e:
            print(f"供花料データ取得エラー: {str(e)}")
            return []
    
    def save_flower_data(self, flower: FlowerModel) -> bool:
        """供花料データを保存"""
        try:
            # バリデーション
            errors = flower.validate()
            if errors:
                print(f"バリデーションエラー: {self.validation_service.get_validation_summary(errors)}")
                return False
            
            # Excelに保存
            row_data = flower.to_excel_row()
            self.excel_service.update_flower_data(flower.number, row_data)
            return True
        except Exception as e:
            print(f"供花料データ保存エラー: {str(e)}")
            return False
    
    def delete_flower_data(self, number: int) -> bool:
        """供花料データを削除"""
        try:
            self.excel_service.delete_flower_data(number)
            return True
        except Exception as e:
            print(f"供花料データ削除エラー: {str(e)}")
            return False
    
    # 弔辞弔電データ関連
    def get_condolence_data(self, row: int = None) -> List[CondolenceModel]:
        """弔辞弔電データを取得"""
        try:
            if row is not None:
                # 特定の行のデータを取得
                data = self.excel_service.read_condolence_data(row)
                if data:
                    condolence = CondolenceModel()
                    condolence.from_excel_row(data)
                    return [condolence]
            else:
                # 全データを取得
                all_data = self.excel_service.read_all_condolence_data()
                condolences = []
                for data in all_data:
                    condolence = CondolenceModel()
                    condolence.from_excel_row(data)
                    condolences.append(condolence)
                return condolences
            return []
        except Exception as e:
            print(f"弔辞弔電データ取得エラー: {str(e)}")
            return []
    
    def save_condolence_data(self, condolence: CondolenceModel) -> bool:
        """弔辞弔電データを保存"""
        try:
            # バリデーション
            errors = condolence.validate()
            if errors:
                print(f"バリデーションエラー: {self.validation_service.get_validation_summary(errors)}")
                return False
            
            # Excelに保存
            row_data = condolence.to_excel_row()
            self.excel_service.update_condolence_data(condolence.number, row_data)
            return True
        except Exception as e:
            print(f"弔辞弔電データ保存エラー: {str(e)}")
            return False
    
    def delete_condolence_data(self, number: int) -> bool:
        """弔辞弔電データを削除"""
        try:
            self.excel_service.delete_condolence_data(number)
            return True
        except Exception as e:
            print(f"弔辞弔電データ削除エラー: {str(e)}")
            return False
    
    # ファイル操作関連
    def create_project_folder(self, folder_name: str) -> bool:
        """プロジェクトフォルダを作成"""
        try:
            current_path = self.file_service.get_current_path()
            if not current_path:
                print("現在のパスが設定されていません")
                return False
            
            results = self.file_service.create_folder_structure(current_path, folder_name)
            return all(results.values())
        except Exception as e:
            print(f"プロジェクトフォルダ作成エラー: {str(e)}")
            return False
    
    def get_project_list(self) -> List[str]:
        """プロジェクト一覧を取得"""
        try:
            current_path = self.file_service.get_current_path()
            if not current_path:
                return []
            
            contents = self.file_service.get_directory_contents(current_path)
            # ディレクトリのみをフィルタリング
            return [item for item in contents if self.file_service.directory_exists(
                self.file_service.join_paths(current_path, item)
            )]
        except Exception as e:
            print(f"プロジェクト一覧取得エラー: {str(e)}")
            return []
    
    # 設定関連
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """設定を保存"""
        try:
            # パス設定の保存
            if 'current_path' in settings:
                vix_path = settings.get('vix_path')
                self.file_service.save_paths(settings['current_path'], vix_path)
            
            return True
        except Exception as e:
            print(f"設定保存エラー: {str(e)}")
            return False
    
    def load_settings(self) -> Dict[str, Any]:
        """設定を読み込み"""
        try:
            return {
                'current_path': self.file_service.get_current_path(),
                'vix_path': self.file_service.get_vix_path()
            }
        except Exception as e:
            print(f"設定読み込みエラー: {str(e)}")
            return {}
    
    # クリーンアップ
    def cleanup(self) -> None:
        """リソースのクリーンアップ"""
        try:
            self.excel_service.safe_close_excel()
        except Exception as e:
            print(f"クリーンアップエラー: {str(e)}")