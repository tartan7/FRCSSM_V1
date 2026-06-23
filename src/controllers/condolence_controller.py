"""
弔辞弔電入力コントローラー
弔辞弔電入力画面の処理を管理
"""
import TkEasyGUI as sg
from controllers.base_controller import BaseController
from models.condolence_model import CondolenceModel

class CondolenceController(BaseController):
    """弔辞弔電入力のコントローラー"""
    
    def __init__(self, window):
        super().__init__(window)
        self.condolence_data = []  # 弔辞弔電データのリスト
        self.current_condolence = None  # 現在編集中の弔辞弔電
    
    def handle_condolence_input(self, values):
        """弔辞弔電入力ボタンが押された時の処理"""
        print("弔辞弔電入力ボタンが押されました")
        
        # ウィンドウを切り替える（元のプログラムの方式）
        self.window = self.switch_window(
            self._create_condolence_input_layout(),
            '弔辞弔電入力',
            use_hide=False  # 元のプログラムでは close() を使用
        )
        
        # ウィンドウの切り替えが成功したかチェック
        if not self.window:
            print("ウィンドウの切り替えに失敗しました")
            return False
        
        # Excelファイルを開く
        try:
            self.data_service.excel_service.get_condolence_workbook()
        except Exception as e:
            print(f"Excelファイルの読み込みに失敗: {str(e)}")
            self.show_error(f"Excelファイルの読み込みに失敗しました。\\n{str(e)}")
            return True  # ウィンドウは表示されたのでTrueを返す
        
        return True
    
    def _open_condolence_input_window(self):
        """弔辞弔電入力画面を開く"""
        # 弔辞弔電入力画面のレイアウトを作成
        layout = self._create_condolence_input_layout()
        
        # ウィンドウを作成
        condolence_window = sg.Window(
            '弔辞弔電入力',
            layout,
            modal=True,
            finalize=True
        )
        
        # イベントループ
        while True:
            event, values = condolence_window.read()
            
            if event == sg.WIN_CLOSED:
                break
            elif event == 'btn_save':
                self._save_condolence_data(condolence_window, values)
            elif event == 'btn_clear':
                self._clear_condolence_data(condolence_window)
            elif event == 'btn_delete':
                self._delete_condolence_data(condolence_window, values)
            elif event == 'btn_exit':
                break
        
        # ウィンドウを閉じる
        condolence_window.close()
        
        # メインウィンドウを再表示
        self.window.un_hide()
    
    def _create_condolence_input_layout(self):
        """弔辞弔電入力画面のレイアウトを作成"""
        return [
            [sg.Text('弔辞弔電入力', font=('Arial', 16, 'bold'))],
            [sg.HSeparator()],
            [sg.Text('番号:'), sg.Input(key='condolence_number', size=(10, 1))],
            [sg.Text('会社名:'), sg.Input(key='condolence_company', size=(30, 1))],
            [sg.Text('弔辞:'), sg.Multiline(key='condolence_message', size=(50, 3))],
            [sg.Text('弔電:'), sg.Multiline(key='condolence_telegram', size=(50, 3))],
            [sg.Checkbox('チェック', key='condolence_check')],
            [sg.Text('備考:'), sg.Input(key='condolence_notes', size=(50, 1))],
            [sg.HSeparator()],
            [sg.Button('保存', key='btn_save_condolence'), 
             sg.Button('クリア', key='btn_clear_condolence'),
             sg.Button('削除', key='btn_delete_condolence'),
             sg.Button('終了', key='btn_exit_condolence')]
        ]
    
    def _save_condolence_data(self, values):
        """弔辞弔電データを保存"""
        try:
            # データを取得
            condolence = CondolenceModel()
            condolence.number = int(values.get('condolence_number', 0) or 0)
            condolence.company_name = values.get('condolence_company', '')
            condolence.condolence_message = values.get('condolence_message', '')
            condolence.telegram_message = values.get('condolence_telegram', '')
            condolence.check = values.get('condolence_check', False)
            condolence.notes = values.get('condolence_notes', '')
            
            # データを検証
            errors = condolence.validate()
            if errors:
                self.show_error("データの検証に失敗しました:\\n" + "\\n".join(errors))
                return
            
            # データを保存
            self.data_service.save_condolence_data(condolence)
            
            # 成功メッセージを表示
            self.show_success("弔辞弔電データを保存しました")
            
            # フォームをクリア
            self._clear_condolence_data()
            
        except Exception as e:
            self.show_error(f"データの保存に失敗しました: {str(e)}")
    
    def _clear_condolence_data(self):
        """弔辞弔電データをクリア"""
        self.window['condolence_number'].update('')
        self.window['condolence_company'].update('')
        self.window['condolence_message'].update('')
        self.window['condolence_telegram'].update('')
        self.window['condolence_check'].update(False)
        self.window['condolence_notes'].update('')
    
    def _delete_condolence_data(self, values):
        """弔辞弔電データを削除"""
        try:
            condolence_number = int(values.get('condolence_number', 0) or 0)
            if condolence_number <= 0:
                self.show_error("削除する番号を入力してください")
                return
            
            # 削除確認
            if self.show_confirm(f"番号 {condolence_number} の弔辞弔電データを削除しますか？"):
                # データを削除
                self.data_service.delete_condolence_data(condolence_number)
                self.show_success("弔辞弔電データを削除しました")
                self._clear_condolence_data()
            
        except Exception as e:
            self.show_error(f"データの削除に失敗しました: {str(e)}")