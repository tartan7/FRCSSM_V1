"""
供物データモデル
供物情報を管理
"""
from typing import List, Optional, Any
from models.base_model import BaseModel

class OfferingModel(BaseModel):
    """供物データのモデル"""
    
    def __init__(self):
        super().__init__()
        self.number = 0  # 番号
        self.offering_type = ""  # 供物の種類
        self.quantity = 0  # 数量
        self.unit = ""  # 単位
        self.notes = ""  # 備考
        self.check = False  # チェック
    
    def validate(self) -> List[str]:
        """供物データの検証"""
        errors = []
        
        # 番号の検証
        if self.number < 1:
            errors.append("番号は1以上である必要があります")
        
        # 供物の種類の検証
        if self.offering_type and len(self.offering_type) > 50:
            errors.append("供物の種類は50文字以内である必要があります")
        
        # 数量の検証
        if self.quantity < 0:
            errors.append("数量は0以上である必要があります")
        if self.quantity > 1000:  # 1000個を上限とする
            errors.append("数量は1,000個以下である必要があります")
        
        # 単位の検証
        if self.unit and len(self.unit) > 20:
            errors.append("単位は20文字以内である必要があります")
        
        # 禁止文字のチェック
        forbidden_chars = ['<', '>', '&', '"', "'", '\\', '/']
        for char in forbidden_chars:
            if char in (self.offering_type or ""):
                errors.append(f"供物の種類に使用できない文字が含まれています: {char}")
            if char in (self.unit or ""):
                errors.append(f"単位に使用できない文字が含まれています: {char}")
            if char in (self.notes or ""):
                errors.append(f"備考に使用できない文字が含まれています: {char}")
        
        return errors
    
    def get_display_name(self) -> str:
        """表示用の名前を取得"""
        if self.offering_type:
            quantity_text = f"{self.quantity}{self.unit}" if self.unit else str(self.quantity)
            return f"{self.offering_type} ({quantity_text})"
        return f"供物 #{self.number}"
    
    def get_summary(self) -> str:
        """サマリー情報を取得"""
        summary = f"No.{self.number}"
        if self.offering_type:
            summary += f" - {self.offering_type}"
        if self.quantity > 0:
            quantity_text = f"{self.quantity}{self.unit}" if self.unit else str(self.quantity)
            summary += f" ({quantity_text})"
        return summary
    
    def is_empty(self) -> bool:
        """空のデータかチェック"""
        return not any([
            self.offering_type,
            self.quantity,
            self.unit
        ])
    
    def clear(self) -> None:
        """データをクリア"""
        self.offering_type = ""
        self.quantity = 0
        self.unit = ""
        self.notes = ""
        self.check = False
        self.update_timestamp()
    
    def to_excel_row(self) -> List[Any]:
        """Excel行データに変換"""
        return [
            self.number,
            self.offering_type,
            self.quantity,
            self.unit,
            "○" if self.check else ""
        ]
    
    def from_excel_row(self, row_data: List[Any]) -> None:
        """Excel行データから設定"""
        if len(row_data) >= 5:
            self.number = row_data[0] or 0
            self.offering_type = row_data[1] or ""
            self.quantity = row_data[2] or 0
            self.unit = row_data[3] or ""
            self.check = row_data[4] == "○"
    
    def get_quantity_display(self) -> str:
        """数量の表示文字列を取得"""
        if self.unit:
            return f"{self.quantity}{self.unit}"
        return str(self.quantity)
    
    def is_valid_quantity(self) -> bool:
        """有効な数量かチェック"""
        return self.quantity > 0 and self.quantity <= 1000