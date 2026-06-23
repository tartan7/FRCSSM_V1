"""
バリデーションサービス
入力データの検証を統一管理
"""
import re
import datetime
import unicodedata
from typing import Dict, List, Any, Optional, Tuple
import pykakasi

class ValidationService:
    """バリデーション処理の共通サービス"""
    
    def __init__(self):
        self.kks = pykakasi.kakasi()
    
    def validate_required(self, value: Any, field_name: str) -> Tuple[bool, str]:
        """必須項目の検証"""
        if value is None or value == "" or (isinstance(value, str) and value.strip() == ""):
            return False, f"{field_name}は必須項目です"
        return True, ""
    
    def validate_number(self, value: Any, field_name: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> Tuple[bool, str]:
        """数値の検証"""
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                return False, f"{field_name}は{min_val}以上である必要があります"
            if max_val is not None and num > max_val:
                return False, f"{field_name}は{max_val}以下である必要があります"
            return True, ""
        except (ValueError, TypeError):
            return False, f"{field_name}は数値である必要があります"
    
    def validate_price(self, value: Any, field_name: str = "金額") -> Tuple[bool, str]:
        """金額の検証"""
        if value is None or value == "":
            return True, ""  # 金額は空でもOK
        
        try:
            price = int(value)
            if price < 0:
                return False, f"{field_name}は0以上である必要があります"
            if price > 10000000:  # 1000万円を上限とする
                return False, f"{field_name}は10,000,000円以下である必要があります"
            return True, ""
        except (ValueError, TypeError):
            return False, f"{field_name}は数値である必要があります"
    
    def validate_name(self, value: str, field_name: str = "名前") -> Tuple[bool, str]:
        """名前の検証"""
        if not value or value.strip() == "":
            return True, ""  # 名前は空でもOK
        
        # 文字数制限
        if len(value) > 50:
            return False, f"{field_name}は50文字以内である必要があります"
        
        # 禁止文字のチェック
        forbidden_chars = ['<', '>', '&', '"', "'", '\\', '/']
        for char in forbidden_chars:
            if char in value:
                return False, f"{field_name}に使用できない文字が含まれています: {char}"
        
        return True, ""
    
    def validate_address(self, value: str, field_name: str = "住所") -> Tuple[bool, str]:
        """住所の検証"""
        if not value or value.strip() == "":
            return True, ""  # 住所は空でもOK
        
        # 文字数制限
        if len(value) > 100:
            return False, f"{field_name}は100文字以内である必要があります"
        
        return True, ""
    
    def validate_furigana(self, value: str, field_name: str = "フリガナ") -> Tuple[bool, str]:
        """フリガナの検証"""
        if not value or value.strip() == "":
            return True, ""  # フリガナは空でもOK
        
        # ひらがな、カタカナ、長音符のみ許可
        if not re.match(r'^[ひらがなカタカナー]*$', value):
            return False, f"{field_name}はひらがな、カタカナ、長音符のみ使用できます"
        
        # 文字数制限
        if len(value) > 50:
            return False, f"{field_name}は50文字以内である必要があります"
        
        return True, ""
    
    def validate_date(self, value: str, field_name: str = "日付") -> Tuple[bool, str]:
        """日付の検証"""
        if not value or value.strip() == "":
            return True, ""  # 日付は空でもOK
        
        try:
            # 和暦形式の日付をチェック
            if re.match(r'\\d+年\\d+月\\d+日', value):
                return True, ""
            
            # 西暦形式の日付をチェック
            datetime.datetime.strptime(value, '%Y/%m/%d')
            return True, ""
        except ValueError:
            return False, f"{field_name}の形式が正しくありません"
    
    def validate_phone_number(self, value: str, field_name: str = "電話番号") -> Tuple[bool, str]:
        """電話番号の検証"""
        if not value or value.strip() == "":
            return True, ""  # 電話番号は空でもOK
        
        # 数字、ハイフン、括弧のみ許可
        if not re.match(r'^[0-9\\-()]*$', value):
            return False, f"{field_name}は数字、ハイフン、括弧のみ使用できます"
        
        # 文字数制限
        if len(value) > 20:
            return False, f"{field_name}は20文字以内である必要があります"
        
        return True, ""
    
    def validate_email(self, value: str, field_name: str = "メールアドレス") -> Tuple[bool, str]:
        """メールアドレスの検証"""
        if not value or value.strip() == "":
            return True, ""  # メールアドレスは空でもOK
        
        # 基本的なメールアドレス形式のチェック
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            return False, f"{field_name}の形式が正しくありません"
        
        return True, ""
    
    def validate_koden_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """香典データの総合検証"""
        errors = {}
        
        # 金額の検証
        if 'price' in data:
            is_valid, error_msg = self.validate_price(data['price'], "金額")
            if not is_valid:
                errors['price'] = error_msg
        
        # 名前の検証
        if 'name' in data:
            is_valid, error_msg = self.validate_name(data['name'], "御芳名")
            if not is_valid:
                errors['name'] = error_msg
        
        # 住所の検証
        if 'address' in data:
            is_valid, error_msg = self.validate_address(data['address'], "住所")
            if not is_valid:
                errors['address'] = error_msg
        
        # フリガナの検証
        if 'furigana' in data:
            is_valid, error_msg = self.validate_furigana(data['furigana'], "フリガナ")
            if not is_valid:
                errors['furigana'] = error_msg
        
        return errors
    
    def validate_funeral_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """葬儀データの総合検証"""
        errors = {}
        
        # 故人名の検証
        if 'deceased_name' in data:
            is_valid, error_msg = self.validate_name(data['deceased_name'], "故人名")
            if not is_valid:
                errors['deceased_name'] = error_msg
        
        # 生年月日の検証
        if 'birth_date' in data:
            is_valid, error_msg = self.validate_date(data['birth_date'], "生年月日")
            if not is_valid:
                errors['birth_date'] = error_msg
        
        # 死亡日時の検証
        if 'death_date' in data:
            is_valid, error_msg = self.validate_date(data['death_date'], "死亡日時")
            if not is_valid:
                errors['death_date'] = error_msg
        
        return errors
    
    def normalize_text(self, text: str) -> str:
        """テキストを正規化"""
        if not text:
            return ""
        
        # Unicode正規化
        normalized = unicodedata.normalize('NFKC', text)
        
        # 前後の空白を削除
        return normalized.strip()
    
    def convert_to_furigana(self, text: str) -> str:
        """テキストをフリガナに変換"""
        if not text:
            return ""
        
        try:
            result = self.kks.convert(text)
            furigana = ''.join([item['kana'] for item in result])
            return furigana
        except Exception as e:
            print(f"フリガナ変換エラー: {str(e)}")
            return ""
    
    def validate_construction_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """施工状況データの検証"""
        errors = {}
        
        # 番号の検証
        if 'number' in data:
            is_valid, error_msg = self.validate_number(data['number'], "番号", min_val=1)
            if not is_valid:
                errors['number'] = error_msg
        
        # 役職の検証
        if 'role' in data:
            is_valid, error_msg = self.validate_name(data['role'], "役職")
            if not is_valid:
                errors['role'] = error_msg
        
        # 名前の検証
        if 'name' in data:
            is_valid, error_msg = self.validate_name(data['name'], "名前")
            if not is_valid:
                errors['name'] = error_msg
        
        return errors
    
    def validate_offering_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """供物データの検証"""
        errors = {}
        
        # 数量の検証
        if 'quantity' in data:
            is_valid, error_msg = self.validate_number(data['quantity'], "数量", min_val=1)
            if not is_valid:
                errors['quantity'] = error_msg
        
        # 寄贈者名の検証
        if 'donor_name' in data:
            is_valid, error_msg = self.validate_name(data['donor_name'], "寄贈者名")
            if not is_valid:
                errors['donor_name'] = error_msg
        
        return errors
    
    def get_validation_summary(self, errors: Dict[str, str]) -> str:
        """検証エラーのサマリーを取得"""
        if not errors:
            return "検証エラーはありません"
        
        error_list = [f"• {field}: {error}" for field, error in errors.items()]
        return "以下の項目にエラーがあります:\\n" + "\\n".join(error_list)