"""
フォルダ作成・設定ウィンドウのレイアウト定義
gui08.py から移植。gv / func1 依存をパラメータ化。
"""
import TkEasyGUI as sg
import os
import datetime


def _get_day_result() -> str:
    """今日の月日を MMDD 形式で返す"""
    try:
        now = datetime.date.today()
        return f"{now.month:02d}{now.day:02d}"
    except Exception:
        return "0101"


def update_folder_name(window, values) -> None:
    """遺族名が入力されたときに作成フォルダ名を更新する"""
    if values.get('-x_dir2-'):
        day_result = _get_day_result()
        base_path = os.path.dirname(values.get('-x_dir-', ''))
        new_folder_name = f"{day_result}{values['-x_dir2-']}"
        new_path = os.path.join(base_path, new_folder_name)
        window['-x_dir-'].update(new_path)


def get_folder_layout(basepath: str, tpath1: str, tpath2: str, tpath3: str,
                      tmppath: str, x_dir2: str) -> list:
    """フォルダ作成・設定ウィンドウのレイアウトを返す"""
    s_inp_04 = sg.InputText(key='-ini_dir-', default_text=basepath,
                            font=('Meiryo UI', 16), size=(32, 1))
    s_fbtn_04 = sg.FolderBrowse('開く', font=('Meiryo UI', 16),
                                default_path=basepath, key='filebtn1')
    s_inp_05 = sg.InputText(key='-wrk_dir-',
                            default_text=basepath + '\\' + tpath1 + '\\' + tpath2,
                            font=('Meiryo UI', 16), size=(32, 1))
    s_fbtn_05 = sg.FolderBrowse('開く', font=('Meiryo UI', 16),
                                default_path=basepath + '\\' + tpath1 + '\\' + tpath2,
                                key='filebtn2')
    s_inp_06 = sg.InputText(key='-x_dir-', default_text=tmppath,
                            font=('Meiryo UI', 16), size=(32, 1))
    s_fbtn_06 = sg.FolderBrowse('開く', font=('Meiryo UI', 16),
                                default_path=basepath + '\\' + tpath3 + '\\',
                                key='filebtn3', target_key='-x_dir-', enable_events=True)
    s_inp_07 = sg.InputText(key='-x_dir2-', default_text=x_dir2,
                            font=('Meiryo UI', 16), size=(20, 1), enable_events=True)

    frame81 = sg.Frame(layout=[
        [sg.Text(text='初期フォルダ名', size=(16, 1), font=('Meiryo UI', 14)), s_inp_04, s_fbtn_04],
        [sg.Text(text='テンプレートフォルダ名', size=(16, 1), font=('Meiryo UI', 14)), s_inp_05, s_fbtn_05],
        [sg.Text(text='作成フォルダ名', size=(16, 1), font=('Meiryo UI', 14)), s_inp_06, s_fbtn_06],
        [sg.Text(text='遺族名', size=(16, 1), font=('Meiryo UI', 14)), s_inp_07],
    ], title='フォルダ設定', text='フォルダ設定', fg='#0000FF',
        font=('Meiryo UI', 16, 'bold'), relief='sunken')

    s_button_82 = sg.Submit(button_text='フォルダ作成', key='-su82-',
                            button_color=('#0000FF', '#FFF'), font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_83 = sg.Submit(button_text='フォルダ設定', key='-su83-',
                            button_color=('#0000FF', '#FFF'), font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_84 = sg.Submit(button_text='戻る', key='-Close-',
                            button_color=('#0000FF', '#FFF'), font=('Meiryo UI', 12, "bold"), size=(12, 3))

    return [[frame81], [s_button_82, s_button_83, s_button_84]]
