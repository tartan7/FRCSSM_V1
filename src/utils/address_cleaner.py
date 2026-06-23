"""
住所クレンジングユーティリティ
address-cleansing/address_cleaner.py から移植。
normalize-japanese-addresses (Geolonia) を使い、住所を正規化して1本の文字列に整形する。

後処理ルール:
  ・X番Y号 → X-Y（半角アラビア数字・半角ハイフン）
  ・北海道の住所: 「北海道」と「XX郡」を削除
  ・他都府県: 県名等はそのまま維持

キャッシュ戦略（2層）:
  Level 1: lru_cache  — プロセス内メモリ、ナノ秒アクセス
  Level 2: SQLite DB  — %APPDATA%\\FRCSSM\\address_cache.db、セッション跨ぎで永続
"""
import os
import re
import time
import sqlite3
import logging
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

# Windows 環境で Python の CA 証明書が OS ストアと合わない場合に
# Geolonia (geolonia.github.io) への HTTPS が失敗することがある。
# requests のセッション既定を verify=False にして回避する。
try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _orig_request = requests.Session.request

    def _request_no_verify(self, method, url, **kwargs):
        kwargs.setdefault('verify', False)
        return _orig_request(self, method, url, **kwargs)

    requests.Session.request = _request_no_verify
except Exception:
    pass

from normalize_japanese_addresses import normalize

logger = logging.getLogger(__name__)

# 全角数字 → 半角変換テーブル
_ZEN_TO_HAN = str.maketrans('０１２３４５６７８９', '0123456789')

# ------------------------------------------------------------------ #
# SQLite 永続キャッシュ                                                #
# ------------------------------------------------------------------ #

_DB_DIR  = Path(__file__).resolve().parent.parent.parent / 'cache'
_DB_PATH = _DB_DIR / 'address_cache.db'
_CACHE_TTL_DAYS = 90          # キャッシュ有効期限（日）
_db_local = threading.local() # スレッドごとに独立した接続を持つ


def _get_db_conn() -> sqlite3.Connection:
    """スレッドローカルな SQLite 接続を返す（なければ初期化する）。"""
    if getattr(_db_local, 'conn', None) is None:
        _DB_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")   # 読み書き並行を許可
        conn.execute("PRAGMA synchronous=NORMAL") # 速度と安全性のバランス
        conn.execute("""
            CREATE TABLE IF NOT EXISTS address_cache (
                raw       TEXT PRIMARY KEY,
                cleaned   TEXT NOT NULL,
                cached_at REAL NOT NULL
            )
        """)
        conn.commit()
        _db_local.conn = conn
    return _db_local.conn


def _db_lookup(raw: str) -> str | None:
    """SQLite から正規化済み住所を取得する。期限切れは None 扱い。"""
    try:
        cutoff = time.time() - _CACHE_TTL_DAYS * 86400
        row = _get_db_conn().execute(
            "SELECT cleaned FROM address_cache WHERE raw=? AND cached_at>?",
            (raw, cutoff)
        ).fetchone()
        return row[0] if row else None
    except Exception as e:
        logger.debug(f"キャッシュ読み込みエラー: {e}")
        return None


def _db_store(raw: str, cleaned: str) -> None:
    """正規化結果を SQLite に保存する。変換できなかった場合は保存しない。"""
    if raw == cleaned:  # Geoloniaが解決できなかった場合はキャッシュしない
        return
    try:
        conn = _get_db_conn()
        conn.execute(
            "INSERT OR REPLACE INTO address_cache(raw, cleaned, cached_at) VALUES(?,?,?)",
            (raw, cleaned, time.time())
        )
        conn.commit()
    except Exception as e:
        logger.debug(f"キャッシュ書き込みエラー: {e}")


