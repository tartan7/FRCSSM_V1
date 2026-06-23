"""
供花料データモデル
供花料情報を管理
"""
from typing import List, Optional, Any
from models.base_model import BaseModel

class FlowerModel(BaseModel):
    """供花料データのモデル"""
    
    def __init__(self):
        super().__init__()
        self.number = 0  # 番号
        self.amount = 0  # 金額
        self.address = ""  # 住所
        self.name = ""  # 名前
        self.receipt = False  # 領収証
        self.notes = ""  # 備考
    
    def validate(self) -> List[str]:
        """供花料データの検証"""
        errors = []
        
        # 番号の検証
        if self.number < 1:
            errors.append("番号は1以上である必要があります")
        
        # 金額の検証
        if self.amount < 0:
            errors.append("金額は0以上である必要があります")
        if self.amount > 1000000:  # 100万円を上限とする
            errors.append("金額は1,000,000円以下である必要があります")
        
        # 名前の検証
        if self.name and len(self.name) > 50:
            errors.append("名前は50文字以内である必要があります")
        
        # 住所の検証
        if self.address and len(self.address) > 100:
            errors.append("住所は100文字以内である必要があります")
        
        # 禁止文字のチェック
        forbidden_chars = ['<', '>', '&', '"', "'", '\\', '/']
        for char in forbidden_chars:
            if char in (self.name or ""):
                errors.append(f"名前に使用できない文字が含まれています: {char}")
            if char in (self.address or ""):
                errors.append(f"住所に使用できない文字が含まれています: {char}")
        
        return errors
    
    def get_display_name(self) -> str:
        """表示用の名前を取得"""
        if self.name:
            return f"{self.name} ({self.amount:,}円)"
        return f"供花料 #{self.number}"
    
    def get_summary(self) -> str:
        """サマリー情報を取得"""
        summary = f"No.{self.number}"
        if self.name:
            summary += f" - {self.name}"
        if self.amount > 0:
            summary += f" - {self.amount:,}円"
        return summary
    
    def is_empty(self) -> bool:
        """空のデータかチェック"""
        return not any([
            self.amount,
            self.name,
            self.address
        ])
    
    def clear(self) -> None:
        """データをクリア"""
        self.amount = 0
        self.name = ""
        self.address = ""
        self.receipt = False
        self.notes = ""
        self.update_timestamp()
    
    def to_excel_row(self) -> List[Any]:
        """Excel行データに変換"""
        return [
            self.number,
            self.amount,
            self.address,
            self.name,
            "○" if self.receipt else ""
        ]
    
    def from_excel_row(self, row_data: List[Any]) -> None:
        """Excel行データから設定"""
        if len(row_data) >= 5:
            self.number = row_data[0] or 0
            self.amount = row_data[1] or 0
            self.address = row_data[2] or ""
            self.name = row_data[3] or ""
            self.receipt = row_data[4] == "○"