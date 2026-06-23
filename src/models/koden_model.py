"""
香典データモデル
香典情報を管理
"""
from typing import List, Optional, Any
from models.base_model import BaseModel

class KodenModel(BaseModel):
    """香典データのモデル"""
    
    def __init__(self):
        super().__init__()
        self.row_number = 0
        self.price = 0
        self.name = ""
        self.address = ""
        self.furigana = ""
        self.receipt = False
        self.check = False
        self.notes = ""
    
    def validate(self) -> List[str]:
        """香典データの検証"""
        errors = []
        
        # 金額の検証
        if self.price < 0:
            errors.append("金額は0以上である必要があります")
        if self.price > 10000000:  # 1000万円を上限とする
            errors.append("金額は10,000,000円以下である必要があります")
        
        # 名前の検証
        if self.name and len(self.name) > 50:
            errors.append("御芳名は50文字以内である必要があります")
        
        # 住所の検証
        if self.address and len(self.address) > 100:
            errors.append("住所は100文字以内である必要があります")
        
        # フリガナの検証
        if self.furigana and len(self.furigana) > 50:
            errors.append("フリガナは50文字以内である必要があります")
        
        # 禁止文字のチェック
        forbidden_chars = ['<', '>', '&', '"', "'", '\\', '/']
        for char in forbidden_chars:
            if char in (self.name or ""):
                errors.append(f"御芳名に使用できない文字が含まれています: {char}")
            if char in (self.address or ""):
                errors.append(f"住所に使用できない文字が含まれています: {char}")
        
        return errors
    
    def get_display_name(self) -> str:
        """表示用の名前を取得"""
        if self.name:
            return f"{self.name} ({self.price:,}円)"
        return f"香典 #{self.row_number}"
    
    def get_summary(self) -> str:
        """サマリー情報を取得"""
        summary = f"No.{self.row_number}"
        if self.name:
            summary += f" - {self.name}"
        if self.price > 0:
            summary += f" - {self.price:,}円"
        return summary
    
    def is_empty(self) -> bool:
        """空のデータかチェック"""
        return not any([
            self.price,
            self.name,
            self.address,
            self.furigana
        ])
    
    def clear(self) -> None:
        """データをクリア"""
        self.price = 0
        self.name = ""
        self.address = ""
        self.furigana = ""
        self.receipt = False
        self.check = False
        self.notes = ""
        self.update_timestamp()
    
    def copy_from(self, other: 'KodenModel') -> None:
        """他の香典データからコピー"""
        self.row_number = other.row_number
        self.price = other.price
        self.name = other.name
        self.address = other.address
        self.furigana = other.furigana
        self.receipt = other.receipt
        self.check = other.check
        self.notes = other.notes
        self.update_timestamp()
    
    def to_excel_row(self) -> List[Any]:
        """Excel行データに変換"""
        return [
            self.row_number,
            self.price,
            "",  # 空の列
            self.address,
            self.name,
            "",  # 空の列
            "",  # 空の列
            self.furigana,
            "○" if self.receipt else "",
            "○" if self.check else ""
        ]
    
    def from_excel_row(self, row_data: List[Any]) -> None:
        """Excel行データから設定"""
        if len(row_data) >= 10:
            self.row_number = row_data[0] or 0
            self.price = row_data[1] or 0
            self.address = row_data[3] or ""
            self.name = row_data[4] or ""
            self.furigana = row_data[7] or ""
            self.receipt = row_data[8] == "○"
            self.check = row_data[9] == "○"