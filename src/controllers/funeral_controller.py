"""
葬儀情報コントローラー
葬儀情報入力機能を管理
"""
import TkEasyGUI as sg
import os
import config
from controllers.base_controller import BaseController
from models.funeral_model import FuneralModel
from views.funeral_layout import get_funeral_layout
from utils.calendar_utils import cal_calendar

class FuneralController(BaseController):
    """葬儀情報入力機能のコントローラー"""
    
    def __init__(self, window):
        super().__init__(window)
        self.funeral_model = FuneralModel()
    
    def handle_basic_info_input(self, values):
        """基本情報・施工情報入力ボタンが押された時の処理"""
        print("基本情報・施工情報入力ボタンが押されました")
        
        # 基本情報・施工情報入力ウィンドウを作成（元のプログラムの方式）
        window_basic = sg.Window('基本情報・施工情報入力', get_funeral_layout(), finalize=True)

        # Excelファイルを開く（エラーが発生してもウィンドウは表示）
        try:
            cpath = self.data_service.file_service.get_current_path()
            excel_path = os.path.join(cpath, config.XLBOOK_B)
            print(f"Opening Excel file: {excel_path}")
            if not os.path.exists(excel_path):
                print(f"Excelファイルが見つかりません：{excel_path}")
                self.show_error(f"Excelファイルが見つかりません：\n{excel_path}")
                window_basic.close()
                self.window.un_hide()
                return False

            # 既存のデータを読み込む
            self.data_service.excel_service.read_funeral_info1(window_basic)
            print("Data read from sheet 1 successfully")

            self.data_service.excel_service.read_funeral_info2(window_basic)
            print("Data read from sheet 2 successfully")

        except Exception as e:
            cpath = self.data_service.file_service.get_current_path()
            error_msg = (
                f"Excelファイルの読み込みに失敗しました。\n"
                f"パス: {cpath}\n"
                f"ファイル: {config.XLBOOK_B}\n"
                f"エラー: {str(e)}"
            )
            print(error_msg)
            self.show_error(error_msg)
            window_basic.close()
            self.window.un_hide()
            return False
        
        # 基本情報・施工情報入力ウィンドウのイベントループ（元のプログラムの方式）
        while True:
            event_basic, values_basic = window_basic.read()
            
            if event_basic == sg.WIN_CLOSED or event_basic == '-Close-':
                break
            elif event_basic == '-su23-':
                print("情報を設定するボタンが押されました")
                self.data_service.excel_service.save_funeral_info1(values_basic)
                self.data_service.excel_service.save_funeral_info2(values_basic)
                self.show_success("データを保存しました")
            elif event_basic in ['-ccal1-', '-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']:
                print(f"カレンダーボタン {event_basic} が押されました")
                # カレンダー処理
                self._handle_calendar_event(window_basic, values_basic, event_basic)
        
        # 基本情報・施工情報入力ウィンドウを閉じる
        window_basic.close()
        
        return True
    
    def handle_funeral_data_save(self, values):
        """葬儀データの保存処理"""
        print("葬儀データの保存処理")
        
        try:
            # 入力データをモデルに設定
            self._update_funeral_model_from_values(values)
            
            # バリデーション
            errors = self.funeral_model.validate()
            if errors:
                error_msg = "以下の項目にエラーがあります:\\n" + "\\n".join(errors)
                self.show_error(error_msg)
                return False
            
            # データを保存
            self.data_service.excel_service.save_funeral_info1(values)
            self.data_service.excel_service.save_funeral_info2(values)
            
            self.show_success("葬儀情報を保存しました。")
            return True
            
        except Exception as e:
            self.show_error(f"葬儀データの保存に失敗しました。\\n{str(e)}")
            return False
    
    def _update_funeral_model_from_values(self, values):
        """入力値から葬儀モデルを更新"""
        # 故人情報
        self.funeral_model.deceased_name = values.get('-deceased_name-', '')
        self.funeral_model.deceased_furigana = values.get('-deceased_furigana-', '')
        self.funeral_model.birth_date = values.get('-birth_date-', '')
        self.funeral_model.death_date = values.get('-death_date-', '')
        self.funeral_model.age = int(values.get('-age-', 0)) if values.get('-age-', 0) else 0
        
        # 遺族情報
        self.funeral_model.family_name = values.get('-family_name-', '')
        self.funeral_model.family_furigana = values.get('-family_furigana-', '')
        
        # 寺院情報
        self.funeral_model.temple_name = values.get('-temple_name-', '')
        self.funeral_model.temple_address = values.get('-temple_address-', '')
        self.funeral_model.temple_phone = values.get('-temple_phone-', '')
        
        # 会場情報
        self.funeral_model.venue_name = values.get('-venue_name-', '')
        self.funeral_model.venue_address = values.get('-venue_address-', '')
        self.funeral_model.venue_phone = values.get('-venue_phone-', '')
        
        # 日時情報
        self.funeral_model.overnight_date = values.get('-overnight_date-', '')
        self.funeral_model.funeral_date = values.get('-funeral_date-', '')
        self.funeral_model.departure_date = values.get('-departure_date-', '')
        
        # 火葬場情報
        self.funeral_model.crematory_name = values.get('-crematory_name-', '')
        self.funeral_model.crematory_address = values.get('-crematory_address-', '')
        self.funeral_model.crematory_phone = values.get('-crematory_phone-', '')
        
        # 備考
        self.funeral_model.notes = values.get('-notes-', '')
        
        # 年齢を自動計算
        self.funeral_model.update_age()
    
    def _handle_calendar_event(self, window_basic, values, event):
        """カレンダーイベントの処理"""
        print(f"カレンダーイベント: {event}")
        
        try:
            # カレンダーダイアログを表示して日付を取得
            if event in ['-ccal1-', '-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']:
                # 対応する日付入力フィールドのキーを取得（gui02.pyの実際のキー名を使用）
                date_key_map = {
                    '-ccal1-': '-r_date-',  # 故人生年月日
                    '-ccal2-': '-s_date-',  # 死亡日時
                    '-ccal3-': '-day1_date-',  # 施工日時：通夜
                    '-ccal4-': '-day2_date-',  # 施工日時：葬儀
                    '-ccal5-': '-day3_date-'   # 施工日時：出棺
                }
                display_key = date_key_map[event]
                print(f"対象キー: {display_key}")
                
                # キーの存在確認
                try:
                    current_value = window_basic[display_key].get()
                    print(f"現在の値: '{current_value}'")
                except Exception as key_error:
                    print(f"❌ キー '{display_key}' が存在しません: {str(key_error)}")
                    self.show_error(f"日付入力フィールド '{display_key}' が見つかりません。\\nレイアウトを確認してください。")
                    return
                
                # カレンダーダイアログを表示（元のmain00.pyと同じ実装）
                try:
                    print(f"カレンダーダイアログを表示中... (時間指定: {event in ['-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']})")
                    if event in ['-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']:  # 時間指定あり
                        cal_calendar(window_basic, values, display_key, True)
                    else:  # 時間指定なし
                        cal_calendar(window_basic, values, display_key, False)
                    
                except Exception as calendar_error:
                    print(f"❌ カレンダーダイアログエラー: {str(calendar_error)}")
                    import traceback
                    traceback.print_exc()
                    self.show_error(f"カレンダーダイアログでエラーが発生しました。\\n{str(calendar_error)}")
                    return
                
                # 故人の生年月日が入力されている場合、年齢を計算
                if event == '-ccal2-':  # 死亡日時の場合
                    self._update_age_calculation_from_window(window_basic)
                    
        except Exception as e:
            print(f"カレンダー入力エラー: {str(e)}")
            import traceback
            traceback.print_exc()
            self.show_error(f"カレンダー入力でエラーが発生しました。\\n{str(e)}")
    
    def _update_age_calculation_from_window(self, window_basic):
        """年齢計算の更新（ウィンドウ指定版）"""
        try:
            birth_date_str = window_basic['-r_date-'].get()  # 故人生年月日
            death_date_str = window_basic['-s_date-'].get()  # 死亡日時
            
            if birth_date_str and death_date_str:
                # 年齢を計算して表示
                self.funeral_model.birth_date = birth_date_str
                self.funeral_model.death_date = death_date_str
                self.funeral_model.update_age()
                
                if self.funeral_model.age > 0:
                    window_basic['-syear2-'].update(str(self.funeral_model.age))  # 享年・行年の入力欄
                    
        except Exception as e:
            print(f"年齢計算エラー: {str(e)}")
    
    def handle_calendar_event(self, event, values):
        """カレンダーイベントの処理（互換性のため）"""
        print(f"カレンダーイベント: {event}")
        
        try:
            # カレンダーダイアログを表示して日付を取得
            if event in ['-ccal1-', '-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']:
                # 対応する日付入力フィールドのキーを取得
                date_key_map = {
                    '-ccal1-': '-birth_date-',  # 生年月日
                    '-ccal2-': '-death_date-',  # 死亡日時
                    '-ccal3-': '-overnight_date-',  # 通夜日時
                    '-ccal4-': '-funeral_date-',  # 葬儀日時
                    '-ccal5-': '-departure_date-'   # 出棺日時
                }
                display_key = date_key_map[event]
                
                # カレンダーダイアログを表示
                if event in ['-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']:  # 時間指定あり
                    cal_calendar(self.window, values, display_key, True)
                else:  # 時間指定なし
                    cal_calendar(self.window, values, display_key, False)
                
                # 故人の生年月日が入力されている場合、年齢を計算
                if event == '-ccal2-':  # 死亡日時の場合
                    self._update_age_calculation()
                    
        except Exception as e:
            print(f"カレンダー入力エラー: {str(e)}")
            self.show_error(f"カレンダー入力でエラーが発生しました。\\n{str(e)}")
    
    def _update_age_calculation(self):
        """年齢計算の更新"""
        try:
            birth_date_str = self.window['-birth_date-'].get()
            death_date_str = self.window['-death_date-'].get()
            
            if birth_date_str and death_date_str:
                # 年齢を計算して表示
                self.funeral_model.birth_date = birth_date_str
                self.funeral_model.death_date = death_date_str
                self.funeral_model.update_age()
                
                if self.funeral_model.age > 0:
                    self.window['-age-'].update(str(self.funeral_model.age))
                    
        except Exception as e:
            print(f"年齢計算エラー: {str(e)}")
    
    def handle_funeral_events(self, event, values):
        """葬儀関連のイベント処理"""
        if event == '-su23-':  # 情報を設定するボタン
            self.handle_funeral_data_save(values)
        elif event in ['-ccal1-', '-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']:
            self.handle_calendar_event(event, values)
        elif event == '-birth_date-':  # 生年月日変更時
            self._update_age_calculation()
        elif event == '-death_date-':  # 死亡日時変更時
            self._update_age_calculation()