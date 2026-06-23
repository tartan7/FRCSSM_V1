"""
葬儀データモデル
葬儀情報を管理
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from models.base_model import BaseModel

class FuneralModel(BaseModel):
    """葬儀データのモデル"""
    
    def __init__(self):
        super().__init__()
        self.deceased_name = ""  # 故人名
        self.deceased_furigana = ""  # 故人フリガナ
        self.birth_date = ""  # 生年月日
        self.death_date = ""  # 死亡日時
        self.age = 0  # 年齢
        self.family_name = ""  # 遺族名
        self.family_furigana = ""  # 遺族フリガナ
        self.temple_name = ""  # 寺院名
        self.temple_address = ""  # 寺院住所
        self.temple_phone = ""  # 寺院電話番号
        self.venue_name = ""  # 会場名
        self.venue_address = ""  # 会場住所
        self.venue_phone = ""  # 会場電話番号
        self.overnight_date = ""  # 通夜日時
        self.funeral_date = ""  # 葬儀日時
        self.departure_date = ""  # 出棺日時
        self.crematory_name = ""  # 火葬場名
        self.crematory_address = ""  # 火葬場住所
        self.crematory_phone = ""  # 火葬場電話番号
        self.notes = ""  # 備考
    
    def validate(self) -> List[str]:
        """葬儀データの検証"""
        errors = []
        
        # 故人名の検証
        if not self.deceased_name:
            errors.append("故人名は必須項目です")
        elif len(self.deceased_name) > 50:
            errors.append("故人名は50文字以内である必要があります")
        
        # 遺族名の検証
        if not self.family_name:
            errors.append("遺族名は必須項目です")
        elif len(self.family_name) > 50:
            errors.append("遺族名は50文字以内である必要があります")
        
        # 年齢の検証
        if self.age < 0 or self.age > 150:
            errors.append("年齢は0-150の範囲である必要があります")
        
        # 日付の検証
        if self.birth_date and not self._is_valid_date(self.birth_date):
            errors.append("生年月日の形式が正しくありません")
        
        if self.death_date and not self._is_valid_date(self.death_date):
            errors.append("死亡日時の形式が正しくありません")
        
        if self.overnight_date and not self._is_valid_date(self.overnight_date):
            errors.append("通夜日時の形式が正しくありません")
        
        if self.funeral_date and not self._is_valid_date(self.funeral_date):
            errors.append("葬儀日時の形式が正しくありません")
        
        if self.departure_date and not self._is_valid_date(self.departure_date):
            errors.append("出棺日時の形式が正しくありません")
        
        # 電話番号の検証
        if self.temple_phone and not self._is_valid_phone(self.temple_phone):
            errors.append("寺院電話番号の形式が正しくありません")
        
        if self.venue_phone and not self._is_valid_phone(self.venue_phone):
            errors.append("会場電話番号の形式が正しくありません")
        
        if self.crematory_phone and not self._is_valid_phone(self.crematory_phone):
            errors.append("火葬場電話番号の形式が正しくありません")
        
        return errors
    
    def _is_valid_date(self, date_str: str) -> bool:
        """日付形式の検証"""
        if not date_str:
            return True
        
        try:
            # 和暦形式のチェック
            if "年" in date_str and "月" in date_str and "日" in date_str:
                return True
            
            # 西暦形式のチェック
            datetime.strptime(date_str, '%Y/%m/%d')
            return True
        except ValueError:
            return False
    
    def _is_valid_phone(self, phone: str) -> bool:
        """電話番号形式の検証"""
        if not phone:
            return True
        
        # 数字、ハイフン、括弧のみ許可
        import re
        return bool(re.match(r'^[0-9\-()]*$', phone))
    
    def get_display_name(self) -> str:
        """表示用の名前を取得"""
        if self.deceased_name:
            return f"{self.deceased_name}様の葬儀"
        return "葬儀情報"
    
    def get_summary(self) -> str:
        """サマリー情報を取得"""
        summary = f"故人: {self.deceased_name}"
        if self.age > 0:
            summary += f" ({self.age}歳)"
        if self.family_name:
            summary += f" / 遺族: {self.family_name}"
        return summary
    
    def calculate_age(self) -> int:
        """年齢を計算"""
        if not self.birth_date or not self.death_date:
            return 0
        
        try:
            # 簡易的な年齢計算（実際の実装ではより詳細な計算が必要）
            birth_year = self._extract_year(self.birth_date)
            death_year = self._extract_year(self.death_date)
            
            if birth_year and death_year:
                return death_year - birth_year
        except Exception:
            pass
        
        return 0
    
    def _extract_year(self, date_str: str) -> Optional[int]:
        """日付文字列から年を抽出"""
        if not date_str:
            return None
        
        try:
            # 和暦形式の場合
            if "年" in date_str:
                year_part = date_str.split("年")[0]
                # 令和の場合の簡易処理
                if "令和" in year_part:
                    reiwa_year = int(year_part.replace("令和", ""))
                    return 2018 + reiwa_year
                elif "平成" in year_part:
                    heisei_year = int(year_part.replace("平成", ""))
                    return 1988 + heisei_year
                elif "昭和" in year_part:
                    showa_year = int(year_part.replace("昭和", ""))
                    return 1925 + showa_year
            
            # 西暦形式の場合
            datetime.strptime(date_str, '%Y/%m/%d')
            return int(date_str.split('/')[0])
        except Exception:
            return None
    
    def update_age(self) -> None:
        """年齢を更新"""
        self.age = self.calculate_age()
        self.update_timestamp()
    
    def get_funeral_schedule(self) -> List[Dict[str, str]]:
        """葬儀スケジュールを取得"""
        schedule = []
        
        if self.overnight_date:
            schedule.append({
                "event": "通夜",
                "date": self.overnight_date,
                "location": self.venue_name
            })
        
        if self.funeral_date:
            schedule.append({
                "event": "葬儀",
                "date": self.funeral_date,
                "location": self.venue_name
            })
        
        if self.departure_date:
            schedule.append({
                "event": "出棺",
                "date": self.departure_date,
                "location": self.crematory_name
            })
        
        return schedule
    
    def get_contact_info(self) -> Dict[str, str]:
        """連絡先情報を取得"""
        return {
            "寺院": f"{self.temple_name} ({self.temple_phone})",
            "会場": f"{self.venue_name} ({self.venue_phone})",
            "火葬場": f"{self.crematory_name} ({self.crematory_phone})"
        }