def get_cache_stats() -> dict:
    """キャッシュの統計情報を返す（デバッグ・運用確認用）。"""
    try:
        cutoff = time.time() - _CACHE_TTL_DAYS * 86400
        conn = _get_db_conn()
        total  = conn.execute("SELECT COUNT(*) FROM address_cache").fetchone()[0]
        valid  = conn.execute(
            "SELECT COUNT(*) FROM address_cache WHERE cached_at>?", (cutoff,)
        ).fetchone()[0]
        return {'total': total, 'valid': valid, 'expired': total - valid,
                'db_path': str(_DB_PATH)}
    except Exception:
        return {}


def clear_address_cache() -> None:
    """キャッシュDBを全消去する（Geoloniaデータ更新後などに使用）。"""
    try:
        _get_db_conn().execute("DELETE FROM address_cache")
        _get_db_conn().commit()
        logger.info("住所キャッシュをクリアしました")
    except Exception as e:
        logger.error(f"キャッシュクリアエラー: {e}")


# ------------------------------------------------------------------ #
# 住所変換ロジック                                                      #
# ------------------------------------------------------------------ #

def _kanji_chome_to_arabic(text: str) -> str:
    """漢数字をアラビア数字に変換する。
    ・「三丁目」→「3丁目」
    ・「北十四条」→「北14条」（北/南/東/西 + 漢数字 + 条 のパターン）
    """
    from kanjize import kanji2number

    def _replace_chome(m: re.Match) -> str:
        try:
            return str(kanji2number(m.group(1))) + '丁目'
        except Exception:
            return m.group(0)

    def _replace_jo(m: re.Match) -> str:
        try:
            return m.group(1) + str(kanji2number(m.group(2))) + '条'
        except Exception:
            return m.group(0)

    def _replace_jo_bare(m: re.Match) -> str:
        try:
            return str(kanji2number(m.group(1))) + '条'
        except Exception:
            return m.group(0)

    text = re.sub(r'([一二三四五六七八九十百千万]+)丁目', _replace_chome, text)
    # 条の後に数字・丁目・方角が続く場合のみ変換（四条通・三条市など地名の誤変換を防ぐ）
    # 例: 宮の森二条10丁目 → 宮の森2条10丁目 / 北十四条西3丁目 → 北14条西3丁目
    text = re.sub(r'([一二三四五六七八九十百千万]+)条(?=[0-9丁東西南北])', _replace_jo_bare, text)
    # 上記でカバーできない方角付き条（「北二条」単独など、後続文字なし）
    text = re.sub(r'([北南東西])([一二三四五六七八九十百千万]+)条', _replace_jo, text)
    return text


def _ban_go_to_hyphen(text: str) -> str:
    """X番Y号 を X-Y（半角数字・半角ハイフン）に変換する。"""
    text = text.translate(_ZEN_TO_HAN)
    return re.sub(r'(\d+)番(\d+)号', r'\1-\2', text)


def _display_width(text: str) -> int:
    """Excel 列幅換算の表示幅を返す（全角=2、半角=1）。
    unicodedata.east_asian_width が W/F の文字（漢字・ひらがな・カタカナ等）を2、それ以外を1とする。
    """
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in text)


def _insert_linebreak(address: str, col_width: int = 35) -> str:
    """Excel 列幅(col_width=35)を超える住所に丁目の直後でセル内改行(\\n)を挿入する。

    既存の \\n は一旦除去して再判定するため、再処理でも正しい位置に改行が入る。

    挿入位置の優先順位:
      1. 丁目の直後          例) 5丁目|13-15
      2. 条の直後            例) 北14条|西3丁目  / 宮の森2条|10丁目7-30
      3. 番地数字列の先頭    例) 北栄町|1-1-1（丁目・条がない場合）
    """
    # 既存の改行を除去して再評価（前回の改行位置を上書き修正できる）
    address = address.replace('\n', '')

    if _display_width(address) < col_width:
        return address

    # 優先1: 丁目の直後で改行
    m = re.search(r'丁目', address)
    if m and m.end() < len(address):
        return address[:m.end()] + '\n' + address[m.end():]

    # 優先2: 条の直後で改行
    m = re.search(r'条', address)
    if m and m.end() < len(address):
        return address[:m.end()] + '\n' + address[m.end():]

    # 優先3: 番地数字列の先頭で改行
    m = re.search(r'(?<=[^\d\-])(\d+(?:\-\d+)+)', address)
    if m:
        return address[:m.start()] + '\n' + address[m.start():]

    return address


