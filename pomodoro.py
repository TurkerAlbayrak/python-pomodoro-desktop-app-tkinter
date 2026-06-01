import tkinter as tk
from tkinter import messagebox
import time
import os

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sade Pomodoro")
        self.root.geometry("350x250")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # SÃ¼re AyarlarÄ± (Saniye cinsinden: 25 dk ve 5 dk)
        self.WORK_TIME = 25 * 60
        self.BREAK_TIME = 5 * 60

        # Durum DeÄŸiÅŸkenleri
        self.time_left = self.WORK_TIME
        self.is_running = False
        self.is_break = False
        self.completed_pomodoros = 0
        self.timer_id = None

        self.create_widgets()

    def create_widgets(self):
        # Durum Etiketi (Ã‡alÄ±ÅŸma / Mola)
        self.status_label = tk.Label(
            self.root, text="Odaklanma ZamanÄ±",
            font=("Helvetica", 14, "bold"), fg="#ecf0f1", bg="#2c3e50"
        )
        self.status_label.pack(pady=10)

        # ZamanlayÄ±cÄ± GÃ¶stergesi
        self.timer_label = tk.Label(
            self.root, text="25:00",
            font=("Helvetica", 40, "bold"), fg="#e74c3c", bg="#2c3e50"
        )
        self.timer_label.pack(pady=10)

        # Buton Paneli
        self.button_frame = tk.Frame(self.root, bg="#2c3e50")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.button_frame, text="BaÅŸlat", command=self.start_timer,
            font=("Helvetica", 10, "bold"), bg="#2ecc71", fg="white", width=8, relief="flat"
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(
            self.button_frame, text="Durdur", command=self.pause_button_clicked,
            font=("Helvetica", 10, "bold"), bg="#f39c12", fg="white", width=8, relief="flat"
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(
            self.button_frame, text="SÄ±fÄ±rla", command=self.reset_timer,
            font=("Helvetica", 10, "bold"), bg="#95a5a6", fg="white", width=8, relief="flat"
        )
        self.reset_button.grid(row=0, column=2, padx=5)

        # GÃ¼nlÃ¼k Ä°statistik Paneli
        self.stats_label = tk.Label(
            self.root, text=f"BugÃ¼n Tamamlanan: {self.completed_pomodoros} Pomodoro",
            font=("Helvetica", 10, "italic"), fg="#bdc3c7", bg="#2c3e50"
        )
        self.stats_label.pack(pady=15)

    def play_sound(self):
        """SÃ¼re bittiÄŸinde iÅŸletim sistemine gÃ¶re bip sesi Ã§Ä±karÄ±r."""
        try:
            if os.name == 'nt':  # Windows iÃ§in
                import winsound
                winsound.Beep(1000, 1000)  # 1000 Hz frekans, 1 saniye sÃ¼re
            else:  # macOS ve Linux iÃ§in
                print('\a')
        except Exception:
            pass # Ses Ã§alÄ±namazsa hata verip uygulamayÄ± kilitlemesin

    def update_timer(self):
        if self.is_running:
            if self.time_left > 0:
                mins, secs = divmod(self.time_left, 60)
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
                self.time_left -= 1
                # 1000 ms (1 saniye) sonra tekrar bu fonksiyonu Ã§aÄŸÄ±r
                self.timer_id = self.root.after(1000, self.update_timer)
            else:
                self.play_sound()
                if not self.is_break:
                    # Ã‡alÄ±ÅŸma bitti, molaya geÃ§iÅŸ
                    self.completed_pomodoros += 1
                    self.stats_label.config(text=f"BugÃ¼n Tamamlanan: {self.completed_pomodoros} Pomodoro")
                    messagebox.showinfo("Tebrikler!", "Bir Pomodoro bitti! Åimdi mola zamanÄ±.")
                    self.is_break = True
                    self.time_left = self.BREAK_TIME
                    self.status_label.config(text="Mola ZamanÄ±", fg="#2ecc71")
                    self.timer_label.config(text="05:00", fg="#2ecc71")
                else:
                    # Mola bitti, Ã§alÄ±ÅŸmaya geÃ§iÅŸ
                    messagebox.showinfo("SÃ¼re Doldu", "Mola bitti! Ã‡alÄ±ÅŸmaya geri dÃ¶nme zamanÄ±.")
                    self.is_break = False
                    self.time_left = self.WORK_TIME
                    self.status_label.config(text="Odaklanma ZamanÄ±", fg="#ecf0f1")
                    self.timer_label.config(text="25:00", fg="#e74c3c")

                self.is_running = False
                self.start_button.config(text="BaÅŸlat")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(text="Devam")
            self.update_timer()

    def pause_button_clicked(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

    def reset_timer(self):
        self.pause_button_clicked()
        self.is_break = False
        self.time_left = self.WORK_TIME
        self.status_label.config(text="Odaklanma ZamanÄ±", fg="#ecf0f1")
        self.timer_label.config(text="25:00", fg="#e74c3c")
        self.start_button.config(text="BaÅŸlat")


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
