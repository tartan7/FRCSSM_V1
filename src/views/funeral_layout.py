"""
葬儀情報入力ウィンドウのレイアウト定義
gui02.py から移植。global_list 依存を data.list_data に置き換え済み。
"""
import TkEasyGUI as sg
from data.list_data import (
    temple_list, venue_list, fform_list, xform_list1, xform_list2, s_choice
)


def get_funeral_layout():
    """葬儀情報入力ウィンドウのレイアウトを返す"""
    t_choice = [
        k + "/" + v[0] + "/" + v[1] + "/" + v[2] + "/" + v[3] + "/" + v[4]
        for k, v in temple_list.items()
    ]
    v_choice = [
        k + "/" + v[0] + "/" + v[3] + "/" + v[4]
        for k, v in venue_list.items()
    ]
    ff_choice = [k + "/" + v[0] + "/" + v[1] + "/" + v[2] for k, v in fform_list.items()]
    x1_choice = [k + "/" + v[0] for k, v in xform_list1.items()]
    x2_choice = [k + "/" + v[0] for k, v in xform_list2.items()]

    s_inp_01 = sg.InputText(key='-rname0-', default_text="", font=('Meiryo UI', 16), size=(32, 1))
    s_inp_02 = sg.InputText(key='-sname0-', default_text="", font=('Meiryo UI', 14), size=(25, 1))
    s_inp_021 = sg.Combo(s_choice, key='-sname1-', font=('Meiryo UI', 16), size=(7, 1))
    s_inp_03 = sg.InputText(key='-hname0-', default_text="", font=('Meiryo UI', 16), size=(32, 1))
    s_d_btn_1 = sg.InputText(key='-r_date-', default_text="", font=('Meiryo UI', 16), size=(25, 1), enable_events=False)
    x_d_btn_1 = sg.InputText(key='-r_date_x-', default_text="", font=('Meiryo UI', 11), size=(1, 1), enable_events=True)
    s_d_btn_2 = sg.InputText(key='-s_date-', default_text="", font=('Meiryo UI', 16), size=(25, 1), enable_events=False)
    x_d_btn_2 = sg.InputText(key='-s_date_x-', default_text="", font=('Meiryo UI', 11), size=(1, 1), enable_events=True)
    s_inp_13 = sg.Combo(["行年", "享年"], key='-syear1-', font=('Meiryo UI', 16, 'bold'), size=(6, 1))
    s_inp_14 = sg.InputText(key='-syear2-', default_text="", font=('Meiryo UI', 16), size=(6, 1))

    x_list_01 = sg.InputText(key='x_temple00', size=(1, 1), enable_events=False)
    s_list_01 = sg.Combo(t_choice, size=(35, 5), font=('Meiryo UI', 16), key='temple00', enable_events=True)
    x_list_02 = sg.InputText(key='x_venue00', size=(1, 1), enable_events=False)
    s_list_02 = sg.Combo(v_choice, size=(35, 5), font=('Meiryo UI', 16), key='venue00')
    x_list_03 = sg.InputText(key='x_fz_format00', size=(1, 1), enable_events=False)
    s_list_03 = sg.Combo(ff_choice, size=(30, 5), font=('Meiryo UI', 16), key='fz_format00', enable_events=True)
    x1_list_04 = sg.Combo(x1_choice, size=(30, 5), font=('Meiryo UI', 16), key='fz_format01', enable_events=True)
    x2_list_05 = sg.Combo(x2_choice, size=(30, 5), font=('Meiryo UI', 16), key='fz_format02', enable_events=True)

    s_d_btn_3 = sg.InputText(key='-day1_date-', default_text="", font=('Meiryo UI', 16), size=(25, 1), enable_events=False)
    x_d_btn_3 = sg.InputText(key='-day1_date_x-', default_text="", font=('Meiryo UI', 11), size=(1, 1), enable_events=True)
    s_d_btn_4 = sg.InputText(key='-day2_date-', default_text="", font=('Meiryo UI', 16), size=(25, 1), enable_events=False)
    x_d_btn_4 = sg.InputText(key='-day2_date_x-', default_text="", font=('Meiryo UI', 11), size=(1, 1), enable_events=True)
    s_d_btn_5 = sg.InputText(key='-day3_date-', default_text="", font=('Meiryo UI', 16), size=(25, 1), enable_events=False)
    x_d_btn_5 = sg.InputText(key='-day3_date_x-', default_text="", font=('Meiryo UI', 11), size=(1, 1), enable_events=True)

    s_button_C1 = sg.Submit('カレンダー入力', key="-ccal1-", font=('Meiryo UI', 10, "bold"), size=(10, 1))
    s_button_C2 = sg.Submit('カレンダー入力', key="-ccal2-", font=('Meiryo UI', 10, "bold"), size=(10, 1))
    s_button_C3 = sg.Submit('カレンダー入力', key="-ccal3-", font=('Meiryo UI', 10, "bold"), size=(10, 1))
    s_button_C4 = sg.Submit('カレンダー入力', key="-ccal4-", font=('Meiryo UI', 10, "bold"), size=(10, 1))
    s_button_C5 = sg.Submit('カレンダー入力', key="-ccal5-", font=('Meiryo UI', 10, "bold"), size=(10, 1))

    s_button_13 = sg.Submit(button_text='情報を設定する', key='-su23-',
                            button_color=('#0000FF', '#FFF'), font=('Meiryo UI', 12, "bold"), size=(12, 3))
    s_button_14 = sg.Submit(button_text='Topへ戻る', key='-Close-',
                            button_color=('#0000FF', '#FFF'), font=('Meiryo UI', 12, "bold"), size=(12, 3))

    return [
        [sg.Text(text='故人名', size=(12, 1), font=('Meiryo UI', 14, "bold")), s_inp_01],
        [sg.Text(text='(戒名)', size=(12, 1), font=('Meiryo UI', 14, "bold")), s_inp_021, s_inp_02],
        [sg.Text(text='遺族名', size=(12, 1), font=('Meiryo UI', 14, "bold")), s_inp_03],
        [sg.Text(text='故人生年月日', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_d_btn_1, s_d_btn_1, s_button_C1],
        [sg.Text(text='死亡日時', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_d_btn_2, s_d_btn_2, s_button_C2],
        [sg.Text(text='享年・行年', size=(12, 1), font=('Meiryo UI', 14, "bold")), s_inp_13, s_inp_14,
         sg.Text(text='歳', size=(6, 1), font=('Meiryo UI', 14, "bold"))],
        [sg.Text(text='菩提寺 宗派', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_list_01, s_list_01],
        [sg.Text(text='会場', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_list_02, s_list_02],
        [sg.Text(text='葬儀形態', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_list_03, s_list_03],
        [sg.Text(text='葬儀形態1', size=(12, 1), font=('Meiryo UI', 14, "bold")), x1_list_04],
        [sg.Text(text='葬儀形態2', size=(12, 1), font=('Meiryo UI', 14, "bold")), x2_list_05],
        [sg.Text(text='施工日時：通夜', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_d_btn_3, s_d_btn_3, s_button_C3],
        [sg.Text(text='施工日時：葬儀', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_d_btn_4, s_d_btn_4, s_button_C4],
        [sg.Text(text='施工日時：出棺', size=(12, 1), font=('Meiryo UI', 14, "bold")), x_d_btn_5, s_d_btn_5, s_button_C5],
        [s_button_13, s_button_14],
    ]
