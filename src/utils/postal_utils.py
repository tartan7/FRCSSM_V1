import urllib.request
import json
import re


def lookup_postal_code(zipcode: str) -> dict | None:
    """郵便番号から住所を検索（zipcloud API使用、zipcode7.xla不要）

    Args:
        zipcode: 郵便番号（ハイフンあり・なし両対応）例: "123-4567" or "1234567"
    Returns:
        {'pref': 都道府県, 'city': 市区町村, 'town': 町域, 'address': 連結住所}
        見つからない・通信エラーの場合は None
    """
    zipcode_clean = re.sub(r'[^0-9]', '', zipcode)
    if len(zipcode_clean) != 7:
        return None

    url = 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=' + zipcode_clean
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data.get('status') == 200 and data.get('results'):
            r = data['results'][0]
            return {
                'pref': r['address1'],
                'city': r['address2'],
                'town': r['address3'],
                'address': r['address1'] + r['address2'] + r['address3'],
            }
    except Exception:
        pass
    return None
