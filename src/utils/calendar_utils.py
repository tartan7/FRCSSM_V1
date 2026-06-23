"""
カレンダー関連のユーティリティ関数
func1.cal_calendar から移植。
"""
import datetime
from utils.calendar_dialog import CalenderDialog
from utils.date_utils import convert_japanese_date_to_gregorian


def cal_calendar(window, values, display_key: str, is_time: bool = False) -> bool:
    """カレンダーダイアログを表示して選択した日付をウィンドウに反映する。

    Args:
        window: TkEasyGUI ウィンドウ
        values: 現在のウィンドウ値辞書
        display_key: 表示対象のウィンドウキー（例: '-r_date-'）
        is_time: 時刻入力を含む場合 True

    Returns:
        日付が選択された場合 True、キャンセルの場合 False
    """
    try:
        window_key = display_key
        x_key = f"{display_key.rstrip('-')}_x-"

        current_value = window[window_key].get()

        current_x_value = None
        try:
            if x_key in values:
                current_x_value = values[x_key]
            else:
                try:
                    current_x_value = window[x_key].get()
                except KeyError:
                    current_x_value = None
        except Exception:
            current_x_value = None

        initial_date = None
        if current_x_value and current_x_value.strip():
            try:
                if is_time:
                    initial_date = datetime.datetime.strptime(current_x_value.strip(), '%Y/%m/%d %H:%M')
                else:
                    date_str = current_x_value.strip().split(' ')[0]
                    initial_date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
            except ValueError:
                initial_date = None

        if initial_date is None and current_value and current_value.strip():
            try:
                gregorian_date = convert_japanese_date_to_gregorian(current_value.strip())
                if gregorian_date:
                    fmt = '%Y/%m/%d %H:%M' if is_time else '%Y/%m/%d'
                    initial_date = datetime.datetime.strptime(gregorian_date, fmt)
            except Exception:
                initial_date = None

        dialog = CalenderDialog(initial_date=initial_date, is_time=is_time)
        result = dialog.show()

        if result:
            window[window_key].update(result['jp_date'])
            try:
                window[x_key].update(result['x_date'])
            except KeyError:
                pass
            return True

        return False

    except Exception as e:
        import traceback
        print(f"カレンダー入力エラー: {str(e)}\n{traceback.format_exc()}")
        return False
