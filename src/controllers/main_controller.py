"""
メインコントローラー
アプリケーション全体の制御を管理
"""
import TkEasyGUI as sg
import os
import re
import config
from utils.postal_utils import lookup_postal_code
from utils.table_utils import sort_table, remove_parentheses
from views.main_layout import get_main_layout
from views.tab_layouts import get_tab_layout
from views.folder_layout import get_folder_layout, update_folder_name
from views.settings_layout import get_settings_layout
from views.print_layout import get_print_layout
from data.list_data import class_list
from controllers.koden_controller import KodenController
from controllers.construction_controller import ConstructionController
from controllers.funeral_controller import FuneralController
from controllers.flower_controller import FlowerController
from controllers.condolence_controller import CondolenceController
from controllers.base_controller import BaseController

class MainController(BaseController):
    """アプリケーション全体のメインコントローラー"""

    def __init__(self, window):
        super().__init__(window)
        # サブコントローラーは初回アクセス時に生成（起動コスト削減）
        self._koden_controller = None
        self._construction_controller = None
        self._funeral_controller = None
        self._flower_controller = None
        self._condolence_controller = None

        # テーブルデータのインスタンス変数（旧 gv.list03/04/05/06）
        self.list03 = []
        self.list04 = []
        self.list05 = []
        self.list06 = []

        # イベントマッピング（lambda でコントローラーを遅延参照）
        self.event_handlers = {
            # メイン機能
            '-sm01-': lambda v: self.koden_controller.handle_koden_input(v),
            '-sm18-': self._handle_construction_input,
            '-sm02-': self._handle_flower_input,
            '-sm03-': self._handle_condolence_input,
            '-sm04-': self._handle_accounting_input,
            '-sm05-': self._handle_offering_input,
            '-sm06-': self._handle_incense_input,
            '-sm07-': self._handle_koden_list,
            '-sm08-': self._handle_folder_setup,
            '-sm00-': lambda v: self.funeral_controller.handle_basic_info_input(v),
            '-sm14-': self._handle_detail_settings,
            '-sm15-': self._handle_overnight_summary,
            '-sm16-': self._handle_funeral_summary,
            '-sm11-': self._handle_receipt_check,
            '-sm13-': self._handle_clean_output,
            '-sm10-': self._handle_cd_creation,
            '-Print-': self._handle_print,
            '-sm17-': self._handle_construction_list,
            '-Quit-': self._handle_quit,
            '-Close-': self._handle_return_to_top,

            # サブウィンドウのイベント
            '-su82-': self._handle_create_folder,
            '-su83-': self._handle_set_path,
            '-x_dir2-': self._handle_update_folder_name,
            'filebtn3': self._handle_folder_browse,

            # 供花料入力のボタンイベント
            '-read6Z-': self._handle_postal_lookup,
            '-input6z--r6ZX-': self._handle_postal_lookup,
            '-read6A-': self._handle_flower_add,
            '-read6B-': self._handle_flower_update,
            '-read6C-': self._handle_flower_delete,

            # 弔辞弔電入力のボタンイベント
            '-read3A-': self._handle_condolence_add,
            '-read3B-': self._handle_condolence_update,
            '-read3C-': self._handle_condolence_delete,
            '-read3D-': self._handle_condolence_sort,

            # 供物入力のボタンイベント
            '-read4A-': self._handle_offering_add,
            '-read4B-': self._handle_offering_update,
            '-read4C-': self._handle_offering_delete,
            '-read4D-': self._handle_offering_sort,

            # 焼香順入力のボタンイベント
            '-read5A-': self._handle_incense_add,
            '-read5B-': self._handle_incense_update,
            '-read5C-': self._handle_incense_delete,
            '-read5D-': self._handle_incense_sort,

            # 供物コンボ連動
            '-input43-': self._handle_class_no_change,
            '-input42-': self._handle_class_name_change,

            # テーブル行クリックイベント（TkEasyGUIはstring keyで発火）
            'T3': self._handle_t3_row_click,
            'T4': self._handle_t4_row_click,
            'T5': self._handle_t5_row_click,
            'T6': self._handle_t6_row_click,
        }

    @property
    def koden_controller(self):
        if self._koden_controller is None:
            self._koden_controller = KodenController(self.window)
        return self._koden_controller

    @property
    def construction_controller(self):
        if self._construction_controller is None:
            self._construction_controller = ConstructionController(self.window)
        return self._construction_controller

    @property
    def funeral_controller(self):
        if self._funeral_controller is None:
            self._funeral_controller = FuneralController(self.window)
        return self._funeral_controller

    @property
    def flower_controller(self):
        if self._flower_controller is None:
            self._flower_controller = FlowerController(self.window)
        return self._flower_controller

    @property
    def condolence_controller(self):
        if self._condolence_controller is None:
            self._condolence_controller = CondolenceController(self.window)
        return self._condolence_controller

    def handle_event(self, event, values):
        """イベントを適切なハンドラーに振り分け"""
        self.update_values(values)

        # イベントハンドラーが存在する場合
        if event in self.event_handlers:
            handler = self.event_handlers[event]
            return handler(values)

        # 施工状況関連のイベント
        elif event in ['-upd02-', 'iip09', 'iip0A', 'iip0B', 'iip0C', 'iip0D', 'iip0e', 'iip0g',
                      '-read1A-', '-read1B-', '-read1C-']:
            self.construction_controller.handle_construction_events(event, values)
            return True

        # その他のイベント処理
        elif isinstance(event, str) and event.startswith('-input'):
            self._handle_input_events(event, values)
            return True

        # カレンダー関連のイベント
        elif event in ['-ccal1-', '-ccal2-', '-ccal3-', '-ccal4-', '-ccal5-']:
            self._handle_calendar_events(event, values)
            return True

        # テーブル選択イベント
        elif isinstance(event, tuple) and len(event) >= 3:
            self._handle_table_events(event, values)
            return True

        return True

    def _ops(self):
        return self.data_service.operations_service

    def _handle_flower_input(self, values):
        """供花料入力の処理"""
        self.window = self.switch_window(
            get_tab_layout('tab2', list06=self.list06),
            '記録書簡易システム(β版)'
        )
        if self.window is None:
            return True
        try:
            self.list06 = self._ops().get_foFF_input(self.window)
            self.window['T6'].update(self.list06)
        except Exception as e:
            print(f"供花料データ読み込みエラー: {e}")
        try:
            self.window['-input6z-'].bind('<Return>', '-r6ZX-')
        except Exception:
            pass
        return True

    def _handle_condolence_input(self, values):
        """弔辞弔電入力の処理"""
        self.window = self.switch_window(
            get_tab_layout('tab3', list03=self.list03),
            '記録書簡易システム(β版)'
        )
        if self.window is None:
            return True
        try:
            self.list03 = self._ops().get_cd_msg(self.window)
            self.window['T3'].update(self.list03)
        except Exception as e:
            print(f"弔辞弔電データ読み込みエラー: {e}")
        return True

    def _handle_offering_input(self, values):
        """供物入力の処理"""
        self.window = self.switch_window(
            get_tab_layout('tab4', list04=self.list04),
            '記録書簡易システム(β版)'
        )
        if self.window is None:
            return True
        try:
            self.list04 = self._ops().get_of_input(self.window)
            self.window['T4'].update(self.list04)
        except Exception as e:
            print(f"供物データ読み込みエラー: {e}")
        return True

    def _handle_construction_input(self, values):
        """施工状況入力・袋印刷の処理"""
        print("施工状況入力・袋印刷ボタンが押されました")
        self.window = self.switch_window(
            get_tab_layout('tab1'),
            '記録書簡易システム(β版)'
        )
        if self.window is None:
            return True
        try:
            self._ops().read_construction_status(self.window)
        except Exception as e:
            print(f"施工状況データ読み込みエラー: {e}")
        return True

    def _handle_incense_input(self, values):
        """焼香順入力の処理"""
        self.window = self.switch_window(
            get_tab_layout('tab5', list05=self.list05),
            '記録書簡易システム(β版)'
        )
        if self.window is None:
            return True
        try:
            self.list05 = self._ops().get_ince_bo(self.window)
            self.window['T5'].update(self.list05)
        except Exception as e:
            print(f"焼香順データ読み込みエラー: {e}")
        return True

    def _handle_accounting_input(self, values):
        """会計情報入力の処理"""
        print("会計情報入力ボタンが押されました")
        try:
            self._ops().acc_disp()
        except Exception as e:
            self.show_error(f"Excelファイルの操作に失敗しました。\\n{str(e)}")
        return True

    def _handle_koden_list(self, values):
        """香典一覧の処理"""
        print("香典一覧ボタンが押されました")
        return True

    def _handle_folder_setup(self, values):
        """フォルダ作成・設定の処理"""
        print("フォルダ作成・設定ボタンが押されました")
        cpath = self.data_service.file_service.get_current_path()
        from services.excel_service import ExcelService
        x_dir2 = ExcelService._extract_family_name_from_path(cpath)
        basepath = self.data_service.file_service.get_basepath()
        tmppath = cpath if cpath else basepath + '\\' + config.TPATH3 + '\\'
        self.window = self.switch_window(
            get_folder_layout(basepath, config.TPATH1, config.TPATH2, config.TPATH3, tmppath, x_dir2),
            'フォルダ作成・設定',
            use_hide=False
        )
        return True

    def _handle_update_folder_name(self, values):
        """遺族名入力時のフォルダ名更新処理"""
        try:
            update_folder_name(self.window, values)
        except Exception as e:
            print(f"フォルダ名更新中にエラーが発生しました: {str(e)}")

    def _handle_update_folder_name_modal(self, window, values):
        """モーダルウィンドウでの遺族名入力時のフォルダ名更新処理"""
        try:
            update_folder_name(window, values)
        except Exception as e:
            print(f"フォルダ名更新中にエラーが発生しました: {str(e)}")

    def _open_modal_sub_window(self):
        """モーダルサブウィンドウを開く"""
        cpath = self.data_service.file_service.get_current_path()
        from services.excel_service import ExcelService
        x_dir2 = ExcelService._extract_family_name_from_path(cpath)
        basepath = self.data_service.file_service.get_basepath()
        tmppath = cpath if cpath else basepath + '\\' + config.TPATH3 + '\\'
        sub_layout = get_folder_layout(basepath, config.TPATH1, config.TPATH2, config.TPATH3, tmppath, x_dir2)

        sub_window = sg.Window('フォルダ作成・設定', sub_layout, modal=True, finalize=True, size=(600, 400))

        while True:
            event, values = sub_window.read()
            if event == sg.WIN_CLOSED or event == '-Quit-' or event == '-Close-':
                break
            elif event == '-su82-':
                self._handle_create_folder(values)
            elif event == '-su83-':
                self._handle_set_path(values)
            elif event == '-x_dir2-':
                self._handle_update_folder_name_modal(sub_window, values)
            elif event == 'filebtn3':
                self._handle_folder_browse(values)
            else:
                self._handle_sub_window_event(event, values)

        sub_window.close()

    def _run_sub_window_loop(self):
        """サブウィンドウのイベントループ"""
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == '-Quit-':
                break
            elif event == '-Close-':
                self.window = self.switch_window(get_main_layout(), '記録書簡易システム(β版)')
                break
            elif event == '-su82-':
                self._handle_create_folder(values)
            elif event == '-su83-':
                self._handle_set_path(values)
            elif event == '-x_dir2-':
                self._handle_update_folder_name(values)
            elif event == 'filebtn3':
                self._handle_folder_browse(values)
            else:
                self._handle_sub_window_event(event, values)

    def _handle_create_folder(self, values):
        """フォルダ作成処理"""
        try:
            print("フォルダ作成処理を実行")
            self.show_success("フォルダが作成されました", "フォルダ作成")
        except Exception as e:
            self.show_error(f"フォルダ作成中にエラーが発生しました: {str(e)}")

    def _handle_set_path(self, values):
        """パス設定処理 — '-x_dir-' の値を作業パスとして確定する"""
        try:
            new_path = os.path.normpath(values.get('-x_dir-', '').strip())
            if not new_path or new_path == '.':
                self.show_error("フォルダが選択されていません", "パス設定")
                return
            if not os.path.exists(new_path):
                self.show_error(f"フォルダが存在しません:\n{new_path}", "パス設定")
                return
            # config.ini に保存 & FileService.current_path を更新
            self.data_service.file_service.save_paths(new_path)
            # ExcelService のキャッシュをリセット（別案件のブックが開いている可能性）
            self.data_service.excel_service.safe_close_excel()
            # ExcelService の作業パスを更新
            self.data_service.excel_service.set_cpath(new_path)
            # サブコントローラーもリセット（各自の DataService が古いパスをキャッシュしているため）
            for attr in ('_koden_controller', '_construction_controller', '_funeral_controller',
                         '_flower_controller', '_condolence_controller'):
                ctrl = getattr(self, attr, None)
                if ctrl is not None:
                    try:
                        ctrl.close_excel_safely()
                    except Exception:
                        pass
                    setattr(self, attr, None)
            print(f"パス設定完了: {new_path}")
            self.show_success(f"フォルダを設定しました:\n{new_path}", "パス設定")
        except Exception as e:
            self.show_error(f"パス設定中にエラーが発生しました: {str(e)}")

    def _handle_folder_browse(self, values):
        """フォルダブラウザでフォルダ選択時の処理（target_key により -x_dir- が更新済み）"""
        try:
            selected = values.get('-x_dir-', '')
            print(f"フォルダが選択されました: {selected}")
        except Exception as e:
            print(f"フォルダ選択処理中にエラーが発生しました: {str(e)}")

    def _handle_sub_window_event(self, event, values):
        """サブウィンドウのその他のイベント処理"""
        print(f"サブウィンドウイベント: {event} = {values.get(event, '')}")

    def _handle_detail_settings(self, values):
        """詳細設定の処理"""
        print("詳細設定ボタンが押されました")
        self.window.close()
        try:
            tmp = self._ops().make_detail_settings(None, values, 0, 0)
            if tmp is not None:
                self.window = tmp
        except NotImplementedError:
            # 詳細設定ウィンドウを直接開く（operations_service 未実装時のフォールバック）
            layout = get_settings_layout()
            self.window = sg.Window('詳細設定', layout, finalize=True)
        return True

    def _handle_overnight_summary(self, values):
        """通夜集計の処理"""
        print("通夜集計ボタンが押されました")
        self._ops().subt_first()
        self.show_success('通夜集計しました。会計帳と供物一覧を出力します。', "集計：通夜")
        return True

    def _handle_funeral_summary(self, values):
        """葬儀集計の処理"""
        print("葬儀集計ボタンが押されました")
        self._ops().subt_second()
        self.show_success('葬儀集計(50音生成)しました。清書出力を行ってください。', "集計：葬儀")
        return True

    def _handle_receipt_check(self, values):
        """領収書チェックの処理"""
        print("領収書チェックボタンが押されました")
        try:
            self._ops().check_bill()
        except Exception as e:
            self.show_error(f"領収書チェック中にエラーが発生しました。\\n{str(e)}")
        finally:
            book_c = self.data_service.excel_service.current_book_c
            if book_c is not None:
                book_c.close()
                self.data_service.excel_service.current_book_c = None
                self.data_service.excel_service.current_sheet_c = None
        return True

    def _handle_clean_output(self, values):
        """清書出力の処理"""
        print("清書出力ボタンが押されました")
        vix_path = self.data_service.file_service.get_vix_path() or r"C:\vix221\ViX.exe"
        self.window = self.switch_window(get_print_layout(vix_path), '清書出力')
        if self.window is None:
            return True
        try:
            self._ops().show_print_window(self.window)
        except Exception as e:
            print(f"印刷ウィンドウ初期化エラー: {e}")
        return True

    def _handle_print(self, values):
        """清書出力ウィンドウの印刷ボタン処理"""
        print("印刷ボタンが押されました")
        try:
            self._ops().chk_on_print(values)
            self.show_success("印刷が完了しました。", "印刷完了")
        except Exception as e:
            print(f"印刷処理中にエラーが発生しました: {e}")
            self.show_error(f"印刷中にエラーが発生しました。\nエラー内容: {str(e)}")
        return True

    def _handle_cd_creation(self, values):
        """CD下準備＆作成の処理"""
        print("CD下準備＆作成ボタンが押されました")
        y_n = self.show_confirm("DVDドライブとディスクをセットしましたか？\\nOKを押すと処理を実行します。\\nよろしいですか？", "CD下準備&作成")
        if y_n == "OK":
            try:
                if self._ops().create_cd(values):
                    self.show_success("CDの作成が完了しました。", "処理完了")
                else:
                    raise Exception("CD作成に失敗しました")
            except Exception as e:
                print(f"CD作成処理中にエラーが発生しました: {str(e)}")
                self.show_error(f"CD作成中にエラーが発生しました。\\nエラー内容: {str(e)}")
        else:
            self.show_success('準備を確認してもう一度行ってください', "CD作成")
        return True

    def _handle_construction_list(self, values):
        """施工状況一覧の処理"""
        print("施工状況一覧ボタンが押されました")
        return True

    def _handle_quit(self, values):
        """終了処理"""
        print("終了ボタンが押されました")
        # MainController 自身の Excel を閉じる
        self.close_excel_safely()
        # 生成済みのサブコントローラーの Excel もそれぞれ閉じる
        for attr in ('_koden_controller', '_construction_controller', '_funeral_controller',
                     '_flower_controller', '_condolence_controller'):
            ctrl = getattr(self, attr, None)
            if ctrl is not None:
                ctrl.close_excel_safely()
        return False  # ループを終了

    def _handle_return_to_top(self, values):
        """トップに戻る処理"""
        print("Topへ戻るボタンが押されました")
        self.window = self.switch_window(get_main_layout(), '記録書簡易システム(β版)')
        return True

    def _handle_input_events(self, event, values):
        """入力フィールドのイベント処理"""
        if event == '-input61-':
            val = values.get('-input61-', '')
            if val and val != val.zfill(3):
                self.window['-input61-'].update(val.zfill(3))
        return True

    def _handle_calendar_events(self, event, values):
        """カレンダー関連のイベント処理"""
        print(f"カレンダーイベント: {event}")
        return True

    def _handle_table_events(self, event, values):
        """テーブル選択のイベント処理"""
        if event[0] == 'T3':
            if event[2][0] != -1 and event[2][1] != -1:
                for key in ['-w1-', '-w2-', '-w3-', '-w4-']:
                    self.window[key].update(False)
                self.window['-inputwa-'].update('')
                record_id = int(event[2][0])
                if not self.list03 or record_id >= len(self.list03):
                    return True
                temp_s1 = ','.join(self.list03[record_id])
                temp_s4 = temp_s1.split(',')
                self.window['-input31-'].update(temp_s4[0].zfill(3))
                self.window['-input32-'].update(temp_s4[1])
                s = str(temp_s4[2]).replace(r'\n', '')
                ss = remove_parentheses(s)
                self.window['-input33-'].update(ss)
                if str(temp_s4[2]).find('(') >= 1:
                    m = re.search(r'(?<=\().+?(?=\))', s)
                    if m:
                        text = m.group()
                        if text == '線香　月':
                            self.window['-w1-'].update(True)
                        elif text == '線香　哀星':
                            self.window['-w2-'].update(True)
                        elif text == 'プリザーブドフラワー':
                            self.window['-w3-'].update(True)
                        else:
                            self.window['-w4-'].update(True)
                            self.window['-inputwa-'].update(text)
                if len(temp_s4) == 4 and temp_s4[3]:
                    self.window['-input34-'].update(temp_s4[3])
            elif event[2][0] == -1 and event[2][1] != -1:
                if self.list03:
                    self.list03 = sort_table(self.list03, (event[2][1], 0))
                    self.window['T3'].update(self.list03)
        elif event[0] == 'T6':
            if event[2][0] != -1 and event[2][1] != -1:
                if self.list06:
                    record_id = int(event[2][0])
                    if record_id < len(self.list06):
                        temp_s1 = ','.join(self.list06[record_id])
                        temp_s4 = temp_s1.split(',')
                        self.window['-input61-'].update(temp_s4[0])
                        self.window['-input62-'].update(temp_s4[1] + ',' + temp_s4[2])
                        self.window['-input63-'].update(temp_s4[3])
                        self.window['-input64-'].update(temp_s4[4])
                        self.window['-input65-'].update(temp_s4[5])
            elif event[2][0] == -1 and event[2][1] != -1:
                if self.list06:
                    self.list06 = sort_table(self.list06, (event[2][1], 0))
                    self.window['T6'].update(self.list06)
        elif event[0] == 'T4':
            if event[2][0] != -1 and event[2][1] != -1:
                c = self.window['T4'].get()
                if c is not None and len(c) > 0 and self.list04:
                    temp_s1 = ','.join(str(x) for x in self.list04[c[0]])
                    temp_s4 = temp_s1.split(',')
                    self.window['-input41-'].update(str(temp_s4[0]).zfill(3))
                    self.window['-input42-'].update(str(temp_s4[1]))
                    self.window['-input43-'].update(str(temp_s4[2]))
                    self.window['-input44-'].update(str(temp_s4[3]))
                    self.window['-input45-'].update(str(temp_s4[4]))
            elif event[2][0] == -1 and event[2][1] != -1:
                if self.list04:
                    self.list04 = sort_table(self.list04, (event[2][1], 0))
                    self.window['T4'].update(self.list04)
        elif event[0] == 'T5':
            if event[2][0] != -1 and event[2][1] != -1:
                c = self.window['T5'].get()
                if c is not None and len(c) > 0 and self.list05:
                    temp_s1 = ','.join(str(x) for x in self.list05[c[0]])
                    temp_s4 = temp_s1.split(',')
                    self.window['-input51-'].update(temp_s4[0])
                    ls = str(temp_s4[1]).split()
                    try:
                        no_int = int(temp_s4[0])
                    except (ValueError, TypeError):
                        no_int = 0
                    if len(ls) >= 2 and ((no_int >= 81 and no_int < 999) or no_int == 1000):
                        role_val = str(ls[0])
                        ls.pop(0)
                        name_val = ' '.join(ls)
                    else:
                        role_val = temp_s4[1]
                        name_val = temp_s4[1]
                    self.window['-input52-'].update('' if role_val == name_val else role_val)
                    self.window['-input53-'].update(name_val)
                    self.window['-input54-'].update(temp_s4[2])
                    self.window['-input55-'].update(temp_s4[3])
            elif event[2][0] == -1 and event[2][1] != -1:
                if self.list05:
                    self.list05 = sort_table(self.list05, (event[2][1], 0))
                    self.window['T5'].update(self.list05)
        return True

    def _handle_postal_lookup(self, values):
        """郵便番号から住所を検索"""
        result = lookup_postal_code(values.get('-input6z-', ''))
        if result:
            self.window['-input63-'].update(result['address'])
        else:
            self.show_error('住所が見つかりませんでした。\n郵便番号を確認してください。', '住所検索')
        return True

    def _handle_flower_add(self, values):
        """供花料を新規追加"""
        l = [str(values.get('-input61-', '')).zfill(3), str(values.get('-input62-', '')),
             str(values.get('-input63-', '')), str(values.get('-input64-', '')),
             str(values.get('-input65-', ''))]
        self._ops().set_foFF_input(l)
        self.list06 = self._ops().get_foFF_input(self.window)
        self.window['T6'].update(self.list06)
        self._clear_flower_fields()
        return True

    def _handle_flower_update(self, values):
        """供花料を更新"""
        l = [str(values.get('-input61-', '')).zfill(3), str(values.get('-input62-', '')),
             str(values.get('-input63-', '')), str(values.get('-input64-', '')),
             str(values.get('-input65-', ''))]
        self._ops().set_foFF_input(l, int(values.get('-input61-', 0)))
        self.list06 = self._ops().get_foFF_input(self.window)
        self.window['T6'].update(self.list06)
        self._clear_flower_fields()
        return True

    def _handle_flower_delete(self, values):
        """供花料を削除"""
        l = [' ', ' ', ' ', ' ', ' ']
        self._ops().set_foFF_input(l, int(values.get('-input61-', 0)))
        self.list06 = self._ops().get_foFF_input(self.window)
        self.window['T6'].update(self.list06)
        self._clear_flower_fields()
        return True

    def _clear_flower_fields(self):
        """供花料入力フィールドをクリア"""
        for key in ['-input6z-', '-input61-', '-input62-', '-input63-', '-input64-']:
            self.window[key].update('')
        self.window['-input65-'].update('')

    def _handle_condolence_add(self, values):
        """弔辞弔電を新規追加"""
        w4 = values.get('-w4-', False) is True
        l = [str(values.get('-input31-', '')), str(values.get('-input32-', '')),
             str(values.get('-input33-', '')), str(values.get('-input34-', '')),
             values.get('-w1-', False) is True,
             values.get('-w2-', False) is True,
             values.get('-w3-', False) is True,
             w4,
             values.get('-inputwa-', '') if w4 else '']
        self._ops().set_cd_msg(l)
        self.list03 = self._ops().get_cd_msg(self.window)
        self.window['T3'].update(self.list03)
        self._clear_condolence_fields()
        return True

    def _handle_condolence_update(self, values):
        """弔辞弔電を更新"""
        w4 = values.get('-w4-', False) is True
        l = [str(values.get('-input31-', '')), str(values.get('-input32-', '')),
             str(values.get('-input33-', '')), str(values.get('-input34-', '')),
             values.get('-w1-', False) is True,
             values.get('-w2-', False) is True,
             values.get('-w3-', False) is True,
             w4,
             values.get('-inputwa-', '') if w4 else '']
        self._ops().set_cd_msg(l, int(values.get('-input31-', 0)))
        self.list03 = self._ops().get_cd_msg(self.window)
        self.window['T3'].update(self.list03)
        self._clear_condolence_fields()
        return True

    def _handle_condolence_delete(self, values):
        """弔辞弔電を削除"""
        l = ['', '', '', '', False, False, False, False, '']
        self._ops().set_cd_msg(l, int(values.get('-input31-', 0)))
        self._ops().subt_sort_t3()
        self.list03 = self._ops().get_cd_msg(self.window)
        self.window['T3'].update(self.list03)
        self._clear_condolence_fields()
        return True

    def _handle_condolence_sort(self, values):
        """弔辞弔電を並べ替え"""
        self._ops().subt_sort_t3()
        self.list03 = self._ops().get_cd_msg(self.window)
        self.window['T3'].update(self.list03)
        return True

    def _clear_condolence_fields(self):
        """弔辞弔電入力フィールドをクリア"""
        for key in ['-input31-', '-input32-', '-input33-', '-input34-', '-inputwa-']:
            self.window[key].update('')
        for key in ['-w1-', '-w2-', '-w3-', '-w4-']:
            self.window[key].update(False)

    def _handle_offering_add(self, values):
        """供物を新規追加"""
        l = [str(values.get('-input41-', '')), str(values.get('-input43-', '')),
             str(values.get('-input44-', '')), str(values.get('-input45-', ''))]
        self._ops().set_of_input(l, 0)
        self.list04 = self._ops().get_of_input(self.window)
        self.window['T4'].update(self.list04)
        self._clear_offering_fields()
        return True

    def _handle_offering_update(self, values):
        """供物を更新"""
        no_str = str(values.get('-input41-', '')).strip()
        try:
            no_int = int(no_str)
        except (ValueError, TypeError):
            no_int = 0
        l = [no_str, str(values.get('-input43-', '')),
             str(values.get('-input44-', '')), str(values.get('-input45-', ''))]
        self._ops().set_of_input(l, no_int)
        self.list04 = self._ops().get_of_input(self.window)
        self.window['T4'].update(self.list04)
        self._clear_offering_fields()
        return True

    def _handle_offering_delete(self, values):
        """供物を削除"""
        no_str = str(values.get('-input41-', '')).strip()
        try:
            no_int = int(no_str)
        except (ValueError, TypeError):
            no_int = 0
        l = [no_str, None, None, None]
        self._ops().set_of_input(l, no_int)
        self.list04 = self._ops().get_of_input(self.window)
        self.window['T4'].update(self.list04)
        self._clear_offering_fields()
        return True

    def _handle_offering_sort(self, values):
        """供物を並べ替え"""
        self._ops().subt_sort_t4()
        self.list04 = self._ops().get_of_input(self.window)
        self.window['T4'].update(self.list04)
        return True

    def _clear_offering_fields(self):
        """供物入力フィールドをクリア"""
        for key in ['-input41-', '-input42-', '-input43-', '-input44-', '-input45-']:
            self.window[key].update('')

    def _handle_incense_add(self, values):
        """焼香順を新規追加"""
        s = str(values.get('-input52-', '')).split(' ')
        l = [str(values.get('-input51-', '')), str(values.get('-input53-', '')),
             str(values.get('-input54-', '')), str(values.get('-input55-', '')), s[0]]
        self._ops().insert_ince_bo(l)
        self.list05 = self._ops().get_ince_bo(self.window)
        self.window['T5'].update(self.list05)
        self._clear_incense_fields()
        return True

    def _handle_incense_update(self, values):
        """焼香順を更新"""
        l = [str(values.get('-input51-', '')), str(values.get('-input53-', '')),
             str(values.get('-input54-', '')), str(values.get('-input55-', ''))]
        self._ops().set_ince_bo(l)
        self.list05 = self._ops().get_ince_bo(self.window)
        self.window['T5'].update(self.list05)
        self._clear_incense_fields()
        return True

    def _handle_incense_delete(self, values):
        """焼香順を削除"""
        self._ops().del_ince_bo(int(values.get('-input51-', 0)))
        self.list05 = self._ops().get_ince_bo(self.window)
        self.window['T5'].update(self.list05)
        self._clear_incense_fields()
        return True

    def _handle_incense_sort(self, values):
        """焼香順を並べ替え"""
        self._ops().subt_sort_t5()
        self.list05 = self._ops().get_ince_bo(self.window)
        self.window['T5'].update(self.list05)
        return True

    def _clear_incense_fields(self):
        """焼香順入力フィールドをクリア"""
        for key in ['-input51-', '-input52-', '-input53-', '-input54-', '-input55-']:
            self.window[key].update('')

    def _handle_class_no_change(self, values):
        """種類NO変更時に名称を自動更新"""
        k = values.get('-input43-', '')
        if k and k in class_list:
            v = class_list[k]
            self.window['-input42-'].update(v[0] if isinstance(v, list) else v)
        return True

    def _handle_class_name_change(self, values):
        """名称変更時に種類NOを自動更新"""
        val = values.get('-input42-', '')
        keys = [k for k, v in class_list.items()
                if (v[0] if isinstance(v, list) else v) == val]
        if keys:
            self.window['-input43-'].update(keys[0])
        return True

    def _handle_t3_row_click(self, values):
        """弔辞弔電テーブル行クリック"""
        data = self.window['T3'].get()
        if not data or len(data) < 3:
            return True
        for key in ['-w1-', '-w2-', '-w3-', '-w4-']:
            self.window[key].update(False)
        self.window['-inputwa-'].update('')
        self.window['-input31-'].update(str(data[0]).zfill(3))
        self.window['-input32-'].update(str(data[1]))
        s = str(data[2]).replace(r'\n', '')
        ss = remove_parentheses(s)
        self.window['-input33-'].update(ss)
        if str(data[2]).find('(') >= 1:
            m = re.search(r'(?<=\().+?(?=\))', s)
            if m:
                text = m.group()
                if text == '線香　月':
                    self.window['-w1-'].update(True)
                elif text == '線香　哀星':
                    self.window['-w2-'].update(True)
                elif text == 'プリザーブドフラワー':
                    self.window['-w3-'].update(True)
                else:
                    self.window['-w4-'].update(True)
                    self.window['-inputwa-'].update(text)
        if len(data) >= 4 and data[3]:
            self.window['-input34-'].update(str(data[3]))
        return True

    def _handle_t4_row_click(self, values):
        """供物テーブル行クリック"""
        data = self.window['T4'].get()
        if not data or len(data) < 5:
            return True
        self.window['-input41-'].update(str(data[0]).zfill(3))
        self.window['-input42-'].update(str(data[1]))
        self.window['-input43-'].update(str(data[2]))
        self.window['-input44-'].update(str(data[3]))
        self.window['-input45-'].update(str(data[4]))
        return True

    def _handle_t5_row_click(self, values):
        """焼香順テーブル行クリック"""
        data = self.window['T5'].get()
        if not data or len(data) < 4:
            return True
        self.window['-input51-'].update(str(data[0]))
        ls = str(data[1]).split()
        try:
            no_int = int(data[0])
        except (ValueError, TypeError):
            no_int = 0
        if len(ls) >= 2 and ((no_int >= 81 and no_int < 999) or no_int == 1000):
            role_val = str(ls[0])
            ls.pop(0)
            name_val = ' '.join(ls)
        else:
            role_val = str(data[1])
            name_val = str(data[1])
        self.window['-input52-'].update('' if role_val == name_val else role_val)
        self.window['-input53-'].update(name_val)
        self.window['-input54-'].update(str(data[2]))
        self.window['-input55-'].update(str(data[3]))
        return True

    def _handle_t6_row_click(self, values):
        """供花料テーブル行クリック"""
        data = self.window['T6'].get()
        if not data or len(data) < 5:
            return True
        self.window['-input61-'].update(str(data[0]).zfill(3))
        self.window['-input62-'].update(str(data[1]))
        self.window['-input63-'].update(str(data[2]))
        self.window['-input64-'].update(str(data[3]))
        self.window['-input65-'].update(str(data[4]))
        return True

    def _handle_koden_word_export(self, values):
        """香典Wordエクスポート処理"""
        print("別紙(Word)ボタンが押されました")
        return True

    def _handle_koden_excel_export(self, values):
        """香典Excelエクスポート処理"""
        print("別紙(Excel)ボタンが押されました")
        return True
