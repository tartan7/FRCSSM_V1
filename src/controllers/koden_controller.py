"""
香典入力コントローラー
香典入力機能を管理
"""
import TkEasyGUI as sg
import pykakasi
import unicodedata
import config
from controllers.base_controller import BaseController
from views.koden_layout import get_koden_layout

class KodenController(BaseController):
    """香典入力機能のコントローラー"""
    
    def __init__(self, window):
        super().__init__(window)
        self.current_no = 1
    
    def handle_koden_input(self, values):
        """香典入力ボタンが押された時の処理"""
        print("香典入力ボタンが押されました")
        
        # Excelファイルを開く
        try:
            self.data_service.excel_service.get_koden_workbook()
        except Exception as e:
            self.show_error(f"Excelファイルの読み込みに失敗しました。\\n{str(e)}")
            return False

        # 香典入力ウィンドウを作成（元のプログラムの方式）
        window_koden = sg.Window('香典入力', get_koden_layout(), finalize=True)

        # 初期データの読み込み
        self.current_no = 1
        window_koden['-i_no-'].update(str(self.current_no))
        self.data_service.excel_service.load_koden_into_window(self.current_no, window_koden)
        
        # 香典入力ウィンドウのイベントループ（元のプログラムの方式）
        while True:
            event_koden, values_koden = window_koden.read()
            
            if event_koden == sg.WIN_CLOSED or event_koden == '-Close-':
                break
            elif event_koden == '-Update_Prev-':
                self._handle_update_prev(window_koden, values_koden)
            elif event_koden == '-Update_Next-':
                self._handle_update_next(window_koden, values_koden)
            elif event_koden == '-no_btn-':
                self._handle_no_change(window_koden, values_koden)
            elif event_koden == '-rng_btn-':
                self._handle_range_change(window_koden, values_koden)
            elif event_koden == '-bunch-':
                self._handle_bunch_change(window_koden, values_koden)
            elif event_koden == '-i_name-':
                self._handle_name_change(window_koden, values_koden)
            elif event_koden == '-i_address-':
                self._handle_address_change(window_koden, values_koden)
            elif event_koden == '-Om1-':
                print("別紙(Word)ボタンが押されました")
            elif event_koden == '-Om2-':
                print("別紙(Excel)ボタンが押されました")
        
        # 香典入力ウィンドウを閉じる
        window_koden.close()
        
        return True
    
    def _handle_koden_window(self, window_koden):
        """香典入力ウィンドウのイベント処理"""
        while True:
            event_koden, values_koden = window_koden.read()
            
            if event_koden == sg.WIN_CLOSED or event_koden == '-Close-':
                break
            elif event_koden == '-Update_Prev-':
                self._handle_update_prev(window_koden, values_koden)
            elif event_koden == '-Update_Next-':
                self._handle_update_next(window_koden, values_koden)
            elif event_koden == '-no_btn-':
                self._handle_no_change(window_koden, values_koden)
            elif event_koden == '-rng_btn-':
                self._handle_range_change(window_koden, values_koden)
            elif event_koden == '-bunch-':
                self._handle_bunch_change(window_koden, values_koden)
            elif event_koden == '-i_name-':
                self._handle_name_change(window_koden, values_koden)
            elif event_koden == '-i_address-':
                self._handle_address_change(window_koden, values_koden)
            elif event_koden == '-Om1-':
                print("別紙(Word)ボタンが押されました")
            elif event_koden == '-Om2-':
                print("別紙(Excel)ボタンが押されました")
    
    def _handle_update_prev(self, window_koden, values):
        """更新・前へボタンの処理"""
        print("更新・前へボタンが押されました")
        self.data_service.excel_service.save_koden_from_window(window_koden, values)
        self.current_no = int(values['-i_no-']) - 1
        if self.current_no < 1:
            self.current_no = 1
        window_koden['-i_no-'].update(str(self.current_no))
        self.data_service.excel_service.load_koden_into_window(self.current_no, window_koden)
        window_koden['-i_price-'].focus_set()

    def _handle_update_next(self, window_koden, values):
        """更新・次へボタンの処理"""
        print("更新・次へボタンが押されました")
        self.data_service.excel_service.save_koden_from_window(window_koden, values)
        self.current_no = int(values['-i_no-']) + 1
        window_koden['-i_no-'].update(str(self.current_no))
        self.data_service.excel_service.load_koden_into_window(self.current_no, window_koden)
        window_koden['-i_price-'].focus_set()

    def _handle_no_change(self, window_koden, values):
        """No変更の処理"""
        print("Noが変更されました")
        new_no = int(values['-no_btn-'])
        old_no = int(values['-i_no-'])

        if old_no == new_no:
            return

        self.data_service.excel_service.save_koden_from_window(window_koden, values)
        window_koden['-i_no-'].update(str(new_no))
        self.data_service.excel_service.load_koden_into_window(new_no, window_koden)
        window_koden['-i_price-'].focus_set()
    
    def _handle_range_change(self, window_koden, values):
        """範囲変更の処理"""
        start_no = values['-rng_btn-']
        window_koden['-start_range-'].update(start_no)
        step_a = int(config.DEFAULT_STEP) - 1
        window_koden['-end_range-'].update(str(int(start_no) + int(step_a)))
        window_koden['-i_no-'].update(str(start_no))
        window_koden['-no_btn-'].update(str(start_no))
        self.data_service.excel_service.load_koden_into_window(start_no, window_koden)
        window_koden['-i_price-'].focus_set()
    
    def _handle_bunch_change(self, window_koden, values):
        """束単位変更の処理"""
        print("束単位が変更されました")
        stp = int(values['-bunch-'])
        v = [i for i in range(1, config.MAX_VAL, stp)]
        window_koden['-rng_btn-'].update(values=v)

        current_val = int(values['-rng_btn-'])
        if current_val not in v:
            nearest_val = min(v, key=lambda x: abs(x - current_val))
            window_koden['-rng_btn-'].update(value=nearest_val)
            window_koden['-start_range-'].update(nearest_val)
            step_a = int(config.DEFAULT_STEP) - 1
            window_koden['-end_range-'].update(str(int(nearest_val) + int(step_a)))
            window_koden['-i_no-'].update(str(nearest_val))
            window_koden['-no_btn-'].update(nearest_val)
            self.data_service.excel_service.load_koden_into_window(nearest_val, window_koden)
    
    def _handle_name_change(self, window_koden, values):
        """名前変更時のフリガナ自動変換"""
        text = values['-i_name-']
        kks = pykakasi.kakasi()
        result = kks.convert(text)
        rea = ''
        for item in result:
            rea = rea + item['kana']
        window_koden['-i_furigana-'].update(rea)
    
    def _handle_address_change(self, window_koden, values):
        """住所変更時の正規化"""
        text = values['-i_address-']
        t = unicodedata.normalize('NFKC', text)
        window_koden['-i_address-'].update(t)