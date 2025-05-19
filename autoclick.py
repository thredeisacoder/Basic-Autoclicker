import tkinter as tk
from tkinter import messagebox, ttk
import threading
import pyautogui
import time
import keyboard
from tkinter.font import Font

class AutoClickerApp:
    def __init__(self, master):
        self.master = master
        master.title("Auto Clicker - Nhiều vị trí")
        master.configure(bg="#f0f0f0")
        master.resizable(False, False)
        master.iconbitmap(default=None)  # Nếu bạn có file icon, thay None bằng đường dẫn
        
        # Thiết lập style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Sử dụng theme "clam" cho giao diện hiện đại
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=('Arial', 9), padding=6)
        self.style.map('TButton', 
                   background=[('active', '#4CAF50'), ('!disabled', '#2E7D32')],
                   foreground=[('!disabled', 'white')])
        self.style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        self.style.configure("Header.TLabel", font=('Arial', 10, 'bold'))
        self.style.configure("Title.TLabel", font=('Arial', 14, 'bold'), foreground="#1976D2")
        self.style.configure("Status.TLabel", foreground="#1E88E5", font=('Arial', 10, 'italic'))
        self.style.configure("Selected.TFrame", background="#e6f7ff")
        
        # Tạo style cho Entry
        self.style.configure("TEntry", padding=5, relief="flat")
        self.style.map('TEntry', 
                   fieldbackground=[('focus', '#e6f7ff'), ('!disabled', 'white')])
                   
        # Tùy chỉnh cho nút Start/Stop
        self.style.configure("Start.TButton", 
                         font=('Arial', 10, 'bold'),
                         background="#4CAF50", 
                         foreground="white")
        self.style.configure("Stop.TButton", 
                         font=('Arial', 10, 'bold'),
                         background="#F44336", 
                         foreground="white")
          # Frame chính
        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="Auto Clicker - Nhiều vị trí", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Khung chứa các dòng nhập vị trí và delay
        positions_container = ttk.Frame(main_frame, padding="8", relief="solid")
        positions_container.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        # Tiêu đề cho khung chứa vị trí
        positions_title = ttk.Label(positions_container, text="Cấu hình vị trí click", style="Header.TLabel")
        positions_title.grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")
        
        # Frame cho các vị trí
        self.frame_positions = ttk.Frame(positions_container)
        self.frame_positions.grid(row=1, column=0, columnspan=4, sticky="ew")
        
        # Tiêu đề cột
        ttk.Label(self.frame_positions, text="X", style="Header.TLabel").grid(row=0, column=0, padx=5)
        ttk.Label(self.frame_positions, text="Y", style="Header.TLabel").grid(row=0, column=1, padx=5)
        ttk.Label(self.frame_positions, text="Delay (giây)", style="Header.TLabel").grid(row=0, column=2, padx=5)
        ttk.Label(self.frame_positions, text="", style="Header.TLabel").grid(row=0, column=3)        # Frame cho các nút điều khiển
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        # Các nút trong frame điều khiển
        self.btn_add = ttk.Button(control_frame, text="+ Thêm vị trí", command=self.add_position_row, style="TButton")
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_get_pos = ttk.Button(control_frame, text="📍 Lấy tọa độ", command=self.get_mouse_position, style="TButton")
        self.btn_get_pos.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame cho nút bắt đầu/dừng
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        self.start_button = ttk.Button(action_frame, text="▶️ Bắt đầu", command=self.start_clicking, style="Start.TButton")
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_button = ttk.Button(action_frame, text="⏹️ Dừng", command=self.stop_clicking, state=tk.DISABLED, style="Stop.TButton")
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame thông tin
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        # Label trạng thái
        self.status_label = ttk.Label(info_frame, text="Trạng thái: Đang chờ", style="Status.TLabel")
        self.status_label.grid(row=0, column=0, pady=5, sticky="w")
        
        # Phím tắt
        shortcut_label = ttk.Label(info_frame, text="Phím tắt: F1 - Dừng")
        shortcut_label.grid(row=1, column=0, pady=5, sticky="w")
        
        self.position_rows = []  # lưu các dòng nhập liệu        self.stop_flag = False
        self.click_thread = None

        # Bắt sự kiện phím F1 để dừng
        keyboard.on_press_key("f1", lambda e: self.stop_clicking())

        # Tạo dòng nhập đầu tiên
        self.add_position_row()

        # Biến lưu dòng được chọn để lấy tọa độ
        self.selected_row_index = None
        
        # Tạo style cho hàng được chọn
        self.selected_bg = "#e6f7ff"
        self.normal_bg = "#ffffff"

    def add_position_row(self):
        row = len(self.position_rows) + 1
        
        # Frame cho một hàng
        row_frame = ttk.Frame(self.frame_positions)
        row_frame.grid(row=row, column=0, columnspan=4, sticky="ew", pady=2)
        
        entry_x = ttk.Entry(row_frame, width=10)
        entry_y = ttk.Entry(row_frame, width=10)
        entry_delay = ttk.Entry(row_frame, width=10)
        btn_remove = ttk.Button(row_frame, text="🗑️", width=3, 
                              command=lambda: self.remove_position_row(row-1))
        
        entry_x.grid(row=0, column=0, padx=5, pady=2)
        entry_y.grid(row=0, column=1, padx=5, pady=2)
        entry_delay.grid(row=0, column=2, padx=5, pady=2)
        btn_remove.grid(row=0, column=3, padx=5, pady=2)
          # Gán sự kiện chọn dòng khi nhấn vào entry
        entry_x.bind("<FocusIn>", lambda e, idx=row-1: self.select_row(idx))
        entry_y.bind("<FocusIn>", lambda e, idx=row-1: self.select_row(idx))
        entry_delay.bind("<FocusIn>", lambda e, idx=row-1: self.select_row(idx))
        
        self.position_rows.append({
            "entry_x": entry_x,
            "entry_y": entry_y,
            "entry_delay": entry_delay,
            "btn_remove": btn_remove,
            "row_frame": row_frame
        })
        
    def remove_position_row(self, index):
        if len(self.position_rows) <= 1:
            messagebox.showwarning("Cảnh báo", "Phải có ít nhất một vị trí!")
            return
        row_widgets = self.position_rows.pop(index)
        row_widgets["row_frame"].destroy()
        self.refresh_position_rows()
        self.selected_row_index = None

    def refresh_position_rows(self):
        for i, row_widgets in enumerate(self.position_rows):
            row = i + 1
            row_widgets["row_frame"].grid(row=row, column=0, columnspan=4, sticky="ew", pady=2)
            
            # Cập nhật lại sự kiện chọn dòng
            row_widgets["entry_x"].bind("<FocusIn>", lambda e, idx=i: self.select_row(idx))
            row_widgets["entry_y"].bind("<FocusIn>", lambda e, idx=i: self.select_row(idx))
            row_widgets["entry_delay"].bind("<FocusIn>", lambda e, idx=i: self.select_row(idx))

    def select_row(self, index):
        # Bỏ chọn hàng trước đó nếu có
        if self.selected_row_index is not None and self.selected_row_index < len(self.position_rows):
            self.position_rows[self.selected_row_index]["row_frame"].configure(style="TFrame")
            
        self.selected_row_index = index
        # Tô màu hàng được chọn
        if index < len(self.position_rows):
            self.position_rows[index]["row_frame"].configure(style="Selected.TFrame")
        
        self.status_label.config(text=f"Đã chọn dòng {index + 1} để lấy tọa độ")

    def get_mouse_position(self):
        if self.selected_row_index is None:
            messagebox.showinfo("Thông báo", "Vui lòng chọn dòng cần lấy tọa độ bằng cách click vào ô nhập.")
            return

        def countdown_and_get():
            self.status_label.config(text="Chuẩn bị lấy tọa độ trong 3 giây...")
            for i in range(3, 0, -1):
                self.status_label.config(text=f"Lấy tọa độ sau {i} giây...")
                time.sleep(1)
            x, y = pyautogui.position()
            row = self.position_rows[self.selected_row_index]
            row["entry_x"].delete(0, tk.END)
            row["entry_y"].delete(0, tk.END)
            row["entry_x"].insert(0, str(x))
            row["entry_y"].insert(0, str(y))
            self.status_label.config(text=f"Đã lấy tọa độ: ({x}, {y}) cho dòng {self.selected_row_index + 1}")

        threading.Thread(target=countdown_and_get).start()

    def start_clicking(self):
        positions = []
        delays = []
        try:
            for row in self.position_rows:
                x = int(row["entry_x"].get())
                y = int(row["entry_y"].get())
                delay = float(row["entry_delay"].get())
                positions.append((x, y))
                delays.append(delay)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số cho tất cả các dòng.")
            return

        self.positions = positions
        self.delays = delays
        self.stop_flag = False
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Trạng thái: Đang chạy...")

        self.click_thread = threading.Thread(target=self.auto_click)
        self.click_thread.start()

    def stop_clicking(self):
        if self.stop_flag:
            return
        self.stop_flag = True
        self.status_label.config(text="Trạng thái: Đã dừng")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def auto_click(self):
        while not self.stop_flag:
            for pos, delay in zip(self.positions, self.delays):
                if self.stop_flag:
                    break
                pyautogui.click(pos[0], pos[1])
                self.status_label.config(text=f"Clicked tại {pos}, delay {delay}s")
                time.sleep(delay)
        self.master.after(0, self.reset_buttons)

    def reset_buttons(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Trạng thái: Hoàn thành / Đã dừng")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