def _apply_hokkaido_rule(address: str) -> str:
    """北海道住所から「北海道」と「XX郡」を削除する。"""
    address = address[3:]                    # 「北海道」を削除（3文字）
    address = re.sub(r'\S+郡', '', address)  # 「上川郡」「河東郡」等を削除
    return address


def clean_address_logic(address: str) -> str:
    """住所文字列を正規化して1本の文字列で返す（キャッシュなし純粋変換）。

    ・Geolonia ライブラリで都道府県～番地を正規化
    ・丁目前の漢数字 → アラビア数字（「三丁目」→「3丁目」）
    ・X番Y号 → X-Y（半角数字・半角ハイフン）
    ・北海道の場合は「北海道」と「XX郡」を削除
    ・正規化に失敗した場合は元の住所をそのまま返す
    """
    if not address or str(address).strip() == "":
        return ""

    address_str = str(address).strip()
    try:
        norm = normalize(address_str)
        pref = norm.get('pref', '')
        cleaned = pref + norm.get('city', '') + norm.get('town', '') + norm.get('addr', '')
        if not cleaned:
            return address_str

        # 1. 丁目前の漢数字 → アラビア数字
        cleaned = _kanji_chome_to_arabic(cleaned)

        # 2. X番Y号 → X-Y（半角数字・半角ハイフン）
        cleaned = _ban_go_to_hyphen(cleaned)

        # 3. 北海道ルール: 「北海道」と「XX郡」を削除
        if pref == '北海道':
            cleaned = _apply_hokkaido_rule(cleaned)

        return cleaned
    except Exception as e:
        logger.error(f"住所正規化エラー '{address_str}': {e}")
        return address_str


@lru_cache(maxsize=2000)
def _cached_clean(address_str: str) -> str:
    """2層キャッシュ付きクレンジング。
    Level1: lru_cache（本デコレータ） → Level2: SQLite → Level3: HTTP normalize
    """
    # Level 2: SQLite 永続キャッシュ
    cached = _db_lookup(address_str)
    if cached is not None:
        # キャッシュ生成後に追加されたローカル変換を再適用する（漢数字→アラビア数字など）
        return _kanji_chome_to_arabic(cached)

    # Level 3: Geolonia HTTP 正規化（キャッシュミス時のみ）
    result = clean_address_logic(address_str)
    _db_store(address_str, result)
    return result


# ------------------------------------------------------------------ #
# 郵便番号データ補完（01HOKKAI.xlsx）                                   #
# ------------------------------------------------------------------ #

class PostalLookup:
    """Japan Post の郵便番号 XLSX から町域名→完全住所を引くインデックス。

    Japan Post のデータ列構成（0始まり）:
      0: 全国地方公共団体コード  1: 旧郵便番号  2: 郵便番号
      3: 都道府県名カナ          4: 市区町村名カナ  5: 町域名カナ
      6: 都道府県名              7: 市区町村名      8: 町域名
      9-14: 各種フラグ
    """

    def __init__(self, xlsx_path: str):
        self._index: dict[str, list[tuple[str, str, str]]] = {}
        self._load(xlsx_path)
        logger.info(f"郵便番号DB読込完了: {len(self._index)} 町域, {xlsx_path}")

    @staticmethod
    def _normalize_key(town: str) -> str:
        """照合キー用に町域名を正規化する。"""
        town = re.sub(r'[（(].*?[）)]', '', town)  # 括弧内（丁目情報等）を除去
        town = re.sub(r'^字', '', town)             # 先頭の「字」を除去
        return town.strip()

    def _load(self, xlsx_path: str) -> None:
        import openpyxl
        wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
        # 「各項目説明」シートはヘッダー説明なのでスキップ、他の全シートを読む
        for ws in wb.worksheets:
            if ws.title == '各項目説明':
                continue
            for row in ws.iter_rows(values_only=True):
                if not row or len(row) < 9:
                    continue
                pref = str(row[6] or '').strip()  # 列G: 都道府県名
                city = str(row[7] or '').strip()  # 列H: 市区町村名
                town = str(row[8] or '').strip()  # 列I: 町域名
                if not (pref and city and town):
                    continue
                if '以下に掲載がない場合' in town:
                    continue
                key = self._normalize_key(town)
                if not key:
                    continue
                entry = (pref, city, town)
                if key not in self._index:
                    self._index[key] = [entry]
                elif entry not in self._index[key]:
                    self._index[key].append(entry)
        wb.close()

    def lookup(self, partial: str) -> str | None:
        """部分住所から完全住所を返す。候補が複数の場合は None（曖昧）。"""
        key = self._normalize_key(partial)
        if not key:
            return None
        matches = self._index.get(key, [])
        if len(matches) == 1:
            pref, city, town = matches[0]
            return pref + city + town
        if len(matches) > 1:
            logger.debug(f"郵便番号照合 '{partial}': {len(matches)}件の候補あり（曖昧のためスキップ）")
        return None


