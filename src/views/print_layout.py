"""
清書出力ウィンドウのレイアウト定義
gui13.py から移植。
"""
import TkEasyGUI as sg


def get_print_layout(vix_path: str = r"C:\vix221\ViX.exe") -> list:
    """清書出力ウィンドウのレイアウトを返す"""

    frame_sheets = sg.Frame(layout=[
        [sg.Checkbox('基本情報(1,2)', key='-k1-', default=True,  font=('Meiryo UI', 16)),
         sg.Checkbox('葬儀役員(3)',   key='-k3-', default=False, font=('Meiryo UI', 16))],
        [sg.Checkbox('施工状況(4)',   key='-k4-', default=True,  font=('Meiryo UI', 16)),
         sg.Checkbox('会計情報(5)',   key='-k5-', default=True,  font=('Meiryo UI', 16))],
        [sg.Checkbox('弔辞弔電(6)',   key='-k6-', default=False, font=('Meiryo UI', 16)),
         sg.Checkbox('供物(7)',       key='-k7-', default=False, font=('Meiryo UI', 16))],
        [sg.Checkbox('焼香順(8)',     key='-k8-', default=False, font=('Meiryo UI', 16)),
         sg.Checkbox('供花料(9,10)', key='-k9-', default=False, font=('Meiryo UI', 16))],
    ], title='書式類', text='書式類', fg='#0000FF',
       font=('Meiryo UI', 16, 'bold'), relief='sunken')

    frame_koden = sg.Frame(layout=[
        [sg.Checkbox('香典(受付順)(A,B)', key='-k1A-', default=False, font=('Meiryo UI', 16))],
        [sg.Checkbox('香典(50音順)(C,D)', key='-k1C-', default=False, font=('Meiryo UI', 16))],
        [sg.Radio('50音順(昇順)', key='-k250-',  group_id='koden_sort', default=True,  font=('Meiryo UI', 16)),
         sg.Radio('区分毎',       key='-k2cls-', group_id='koden_sort', default=False, font=('Meiryo UI', 16))],
        [sg.Radio('金額:昇順',   key='-k2A-',   group_id='koden_amt',  default=True,  font=('Meiryo UI', 16)),
         sg.Radio('金額:降順',   key='-k2D-',   group_id='koden_amt',  default=False, font=('Meiryo UI', 16))],
    ], title='香典帳', text='香典帳', fg='#0000FF',
       font=('Meiryo UI', 16, 'bold'), relief='sunken')

    frame_photo = sg.Frame(layout=[
        [sg.Checkbox('供物写真', key='-k71-', default=False, font=('Meiryo UI', 16))],
        [sg.Text('写真原本フォルダ', font=('Meiryo UI', 12, 'bold'))],
        [sg.InputText(key='-pic_dir-', default_text='', font=('Meiryo UI', 9), size=(16, 1)),
         sg.FolderBrowse('開く', font=('Meiryo UI', 9), default_path='', key='filebtn71', target_key='-pic_dir-')],
        [sg.Text('プログラムパス', font=('Meiryo UI', 12, 'bold'))],
        [sg.InputText(key='-inputd1-', default_text=vix_path, font=('Meiryo UI', 10), size=(24, 1))],
    ], title='供物写真', text='供物写真', fg='#0000FF',
       font=('Meiryo UI', 16, 'bold'), relief='sunken')

    return [
        [frame_sheets],
        [frame_koden, frame_photo],
        [sg.Submit('Topへ戻る', key='-Close-', font=('Meiryo UI', 12, 'bold'), size=(12, 2)),
         sg.Submit('印刷',       key='-Print-', font=('Meiryo UI', 12, 'bold'), size=(12, 2))],
    ]
