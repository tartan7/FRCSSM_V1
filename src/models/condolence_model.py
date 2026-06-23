"""
弔辞弔電データモデル
弔辞弔電情報を管理
"""
from typing import List, Optional, Any
from models.base_model import BaseModel

class CondolenceModel(BaseModel):
    """弔辞弔電データのモデル"""
    
    def __init__(self):
        super().__init__()
        self.number = 0  # 番号
        self.company_name = ""  # 会社名
        self.condolence_message = ""  # 弔辞
        self.telegram_message = ""  # 弔電
        self.check = False  # チェック
        self.notes = ""  # 備考
    
    def validate(self) -> List[str]:
        """弔辞弔電データの検証"""
        errors = []
        
        # 番号の検証
        if self.number < 1:
            errors.append("番号は1以上である必要があります")
        
        # 会社名の検証
        if self.company_name and len(self.company_name) > 50:
            errors.append("会社名は50文字以内である必要があります")
        
        # 弔辞の検証
        if self.condolence_message and len(self.condolence_message) > 200:
            errors.append("弔辞は200文字以内である必要があります")
        
        # 弔電の検証
        if self.telegram_message and len(self.telegram_message) > 200:
            errors.append("弔電は200文字以内である必要があります")
        
        # 禁止文字のチェック
        forbidden_chars = ['<', '>', '&', '"', "'", '\\', '/']
        for char in forbidden_chars:
            if char in (self.company_name or ""):
                errors.append(f"会社名に使用できない文字が含まれています: {char}")
            if char in (self.condolence_message or ""):
                errors.append(f"弔辞に使用できない文字が含まれています: {char}")
            if char in (self.telegram_message or ""):
                errors.append(f"弔電に使用できない文字が含まれています: {char}")
        
        return errors
    
    def get_display_name(self) -> str:
        """表示用の名前を取得"""
        if self.company_name:
            return f"{self.company_name} (弔辞弔電)"
        return f"弔辞弔電 #{self.number}"
    
    def get_summary(self) -> str:
        """サマリー情報を取得"""
        summary = f"No.{self.number}"
        if self.company_name:
            summary += f" - {self.company_name}"
        if self.condolence_message:
            summary += f" (弔辞: {len(self.condolence_message)}文字)"
        if self.telegram_message:
            summary += f" (弔電: {len(self.telegram_message)}文字)"
        return summary
    
    def is_empty(self) -> bool:
        """空のデータかチェック"""
        return not any([
            self.company_name,
            self.condolence_message,
            self.telegram_message
        ])
    
    def clear(self) -> None:
        """データをクリア"""
        self.company_name = ""
        self.condolence_message = ""
        self.telegram_message = ""
        self.check = False
        self.notes = ""
        self.update_timestamp()
    
    def to_excel_row(self) -> List[Any]:
        """Excel行データに変換"""
        return [
            self.number,
            self.company_name,
            self.condolence_message,
            self.telegram_message,
            "○" if self.check else ""
        ]
    
    def from_excel_row(self, row_data: List[Any]) -> None:
        """Excel行データから設定"""
        if len(row_data) >= 5:
            self.number = row_data[0] or 0
            self.company_name = row_data[1] or ""
            self.condolence_message = row_data[2] or ""
            self.telegram_message = row_data[3] or ""
            self.check = row_data[4] == "○"
    
    def has_condolence(self) -> bool:
        """弔辞があるかチェック"""
        return bool(self.condolence_message and self.condolence_message.strip())
    
    def has_telegram(self) -> bool:
        """弔電があるかチェック"""
        return bool(self.telegram_message and self.telegram_message.strip())
    
    def get_message_count(self) -> int:
        """メッセージ数を取得"""
        count = 0
        if self.has_condolence():
            count += 1
        if self.has_telegram():
            count += 1
        return count