# xlsx_path → PostalLookup のセッション内キャッシュ
_postal_cache: dict[str, 'PostalLookup'] = {}


def _get_postal_lookup(xlsx_path: str) -> 'PostalLookup | None':
    """PostalLookup をセッション中に1回だけ生成してキャッシュする。"""
    if not os.path.exists(xlsx_path):
        return None
    if xlsx_path not in _postal_cache:
        try:
            _postal_cache[xlsx_path] = PostalLookup(xlsx_path)
        except Exception as e:
            logger.warning(f"郵便番号データ読込エラー ({xlsx_path}): {e}")
            return None
    return _postal_cache[xlsx_path]


# 番地情報を含む住所パターン（丁目・ハイフン・数字など）
_ADDR_NUMBER_RE = re.compile(r'[\d\-ー]|丁目|番地|条|号')


def _is_partial_address(address: str) -> bool:
    """地名のみで番地数字を含まない場合に True を返す。
    郵便番号補完の対象を「兜沼」「字兜沼」のような短い地名に限定するための判定。
    「稚内市宝来3丁目3-42」のような詳細住所には補完を行わない。
    """
    return not bool(_ADDR_NUMBER_RE.search(address))


def _clean_with_postal(address_str: str, postal: 'PostalLookup | None') -> str:
    """Geoloniaで解決できない場合に郵便番号データで住所を補完する。

    1. Geolonia（lru_cache + SQLite 経由）で正規化を試みる
    2. 変換できなかった かつ 部分住所（番地なし地名のみ）の場合に
       PostalLookup でフル住所を取得
    3. 取得できたフル住所を再度 Geolonia で正規化して返す
    """
    from_geolonia = _cached_clean(address_str)
    # Geoloniaが解決できた（入力と結果が異なる）
    if from_geolonia != address_str:
        return from_geolonia
    # 番地数字を含む住所は補完しない（Geoloniaが解決済みだが北海道ルールで同文字列になった場合を含む）
    if postal is None or not _is_partial_address(address_str):
        return from_geolonia
    # Geolonia未解決 かつ 地名のみ → 郵便番号データで補完
    full = postal.lookup(address_str)
    if full:
        return _cached_clean(full)  # フル住所をGeoloniaで再正規化→SQLiteに保存
    return from_geolonia


# ------------------------------------------------------------------ #
# Excel シート操作                                                     #
# ------------------------------------------------------------------ #

