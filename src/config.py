"""
アプリケーション設定定数
global_value.py から移行した静的定数を一元管理する
"""
import os
import sys

def _get_app_root() -> str:
    """exe (PyInstaller frozen) でも .py スクリプトでも正しいアプリルートを返す"""
    if getattr(sys, 'frozen', False):
        # PyInstaller でバンドルされた場合: exe があるフォルダ
        return os.path.dirname(sys.executable)
    else:
        # 通常の Python 実行: src/config.py の2階層上 = プロジェクトルート
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_ROOT = _get_app_root()

# config.ini のパス（アプリルート直下）
CONFIG_INI = os.path.join(APP_ROOT, 'config.ini')

# ----- Excel ファイル名 -----
XLBOOK_A = '合体香典帳v8.xlsm'
XLBOOK_B = '新書類１式v8.xlsm'
XLBOOK_C = '葬儀データ1.xlsm'

# ----- XLBOOK_A シート名 -----
XLBOOK_A_SHEET_I11 = '1～1000'
XLBOOK_A_SHEET_O12 = 'A.御香典帳'
XLBOOK_A_SHEET_O13 = 'B.1～1000(清書用)'
XLBOOK_A_SHEET_O14 = 'C.香典帳'
XLBOOK_A_SHEET_O15 = 'D.temp2'
XLBOOK_A_SHEET_O16 = 'チェック'

# ----- XLBOOK_B シート名 -----
XLBOOK_B_SHEET_I01 = '供物入力シート'
XLBOOK_B_SHEET_I02 = '供物種別表'
XLBOOK_B_SHEET_I03 = '焼香順入力シート'
XLBOOK_B_SHEET_I04 = '役員シート'
XLBOOK_B_SHEET_I05 = '1.御葬儀記録書'
XLBOOK_B_SHEET_I06 = '2.葬儀施行要領'
XLBOOK_B_SHEET_O07 = '3.葬儀役員'
XLBOOK_B_SHEET_I08 = '4､通夜葬儀'
XLBOOK_B_SHEET_I09 = '5.会計帳'
XLBOOK_B_SHEET_I10 = '6.弔辞弔電a'
XLBOOK_B_SHEET_O11 = '7.供物'
XLBOOK_B_SHEET_O12 = '8.焼香順'
XLBOOK_B_SHEET_O13 = '9.供花料表紙'
XLBOOK_B_SHEET_I14 = '10.供花料'
XLBOOK_B_SHEET_I21 = '水引御布施 (導師)'
XLBOOK_B_SHEET_I22 = '水引御布施・院号料ほか'
XLBOOK_B_SHEET_I23 = '御足袋料'
XLBOOK_B_SHEET_I24 = '御車代'
XLBOOK_B_SHEET_I25 = '新亡供養料(禅徳寺)'
XLBOOK_B_SHEET_I26 = '寸志他'
XLBOOK_B_SHEET_I27 = '水引'

# ----- XLBOOK_C シート名 -----
XLBOOK_C_SHEET_I01 = '香典'

# ----- パス関連 -----
# USB対応: exe/スクリプト横の data フォルダをデフォルト作業ルートとする
BASE_PATH = os.path.join(APP_ROOT, 'data')

# ----- フォルダ名 -----
TPATH1 = '初期テンプレート'
TPATH2 = '最新'
TPATH3 = '終了分'
CDPATH = 'CD用'

# ----- 香典入力設定 -----
MAX_VAL = 1000
DEFAULT_STEP = 20
