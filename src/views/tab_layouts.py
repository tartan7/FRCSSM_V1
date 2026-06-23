"""
各入力タブのレイアウト定義
gui04.py から移植。gv.list* 依存をパラメータ化、gl.* を data.list_data に変更。
"""
import TkEasyGUI as sg
from tkinter import ttk
from data.list_data import role_list, class_list

header01 = ['NO', '葬儀内役職', '会社名・役職・名前']
header03 = ['NO', '会社名', '御芳名/付帯物', '並替え']
header04 = ['NO', '名称', '種類NO', '個数', '寄贈者名']
header05 = ['NO', '葬儀内役職・会社名・役職・名前', 'フリガナ', 'フリガナの長さ']
header06 = ['NO', '金額', '住所', '名前', '領収証']

width01 = [5, 15, 35]
width03 = [5, 25, 25, 5]
width04 = [5, 15, 7, 7, 20]
width05 = [5, 30, 25, 5]
width06 = [5, 10, 20, 20, 5]


def _set_table_style():
    style = ttk.Style()
    style.configure("Treeview", font=('Meiryo UI', 16), rowheight=50)
    style.configure("Treeview.Heading", font=('Meiryo UI', 16, 'bold'))


def _create_frame021():
    return sg.Frame(layout=[
        [sg.Text(text='会葬者数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii01"),
         sg.InputText(key='-input021-', default_text='', size=(10, 1), font=('Meiryo UI', 16))],
        [sg.Text(text='僧侶数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii02"),
         sg.InputText(key='-input022-', default_text='', size=(10, 1), font=('Meiryo UI', 16), enable_events=True)],
        [sg.Text(text='花輪数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii03"),
         sg.InputText(key='-input023-', default_text='', size=(10, 1), font=('Meiryo UI', 16))],
        [sg.Text(text='葬儀役員数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii04"),
         sg.InputText(key='-input024-', default_text='', size=(10, 1), font=('Meiryo UI', 16))],
    ], key='f021', title='通夜', text='通夜', fg='#FFFFFF', bg='#0000FF',
        anchor='c', font=('Meiryo UI', 20, 'bold'), relief='sunken')


def _create_frame022():
    return sg.Frame(layout=[
        [sg.Text(text='会葬者数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii05"),
         sg.InputText(key='-input025-', default_text='', size=(10, 1), font=('Meiryo UI', 16))],
        [sg.Text(text='僧侶数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii06"),
         sg.InputText(key='-input026-', default_text='', size=(10, 1), font=('Meiryo UI', 16))],
        [sg.Text(text='花輪数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii07"),
         sg.InputText(key='-input027-', default_text='', size=(10, 1), font=('Meiryo UI', 16))],
        [sg.Text(text='葬儀役員数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii08"),
         sg.InputText(key='-input028-', default_text='', size=(10, 1), font=('Meiryo UI', 16))],
    ], key='f022', title='葬儀', text='葬儀', fg='#FFFFFF', bg='#0000FF',
        anchor='c', font=('Meiryo UI', 20, 'bold'), relief='sunken')


def _create_frame023():
    return sg.Frame(layout=[
        [sg.Text(text='御布施袋：導師', size=(16, 1), font=('Meiryo UI', 14, "bold"), anchor='e', key="ii09"),
         sg.InputText(key='-input029-', default_text='1', size=(6, 1), font=('Meiryo UI', 12)),
         sg.Button("印刷", key='iip09')],
        [sg.Text(text='御布施袋：脇僧/院号料', size=(16, 1), font=('Meiryo UI', 14, "bold"), anchor='e', key="ii1A", pad=((0, 0), (0, 0))),
         sg.InputText(key='-input02A-', default_text='', size=(6, 1), font=('Meiryo UI', 12)),
         sg.Button("印刷", key='iip0A')],
        [sg.Text(text='御足袋料', size=(16, 1), font=('Meiryo UI', 14, "bold"), anchor='e', key="ii1B"),
         sg.InputText(key='-input02B-', default_text='1', size=(6, 1), font=('Meiryo UI', 12)),
         sg.Button("印刷", key='iip0B')],
        [sg.Text(text='御車代', size=(16, 1), font=('Meiryo UI', 14, "bold"), anchor='e', key="ii1C"),
         sg.InputText(key='-input02C-', default_text='0', size=(6, 1), font=('Meiryo UI', 12)),
         sg.Button("印刷", key='iip0C')],
        [sg.Text(text='新亡供養料\n(禅徳寺のみ)', size=(16, 2), font=('Meiryo UI', 14, "bold"), anchor='e', key="ii1D", pad=((0, 0), (0, 0))),
         sg.InputText(key='-input02D-', default_text='0', size=(6, 1), font=('Meiryo UI', 12), pad=((15, 0), (0, 0))),
         sg.Button("印刷", key='iip0D', pad=((10, 10), (0, 0)))],
    ], key='f023', title='袋印刷', text='袋印刷', fg='#FFFFFF', bg='#0000FF',
        anchor='w', font=('Meiryo UI', 15, 'bold'), relief='sunken')


def _create_frame024():
    return sg.Frame(layout=[
        [sg.Text(text='白無地封筒', size=(8, 1), font=('Meiryo UI', 14, "bold"), anchor='e', key="ii0e"),
         sg.InputText(key='-input02e-', default_text='寸志', size=(8, 1), font=('Meiryo UI', 14)),
         sg.Button("印刷", key='iip0e')],
        [sg.InputText(key='-input02f-', default_text='火葬場', size=(9, 1), font=('Meiryo UI', 14), anchor='e', pad=(110, 0))],
        [sg.Text(text='水引付', size=(8, 1), font=('Meiryo UI', 14, "bold"), anchor='e', key="ii1g"),
         sg.InputText(key='-input02g-', default_text='戒名料', size=(8, 1), font=('Meiryo UI', 14)),
         sg.Button("印刷", key='iip0g')],
    ], key='f024', title='その他印刷', text='その他印刷', fg='#FFFFFF', bg='#0000FF',
        anchor='w', size=(100, 150), font=('Meiryo UI', 15, 'bold'), relief='sunken')


def _create_frame06(list06=None):
    _set_table_style()
    data = list06 if list06 is not None else []
    table = sg.Table(data, header06, key='T6',
                     col_widths=width06, auto_size_columns=True, anchor='w',
                     select_mode="browse", expand_x=True, expand_y=True,
                     enable_events=True, event_returns_values=True)
    return sg.Frame(layout=[[sg.Column([[table]], size=(800, 250))]],
                    title='供花料一覧', text='供花料一覧', fg='#0000FF',
                    size=(800, 380), font=('Meiryo UI', 24, 'bold'), relief='sunken')


def _create_frame16():
    return sg.Frame(layout=[
        [sg.Text(text='番号', size=(6, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii61"),
         sg.InputText(key='-input61-', default_text='', size=(5, 1), font=('Meiryo UI', 16), enable_events=True, pad=((0, 20), (0, 0))),
         sg.Text(text='金額', size=(6, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii62"),
         sg.InputText(key='-input62-', default_text='', size=(12, 1), font=('Meiryo UI', 16), pad=((0, 55), (0, 0))),
         sg.Text(text='領収証', size=(6, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii65"),
         sg.Combo(list(['○', ' ']), default_value=' ', key='-input65-', size=(5, 5), font=('Meiryo UI', 16))],
        [sg.Text(text='郵便番号', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e'),
         sg.InputText(key='-input6z-', default_text='', size=(12, 1), font=('Meiryo UI', 16), pad=((0, 10), (0, 0))),
         sg.Button('住所検索', font=('Meiryo UI', 12, "bold"), key='-read6Z-', size=(10, 1), button_color=('white', '#228B22'))],
        [sg.Text(text='住所', size=(6, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii63"),
         sg.InputText(key='-input63-', default_text='', size=(45, 2), font=('Meiryo UI', 16))],
        [sg.Text(text='名前', size=(6, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii64"),
         sg.Multiline(key='-input64-', default_text='', size=(44, 3), font=('Meiryo UI', 16))],
        [sg.Submit('新規で追加', font=('Meiryo UI', 12, "bold"), key='-read6A-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記内容で更新', font=('Meiryo UI', 12, "bold"), key='-read6B-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記を削除', font=('Meiryo UI', 12, "bold"), key='-read6C-', size=(14, 1), button_color=('white', '#0000ff'))],
    ], title='編集', text='編集', fg='#0000FF', size=(820, 460), font=('Meiryo UI', 16, 'bold'), relief='sunken')


def _create_frame03(list03=None):
    _set_table_style()
    data = list03 if list03 is not None else []
    return sg.Frame(layout=[[
        sg.Column([[sg.Table(data, header03, key='T3',
                             col_widths=width03, auto_size_columns=False, font=('Meiryo UI', 14),
                             anchor='w', vertical_scroll_only=False, enable_events=True,
                             event_returns_values=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE)]],
                  size=(800, 250))
    ]], title='弔辞弔電一覧', text='弔辞弔電一覧', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')


def _create_frame13():
    frame131 = sg.Frame(layout=[
        [sg.Checkbox(text='線香　月', key='-w1-', default=False, font=('Meiryo UI', 16), width=6),
         sg.Checkbox(text='線香　哀星', key='-w2-', default=False, font=('Meiryo UI', 16), width=8),
         sg.Checkbox(text='プリザーブドフラワー', key='-w3-', default=False, font=('Meiryo UI', 16), width=12),
         sg.Checkbox(text='その他', key='-w4-', default=False, font=('Meiryo UI', 16), width=4),
         sg.InputText(key='-inputwa-', default_text='', size=(12, 1), font=('Meiryo UI', 16))],
    ], title='付帯物', text='付帯物', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')

    return sg.Frame(layout=[
        [sg.Text(text='番号', size=(12, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii31"),
         sg.InputText(key='-input31-', default_text='', size=(10, 1), font=('Meiryo UI', 16)),
         sg.Text(text='並び替え', size=(12, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii34"),
         sg.InputText(key='-input34-', default_text='', size=(6, 2), font=('Meiryo UI', 16))],
        [sg.Text(text='会社名', size=(12, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii32"),
         sg.Multiline(key='-input32-', default_text='', size=(40, 2), font=('Meiryo UI', 16))],
        [sg.Text(text='御芳名', size=(12, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii33"),
         sg.Multiline(key='-input33-', default_text='', size=(40, 2), font=('Meiryo UI', 16))],
        [frame131],
        [sg.Submit('新規で追加', font=('Meiryo UI', 12, "bold"), key='-read3A-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記内容で更新', font=('Meiryo UI', 12, "bold"), key='-read3B-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記を削除', font=('Meiryo UI', 12, "bold"), key='-read3C-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記を並べ替え', font=('Meiryo UI', 12, "bold"), key='-read3D-', size=(14, 1), button_color=('white', '#0000ff'))],
    ], title='編集', text='編集', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')


def _create_frame04(list04=None):
    _set_table_style()
    data = list04 if list04 is not None else []
    return sg.Frame(layout=[[
        sg.Column([[sg.Table(data, header04, key='T4',
                             col_widths=width04, auto_size_columns=False, font=('Meiryo UI', 14),
                             anchor='w', vertical_scroll_only=False, enable_events=True,
                             event_returns_values=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE)]],
                  size=(750, 250))
    ]], title='供物一覧', text='供物一覧', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')


def _create_frame14():
    return sg.Frame(layout=[
        [sg.Text(text='番号(順番)', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii41"),
         sg.InputText(key='-input41-', default_text='', size=(20, 1), font=('Meiryo UI', 16)),
         sg.Text(text='種類NO', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii43"),
         sg.Combo(list(class_list.keys()), key='-input43-', size=(20, 10), font=('Meiryo UI', 16), enable_events=True)],
        [sg.Text(text='名称', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii42"),
         sg.Combo(values=[v[0] if isinstance(v, list) else v for v in class_list.values()],
                  key='-input42-', size=(20, 5), font=('Meiryo UI', 16), enable_events=True),
         sg.Text(text='個数', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii44"),
         sg.Combo(list(['1', '1対']), key='-input44-', size=(20, 3), font=('Meiryo UI', 16))],
        [sg.Text(text='寄贈者名', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii45"),
         sg.Multiline(key='-input45-', default_text='', size=(40, 2), font=('Meiryo UI', 16))],
        [sg.Submit('新規で追加', font=('Meiryo UI', 12, "bold"), key='-read4A-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記内容で更新', font=('Meiryo UI', 12, "bold"), key='-read4B-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記を削除', font=('Meiryo UI', 12, "bold"), key='-read4C-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記を並び替え', font=('Meiryo UI', 12, "bold"), key='-read4D-', size=(14, 1), button_color=('white', '#0000ff'))],
    ], title='編集', text='編集', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')


def _create_frame05(list05=None):
    _set_table_style()
    data = list05 if list05 is not None else []
    return sg.Frame(layout=[[
        sg.Column([[sg.Table(data, header05, key='T5',
                             col_widths=width05, auto_size_columns=False, font=('Meiryo UI', 14),
                             anchor='w', vertical_scroll_only=False, enable_events=True,
                             event_returns_values=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE)]],
                  size=(750, 250))
    ]], title='焼香順一覧', text='焼香順一覧', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')


def _create_frame15():
    return sg.Frame(layout=[
        [sg.Text(text='番号(順番)', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii51"),
         sg.InputText(key='-input51-', default_text='', size=(10, 1), font=('Meiryo UI', 16)),
         sg.Text(text='葬儀内役職', size=(10, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii52"),
         sg.Combo(list(role_list.values()), key='-input52-', size=(20, len(role_list)), font=('Meiryo UI', 16), enable_events=True)],
        [sg.Text(text='会社名・役職・名前', size=(10, 2), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii53"),
         sg.Multiline(key='-input53-', default_text='', size=(40, 3), font=('Meiryo UI', 16), enable_events=True)],
        [sg.Text(text='フリガナ', size=(8, 1), font=('Meiryo UI', 16, "bold"), anchor='e', key="ii54"),
         sg.InputText(key='-input54-', default_text='', size=(20, 2), font=('Meiryo UI', 16)),
         sg.InputText(key='-input55-', default_text='', size=(15, 1), font=('Meiryo UI', 16))],
        [sg.Submit('新規で追加', font=('Meiryo UI', 12, "bold"), key='-read5A-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記内容で更新', font=('Meiryo UI', 12, "bold"), key='-read5B-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記を削除', font=('Meiryo UI', 12, "bold"), key='-read5C-', size=(14, 1), button_color=('white', '#0000ff')),
         sg.Submit('上記を並べ替え', font=('Meiryo UI', 12, "bold"), key='-read5D-', size=(14, 1), button_color=('white', '#0000ff'))],
    ], title='編集', text='編集', fg='#0000FF', font=('Meiryo UI', 16, 'bold'), relief='sunken')


def get_tab_layout(tab_name: str, list01=None, list03=None, list04=None, list05=None, list06=None):
    """タブ名に対応するレイアウトを返す。テーブルの初期データはパラメータで受け取る。"""
    tab1_layout = [
        [_create_frame021(), _create_frame022()],
        [sg.Submit('上記内容で更新', font=('Meiryo UI', 15, "bold"), key='-upd02-', size=(22, 1), button_color=('white', '#0000ff'))],
        [_create_frame023(), _create_frame024()],
    ]
    tab2_layout = [
        [_create_frame06(list06)],
        [_create_frame16()],
    ]
    tab3_layout = [
        [_create_frame03(list03)],
        [_create_frame13()],
    ]
    tab4_layout = [
        [_create_frame04(list04)],
        [_create_frame14()],
    ]
    tab5_layout = [
        [_create_frame05(list05)],
        [_create_frame15()],
    ]

    tab_frames = {
        'tab1': ('施工状況入力/袋印刷', tab1_layout),
        'tab2': ('供花料入力', tab2_layout),
        'tab3': ('弔辞弔電入力', tab3_layout),
        'tab4': ('供物入力', tab4_layout),
        'tab5': ('焼香順入力', tab5_layout),
    }
    title, inner_layout = tab_frames.get(tab_name, ('', []))
    tab_group = sg.Frame(title=title, font=('Meiryo UI', 15, "bold"), fg='#FFFFFF', bg='#0000FF',
                         layout=inner_layout, relief='sunken')

    s_btn_close = sg.Submit(button_text='Topへ戻る', key='-Close-',
                            button_color=('#0000FF', '#FFF'), font=('Meiryo UI', 12, "bold"), size=(16, 1))
    return [[tab_group], [s_btn_close]]
