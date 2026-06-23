"""
供花料入力コントローラー
供花料入力画面の処理を管理
"""
import TkEasyGUI as sg
from controllers.base_controller import BaseController
from models.flower_model import FlowerModel

class FlowerController(BaseController):
    """供花料入力のコントローラー"""
    
    def __init__(self, window):
        super().__init__(window)
        self.flower_data = []  # 供花料データのリスト
        self.current_flower = None  # 現在編集中の供花料
    
    def handle_flower_input(self, values):
        """供花料入力ボタンが押された時の処理"""
        print("供花料入力ボタンが押されました")
        
        # ウィンドウを切り替える（元のプログラムの方式）
        self.window = self.switch_window(
            self._create_flower_input_layout(),
            '供花料入力',
            use_hide=False  # 元のプログラムでは close() を使用
        )
        
        # ウィンドウの切り替えが成功したかチェック
        if not self.window:
            print("ウィンドウの切り替えに失敗しました")
            return False
        
        # Excelファイルを開く
        try:
            self.data_service.excel_service.get_flower_workbook()
        except Exception as e:
            print(f"Excelファイルの読み込みに失敗: {str(e)}")
            self.show_error(f"Excelファイルの読み込みに失敗しました。\\n{str(e)}")
            return True  # ウィンドウは表示されたのでTrueを返す
        
        return True
    
    def _open_flower_input_window(self):
        """供花料入力画面を開く"""
        # 供花料入力画面のレイアウトを作成
        layout = self._create_flower_input_layout()
        
        # ウィンドウを作成
        flower_window = sg.Window(
            '供花料入力',
            layout,
            modal=True,
            finalize=True
        )
        
        # イベントループ
        while True:
            event, values = flower_window.read()
            
            if event == sg.WIN_CLOSED:
                break
            elif event == 'btn_save':
                self._save_flower_data(flower_window, values)
            elif event == 'btn_clear':
                self._clear_flower_data(flower_window)
            elif event == 'btn_delete':
                self._delete_flower_data(flower_window, values)
            elif event == 'btn_exit':
                break
        
        # ウィンドウを閉じる
        flower_window.close()
        
        # メインウィンドウを再表示
        self.window.un_hide()
    
    def _create_flower_input_layout(self):
        """供花料入力画面のレイアウトを作成"""
        return [
            [sg.Text('供花料入力', font=('Arial', 16, 'bold'))],
            [sg.HSeparator()],
            [sg.Text('番号:'), sg.Input(key='flower_number', size=(10, 1))],
            [sg.Text('金額:'), sg.Input(key='flower_amount', size=(15, 1))],
            [sg.Text('住所:'), sg.Input(key='flower_address', size=(50, 1))],
            [sg.Text('名前:'), sg.Input(key='flower_name', size=(30, 1))],
            [sg.Checkbox('領収証', key='flower_receipt')],
            [sg.Text('備考:'), sg.Input(key='flower_notes', size=(50, 1))],
            [sg.HSeparator()],
            [sg.Button('保存', key='btn_save'), 
             sg.Button('クリア', key='btn_clear'),
             sg.Button('削除', key='btn_delete'),
             sg.Button('終了', key='btn_exit')]
        ]
    
    def _save_flower_data(self, values):
        """供花料データを保存"""
        try:
            # データを取得
            flower = FlowerModel()
            flower.number = int(values.get('flower_number', 0) or 0)
            flower.amount = int(values.get('flower_amount', 0) or 0)
            flower.address = values.get('flower_address', '')
            flower.name = values.get('flower_name', '')
            flower.receipt = values.get('flower_receipt', False)
            flower.notes = values.get('flower_notes', '')
            
            # データを検証
            errors = flower.validate()
            if errors:
                self.show_error("データの検証に失敗しました:\\n" + "\\n".join(errors))
                return
            
            # データを保存
            self.data_service.save_flower_data(flower)
            
            # 成功メッセージを表示
            self.show_success("供花料データを保存しました")
            
            # フォームをクリア
            self._clear_flower_data()
            
        except Exception as e:
            self.show_error(f"データの保存に失敗しました: {str(e)}")
    
    def _clear_flower_data(self):
        """供花料データをクリア"""
        self.window['flower_number'].update('')
        self.window['flower_amount'].update('')
        self.window['flower_address'].update('')
        self.window['flower_name'].update('')
        self.window['flower_receipt'].update(False)
        self.window['flower_notes'].update('')
    
    def _delete_flower_data(self, values):
        """供花料データを削除"""
        try:
            flower_number = int(values.get('flower_number', 0) or 0)
            if flower_number <= 0:
                self.show_error("削除する番号を入力してください")
                return
            
            # 削除確認
            if self.show_confirm(f"番号 {flower_number} の供花料データを削除しますか？"):
                # データを削除
                self.data_service.delete_flower_data(flower_number)
                self.show_success("供花料データを削除しました")
                self._clear_flower_data()
            
        except Exception as e:
            self.show_error(f"データの削除に失敗しました: {str(e)}")