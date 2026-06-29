"""
メインウィンドウのレイアウト定義
gui01.py から移植。外部依存なし。
"""
import TkEasyGUI as sg


def get_main_layout():
    """メインウィンドウのレイアウトを返す"""
    s_button_18 = sg.Submit(button_text='施工状況入力・袋印刷', key='-sm18-',
                            background='#FFFFFF', foreground='#00FF00',
                            font=('Meiryo UI', 20, "bold"), size=(22, 1), padx=12)
    s_button_08 = sg.Submit(button_text='フォルダ作成・設定', key='-sm08-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_00 = sg.Submit(button_text='基本情報・\n施工情報入力', key='-sm00-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_01 = sg.Submit(button_text='香典入力', key='-sm01-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_02 = sg.Submit(button_text='供花料入力', key='-sm02-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_03 = sg.Submit(button_text='弔辞弔電入力', key='-sm03-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_04 = sg.Submit(button_text='会計情報入力', key='-sm04-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_05 = sg.Submit(button_text='供物入力', key='-sm05-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_06 = sg.Submit(button_text='焼香順入力', key='-sm06-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_07 = sg.Submit(button_text='葬儀役員入力', key='-sm07-',
                            background='#FFFFFF', foreground='#808080',
                            font=('Meiryo UI', 9, "bold"), size=(9, 1), disabled=True)
    s_button_09 = sg.Submit(button_text='別紙作成', key='-sm09-',
                            background='#FFFFFF', foreground='#808080',
                            font=('Meiryo UI', 9, "bold"), size=(9, 1), disabled=True)
    s_button_10 = sg.Submit(button_text='CD下準備&\n作成', key='-sm10-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_11 = sg.Submit(button_text='領収書チェック', key='-sm11-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_12 = sg.Submit(button_text='清書出力', key='-sm13-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_13 = sg.Submit(button_text='詳細設定', key='-sm14-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_14 = sg.Submit(button_text='終了', key='-Quit-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_15 = sg.Submit(button_text='通夜集計', key='-sm15-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_16 = sg.Submit(button_text='葬儀集計', key='-sm16-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_17 = sg.Submit(button_text='寺院詳細別紙作成・出力', key='-sm17-',
                            background='#FFFFFF', foreground='#0000FF',
                            font=('Meiryo UI', 9, "bold"), size=(16, 1))

    frame01 = sg.Frame(layout=[[s_button_08, s_button_00, s_button_13]],
                       title='初期設定', text='初期設定', fg='white', bg='#4472C4',
                       font=('Meiryo UI', 16, 'bold'), relief='sunken', anchor='nw')

    frame01a = sg.Frame(layout=[
        [s_button_02, s_button_03, s_button_05],
        [s_button_04, s_button_06, s_button_01],
        [s_button_18],
        [s_button_09, s_button_07, s_button_17],
    ],
        title='入力操作', text='入力操作', fg='white', bg='#4472C4',
        font=('Meiryo UI', 16, 'bold'), relief='sunken', anchor='nw')

    frame02 = sg.Frame(layout=[[s_button_15, s_button_16, s_button_11]],
                       title='集計作業', text='集計作業', fg='white', bg='#4472C4',
                       font=('Meiryo UI', 16, 'bold'), relief='sunken', anchor='nw')

    frame03 = sg.Frame(layout=[[s_button_12, s_button_10, s_button_14]],
                       title='〆作業', text='〆作業', fg='white', bg='#4472C4',
                       font=('Meiryo UI', 16, 'bold'), relief='sunken', anchor='nw')

    return [
        [sg.Column([[frame01]], anchor='nw', expand_x=True)],
        [sg.Column([[frame01a]], anchor='nw', expand_x=True)],
        [sg.Column([[frame02]], anchor='nw', expand_x=True)],
        [sg.Column([[frame03]], anchor='nw', expand_x=True)],
    ]
