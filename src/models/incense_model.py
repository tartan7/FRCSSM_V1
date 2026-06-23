"""
焼香順データモデル
焼香順情報を管理
"""
from typing import List, Optional, Any
from models.base_model import BaseModel

class IncenseModel(BaseModel):
    """焼香順データのモデル"""
    
    def __init__(self):
        super().__init__()
        self.number = 0  # 番号
        self.name = ""  # 名前
        self.relationship = ""  # 続柄
        self.furigana = ""  # フリガナ
        self.notes = ""  # 備考
        self.check = False  # チェック
    
    def validate(self) -> List[str]:
        """焼香順データの検証"""
        errors = []
        
        # 番号の検証
        if self.number < 1:
            errors.append("番号は1以上である必要があります")
        
        # 名前の検証
        if self.name and len(self.name) > 50:
            errors.append("名前は50文字以内である必要があります")
        
        # 続柄の検証
        if self.relationship and len(self.relationship) > 30:
            errors.append("続柄は30文字以内である必要があります")
        
        # フリガナの検証
        if self.furigana and len(self.furigana) > 100:
            errors.append("フリガナは100文字以内である必要があります")
        
        # 禁止文字のチェック
        forbidden_chars = ['<', '>', '&', '"', "'", '\\', '/']
        for char in forbidden_chars:
            if char in (self.name or ""):
                errors.append(f"名前に使用できない文字が含まれています: {char}")
            if char in (self.relationship or ""):
                errors.append(f"続柄に使用できない文字が含まれています: {char}")
            if char in (self.furigana or ""):
                errors.append(f"フリガナに使用できない文字が含まれています: {char}")
            if char in (self.notes or ""):
                errors.append(f"備考に使用できない文字が含まれています: {char}")
        
        return errors
    
    def get_display_name(self) -> str:
        """表示用の名前を取得"""
        if self.name:
            relationship_text = f" ({self.relationship})" if self.relationship else ""
            return f"{self.name}{relationship_text}"
        return f"焼香順 #{self.number}"
    
    def get_summary(self) -> str:
        """サマリー情報を取得"""
        summary = f"No.{self.number}"
        if self.name:
            summary += f" - {self.name}"
        if self.relationship:
            summary += f" ({self.relationship})"
        return summary
    
    def is_empty(self) -> bool:
        """空のデータかチェック"""
        return not any([
            self.name,
            self.relationship
        ])
    
    def clear(self) -> None:
        """データをクリア"""
        self.name = ""
        self.relationship = ""
        self.furigana = ""
        self.notes = ""
        self.check = False
        self.update_timestamp()
    
    def to_excel_row(self) -> List[Any]:
        """Excel行データに変換"""
        return [
            self.number,
            self.name,
            self.relationship,
            self.furigana,
            "○" if self.check else ""
        ]
    
    def from_excel_row(self, row_data: List[Any]) -> None:
        """Excel行データから設定"""
        if len(row_data) >= 5:
            self.number = row_data[0] or 0
            self.name = row_data[1] or ""
            self.relationship = row_data[2] or ""
            self.furigana = row_data[3] or ""
            self.check = row_data[4] == "○"
    
    def get_relationship_display(self) -> str:
        """続柄の表示文字列を取得"""
        return self.relationship or "未設定"
    
    def has_furigana(self) -> bool:
        """フリガナがあるかチェック"""
        return bool(self.furigana and self.furigana.strip())
    
    def get_full_name(self) -> str:
        """フルネームを取得（名前 + 続柄）"""
        if self.relationship:
            return f"{self.name} ({self.relationship})"
        return self.name