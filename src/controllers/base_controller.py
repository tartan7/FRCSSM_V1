"""
ベースコントローラークラス
すべてのコントローラーの基底クラス
"""
import TkEasyGUI as sg
from services.data_service import DataService

class BaseController:
    """すべてのコントローラーの基底クラス"""
    
    def __init__(self, window):
        self.window = window
        self.current_values = {}
        self.data_service = DataService()
    
    def update_values(self, values):
        """現在の値を更新"""
        self.current_values = values
    
    def show_error(self, message, title="エラー"):
        """エラーメッセージを表示"""
        sg.popup_error(message, title=title)
    
    def show_success(self, message, title="成功"):
        """成功メッセージを表示"""
        sg.popup(message, title=title)
    
    def show_confirm(self, message, title="確認"):
        """確認ダイアログを表示"""
        return sg.popup_ok_cancel(message, title=title)
    
    def close_excel_safely(self):
        """Excelファイルを安全に終了"""
        try:
            self.data_service.cleanup()
        except Exception as e:
            print(f"Excel終了処理中にエラーが発生: {str(e)}")
    
    def switch_window(self, new_layout, title="新規ウィンドウ", use_hide=False):
        """ウィンドウを切り替え（元のプログラムの方式に合わせる）"""
        try:
            # 現在のウィンドウを処理
            if self.window:
                if use_hide:
                    # 香典入力の場合は非表示にする（元のプログラムの方式）
                    self.window.hide()
                else:
                    # その他の場合は閉じる（元のプログラムの方式）
                    self.window.close()
            
            # 新しいウィンドウを作成（元のプログラムと同じパラメータ）
            self.window = sg.Window(title, new_layout,
                                  location=(10, 10),
                                  alpha_channel=1.0,
                                  no_titlebar=False,
                                  grab_anywhere=False,
                                  finalize=True)
            return self.window
        except Exception as e:
            print(f"ウィンドウ切り替え中にエラーが発生: {str(e)}")
            return None