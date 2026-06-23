"""
ベースデータモデル
すべてのデータモデルの基底クラス
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

class BaseModel(ABC):
    """すべてのデータモデルの基底クラス"""
    
    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.id = None
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            else:
                data[key] = value
        return data
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """辞書からデータを設定"""
        for key, value in data.items():
            if hasattr(self, key):
                if key in ['created_at', 'updated_at'] and isinstance(value, str):
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
    
    def to_json(self) -> str:
        """JSON文字列に変換"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def from_json(self, json_str: str) -> None:
        """JSON文字列からデータを設定"""
        data = json.loads(json_str)
        self.from_dict(data)
    
    def validate(self) -> List[str]:
        """データの検証"""
        errors = []
        # 各モデルでオーバーライドして実装
        return errors
    
    def is_valid(self) -> bool:
        """データが有効かチェック"""
        return len(self.validate()) == 0
    
    def update_timestamp(self) -> None:
        """更新日時を更新"""
        self.updated_at = datetime.now()
    
    @abstractmethod
    def get_display_name(self) -> str:
        """表示用の名前を取得"""
        pass
    
    def __str__(self) -> str:
        return self.get_display_name()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.get_display_name()})"