def clean_addresses_in_book(book, cpath: str = '') -> int:
    """既に開いている xlwings Book の「1～1000」シート D 列を住所クレンジングする。

    Args:
        book:  xlwings.Book インスタンス（get_koden_workbook() で取得したもの）
        cpath: 処理フォルダのパス。01HOKKAI.xlsx が存在すれば郵便番号補完を行う。
    Returns:
        処理した行数
    """
    app = book.app
    app.screen_updating = False
    app.calculation = 'manual'
    app.display_alerts = False

    processed = 0
    sheet = None
    was_protected = False
    try:
        sheet = book.sheets["1～1000"]

        last_row = sheet.range(f'D{sheet.cells.last_cell.row}').end('up').row
        if last_row < 2:
            return 0

        raw_values = sheet.range(f'D2:D{last_row}').value

        # 単一行の場合はリストにする
        if not isinstance(raw_values, list):
            raw_values = [raw_values]

        # 01HOKKAI.xlsx: 案件フォルダ優先 → なければテンプレートフォルダ
        postal = None
        if cpath:
            postal = _get_postal_lookup(os.path.join(cpath, '01HOKKAI.xlsx'))
        if postal is None:
            try:
                import config as _cfg
                fallback = os.path.join(_cfg.BASE_PATH, _cfg.TPATH1, _cfg.TPATH2, '01HOKKAI.xlsx')
                postal = _get_postal_lookup(fallback)
            except Exception:
                pass
        if postal:
            print(f"郵便番号DB: {len(postal._index)} 町域読込済")

        # normalize() は HTTP I/O なので ThreadPoolExecutor で並列化する
        # SQLite キャッシュヒット時はほぼ瞬時に返る
        def _worker(val):
            if val is None or str(val).strip() == "":
                return val, False
            cleaned = _clean_with_postal(str(val).strip(), postal)
            return _insert_linebreak(cleaned), True

        n_workers = min(16, max(1, len(raw_values)))
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            pairs = list(executor.map(_worker, raw_values))

        cleaned_values = [[c] for c, _ in pairs]
        count = sum(1 for _, had in pairs if had)

        # シートが保護されている場合は一時解除して書き込む
        # UserInterfaceOnly 保護の場合 Unprotect() がエラーになるが
        # VBA/COM からの直接書き込みは可能なので、失敗を無視して続行する
        was_protected = sheet.api.ProtectContents
        explicitly_unprotected = False
        if was_protected:
            try:
                sheet.api.Unprotect()
                explicitly_unprotected = True
            except Exception as up_err:
                logger.warning(f"Unprotect スキップ（UserInterfaceOnly 保護の可能性）: {up_err}")

        sheet.range('D2').value = cleaned_values
        sheet.range(f'D2:D{last_row}').api.WrapText = True
        processed = count

    except Exception as e:
        logger.error(f"住所クレンジング処理エラー: {e}")
    finally:
        # 明示的に解除した場合のみ保護を元に戻す
        if sheet is not None and explicitly_unprotected:
            try:
                sheet.api.Protect()
            except Exception:
                pass
        app.screen_updating = True
        app.calculation = 'automatic'
        app.display_alerts = True

    return processed


def process_excel(file_path: str) -> None:
    """スタンドアロン実行用：ファイルパスを直接指定してバッチ処理する。"""
    import xlwings as xw

    if not os.path.exists(file_path):
        print(f"対象ファイルが見つかりません: {file_path}")
        return

    print(f"処理開始: {file_path}")
    start_time = time.time()

    with xw.App(visible=False) as app:
        app.screen_updating = False
        app.calculation = 'manual'
        app.display_alerts = False

        wb = app.books.open(file_path)
        processed = 0
        try:
            sheet = wb.sheets["1～1000"]
            last_row = sheet.range(f'D{sheet.cells.last_cell.row}').end('up').row
            if last_row >= 2:
                raw_values = sheet.range(f'D2:D{last_row}').value
                if not isinstance(raw_values, list):
                    raw_values = [raw_values]
                cleaned_values = [[clean_address_logic(val)] for val in raw_values]
                sheet.range('D2').value = cleaned_values
                processed = len(cleaned_values)
        except Exception as e:
            logger.error(f"シート処理エラー: {e}")
        finally:
            wb.save()
            wb.close()

    elapsed = time.time() - start_time
    print(f"処理完了 (処理行数: {processed}, 所要時間: {elapsed:.2f}秒)")


if __name__ == "__main__":
    TARGET_FILE = os.path.join(os.path.dirname(__file__), "data.xlsx")
    process_excel(TARGET_FILE)
