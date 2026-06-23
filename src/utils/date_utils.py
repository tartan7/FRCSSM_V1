"""
日付・和暦ユーティリティ
func1.py から抽出した純粋な日付変換・計算関数群
"""
import re
import datetime
from datetime import datetime as dt
from datetime import timedelta
from datetimejp import JDatetime


def return_days(flag=False, s="", f='%Y/%m/%d', f2=''):
    """今日または指定日を和暦文字列で返す"""
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    if flag:
        sss = dt.strptime(s, f)
        d = sss.date().strftime(f)
        jd = JDatetime.strptime(d, f)
        day_result = jd.strftime('%g%e年%m月%d日')
    else:
        now = dt.now(JST)
        d = now.date().strftime(f)
        jd = JDatetime.strptime(d, f)
        day_result = jd.strftime('%e%m%d')
    return day_result


def diff_years(dateXstr):
    """指定日から現在までの経過年数を返す"""
    dateX = datetime.datetime.strptime(dateXstr, '%Y/%m/%d')
    dateY = dt.now()
    diff_year = dateY.year - dateX.year
    newdateX = datetime.datetime(dateY.year, dateX.month, dateX.day)
    diff_days = (dateY - newdateX).days
    diff_year = round(diff_year + diff_days / 365, 2)
    return int(diff_year) + 1


def calc_age(birth_date, death_date):
    """生年月日と死亡日時から年齢を計算する"""
    try:
        if not birth_date or not death_date:
            return None
        age = death_date.year - birth_date.year
        if death_date.month < birth_date.month or \
           (death_date.month == birth_date.month and death_date.day < birth_date.day):
            age -= 1
        return age
    except Exception as e:
        print(f"calc_age年齢計算エラー: {e}")
        return None


def convert_japanese_date_to_gregorian(japanese_date_str):
    """和暦の日付文字列を西暦の日付文字列に変換"""
    try:
        era_years = {
            '大正': 1911,
            '昭和': 1925,
            '平成': 1988,
            '令和': 2018,
        }
        pattern = r'(大正|昭和|平成|令和)(\d+)年(\d+)月(\d+)日(?:\s+(.+))?'
        match = re.match(pattern, japanese_date_str.strip())
        if match:
            era, year, month, day, time_part = match.groups()
            year, month, day = int(year), int(month), int(day)
            if era in era_years:
                gregorian_year = era_years[era] + year
                base_date = f"{gregorian_year:04d}/{month:02d}/{day:02d}"
                if time_part and time_part.strip():
                    time_str = time_part.strip()
                    if '午前' in time_str:
                        time_str = time_str.replace('午前', '').strip()
                    elif '午後' in time_str:
                        time_str = time_str.replace('午後', '').strip()
                        if ':' in time_str:
                            hour, minute = time_str.split(':')
                            hour = int(hour)
                            if hour != 12:
                                hour += 12
                            time_str = f"{hour:02d}:{minute}"
                        elif '時' in time_str:
                            hour = int(time_str.replace('時', ''))
                            if hour != 12:
                                hour += 12
                            time_str = f"{hour:02d}:00"
                    return f"{base_date} {time_str}"
                return base_date
        return None
    except Exception as e:
        print(f"和暦変換エラー: {str(e)}")
        return None


def convert_to_wareki(date_obj):
    """西暦の日付を和暦に変換する"""
    try:
        if not date_obj or not hasattr(date_obj, 'year'):
            return ""
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        hour = getattr(date_obj, 'hour', 0)
        minute = getattr(date_obj, 'minute', 0)

        if year >= 2019:
            era, era_year = "令和", year - 2018
        elif year >= 1989:
            era, era_year = "平成", year - 1988
        elif year >= 1926:
            era, era_year = "昭和", year - 1925
        elif year >= 1912:
            era, era_year = "大正", year - 1911
        else:
            era, era_year = "明治", year - 1867

        wareki = f"{era}{era_year}年{month}月{day}日"
        if hour == 0 and minute == 0:
            return wareki
        ampm = "午前" if hour < 12 else "午後"
        hour12 = hour if hour <= 12 else hour - 12
        if hour12 == 0:
            hour12 = 12
        return f"{wareki} {ampm}{hour12}時{minute:02d}分"
    except Exception as e:
        print(f"和暦変換エラー: {str(e)}")
        return ""


def increment_day_with_validation(s):
    """内部日付文字列（YYMMDД + 名前）の日付を1日進める"""
    date_part = s[:6]
    name_part = s[6:]
    year_era = int(date_part[:2])
    month = int(date_part[2:4])
    day = int(date_part[4:6])
    year = 2018 + year_era
    try:
        date_obj = dt(year, month, day)
        new_date_obj = date_obj + timedelta(days=1)
        new_year_era = new_date_obj.year - 2000
        new_date_part = f"{new_year_era:02d}{new_date_obj.month:02d}{new_date_obj.day:02d}"
        return new_date_part + name_part
    except ValueError:
        return s
