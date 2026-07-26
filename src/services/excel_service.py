"""
Excel操作サービス
Excelファイルの操作を統一管理
"""
import xlwings as xw
import config
import os
import re
import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Optional, Dict, Any, List, Callable


class _WorkbookContext:
    """ワークブック単体を with 文で安全に扱うヘルパー"""

    def __init__(self, service: 'ExcelService', file_path: str, update_links: bool):
        self._service = service
        self._file_path = file_path
        self._update_links = update_links
        self.book: Optional[xw.Book] = None

    def __enter__(self) -> xw.Book:
        self.book = self._service.open_workbook(self._file_path, self._update_links)
        return self.book

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._service.close_workbook(self._file_path)
        return False


class ExcelService:
    """Excel操作の共通サービス"""

    def __init__(self):
        self.workbooks = {}
        self.sheets = {}
        self._cpath = ""
        self.current_book_a = None
        self.current_book_b = None
        self.current_book_c = None
        self.current_sheet_a = None
        self.current_sheet_b1 = None
        self.current_sheet_b2 = None
        self.current_sheet_b3 = None
        self.current_sheet_c = None

    def set_cpath(self, path: str) -> None:
        """現在の作業パスを設定する（FileService から取得して DataService が注入）"""
        self._cpath = path

    def get_cpath(self) -> str:
        """現在の作業パスを返す。未設定の場合は config.ini から再読込する。"""
        if not self._cpath:
            try:
                import configparser as _cp
                parser = _cp.RawConfigParser()
                parser.read(config.CONFIG_INI, encoding='UTF-8')
                self._cpath = parser.get('Paths', 'current_path', fallback='').strip()
            except Exception:
                pass
        return self._cpath

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.safe_close_excel()
        return False
    
    def open_workbook(self, file_path: str, update_links: bool = True) -> xw.Book:
        """Excelワークブックを開く"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Excelファイルが見つかりません: {file_path}")

            # 同名ブックがすでにExcelで開かれている場合はそのハンドルを返す
            file_name = os.path.basename(file_path)
            for app in xw.apps:
                for book in app.books:
                    if book.name == file_name:
                        self.workbooks[file_path] = book
                        return book

            book = xw.Book(file_path, update_links=update_links)
            self.workbooks[file_path] = book
            return book
        except Exception as e:
            raise Exception(f"Excelファイルの読み込みに失敗しました: {str(e)}")

    def open_book_context(self, file_path: str, update_links: bool = True):
        """ワークブック単体を with 文で安全に扱うコンテキストマネージャーを返す"""
        return _WorkbookContext(self, file_path, update_links)
    
    def get_sheet(self, book: xw.Book, sheet_name: str) -> xw.Sheet:
        """指定されたシートを取得"""
        try:
            sheet = book.sheets[sheet_name]
            return sheet
        except Exception as e:
            raise Exception(f"シート '{sheet_name}' の取得に失敗しました: {str(e)}")
    
    def read_cell_value(self, sheet: xw.Sheet, cell: str) -> Any:
        """セルの値を読み取り"""
        try:
            return sheet.range(cell).value
        except Exception as e:
            raise Exception(f"セル '{cell}' の読み取りに失敗しました: {str(e)}")
    
    def write_cell_value(self, sheet: xw.Sheet, cell: str, value: Any) -> None:
        """セルに値を書き込み"""
        try:
            sheet.range(cell).value = value
        except Exception as e:
            raise Exception(f"セル '{cell}' への書き込みに失敗しました: {str(e)}")
    
    def read_range_values(self, sheet: xw.Sheet, range_str: str) -> List[List[Any]]:
        """範囲の値を読み取り"""
        try:
            return sheet.range(range_str).value
        except Exception as e:
            raise Exception(f"範囲 '{range_str}' の読み取りに失敗しました: {str(e)}")
    
    def write_range_values(self, sheet: xw.Sheet, range_str: str, values: List[List[Any]]) -> None:
        """範囲に値を書き込み"""
        try:
            sheet.range(range_str).value = values
        except Exception as e:
            raise Exception(f"範囲 '{range_str}' への書き込みに失敗しました: {str(e)}")
    
    def close_workbook(self, file_path: str) -> None:
        """指定されたワークブックを閉じる"""
        try:
            if file_path in self.workbooks:
                self.workbooks[file_path].close()
                del self.workbooks[file_path]
        except Exception as e:
            print(f"ワークブックの閉じる処理でエラーが発生: {str(e)}")
    
    def close_all_workbooks(self) -> None:
        """すべてのワークブックを閉じる"""
        for file_path in list(self.workbooks.keys()):
            self.close_workbook(file_path)
    
    def safe_close_excel(self) -> None:
        """Excelを安全に終了。各ブックを独立して閉じ、COM切断済みエラーは無視する。"""
        def _close(book):
            if book is None:
                return
            try:
                book.close()
            except Exception:
                pass  # RPC_E_DISCONNECTED など、既に Excel が閉じられていた場合は無視

        _close(self.current_book_a)
        self.current_book_a = None
        self.current_sheet_a = None

        _close(self.current_book_b)
        self.current_book_b = None
        self.current_sheet_b1 = None
        self.current_sheet_b2 = None
        self.current_sheet_b3 = None

        _close(self.current_book_c)
        self.current_book_c = None
        self.current_sheet_c = None

        # self.workbooks には get_*_workbook() 経由で current_book_* と
        # 同一インスタンスが登録されているため、上記で全て閉じ済み。
        # dict のみクリアして二重 close を防ぐ。
        self.workbooks.clear()
    
    def get_koden_workbook(self) -> xw.Book:
        """香典帳のワークブックを取得"""
        if self.current_book_a is None:
            file_path = os.path.join(self.get_cpath(), config.XLBOOK_A)
            self.current_book_a = self.open_workbook(file_path)
            self.current_sheet_a = self.get_sheet(self.current_book_a, config.XLBOOK_A_SHEET_I11)
        return self.current_book_a

    def get_funeral_workbook(self) -> xw.Book:
        """葬儀記録書のワークブックを取得"""
        if self.current_book_b is None:
            file_path = os.path.join(self.get_cpath(), config.XLBOOK_B)
            self.current_book_b = self.open_workbook(file_path)
            self.current_sheet_b1 = self.get_sheet(self.current_book_b, config.XLBOOK_B_SHEET_I05)
            try:
                self.current_sheet_b2 = self.get_sheet(self.current_book_b, config.XLBOOK_B_SHEET_I06)
            except Exception:
                # シート名の表記揺れ（施行/施工）に対応するためインデックスで取得
                self.current_sheet_b2 = self.current_book_b.sheets[5]
        return self.current_book_b

    def get_accounting_workbook(self) -> xw.Book:
        """会計帳のワークブックを取得"""
        if self.current_book_c is None:
            file_path = os.path.join(self.get_cpath(), config.XLBOOK_C)
            self.current_book_c = self.open_workbook(file_path)
            self.current_sheet_c = self.get_sheet(self.current_book_c, config.XLBOOK_C_SHEET_I01)
        return self.current_book_c
    
    def get_flower_workbook(self) -> xw.Book:
        """供花料のワークブックを取得"""
        # 供花料は会計帳と同じワークブックを使用
        return self.get_accounting_workbook()
    
    def update_koden_data(self, row: int, data: Dict[str, Any]) -> None:
        """香典データを更新"""
        try:
            sheet = self.current_sheet_a
            if sheet is None:
                raise Exception("香典シートが開かれていません")

            # B:J を一括読み込みして変更対象だけ上書き後、一括書き込み（COM往復を2回に削減）
            # 列インデックス: B=0,C=1,D=2,E=3,F=4,G=5,H=6,I=7,J=8
            vals = list(sheet.range(f"B{row}:J{row}").value or [None] * 9)
            if 'price' in data:
                vals[0] = data['price']
            if 'address' in data:
                vals[2] = data['address']
            if 'name' in data:
                vals[3] = data['name']
            if 'furigana' in data:
                vals[6] = data['furigana']
            if 'receipt' in data:
                vals[7] = '○' if data['receipt'] else ''
            if 'check' in data:
                vals[8] = '○' if data['check'] else ''
            sheet.range(f"B{row}:J{row}").value = vals

            if self.current_book_a is not None:
                self.current_book_a.save()

        except Exception as e:
            raise Exception(f"香典データの更新に失敗しました: {str(e)}")
    
    def read_koden_data(self, row: int) -> Dict[str, Any]:
        """香典データを読み取り"""
        try:
            sheet = self.current_sheet_a
            if sheet is None:
                raise Exception("香典シートが開かれていません")

            # B:J を一括取得（COM呼び出し1回）
            # 列インデックス: B=0,C=1,D=2,E=3,F=4,G=5,H=6,I=7,J=8
            vals = sheet.range(f"B{row}:J{row}").value or [None] * 9
            return {
                'price': vals[0],
                'address': vals[2],
                'name': vals[3],
                'furigana': vals[6],
                'receipt': vals[7] == '○',
                'check': vals[8] == '○',
            }
        except Exception as e:
            raise Exception(f"香典データの読み取りに失敗しました: {str(e)}")

    def load_koden_into_window(self, n, window) -> bool:
        """香典データをExcelから読み込んでウィンドウフィールドに反映する。

        func1.get_condo から移植。Phase 4 で gv 参照を instance 変数に移行予定。
        """
        n = int(n)
        if n <= 10:
            rrow = str(n + 2)
        else:
            if n % 10 != 0:
                rrow = str(n + ((n // 10) + 2))
            else:
                rrow = str(n + ((n // 10) + 1))

        sheet = self.current_sheet_a
        if sheet is None:
            sheet = xw.Book(
                self._cpath + "\\" + config.XLBOOK_A, update_links=True
            ).sheets(config.XLBOOK_A_SHEET_I11)
            self.current_sheet_a = sheet

        b_val = sheet.range("B" + rrow).value
        c_val = sheet.range("C" + rrow).value
        p = (str(int(b_val)) + str(c_val)) if b_val not in ("", None) else ",000"
        window['-i_price-'].update(p)

        d_val = sheet.range("D" + rrow).value
        window['-i_address-'].update(d_val if d_val not in ("", None) else " ")

        xname = sheet.range("E" + rrow).value
        window['-i_name-'].update(xname)
        window['-i_furigana-'].update(sheet.range("H" + rrow).value)
        window['-k_rmail-'].update(sheet.range("I" + rrow).value == '○')
        window['-k_inv-'].update(sheet.range("J" + rrow).value == '○')
        return xname is not None

    def save_koden_from_window(self, window, values) -> None:
        """ウィンドウの香典データをExcelに書き込み、フィールドをクリアする。

        func1.update_condo から移植。Phase 4 で gv 参照を instance 変数に移行予定。
        """
        book = self.get_koden_workbook()
        book.activate()
        sheet = self.current_sheet_a
        sheet.activate()

        n = int(values['-i_no-'])
        if (n // 10) < 1 or n == 10:
            rrow = str(n + 2)
        elif n % 10 != 0:
            rrow = str(n + 2 + (n // 10))
        else:
            rrow = str(n + 2 + (n // 10) - 1)

        price = values['-i_price-']
        p_list = price.split(',')
        sheet.range("B" + rrow).value = None if p_list[0] == "000" else p_list[0]
        if p_list[1] != "000":
            sheet.range("C" + rrow).value = "," + p_list[1]

        sheet.range("D" + rrow).value = values['-i_address-']
        sheet.range("E" + rrow).value = values['-i_name-']
        sheet.range("H" + rrow).value = values['-i_furigana-']
        sheet.range("I" + rrow).value = '○' if values['-k_rmail-'] else ''
        sheet.range("J" + rrow).value = '○' if values['-k_inv-'] else ''

        book.save()

        window['-i_price-'].update(",000")
        window['-i_furigana-'].update("")
        window['-i_address-'].update("")
        window['-i_name-'].update("")
        window['-k_rmail-'].update(False)
        window['-k_inv-'].update(False)
        window['-i_price-'].focus_set()

    # ------------------------------------------------------------------ #
    # 非同期実行サポート                                                    #
    # xlwings は COM ベースなので pythoncom.CoInitialize が必要             #
    # ------------------------------------------------------------------ #

    def run_async(self, func: Callable, *args, on_done: Optional[Callable] = None,
                  on_error: Optional[Callable] = None) -> Future:
        """Excel操作をバックグラウンドスレッドで実行する。

        Args:
            func: 実行する関数
            *args: func に渡す引数
            on_done: 成功時コールバック (result を受け取る)
            on_error: 失敗時コールバック (exception を受け取る)

        Returns:
            Future オブジェクト（結果の取得・キャンセルに使用）

        使用例::
            excel.run_async(
                excel.get_koden_workbook,
                on_done=lambda wb: print("開きました"),
                on_error=lambda e: popup_error(str(e)),
            )
        """
        import pythoncom

        def _worker():
            # xlwings/COM はスレッドごとに初期化が必要
            pythoncom.CoInitialize()
            try:
                result = func(*args)
                if on_done:
                    on_done(result)
                return result
            except Exception as exc:
                if on_error:
                    on_error(exc)
                raise
            finally:
                pythoncom.CoUninitialize()

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(_worker)
        executor.shutdown(wait=False)
        return future

    def open_workbook_async(self, file_path: str,
                            on_done: Optional[Callable] = None,
                            on_error: Optional[Callable] = None) -> Future:
        """ワークブックを非同期で開く（UIをブロックしない）"""
        return self.run_async(self.open_workbook, file_path, on_done=on_done, on_error=on_error)

    # ------------------------------------------------------------------ #
    # 葬儀情報 Excel ↔ GUI 同期                                           #
    # func1.read_ginfo1/2 / set_gInfo1/2 から移植                         #
    # ------------------------------------------------------------------ #

    def read_funeral_info1(self, window) -> None:
        """葬儀記録書シート（B1）のデータをウィンドウに反映する。

        func1.read_ginfo1 から移植。gv 参照を self.* / config.* に置き換え済み。
        gl.* 参照は data.list_data から取得。
        """
        from utils.date_utils import convert_to_wareki, calc_age
        from data.list_data import fform_list, xform_list1, xform_list2

        try:
            self.get_funeral_workbook()
            self.current_book_b.activate()
            self.current_sheet_b1.activate()

            sh = self.current_sheet_b1

            window['-rname0-'].update(sh.range("E11").value)
            window['-sname1-'].update(sh.range("B15").value)
            window['-sname0-'].update(sh.range("E15").value)

            izoku = self._extract_family_name_from_path(self._cpath)
            if izoku != sh.range("K11").value:
                sh.range("K11").value = izoku
            sheet_izoku = sh.range("K11").value
            s = izoku if len(izoku) <= 20 else sheet_izoku
            window['-hname0-'].update(s)

            window['-syear1-'].update(sh.range("F22").value)

            birth_date_obj = None
            birth_date = sh.range("M28").value
            if birth_date:
                try:
                    if isinstance(birth_date, (int, float)):
                        base = datetime.datetime(1900, 1, 1)
                        birth_date_obj = base + datetime.timedelta(days=int(birth_date))
                    else:
                        for fmt in ('%Y/%m/%d 00:00:00', '%Y-%m-%d 00:00:00', '%Y/%m/%d 00:00'):
                            try:
                                birth_date_obj = datetime.datetime.strptime(str(birth_date), fmt)
                                break
                            except ValueError:
                                pass
                        if birth_date_obj is None:
                            birth_date_obj = datetime.datetime.strptime(
                                str(birth_date).split()[0], '%Y-%m-%d'
                            )
                    window['-r_date-'].update(convert_to_wareki(birth_date_obj))
                    window['-r_date_x-'].update(birth_date_obj.strftime('%Y/%m/%d 00:00'))
                except Exception as e:
                    print(f"生年月日解析エラー: {e}")

            death_year = sh.range("C28").value
            death_month = sh.range("E28").value
            death_day = sh.range("G28").value
            death_ampm = sh.range("D30").value
            death_hour = sh.range("E30").value
            death_minute = sh.range("G30").value

            death_date_obj = None
            if death_year and death_month and death_day:
                try:
                    year_ad = 2018 + int(death_year)
                    hour_24 = int(death_hour) if death_hour else 0
                    if death_ampm == "午後" and hour_24 != 12:
                        hour_24 += 12
                    elif death_ampm == "午前" and hour_24 == 12:
                        hour_24 = 0
                    death_date_obj = datetime.datetime(
                        year_ad, int(death_month), int(death_day),
                        hour_24, int(death_minute) if death_minute else 0
                    )
                    window['-s_date-'].update(convert_to_wareki(death_date_obj))
                    window['-s_date_x-'].update(death_date_obj.strftime('%Y/%m/%d %H:%M'))
                except Exception as e:
                    print(f"死亡日時解析エラー: {e}")

            current_age = window['-syear2-'].get()
            try:
                if birth_date_obj and death_date_obj:
                    age = calc_age(birth_date_obj, death_date_obj)
                    if age is not None and age >= 0:
                        window['-syear2-'].update(str(age))
                    elif current_age:
                        window['-syear2-'].update(str(current_age))
                elif current_age:
                    window['-syear2-'].update(str(current_age))
            except Exception as e:
                print(f"年齢計算エラー: {e}")
                if current_age:
                    window['-syear2-'].update(str(current_age))

            try:
                ff_choice = [f"{k}/{v[0]}/{v[1]}/{v[2]}" for k, v in fform_list.items()]
                x1_choice = [f"{k}/{v[0]}" for k, v in xform_list1.items()]
                x2_choice = [f"{k}/{v[0]}" for k, v in xform_list2.items()]
                window['fz_format00'].update(values=ff_choice)
                window['fz_format01'].update(values=x1_choice)
                window['fz_format02'].update(values=x2_choice)

                xform_key = sh.range("N28").value
                if xform_key and xform_key in fform_list:
                    v = fform_list[xform_key]
                    window['fz_format00'].update(value=f"{xform_key}/{v[0]}/{v[1]}/{v[2]}")

                xform_keys = sh.range("O28").value
                if xform_keys:
                    keys = xform_keys.split('_')
                    if len(keys) >= 2:
                        if keys[0] in xform_list1:
                            window['fz_format01'].update(value=f"{keys[0]}/{xform_list1[keys[0]][0]}")
                        if keys[1] in xform_list2:
                            window['fz_format02'].update(value=f"{keys[1]}/{xform_list2[keys[1]][0]}")
            except Exception as e:
                print(f"葬儀形態設定エラー: {e}")

        except Exception as e:
            print(f"read_funeral_info1 エラー: {e}")

    def read_funeral_info2(self, window) -> None:
        """葬儀施行要領シート（B2）のデータをウィンドウに反映する。

        func1.read_ginfo2 から移植。
        """
        from utils.date_utils import convert_to_wareki, calc_age
        from data.list_data import temple_list, venue_list, s_choice

        try:
            self.get_funeral_workbook()
            self.current_book_b.activate()
            self.current_sheet_b2.activate()

            sh1 = self.current_sheet_b1
            sh2 = self.current_sheet_b2

            birth_date_obj = None
            birth_date = sh1.range("M28").value if sh1 else None
            if birth_date:
                try:
                    if isinstance(birth_date, (int, float)):
                        base = datetime.datetime(1900, 1, 1)
                        birth_date_obj = base + datetime.timedelta(days=int(birth_date))
                    else:
                        for fmt in ('%Y/%m/%d 00:00', '%Y-%m-%d 00:00:00'):
                            try:
                                birth_date_obj = datetime.datetime.strptime(str(birth_date), fmt)
                                break
                            except ValueError:
                                pass
                        if birth_date_obj is None:
                            birth_date_obj = datetime.datetime.strptime(
                                str(birth_date).split()[0], '%Y-%m-%d'
                            )
                    window['-r_date-'].update(convert_to_wareki(birth_date_obj))
                    window['-r_date_x-'].update(birth_date_obj.strftime('%Y/%m/%d 00:00'))
                except Exception as e:
                    print(f"生年月日変換エラー: {e}")

            death_date_obj = None
            death_date = sh1.range("L28").value if sh1 else None
            if death_date:
                try:
                    if isinstance(death_date, (int, float)):
                        base = datetime.datetime(1900, 1, 1)
                        days = int(death_date)
                        frac = death_date % 1
                        hours = int(frac * 24)
                        minutes = int((frac * 24 - hours) * 60)
                        death_date_obj = base + datetime.timedelta(days=days, hours=hours, minutes=minutes)
                    else:
                        for fmt in ('%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M:%S'):
                            try:
                                death_date_obj = datetime.datetime.strptime(str(death_date), fmt)
                                break
                            except ValueError:
                                pass
                    if death_date_obj:
                        window['-s_date-'].update(convert_to_wareki(death_date_obj))
                        window['-s_date_x-'].update(death_date_obj.strftime('%Y/%m/%d %H:%M'))
                except Exception as e:
                    print(f"死亡日時変換エラー: {e}")

            if birth_date_obj and death_date_obj:
                age = calc_age(birth_date_obj, death_date_obj)
                if age is not None:
                    window['-syear1-'].update('行年')
                    window['-syear2-'].update(str(age))

            def _build_date_str(sh, row):
                val_d = sh.range(f"D{row}").value
                yr_str = str(val_d).replace("令和", "") if isinstance(val_d, str) else str(int(val_d))
                mon = str(int(sh.range(f"G{row}").value)).zfill(2)
                day = str(int(sh.range(f"H{row}").value)).zfill(2)
                ampm = str(sh.range(f"K{row}").value)
                hour = str(int(sh.range(f"L{row}").value)).zfill(2)
                min_val = str(sh.range(f"M{row}").value)
                suffix = ""
                if "より" in min_val:
                    suffix = "00" if len(min_val) == 2 else min_val.replace("より", "")
                else:
                    suffix = "00"
                jp_str = f"令和{yr_str.zfill(2)}年{mon}月{day}日 {ampm}{hour}時"
                year_ad = int(float(yr_str)) + 2018
                h24 = int(hour)
                if ampm == "午後" and h24 < 12:
                    h24 += 12
                elif ampm == "午前" and h24 == 12:
                    h24 = 0
                x_str = f"{year_ad}/{int(mon):02d}/{int(day):02d} {h24:02d}:{suffix}"
                return jp_str, x_str, suffix

            try:
                d1, a1, s1 = _build_date_str(sh2, 13)
                d2, a2, s2 = _build_date_str(sh2, 15)
                d3, a3, s3 = _build_date_str(sh2, 17)
                window['-day1_date-'].update(d1 + (s1 if s1 != "00" else ""))
                window['-day2_date-'].update(d2 + (s2 if s2 != "00" else ""))
                window['-day3_date-'].update(d3 + (s3 if s3 != "00" else ""))
                window['-day1_date_x-'].update(a1)
                window['-day2_date_x-'].update(a2)
                window['-day3_date_x-'].update(a3)
            except Exception as e:
                print(f"施工日時変換エラー: {e}")

            try:
                t1 = str(int(sh2.range("O5").value))
                for i, (k, v) in enumerate(temple_list.items()):
                    if t1 == k:
                        window['temple00'].current(i)
                        break
                v1 = sh2.range("O2").value
                for i, (k, v) in enumerate(venue_list.items()):
                    if v1 == k:
                        window['venue00'].current(i)
                        break
            except Exception as e:
                print(f"寺院・会場情報読み込みエラー: {e}")

        except Exception as e:
            print(f"read_funeral_info2 エラー: {e}")

    def save_funeral_info1(self, values) -> None:
        """ウィンドウの葬儀記録書データを Excel シート B1 に書き込む。

        func1.set_gInfo1 から移植。
        """
        book = self.get_funeral_workbook()
        book.activate()
        sh = self.current_sheet_b1
        sh.activate()

        sh.range("E11").value = values['-rname0-']
        sh.range("B15").value = values.get('-sname1-', '')
        sh.range("E15").value = values['-sname0-']
        sh.range("K11").value = values['-hname0-']
        sh.range("F22").value = values['-syear1-']
        sh.range("G22").value = values['-syear2-']
        sh.range("M28").value = values.get('-r_date_x-', '')

        if values.get('fz_format00'):
            r1 = values['fz_format00'].split('/')
            sh.range("N28").value = r1[0]
        if values.get('fz_format01') and values.get('fz_format02'):
            r2 = values['fz_format01'].split('/')
            r3 = values['fz_format02'].split('/')
            sh.range("O28").value = r2[0] + "_" + r3[0]

        s_date = values.get('-s_date-', '')
        if s_date:
            result = re.split('[令和年月日午前午後時分 ]', s_date)
            lst = [a for a in result if a]
            sh.range("C28").value = lst[0]
            sh.range("E28").value = lst[1]
            sh.range("G28").value = lst[2]
            if '時' in s_date and '分' in s_date:
                sh.range("D30").value = '午前' if '午前' in s_date else '午後'
                sh.range("E30").value = lst[3]
                sh.range("G30").value = lst[4]
            else:
                for cell in ["E30", "F30", "G30", "H30"]:
                    sh.range(cell).value = ""

        book.save()

    def save_funeral_info2(self, values) -> None:
        """ウィンドウの葬儀施行要領データを Excel シート B2 に書き込む。

        func1.set_gInfo2 から移植。
        """
        book = self.get_funeral_workbook()
        book.activate()
        sh = self.current_sheet_b2
        sh.activate()

        r1 = values.get('venue00', '/').split('/')
        sh.range("O2").value = r1[0]

        r1 = values.get('temple00', '/').split('/')
        sh.range("O5").value = r1[0]

        r1 = values.get('fz_format00', '///').split('/')
        sh.range("A13").value = r1[1] if len(r1) > 1 else ''
        sh.range("A15").value = r1[2] if len(r1) > 2 else ''
        sh.range("A17").value = r1[3] if len(r1) > 3 else ''

        for idx, key in zip([13, 15, 17], ['-day1_date-', '-day2_date-', '-day3_date-']):
            datestr = values.get(key, '')
            if not datestr:
                continue
            res = re.split('[令和年月日午前午後時分]', datestr)
            result = [a for a in res if a]
            sh.range(f"D{idx}").value = result[0] if result else ''
            sh.range(f"G{idx}").value = result[1] if len(result) > 1 else ''
            sh.range(f"H{idx}").value = result[2] if len(result) > 2 else ''
            if '午前' in datestr:
                sh.range(f"K{idx}").value = '午前'
            elif '午後' in datestr:
                sh.range(f"K{idx}").value = '午後'
            if len(result) > 4:
                sh.range(f"L{idx}").value = str(int(result[4]))
            if '分' in datestr and len(result) > 5:
                sh.range(f"M{idx}").value = result[5] + "分より"

        book.save()

    @staticmethod
    def _extract_family_name_from_path(cpath: str) -> str:
        """パスの末尾フォルダ名から遺族名（非ASCII部分）を抽出する。
        FolderBrowse が / 区切りを返す場合も os.path.basename で正規化する。
        """
        folder = os.path.basename(cpath.rstrip('/\\'))
        return re.sub(r'[A-Za-z0-9,]', '', folder)