import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar
import datetime
from datetimejp import JDatetime
from tkinter import font

class CalenderDialog:
	def __init__(self, initial_date=None, is_time=False):
		# 例: フォントサイズ18
		self.calendar_font = ("Meiryo UI", 18)
		self.label_font = ("Meiryo UI", 16)
		self.entry_font = ("Meiryo UI", 16)
		self.button_font = ("Meiryo UI", 16)
		self.__date: str
		self.cal : Calendar
		self.initial_date = initial_date
		self.is_time = is_time
		self.result = None
		#self.root = None
		self.time_entry = None

	def show(self):
		def on_ok():
			print("OKボタン押下")
			date_str = self.cal.get_date()
			print("date_str:", date_str)
			if self.is_time:
				time_str = self.time_entry.get()
				try:
					datetime.datetime.strptime(time_str, "%H:%M")
				except ValueError:
					messagebox.showerror("エラー", "時刻はHH:MM形式で入力してください")
					return
				x_date = f"{date_str} {time_str}"
			else:
				x_date = f"{date_str} 00:00"

			try:
				if self.is_time:
					jd = JDatetime.strptime(x_date, "%Y/%m/%d %H:%M")
					jp_date = jd.strftime('%g%e年%m月%d日 %p%I時%M分')
					ampm = jd.strftime('%p')
					jp_ampm = '午前' if ampm == 'AM' else '午後'
					jp_date = jp_date.replace(ampm, jp_ampm)
					jp_date = jp_date.replace("00分", "")
				else:
					jd = JDatetime.strptime(date_str, "%Y/%m/%d")
					jp_date = jd.strftime('%g%e年%m月%d日')
			except Exception as e:
				jp_date = x_date

			self.result = {
				"jp_date": jp_date,
				"x_date": x_date
			}
			print("on_ok self.result:", self.result)
			self.root.destroy()

		def on_cancel():
			print("キャンセル押下")
			self.result = None
			self.root.destroy()

		# 既存のTkアプリがあればそれを親に、なければTk()を作る
		parent = tk._default_root if tk._default_root else tk.Tk()
		self.root = tk.Toplevel(parent)
		self.root.title("日付選択")
		self.root.resizable(False, False)

		# 初期日付の設定
		today = datetime.date.today()
		init_date = self.initial_date
		time_init_str = "00:00"
		if isinstance(init_date, str):
			try:
				if " " in init_date:
					dt_obj = datetime.datetime.strptime(init_date, "%Y/%m/%d %H:%M")
					init_date = dt_obj.date()
					time_init_str = dt_obj.strftime("%H:%M")
				else:
					init_date = datetime.datetime.strptime(init_date, "%Y/%m/%d").date()
			except Exception:
				init_date = today
		elif isinstance(init_date, datetime.datetime):
			time_init_str = init_date.strftime("%H:%M")
			init_date = init_date.date()
		elif isinstance(init_date, datetime.date):
			pass
		else:
			init_date = today

		self.cal = Calendar(
			      self.root, 
				  selectmode='day',
				  year=init_date.year,
				  month=init_date.month,
				  day=init_date.day,
				  date_pattern='yyyy/mm/dd',
				  locale='ja_JP',
				  font=self.calendar_font,
				  showweeknumbers=False)  # ← 週番号を非表示にする
		self.cal.pack(padx=10, pady=10)

		# 和暦表示ラベル
		self.jp_label = tk.Label(self.root, font=self.label_font, fg="darkgreen")
		self.jp_label.pack()

		def update_jp_date(event=None):
			date_str = self.cal.get_date()
			try:
				jd = JDatetime.strptime(date_str, "%Y/%m/%d")
				jp_date = jd.strftime('%g%e年%m月%d日')
				self.jp_label.config(text=f"和暦: {jp_date}")
			except Exception:
				self.jp_label.config(text="")

        # 初期表示時に和暦表示を更新
		update_jp_date()

        # 日付が選択されたときに和暦を更新
		self.cal.bind("<<CalendarSelected>>", update_jp_date)

		if self.is_time:
			tk.Label(self.root, text="時刻 (HH:MM)", font=self.label_font).pack()
			self.time_entry = tk.Entry(self.root, font=self.entry_font)
			self.time_entry.insert(0, time_init_str)
			self.time_entry.pack()

		btn_frame = tk.Frame(self.root)
		btn_frame.pack(pady=10)
		tk.Button(btn_frame, text="OK", command=on_ok, width=10, font=self.button_font).pack(side=tk.LEFT, padx=5)
		tk.Button(btn_frame, text="キャンセル", command=on_cancel, width=10, font=self.button_font).pack(side=tk.LEFT, padx=5)

		self.root.grab_set()  # モーダルにする
		parent.wait_window(self.root)
		print("show return self.result:", self.result)
		return self.result

	def get_result(self):
		return self.result

	def get_root(self):
		return self.root

	def destroy(self):
		self.root.destroy()
