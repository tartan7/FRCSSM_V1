"""
詳細設定ウィンドウのレイアウト定義
gui14.py から移植。gv / gl / func1 依存を除去。
"""
import os
import TkEasyGUI as sg
import config
from data.list_data import (
    company_name, company_addr, company_tel,
    temple_list, venue_list_0, class_list, role_list, fform_list,
)


def _build_choices():
    tt_choice = [f"{k}/{v[0]}/{v[1]}/{v[2]}/{v[3]}/{v[4]}" for k, v in temple_list.items()]
    va_choice = [f"{k}/{v[0]}/{v[3]}/{v[4]}" for k, v in venue_list_0.items()]
    ffm_choice = [f"{k}/{v[0]}" for k, v in class_list.items()]
    ro_choice = [f"{k}/{v[0]}/{v[1]}/{v[2]}" for k, v in role_list.items()]
    cc_choice = [f"{k}/{v[0]}/{v[1]}/{v[2]}" for k, v in fform_list.items()]
    return tt_choice, va_choice, ffm_choice, ro_choice, cc_choice


def get_settings_layout(basepath: str = "", template_path: str = "", cdpath: str = "") -> list:
    """詳細設定ウィンドウのレイアウトを返す。

    Args:
        basepath: 初期フォルダ（終了分）。config.ini の basepath。
        template_path: テンプレートフォルダ（初期テンプレート/最新）。
        cdpath: CD作成フォルダ名。
    """
    tt_choice, va_choice, ffm_choice, ro_choice, cc_choice = _build_choices()

    basepath = basepath or config.BASE_PATH
    if not template_path:
        parent = os.path.dirname(os.path.normpath(basepath))
        template_path = os.path.join(parent, config.TPATH1, config.TPATH2)
    cdpath = cdpath or config.CDPATH

    frame01 = sg.Frame(layout=[
        [sg.Text(text='会社名', size=(12, 1), font=('Meiryo UI', 14)),
         sg.InputText(key='-cname-', default_text=company_name, font=('Meiryo UI', 16), size=(25, 1), readonly=True)],
        [sg.Text(text='住所', size=(12, 1), font=('Meiryo UI', 14)),
         sg.InputText(key='-caddress-', default_text=company_addr, font=('Meiryo UI', 16), size=(25, 1), readonly=True)],
        [sg.Text(text='電話番号', size=(12, 1), font=('Meiryo UI', 14)),
         sg.InputText(key='-ctel-', default_text=company_tel, font=('Meiryo UI', 16), size=(25, 1), readonly=True)],
    ], title='会社設定', text='会社設定', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')

    frame02 = sg.Frame(layout=[
        [sg.Text(text='初期フォルダ名', size=(16, 1), font=('Meiryo UI', 14)),
         sg.InputText(key='-ini_dir-', default_text=basepath, font=('Meiryo UI', 16), size=(30, 1)),
         sg.FolderBrowse('開く', font=('Meiryo UI', 16), initial_folder=basepath, key='filebtn1')],
        [sg.Text(text='テンプレートフォルダ名', size=(16, 1), font=('Meiryo UI', 14)),
         sg.InputText(key='-wrk_dir-', default_text=template_path,
                      font=('Meiryo UI', 16), size=(30, 1)),
         sg.FolderBrowse('開く', font=('Meiryo UI', 16),
                         initial_folder=template_path, key='filebtn2')],
        [sg.Text(text='CD作成フォルダ名', size=(16, 1), font=('Meiryo UI', 14), pad=((0, 10), (0, 0))),
         sg.InputText(key='-cd_dir-', default_text=cdpath + '\\', font=('Meiryo UI', 16),
                      size=(34, 1), pad=((0, 0), (0, 0)))],
    ], title='フォルダ設定', text='フォルダ設定', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')

    combo_settings = {'size': (45, 4), 'font': ('Meiryo UI', 12), 'enable_events': True, 'readonly': True}

    s_button_10 = sg.Button('ここを編集', key='-su10-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 1))
    s_button_11 = sg.Button('ここを編集', key='-su11-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 1))
    s_button_12 = sg.Button('ここを編集', key='-su12-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 1))
    s_button_13 = sg.Button('ここを編集', key='-su13-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 1))
    s_button_14 = sg.Button('ここを編集', key='-su14-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 1))
    s_button_x1 = sg.Button('入力項目を\n設定する', key='-suX1-', button_color=('#0000FF', '#FFF'),
                             font=('Meiryo UI', 12, "bold"), size=(12, 2))
    s_button_x2 = sg.Button('Topへ戻る', key='-Close-', button_color=('#0000FF', '#FFF'),
                             font=('Meiryo UI', 12, "bold"), size=(12, 2))

    settings_layout = [
        [sg.Text('会場設定', size=(12, 1), font=('Meiryo UI', 14, "bold")),
         sg.Frame('', [[sg.Combo(va_choice, key='venue', expand_x=False, **combo_settings)]], size=(350, 35), pad=(0, 0), borderwidth=0),
         sg.Column([[s_button_10]], pad=((5, 0), (0, 0)))],
        [sg.Text('寺院設定', size=(12, 1), font=('Meiryo UI', 14, "bold")),
         sg.Frame('', [[sg.Combo(tt_choice, key='temple', expand_x=False, **combo_settings)]], size=(350, 35), pad=(0, 0), borderwidth=0),
         sg.Column([[s_button_11]], pad=((5, 0), (0, 0)))],
        [sg.Text('供物表設定', size=(12, 1), font=('Meiryo UI', 14, "bold")),
         sg.Frame('', [[sg.Combo(ffm_choice, key='f_format', expand_x=True, **combo_settings)]], size=(350, 35), pad=(0, 0), borderwidth=0),
         sg.Column([[s_button_12]], pad=((5, 0), (0, 0)))],
        [sg.Text('葬儀役員設定', size=(12, 1), font=('Meiryo UI', 14, "bold")),
         sg.Frame('', [[sg.Combo(ro_choice, key='role', expand_x=True, **combo_settings)]], size=(350, 35), pad=(0, 0), borderwidth=0),
         sg.Column([[s_button_13]], pad=((5, 0), (0, 0)))],
        [sg.Text('施工設定', size=(12, 1), font=('Meiryo UI', 14, "bold")),
         sg.Frame('', [[sg.Combo(cc_choice, key='const', expand_x=True, **combo_settings)]], size=(350, 35), pad=(0, 0), borderwidth=0),
         sg.Column([[s_button_14]], pad=((5, 0), (0, 0)))],
    ]

    button_layout = [[sg.Column([[s_button_x1]], pad=(0, 0)),
                      sg.Push(),
                      sg.Column([[s_button_x2]], pad=(0, 0))]]

    return [
        [frame01],
        [frame02],
        [sg.Frame('', settings_layout, borderwidth=0, pad=(20, 10))],
        [sg.Column(button_layout, expand_x=True, pad=(20, 10))],
    ]
