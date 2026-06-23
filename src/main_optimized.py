"""
最適化されたメインアプリケーション
旧 global_list / global_value / gui01 / func1 への依存なし。
"""
import TkEasyGUI as sg
from controllers.main_controller import MainController
from views.main_layout import get_main_layout
from views.layout_manager import LayoutManager
from utils.performance_optimizer import PerformanceOptimizer
from utils.logger import app_logger, error_handler
import sys
from typing import Optional


class OptimizedApplication:
    """最適化されたアプリケーションクラス"""

    def __init__(self):
        self.layout_manager = LayoutManager()
        self.performance_optimizer = PerformanceOptimizer()
        self.controller: Optional[MainController] = None
        self.window: Optional[sg.Window] = None

        self.performance_optimizer.optimize_for_system()
        app_logger.info("アプリケーションを開始",
                        memory_usage=self.performance_optimizer.monitor_memory()['rss'])

    def initialize(self) -> bool:
        """アプリケーションを初期化"""
        try:
            self.layout_manager.set_theme("clam")
            self.layout_manager.set_window_size(450, 700)
            self.layout_manager.set_font("Arial", 10)
            app_logger.info("アプリケーション初期化完了")
            return True
        except Exception as e:
            app_logger.error("アプリケーション初期化エラー", e)
            return False

    def create_main_window(self) -> bool:
        """メインウィンドウを作成"""
        try:
            layout = get_main_layout()
            optimized_layout = self.layout_manager.optimize_layout(layout)

            self.window = self.layout_manager.create_window(
                '記録書簡易システム(β版)',
                optimized_layout,
                anchor='nw',
                padx=5,
                pady=5,
                expand_x=True,
                expand_y=True
            )

            # DataService 内の FileService が config から作業パスを自動読込み
            self.controller = MainController(self.window)

            app_logger.info("メインウィンドウ作成完了")
            return True
        except Exception as e:
            app_logger.error("メインウィンドウ作成エラー", e)
            return False

    def run(self) -> None:
        """アプリケーションを実行"""
        try:
            if not self.initialize():
                app_logger.critical("アプリケーション初期化に失敗")
                return

            if not self.create_main_window():
                app_logger.critical("メインウィンドウ作成に失敗")
                return

            app_logger.info("アプリケーション実行開始")

            while True:
                try:
                    if self.performance_optimizer.check_memory_usage():
                        app_logger.warning("メモリ使用量が閾値を超過")
                        self.performance_optimizer.cleanup_memory()

                    event, values = self.window.read(timeout=100)

                    if event == sg.TIMEOUT_KEY:
                        continue

                    if event == sg.WIN_CLOSED:
                        app_logger.info("ウィンドウが閉じられました")
                        break

                    app_logger.log_user_action("button_click", {
                        'event': event,
                        'values_keys': list(values.keys()) if values else []
                    })

                    try:
                        result = self.controller.handle_event(event, values)

                        if hasattr(self.controller, 'window') and self.controller.window != self.window:
                            self.window = self.controller.window

                        if result is False:
                            app_logger.info("アプリケーション終了要求")
                            break

                    except Exception as e:
                        if hasattr(self.controller, 'window') and \
                                self.controller.window is not None and \
                                self.controller.window != self.window:
                            self.window = self.controller.window
                        app_logger.error(f"イベント処理エラー: {event}", e)
                        error_message = error_handler.handle_exception(e, {
                            'event': event,
                            'values': str(values)
                        })
                        sg.popup_error(f"エラーが発生しました: {error_message}")

                except Exception as e:
                    app_logger.error("メインループエラー", e)
                    error_message = error_handler.handle_exception(e)
                    sg.popup_error(f"予期しないエラーが発生しました: {error_message}")
                    break

        except Exception as e:
            app_logger.critical("アプリケーション実行エラー", e)
            error_message = error_handler.handle_exception(e)
            sg.popup_error(f"致命的なエラーが発生しました: {error_message}")

        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """リソースをクリーンアップ"""
        try:
            if self.controller:
                self.controller.close_excel_safely()
            if self.window:
                self.window.close()
            self.performance_optimizer.cleanup_memory()
            app_logger.cleanup_old_logs(30)
            app_logger.info("アプリケーションクリーンアップ完了")
        except Exception as e:
            app_logger.error("クリーンアップエラー", e)


def main():
    """メイン関数"""
    try:
        app = OptimizedApplication()
        app.run()
    except Exception as e:
        print(f"致命的なエラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
