"""
香典入力ウィンドウのレイアウト定義
gui03.py から移植。global_value 依存を config に置き換え済み。
"""
import TkEasyGUI as sg
import config


def get_koden_layout():
    """香典入力ウィンドウのレイアウトを返す"""
    a_choice = ('10', '20', '30', '40', '50', '60')

    s_inp_01 = sg.InputText(key='-start_range-', default_text="1", font=('Meiryo UI', 16), size=(6, 1))
    s_inp_02 = sg.InputText(key='-end_range-', default_text=config.DEFAULT_STEP, font=('Meiryo UI', 16), size=(6, 1))
    s_c001 = sg.Combo(a_choice, size=(8, len(a_choice)), font=('Meiryo UI', 16, "bold"),
                      key='-bunch-', default_value=config.DEFAULT_STEP, enable_events=True)
    s_inp_0x = sg.Combo(values=[i for i in range(1, config.MAX_VAL, config.DEFAULT_STEP)],
                        key='-rng_btn-', size=(6, 1), font=('Meiryo UI', 12, "bold"), enable_events=True)

    s_inp_03 = sg.Input(key='-i_price-', default_text=",000", font=('Meiryo UI', 16), size=(16, 1))
    s_inp_06 = sg.InputText(key='-i_furigana-', default_text="", font=('Meiryo UI', 16), size=(24, 1))
    s_inp_07 = sg.Multiline(key='-i_name-', default_text="", font=('Meiryo UI', 16), size=(40, 4), enable_events=True)
    s_inp_10 = sg.Multiline(key='-i_address-', default_text="住所", font=('Meiryo UI', 16), size=(40, 4), enable_events=True)

    s_button_61 = sg.Submit(button_text='別紙(Word)', key='-Om1-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 1), disabled=True)
    s_button_62 = sg.Submit(button_text='別紙(Excel)', key='-Om2-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 1), disabled=True)
    s_button_91 = sg.Submit(button_text='更新・前へ', key='-Update_Prev-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 2))
    s_button_92 = sg.Submit(button_text='更新・次へ', key='-Update_Next-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 2))
    s_button_93 = sg.Submit(button_text='Topへ戻る', key='-Close-', button_color=('#0000FF', '#FFF'),
                            font=('Meiryo UI', 12, "bold"), size=(12, 2))

    frame01 = sg.Frame(layout=[
        [sg.Text(text='範囲', size=(10, 1), font=('Meiryo UI', 12, "bold")),
         s_inp_01, sg.Text(text='～', size=(2, 1)), s_inp_02, s_inp_0x,
         sg.Text(text='束単位', size=(4, 1), font=('Meiryo UI', 12, "bold")), s_c001],
        [sg.Text(text='現在のNo', size=(10, 1), font=('Meiryo UI', 12, "bold")),
         sg.InputText(key='-i_no-', default_text="1", font=('Meiryo UI', 16), size=(6, 1), enable_events=True),
         sg.Combo(values=[i for i in range(1, config.MAX_VAL, 1)],
                  key='-no_btn-', size=(6, 1), font=('Meiryo UI', 12, "bold"), enable_events=True)],
        [sg.Text(text='金額', size=(8, 1), font=('Meiryo UI', 16, "bold")),
         s_inp_03, sg.Text(text='円', size=(10, 1), font=('Meiryo UI', 16, "bold"))],
        [sg.Text(text='フリガナ', size=(8, 1), font=('Meiryo UI', 16, "bold")), s_inp_06, s_button_61, s_button_62],
        [sg.Text(text='御芳名', size=(8, 1), font=('Meiryo UI', 16, "bold")), s_inp_07],
        [sg.Text(text='住所', size=(8, 1), font=('Meiryo UI', 16, "bold")), s_inp_10],
    ],
        title='基本情報', text='基本情報', fg='#0000FF',
        font=('Meiryo UI', 16, 'bold'), relief='sunken')

    frame02 = sg.Frame(layout=[
        [sg.Checkbox('領収書', key='-k_inv-', font=('Meiryo UI', 12, "bold")),
         sg.Checkbox('現金書留', key='-k_rmail-', font=('Meiryo UI', 12, "bold"))],
    ],
        title='付属情報', text='付属情報', fg='#0000FF',
        font=('Meiryo UI', 16, 'bold'), relief='sunken')

    frame03 = sg.Frame(layout=[
        [sg.Column([[s_button_91, s_button_92, s_button_93]], anchor='c', expand_x=True)],
    ],
        title='更新', text='更新', fg='#0000FF',
        font=('Meiryo UI', 16, 'bold'), relief='sunken', anchor='c', expand_x=True)

    return [
        [frame01],
        [frame02],
        [frame03],
    ]
