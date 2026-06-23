"""
施工状況入力コントローラー
施工状況入力・袋印刷機能を管理
"""
from views.tab_layouts import get_tab_layout
from controllers.base_controller import BaseController


class ConstructionController(BaseController):
    """施工状況入力機能のコントローラー"""

    def __init__(self, window):
        super().__init__(window)

    def _ops(self):
        return self.data_service.operations_service

    def handle_construction_input(self, values):
        """施工状況入力・袋印刷ボタンが押された時の処理"""
        print("施工状況入力・袋印刷ボタンが押されました")
        self.window = self.switch_window(get_tab_layout('tab1'), '記録書簡易システム(β版)')
        self._ops().read_construction_status(self.window)
        return True

    def handle_construction_update(self, values):
        """施工状況の更新処理"""
        print("施工状況の更新ボタンが押されました")
        try:
            self._ops().save_construction_status(values)
            self.show_success("施工状況を更新しました。", "更新完了")
        except Exception as e:
            self.show_error(f"施工状況の更新中にエラーが発生しました。\\n{str(e)}")

    def handle_print_operations(self, event, values):
        """印刷操作の処理"""
        try:
            if event == 'iip09':
                self._ops().print_a01()
                self.show_success("印刷が完了しました。", "印刷完了")
            elif event == 'iip0A':
                cnt = int(values.get('-input02B-', 0))
                for _ in range(cnt):
                    self._ops().print_a02()
                self.show_success("印刷が完了しました。", "印刷完了")
            elif event == 'iip0B':
                cnt = int(values.get('-input02B-', 0))
                for _ in range(cnt):
                    self._ops().print_a03()
                self.show_success("印刷が完了しました。", "印刷完了")
            elif event == 'iip0C':
                cnt = int(values.get('-input02C-', 0))
                for _ in range(cnt):
                    self._ops().print_a04()
                self.show_success("印刷が完了しました。", "印刷完了")
            elif event == 'iip0D':
                flag = int(values.get('-input02D-', 0)) == 1
                self._ops().print_a05(flag)
                self.show_success("印刷が完了しました。", "印刷完了")
            elif event == 'iip0e':
                hyoudai1 = str(values.get('-input02e-', ''))
                tadasi = str(values.get('-input02f-', ''))
                self._ops().print_a06(hyoudai1, tadasi)
                self.show_success("白無地封筒の印刷が完了しました。", "印刷完了")
            elif event == 'iip0g':
                hyoudai2 = str(values.get('-input02g-', ''))
                self._ops().print_a07(hyoudai2)
                self.show_success("水引付封筒の印刷が完了しました。", "印刷完了")
        except Exception as e:
            self.show_error(f"印刷中にエラーが発生しました。\\n{str(e)}")

    def handle_construction_events(self, event, values):
        """施工状況関連のイベント処理"""
        if event == '-upd02-':
            self.handle_construction_update(values)
        elif event in ['iip09', 'iip0A', 'iip0B', 'iip0C', 'iip0D', 'iip0e', 'iip0g']:
            self.handle_print_operations(event, values)
        elif event == '-read1A-':
            print("施工状況：新規で追加ボタンが押されました")
        elif event == '-read1B-':
            print("施工状況：上記内容で更新ボタンが押されました")
        elif event == '-read1C-':
            print("施工状況：上記を削除ボタンが押されました")
