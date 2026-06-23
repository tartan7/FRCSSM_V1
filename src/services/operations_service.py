"""
複合 Excel 操作サービス
func1.py から移植した複合操作の実装。
"""
import os
import glob as _glob
import shutil
import subprocess
import time
import datetime
import config
from typing import Any, List, Optional


class OperationsService:
    """複合 Excel 操作の共通サービス"""

    def __init__(self, excel_service, file_service):
        self.excel_service = excel_service
        self.file_service = file_service

    # ------------------------------------------------------------------ #
    # 内部ヘルパー                                                          #
    # ------------------------------------------------------------------ #

    def _book_b(self):
        """bookB（新書類１式）を返す（キャッシュ済み）"""
        return self.excel_service.get_funeral_workbook()

    def _book_a(self):
        """bookA（合体香典帳）を返す（キャッシュ済み）"""
        return self.excel_service.get_koden_workbook()

    def _book_c(self):
        """bookC（葬儀データ）を返す（キャッシュ済み）"""
        return self.excel_service.get_accounting_workbook()

    # ------------------------------------------------------------------ #
    # 供花料 (FoFF) 操作  ─ sheets[16] = '10.供花料'                       #
    # ------------------------------------------------------------------ #

    def get_foFF_input(self, window) -> List:
        """供花料データを取得してリストを返す。func1.get_FoFF_input から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[16]
        sh.activate()

        lst = []
        for idx in range(3, 221):
            e_val = sh.range("E" + str(idx)).value
            a_val = sh.range("A" + str(idx)).value
            if e_val is not None:
                c1 = str(int(a_val)).zfill(3)
                b_val = sh.range("B" + str(idx)).value
                c_val = sh.range("C" + str(idx)).value
                c2 = str(int(b_val)) if b_val is not None else "0"
                c3 = str(c_val) if c_val is not None else ""
                ca = c2 + c3
                c4 = sh.range("D" + str(idx)).value or ''
                c5 = str(e_val)
                c7 = sh.range("G" + str(idx)).value or ''
                lst.append([c1, ca, c4, c5, c7])
            elif a_val == "小計":
                continue
            else:
                break
        return lst

    def set_foFF_input(self, val: List, no: int = -1) -> None:
        """供花料データを保存する。func1.set_FoFF_input から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[16]
        sh.activate()

        r_iid = 0
        if no == -1:
            r_iid = int(sh.range("C224").value) + 1
        else:
            r_iid = no

        dv = int(r_iid) // 10
        rrow = r_iid + 2 + dv

        if val[0] not in ("", " ") and val[1] not in ("", " "):
            tmp0 = str(val[1]).replace(",", "")
            try:
                tmp0_int = int(tmp0)
            except ValueError:
                tmp0_int = 0
            tmp1 = tmp0_int // 1000
            tmp2 = tmp0_int % 1000
            tmp3 = val[3] if len(val) > 3 else ''
        else:
            tmp1 = ""
            tmp2 = 0
            tmp3 = ""

        r_row = str(rrow)
        sh.range("B" + r_row).value = str(tmp1) if tmp1 != "" else ""
        if tmp2 != 0:
            sh.range("C" + r_row).value = "," + str(tmp2).zfill(3)
        sh.range("D" + r_row).value = val[2] if len(val) > 2 else ''
        sh.range("E" + r_row).value = tmp3
        sh.range("G" + r_row).value = val[4] if len(val) > 4 else ''
        book.save()

    # ------------------------------------------------------------------ #
    # 弔辞弔電 (CdMsg) 操作  ─ sheets[10] = '6.弔辞弔電a'                  #
    # ------------------------------------------------------------------ #

    def get_cd_msg(self, window) -> List:
        """弔辞弔電データを取得してリストを返す。func1.get_CdMsg から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[10]
        sh.activate()

        lst = []
        for idx in range(3, 152):
            c_val = sh.range("C" + str(idx)).value
            b_val = sh.range("B" + str(idx)).value
            if c_val is not None or b_val is not None:
                c1 = str(int(sh.range("A" + str(idx)).value)).zfill(3)
                c2 = b_val if b_val is not None else " "
                c3 = c_val if c_val is not None else " "
                c5 = sh.range("E" + str(idx)).value
                if c5 is None or c5 == " ":
                    c5 = " "
                else:
                    try:
                        c5 = str(int(c5))
                    except (ValueError, TypeError):
                        c5 = str(c5)
                lst.append([c1, c2, c3, c5])
            else:
                break
        return lst

    def set_cd_msg(self, val: List, no: int = -1) -> None:
        """弔辞弔電データを保存する。func1.set_CdMsg から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[10]
        sh.activate()

        base = 2
        if val[0] != " " and val[0] != "":
            r_iid = int(val[0]) if no == -1 else no
        else:
            r_iid = no

        rrow = base + int(r_iid)
        r_row = str(rrow)
        sh.range("E" + r_row).value = val[3] if len(val) > 3 else ''
        sh.range("B" + r_row).value = val[1] if len(val) > 1 else ''

        tmp_name = ""
        if len(val) > 4 and val[4]:
            tmp_name += " (線香 月)"
        if len(val) > 5 and val[5]:
            tmp_name += " (線香 哀星)"
        if len(val) > 6 and val[6]:
            tmp_name += " (プリザーブドフラワー)"
        if len(val) > 7 and val[7] and len(val) > 8 and val[8]:
            tmp_name += "（" + val[8] + "）"

        base_text = val[2] if len(val) > 2 else ''
        sh.range("C" + r_row).value = base_text if tmp_name == "" else base_text + "\n" + tmp_name

    def subt_sort_t3(self) -> None:
        """弔辞弔電テーブルをソートする（Excelマクロ実行）。func1.subt_sort_T3 から移植。"""
        book = self._book_b()
        book.activate()
        mf = book.macro('Sheet12.Val4Sort_Click')
        mf()
        book.save()

    # ------------------------------------------------------------------ #
    # 供物 (OfInput) 操作  ─ sheets[0] = '供物入力シート'                    #
    # ------------------------------------------------------------------ #

    def get_of_input(self, window) -> List:
        """供物データを取得してリストを返す。func1.get_OfInput から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[0]
        sh.activate()

        raw = sh.range("E26:I225").value  # E,F,G,H,I 列を一括取得
        lst = []
        for row in (raw or []):
            g_val = row[2]  # G列
            if g_val is None:
                break
            e_val = row[0]  # E列
            c1 = str(int(e_val)).zfill(3) if e_val is not None else ""
            c2 = str(row[1])  # F列
            c3 = str(g_val).replace('.0', '')
            c4 = str(row[3]).replace('.0', '')  # H列
            c5 = row[4]  # I列
            lst.append([c1, c2, c3, c4, c5])
        return lst

    def set_of_input(self, val: List, no: int = 0) -> None:
        """供物データを保存する。func1.set_OfInput から移植。

        no=0: 最終行に追加, no>0: 行指定更新, no=-1: IDで検索して更新
        """
        book = self._book_b()
        book.activate()
        sh = book.sheets[0]
        sh.activate()

        base = 25
        rrow = 0

        if no == -1:
            r_iid = val[0]
            for idx in range(26, 226):
                if r_iid == sh.range("E" + str(idx)).value:
                    rrow = idx
                    break
        elif no == 0:
            rrow = sh.range(225, 7).end('up').row + 1
            val = list(val)
            val[0] = ""
        else:
            try:
                r_iid = val[0]
                val = list(val)
                val[0] = no
                rrow = base + int(str(r_iid))
            except (ValueError, TypeError):
                rrow = base + no

        r_row = str(rrow)
        sh.range("E" + r_row).value = val[0]
        sh.range("G" + r_row).value = val[1] if len(val) > 1 else None
        sh.range("H" + r_row).value = val[2] if len(val) > 2 else None
        sh.range("I" + r_row).value = val[3] if len(val) > 3 else None
        book.save()

    def subt_sort_t4(self) -> None:
        """供物テーブルをソートする（Excelマクロ実行）。func1.subt_sort_T4 から移植。"""
        book = self._book_b()
        book.activate()
        me = book.macro('Sheet3.Val2Sort_Click')
        me()
        book.save()

    # ------------------------------------------------------------------ #
    # 焼香順 (InceBO) 操作  ─ sheets[2] = '焼香順入力シート'                 #
    # ------------------------------------------------------------------ #

    def get_ince_bo(self, window) -> List:
        """焼香順データを取得してリストを返す。func1.get_InceBO から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[2]
        sh.activate()

        lst = []
        for idx in range(9, 128):
            d_val = sh.range("D" + str(idx)).value
            if d_val is not None:
                cc1 = sh.range("C" + str(idx)).value
                c1 = str(int(cc1)).zfill(4) if cc1 not in ("", None, " ") else " "
                c2 = d_val
                c3 = sh.range("E" + str(idx)).value
                cc4 = sh.range("F" + str(idx)).value
                c4 = str(int(cc4)) if cc4 not in ("", None, " ") else " "
                lst.append([c1, c2, c3, c4])
            else:
                break
        return lst

    def set_ince_bo(self, val: List) -> None:
        """焼香順データを保存する。func1.set_InceBO から移植（xrow=-1 相当）。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[2]
        sh.activate()

        r_iid = int(val[0])
        rrow = 0
        for idx in range(9, 129):
            cell_val = sh.range("C" + str(idx)).value
            if cell_val is not None:
                try:
                    if r_iid == int(cell_val):
                        rrow = idx
                        break
                except (ValueError, TypeError):
                    pass

        if rrow == 0:
            return

        r_row = str(rrow)
        sh.range("C" + r_row).value = val[0] if val[0] != " " else None
        sh.range("D" + r_row).value = val[1] if val[1] != " " else None
        if len(val) > 2 and val[2] != "":
            sh.range("E" + r_row).value = val[2]
        else:
            formula = self._ince_bo_formula(r_row)
            sh.range("E" + r_row).formula = formula
        sh.range("F" + r_row).value = val[3] if len(val) > 3 and val[3] != "" else 10
        book.save()
        self.subt_sort_t4()

    def insert_ince_bo(self, val: List) -> None:
        """焼香順データを最終行に追加する。func1.insert_InceBO から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[2]
        sh.activate()

        rrow = sh.range(128, 3).end('up').row + 1
        r_row = str(rrow)
        sh.range("C" + r_row).value = val[0] if len(val) > 0 else None
        sh.range("D" + r_row).value = val[1] if len(val) > 1 else None
        sh.range("E" + r_row).value = val[2] if len(val) > 2 else None
        sh.range("F" + r_row).value = val[3] if len(val) > 3 else 10
        book.save()

    def del_ince_bo(self, no: int) -> None:
        """焼香順データを削除する。func1.del_InceBO から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[2]
        sh.activate()

        rrow = 0
        for idx in range(9, 129):
            cell_val = sh.range("C" + str(idx)).value
            if cell_val is not None:
                try:
                    if no == int(cell_val):
                        rrow = sh.range("C" + str(idx)).row
                        break
                except (ValueError, TypeError):
                    pass

        if rrow == 0:
            return

        r_row = str(rrow)
        sh.range("C" + r_row).value = ""
        sh.range("D" + r_row).value = ""
        sh.range("E" + r_row).formula = self._ince_bo_formula(r_row)
        sh.range("F" + r_row).value = 10
        book.save()
        self.subt_sort_t4()

    @staticmethod
    def _ince_bo_formula(r_row: str) -> str:
        """焼香順フリガナ自動生成数式を返す。"""
        return (
            "=IF(D{0}<>'',IF(OR(LEFTB(D{0},4)='顧問',LEFTB(D{0},8)='特別焼香',"
            "LEFTB(D{0},8)='友人代表',LEFTB(D{0},10)='葬儀委員長',"
            "LEFTB(D{0},12)='葬儀副委員長',LEFTB(D{0},8)='特別顧問'),"
            "RIGHT(PHONETIC(D{0}),F{0}),LEFT(PHONETIC(D{0}),F{0})),'')".format(r_row)
        )

    def subt_sort_t5(self) -> None:
        """焼香順テーブルをソートする（Excelマクロ実行）。func1.subt_sort_T5 から移植。"""
        book = self._book_b()
        book.activate()
        mf = book.macro('Sheet10.Val3Sort_Click')
        mf()
        book.save()

    # ------------------------------------------------------------------ #
    # 施工状況 (ConstStatus) 操作  ─ sheets[8]                             #
    # ------------------------------------------------------------------ #

    def read_construction_status(self, window) -> None:
        """施工状況データを取得してウィンドウを更新する。func1.get_ConstStatus から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[8]
        sh.activate()

        i001 = sh.range("B2").value
        i002 = sh.range("D2").value
        ia = sh.range("A3").value
        ib = sh.range("A5").value
        ic = sh.range("A6").value
        id_ = sh.range("A10").value
        i1 = sh.range("B3").value
        i2 = sh.range("B5").value
        i3 = sh.range("B6").value
        i4 = sh.range("B10").value
        i5 = sh.range("D3").value
        i6 = sh.range("D5").value
        i7 = sh.range("D6").value
        i8 = sh.range("D10").value

        sh2 = book.sheets[5]
        sh2.activate()
        try:
            o5 = sh2.range('O5').value
            if o5 is not None and int(o5) == 10:
                window['-input02D-'].update(1)
        except Exception:
            pass

        try:
            if i001 is not None:
                window["f021"].update(i001)
            if i002 is not None:
                window['f022'].update(i002)
        except Exception:
            pass

        if ia is not None:
            window["ii01"].update(ia)
            window["ii05"].update(ia)
        if ib is not None:
            window["ii02"].update(ib)
            window["ii06"].update(ib)
        if ic is not None:
            window["ii03"].update(ic)
            window["ii07"].update(ic)
        if id_ is not None:
            window["ii04"].update(id_)
            window["ii08"].update(id_)

        self._upd_num(window, '-input021-', i1)

        if i2 in ('-', '－'):
            window['-input022-'].update("－")
        elif i2 is not None:
            try:
                iv = int(i2)
                window['-input022-'].update(iv)
                window['-input02A-'].update(iv - 1)
                window['-input02B-'].update(iv)
            except (ValueError, TypeError):
                window['-input022-'].update("")
        else:
            window['-input022-'].update("")

        self._upd_num(window, '-input023-', i3)
        self._upd_num(window, '-input024-', i4)
        self._upd_num(window, '-input025-', i5)
        self._upd_num(window, '-input026-', i6)
        self._upd_num(window, '-input027-', i7)
        self._upd_num(window, '-input028-', i8)

    @staticmethod
    def _upd_num(window, key, value):
        """数値フィールドを更新するヘルパー（'-'／'－'対応）。"""
        if value in ('-', '－'):
            window[key].update("－")
        elif value is not None:
            try:
                window[key].update(int(value))
            except (ValueError, TypeError):
                window[key].update("")
        else:
            window[key].update("")

    def save_construction_status(self, values) -> None:
        """施工状況データを保存する。func1.set_ConstStatus から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[8]
        sh.activate()

        sh.range("B3").value = values.get('-input021-')
        sh.range("B5").value = values.get('-input022-')
        sh.range("B6").value = values.get('-input023-')
        sh.range("B10").value = values.get('-input024-')
        sh.range("D3").value = values.get('-input025-')
        sh.range("D5").value = values.get('-input026-')
        sh.range("D6").value = values.get('-input027-')
        sh.range("D10").value = values.get('-input028-')

    # ------------------------------------------------------------------ #
    # 会計・集計操作                                                        #
    # ------------------------------------------------------------------ #

    def subt_first(self) -> None:
        """1次集計処理（通夜集計）。func1.subt_first から移植。"""
        from utils.address_cleaner import clean_addresses_in_book

        book_a = self._book_a()
        book_a.activate()

        # 住所クレンジング（集計マクロの前に実行）
        try:
            n = clean_addresses_in_book(book_a, cpath=self.excel_service._cpath)
            print(f"住所クレンジング完了: {n} 件")
        except Exception as e:
            print(f"住所クレンジングエラー（無視して続行）: {e}")

        mf = book_a.macro('Sheet6.KValuePaste_Click')
        mf()
        book_a.save()

        book_b = self._book_b()
        book_b.activate()
        book_b.sheets[9].select()
        book_b.sheets[9].api.PrintOut(Copies=1)
        book_b.sheets[12].select()
        book_b.sheets[12].api.PrintOut(Copies=1)

    def subt_second(self) -> None:
        """2次集計処理（葬儀集計）。func1.subt_second から移植。"""
        from utils.address_cleaner import clean_addresses_in_book

        book_a = self._book_a()
        book_a.activate()

        # 住所クレンジング（集計マクロの前に実行）
        try:
            n = clean_addresses_in_book(book_a, cpath=self.excel_service._cpath)
            print(f"住所クレンジング完了: {n} 件")
        except Exception as e:
            print(f"住所クレンジングエラー（無視して続行）: {e}")

        ms = book_a.macro('Sheet1.ValSort_Click')
        ms()
        book_a.save()

    def check_bill(self) -> None:
        """領収書チェックを実行する。func1.checkBill から移植。"""
        book_c = self._book_c()
        book_c.activate()

        sh = book_c.sheets[0]
        sh.activate()
        l = sh.range(1001, 9).end('up').row
        sh.range(f"A1:K{l}").select()
        sh.range(f"A1:K{l}").api.AutoFilter(Field=9, Criteria1="=○")
        sh.api.PrintOut(Copies=1)

        sh2 = book_c.sheets[2]
        sh2.activate()
        l = sh2.range(201, 7).end('up').row
        sh2.range(f"A1:G{l}").select()
        sh2.range(f"A1:G{l}").api.AutoFilter(Field=7, Criteria1="=○")
        sh2.api.PrintOut(Copies=1)

    def acc_disp(self) -> None:
        """会計帳を Excel 上に表示する。func1.acc_disp から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets[9]
        sh.activate()
        sh.range("A1").select()

    # ------------------------------------------------------------------ #
    # 印刷・出力操作                                                        #
    # ------------------------------------------------------------------ #

    def show_print_window(self, window) -> None:
        """印刷ウィンドウの各チェックボックスを有効/無効化する。func1.SetPrintVisible から移植。"""
        book_b = self._book_b()
        book_b.activate()

        try:
            sh = book_b.sheets['3.葬儀役員']
            sh.activate()
            a1 = sh.range('C24').value
            b1 = sh.range('F24').value
            if (a1 is None and b1 is None) or int(a1 or 0) + int(b1 or 0) <= 0:
                window['-k3-'].update(disabled=True)
            else:
                window['-k3-'].update(value=True, disabled=False)
        except Exception as e:
            print(f"役員シート確認エラー: {e}")

        try:
            sh = book_b.sheets['6.弔辞弔電a']
            sh.activate()
            t = sh.range('F154').value
            if t is None or int(t) <= 0:
                window['-k6-'].update(disabled=True)
            else:
                window['-k6-'].update(value=True, disabled=False)
        except Exception as e:
            print(f"弔辞弔電シート確認エラー: {e}")

        try:
            sh = book_b.sheets['供物種別表']
            sh.activate()
            a3 = sh.range('M76').value
            if a3 is None or int(a3) <= 0:
                window['-k7-'].update(disabled=True)
                window['-k71-'].update(disabled=True)
                window['filebtn71'].update(disabled=True)
                window['-pic_dir-'].update(disabled=True)
            else:
                window['-k7-'].update(value=True, disabled=False)
                window['-k71-'].update(value=True, disabled=False)
                window['filebtn71'].update(disabled=False)
                window['-pic_dir-'].update(disabled=False)
        except Exception as e:
            print(f"供物シート確認エラー: {e}")

        try:
            sh = book_b.sheets['焼香順入力シート']
            sh.activate()
            a4 = sh.range('I5').value
            if a4 is None or int(a4) <= 2:
                window['-k8-'].update(disabled=True)
            else:
                window['-k8-'].update(value=True, disabled=False)
        except Exception as e:
            print(f"焼香順シート確認エラー: {e}")

        try:
            sh = book_b.sheets['10.供花料']
            sh.activate()
            a5 = sh.range('C224').value
            if a5 is None or int(a5) <= 0:
                window['-k9-'].update(disabled=True)
            else:
                window['-k9-'].update(value=True, disabled=False)
        except Exception as e:
            print(f"供花料シート確認エラー: {e}")

        try:
            book_a = self._book_a()
            book_a.activate()
            sh_a = book_a.sheets['チェック']
            sh_a.activate()
            a11 = sh_a.range('G5').value
            a12 = sh_a.range('G9').value
            if a11 is None or a12 is None or int(a11 or 0) + int(a12 or 0) <= 0:
                window['-k1A-'].update(disabled=True)
                window['-k1C-'].update(disabled=True)
                window['-k250-'].update(disabled=True)
            else:
                window['-k1A-'].update(value=True, disabled=False)
                window['-k1C-'].update(value=True, disabled=False)
                window['-k250-'].update(disabled=False)
        except Exception as e:
            print(f"チェックシート確認エラー: {e}")

    def chk_on_print(self, values: dict) -> None:
        """チェックボックスに応じて Excel シートを印刷する。func1.chk_on_print から移植。"""
        book_b = self._book_b()
        book_b.activate()

        if values.get('-k1-'):
            book_b.sheets[4].select()
            book_b.sheets[4].api.PrintOut(Copies=1)
            book_b.sheets[5].select()
            book_b.sheets[5].api.PrintOut(Copies=1)

        if values.get('-k3-'):
            book_b.sheets[7].select()
            book_b.sheets[7].api.PrintOut(Copies=1)

        if values.get('-k4-'):
            book_b.sheets[8].select()
            book_b.sheets[8].api.PrintOut(Copies=1)

        if values.get('-k5-'):
            book_b.sheets[9].select()
            book_b.sheets[9].api.PrintOut(Copies=1)

        if values.get('-k6-'):
            book_b.sheets[10].select()
            book_b.sheets[10].api.PrintOut(Copies=1)

        if values.get('-k7-'):
            book_b.sheets[13].select()
            book_b.sheets[13].api.PrintOut(Copies=1)

        if values.get('-k71-'):
            p_a = values.get('-inputd1-', r'C:\vix221\ViX.exe')
            cpath = self.file_service.get_current_path()
            dist = os.path.join(cpath, config.CDPATH, '供物等写真')
            os.makedirs(dist, exist_ok=True)
            pic_dir = values.get('-pic_dir-')
            if pic_dir:
                for f in _glob.glob(os.path.join(pic_dir, '*.jpg')):
                    try:
                        shutil.copy(f, dist)
                    except (FileNotFoundError, OSError):
                        pass
            subprocess.run(f'"{p_a}" /root "{dist}" /select "{dist}\\*.jpg"', shell=True)

        if values.get('-k8-'):
            book_b.sheets[14].select()
            book_b.sheets[14].api.PrintOut(Copies=1)

        if values.get('-k9-'):
            book_b.sheets[15].select()
            book_b.sheets[15].api.PrintOut(Copies=1)
            book_b.sheets[16].select()
            book_b.sheets[16].api.PrintOut(Copies=1)

        book_a = self._book_a()
        book_a.activate()

        if values.get('-k1A-'):
            book_a.sheets[6].activate()
            book_a.sheets[6].api.PrintOut(Copies=1)
            book_a.sheets[4].activate()
            book_a.sheets[4].api.PrintOut(Copies=1)

        if values.get('-k1C-'):
            book_a.sheets[0].activate()
            book_a.sheets[0].api.PrintOut(Copies=1)
            book_a.sheets[3].activate()
            book_a.sheets[3].api.PrintOut(Copies=1)

    def create_cd(self, values) -> bool:
        """CD 用データを作成する。func1.createcd から移植。"""
        cpath = self.file_service.get_current_path()
        if not cpath:
            raise RuntimeError("現在のパスが設定されていません")

        # ── bookA を保存・閉じる ──────────────────────────────────────────
        book_a = self._book_a()
        book_a.activate()
        book_a.save()
        book_a.close()
        self.excel_service.current_book_a = None
        self.excel_service.current_sheet_a = None
        self.excel_service.workbooks.pop(os.path.join(cpath, config.XLBOOK_A), None)

        # ── bookB を保存・閉じる ──────────────────────────────────────────
        book_b = self._book_b()
        book_b.activate()
        book_b.save()
        book_b.close()
        self.excel_service.current_book_b = None
        self.excel_service.current_sheet_b1 = None
        self.excel_service.current_sheet_b2 = None
        self.excel_service.current_sheet_b3 = None
        self.excel_service.workbooks.pop(os.path.join(cpath, config.XLBOOK_B), None)

        # ── bookC: マクロ実行 → 値貼り付け → xlsx として保存 ─────────────
        book_c = self._book_c()
        book_c.activate()

        try:
            mp1 = book_c.macro("ThisWorkbook.ConvertToZip()")
            mp1()
        except Exception as e:
            print(f"マクロ ConvertToZip 実行エラー（無視）: {e}")

        book_c.sheets[0].activate()
        book_c.sheets[0].range("A1:J1001").copy()
        book_c.sheets[0].range("A1:J1001").paste(paste='values_and_number_formats')

        book_c.sheets[1].activate()
        book_c.sheets[1].range("A1:E201").copy()
        book_c.sheets[1].range("A1:E201").paste(paste='values_and_number_formats')

        book_c.activate()
        book_c.sheets[2].activate()
        book_c.sheets[2].range("A1:G201").copy()
        book_c.sheets[2].range("A1:G201").paste(paste='values_and_number_formats')

        time.sleep(5)

        fullpath_x = os.path.join(cpath, "葬儀データA.xlsx")
        book_c.save(fullpath_x)
        book_c.close()
        self.excel_service.current_book_c = None
        self.excel_service.current_sheet_c = None
        self.excel_service.workbooks.pop(os.path.join(cpath, config.XLBOOK_C), None)

        # ── win32com で xlsx を開き xls (FileFormat=56) として保存 ─────────
        fullpath_s  = os.path.join(cpath, "葬儀データA.xls")
        fullpath_lx = os.path.join(cpath, "葬儀データA_2007.lnk")
        fullpath_ls = os.path.join(cpath, "葬儀データA_2003.lnk")

        import win32com.client as _win32
        excel = _win32.Dispatch('Excel.Application')
        excel.Visible = True
        excel.DisplayAlerts = False
        try:
            wb = excel.Workbooks.Open(Filename=fullpath_x)
            wb.DoNotPromptForConvert = False
            wb.CheckCompatibility = False
            wb.Worksheets(1).Activate()
            wb.SaveAs(Filename=fullpath_s, FileFormat=56)
            time.sleep(5)
            wb.Close(SaveChanges=False)
        finally:
            excel.DisplayAlerts = True
            excel.Application.Quit()

        # ── CD用フォルダへ移動 ──────────────────────────────────────────
        cd_dir = os.path.join(cpath, config.CDPATH)
        os.makedirs(cd_dir, exist_ok=True)

        shutil.move(fullpath_x, os.path.join(cd_dir, "葬儀データA.xlsx"))
        shutil.move(fullpath_s, os.path.join(cd_dir, "葬儀データA.xls"))

        # ── ショートカット作成（失敗しても続行）──────────────────────────
        self._create_shortcut(os.path.join(cd_dir, "葬儀データA.xlsx"), fullpath_lx)
        self._create_shortcut(os.path.join(cd_dir, "葬儀データA.xls"),  fullpath_ls)

        # ── ISO 作成 → CD 書き込み ───────────────────────────────────────
        self._write_cd(cd_dir)
        return True

    # ------------------------------------------------------------------ #
    # CD 書き込みヘルパー                                                  #
    # ------------------------------------------------------------------ #

    def _get_cd_drives(self) -> list:
        """システム上の CD/DVD ドライブを検出して返す。"""
        drives = []
        try:
            import win32api
            import win32file
            for letter in win32api.GetLogicalDriveStrings().split('\x00')[:-1]:
                try:
                    if win32file.GetDriveType(letter) == 5:
                        vol = win32api.GetVolumeInformation(letter)[0]
                        drives.append((letter.rstrip('\\'), vol or "CD/DVDドライブ"))
                except Exception:
                    continue
        except ImportError:
            try:
                import ctypes
                for c in 'DEFGHIJKLMNOPQRSTUVWXYZ':
                    if ctypes.windll.kernel32.GetDriveTypeW(f"{c}:\\") == 5:
                        drives.append((f"{c}:", "CD/DVDドライブ"))
            except Exception:
                pass
        return drives or [("D:", "CD/DVDドライブ")]

    def _get_iso_label(self) -> str:
        """ISO ボリュームラベルを生成する（日付 + 遺族名）。"""
        cpath = self.file_service.get_current_path()
        last = cpath.split("\\")[-1] if cpath else ""
        family = "".join(c for c in last if not c.isdigit())
        today = datetime.datetime.now().strftime("%y%m%d")
        return (today + family)[:16]

    def _write_cd(self, cd_dir: str) -> None:
        """oscdimg で ISO を作成し ImgBurn で DVD に書き込む。"""
        cpath = self.file_service.get_current_path()
        iso_path = os.path.join(cpath, "info.iso")
        iname = self._get_iso_label()

        oscdimg = (r"C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit"
                   r"\Deployment Tools\amd64\Oscdimg\oscdimg.exe")
        imgburn = r"C:\Program Files (x86)\ImgBurn\ImgBurn.exe"

        if not os.path.exists(oscdimg):
            raise FileNotFoundError(f"oscdimg.exe が見つかりません:\n{oscdimg}")

        cmd_iso = f'"{oscdimg}" -d -k -n -l"{iname}" "{cd_dir}" "{iso_path}"'
        result = subprocess.run(cmd_iso, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ISO ファイル作成に失敗しました:\n{result.stderr}")

        if not os.path.exists(imgburn):
            raise FileNotFoundError(f"ImgBurn.exe が見つかりません:\n{imgburn}")

        drive = self._get_cd_drives()[0][0]
        cmd_burn = (f'"{imgburn}" /MODE WRITE /SRC "{iso_path}" /DEST {drive}'
                    f' /START /EJECT YES /COPIES 1 /VERIFY YES /CLOSE')
        subprocess.run(cmd_burn, shell=True)

    def _create_shortcut(self, target_file: str, link_file: str) -> None:
        """Windows ショートカット (.lnk) を作成する。"""
        try:
            import comtypes.client
            wsh = comtypes.client.CreateObject("wScript.Shell", dynamic=True)
            sc = wsh.CreateShortcut(link_file)
            sc.TargetPath = target_file
            sc.Save()
        except Exception as e:
            print(f"ショートカット作成エラー（無視）: {e}")

    def print_a01(self) -> None:
        """水引御布施（導師）を印刷する。func1.printA01 から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets['水引御布施 (導師)']
        sh.activate()
        sh.select()
        sh.page_setup.print_area = None
        sh.page_setup.print_area = '$A$1:$M$82'
        sh.page_setup.Zoom = False
        sh.page_setup.FitToPagesWide = 1
        sh.page_setup.FitToPagesTall = 1
        sh.api.PrintOut(Copies=1)

    def print_a02(self) -> None:
        """水引御布施・院号料ほかを印刷する。func1.printA02 から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets['水引御布施・院号料ほか']
        sh.activate()
        sh.select()
        sh.page_setup.print_area = None
        sh.page_setup.print_area = '$A$1:$M$82'
        sh.page_setup.Zoom = False
        sh.page_setup.FitToPagesWide = 1
        sh.page_setup.FitToPagesTall = 1
        sh.api.PrintOut(Copies=1)

    def print_a03(self) -> None:
        """御足袋料を印刷する。func1.printA03 から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets['御足袋料']
        sh.activate()
        sh.select()
        sh.api.PrintOut(Copies=1)

    def print_a04(self) -> None:
        """御車代を印刷する。func1.printA04 から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets['御車代']
        sh.activate()
        sh.select()
        sh.api.PrintOut(Copies=1)

    def print_a05(self, flag: bool = False) -> None:
        """新亡供養料（禅徳寺）を印刷する。func1.printA05 から移植。"""
        if flag:
            book = self._book_b()
            book.activate()
            sh = book.sheets['新亡供養料(禅徳寺)']
            sh.activate()
            sh.select()
            sh.api.PrintOut(Copies=1)

    def print_a06(self, hyoudai1: str, tadasi: str) -> None:
        """寸志他（白無地封筒）を印刷する。func1.printA06 から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets['寸志他']
        sh.activate()
        sh.range('G2').value = hyoudai1
        sh.range('G3').value = tadasi
        sh.select()
        sh.api.PrintOut(Copies=1)

    def print_a07(self, hyoudai2: str) -> None:
        """水引（水引付封筒）を印刷する。func1.printA07 から移植。"""
        book = self._book_b()
        book.activate()
        sh = book.sheets['水引']
        sh.activate()
        sh.range('P2').value = hyoudai2
        sh.select()
        sh.page_setup.print_area = None
        sh.page_setup.print_area = '$A$1:$M$82'
        sh.page_setup.Zoom = False
        sh.page_setup.FitToPagesWide = 1
        sh.page_setup.FitToPagesTall = 1
        sh.api.PrintOut(Copies=1)

    # ------------------------------------------------------------------ #
    # 詳細設定（未移植）                                                     #
    # ------------------------------------------------------------------ #

    def make_detail_settings(self, event, values, x=None, y=None):
        """詳細設定ウィンドウを表示してメインウィンドウを返す。"""
        raise NotImplementedError("make_detail_settings の移植が必要です")
