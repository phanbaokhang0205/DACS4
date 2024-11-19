# import tkinter as tk
# import customtkinter as ctk
# import requests

# class SystemInfoApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("System Information")
#         self.root.geometry("400x300")

#         self.label_cpu = ctk.CTkLabel(self.root, text="CPU Usage: ", font=('Arial', 14))
#         self.label_cpu.pack(pady=10)

#         self.label_memory = ctk.CTkLabel(self.root, text="Memory Usage: ", font=('Arial', 14))
#         self.label_memory.pack(pady=10)

#         self.label_disk = ctk.CTkLabel(self.root, text="Disk Usage: ", font=('Arial', 14))
#         self.label_disk.pack(pady=10)

#         self.update_info()

#     def update_info(self):
#         try:
#             data = get_system_info()

#             cpu_text = f"CPU Usage: {data['cpu_usage']}%"
#             memory_text = (f"Memory Usage: {data['used_memory']}GB / {data['total_memory']}GB "
#                            f"({data['memory_usage_percent']}%)")
#             disk_text = (f"Disk Usage: {data['used_disk']}GB / {data['total_disk']}GB "
#                          f"({data['disk_usage_percent']}%)")

#             self.label_cpu.configure(text=cpu_text)
#             self.label_memory.configure(text=memory_text)
#             self.label_disk.configure(text=disk_text)

#         except Exception as e:
#             self.label_cpu.configure(text="Failed to get data")
#             print(e)

#         # Cập nhật sau mỗi 5 giây
#         self.root.after(5000, self.update_info)

# if __name__ == '__main__':
#     root = ctk.CTk()
#     app = SystemInfoApp(root)
#     root.mainloop()


import customtkinter as ctk
import psutil
import threading
import time

class SystemMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor")
        self.geometry("500x300")

        # Tạo các thanh trạng thái
        self.cpu_monitor = self.create_monitor_frame("CPU", "#76CF8C")
        self.cpu_monitor["frame"].pack(pady=10)

        self.ram_monitor = self.create_monitor_frame("RAM", "#CFCC76")
        self.ram_monitor["frame"].pack(pady=10)

        self.disk_monitor = self.create_monitor_frame("Disk", "#6D96FF")
        self.disk_monitor["frame"].pack(pady=10)

        # Tạo thread để cập nhật dữ liệu liên tục
        self.update_thread = threading.Thread(target=self.update_monitors)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_monitor_frame(self, label_text, color):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, fg_color="transparent", font=("Arial", 14))
        label.pack(side="left", padx=10)

        # Thanh trạng thái
        progress_var = ctk.DoubleVar()
        progress_bar = ctk.CTkProgressBar(frame, variable=progress_var, fg_color="#DDDDDD", progress_color=color)
        progress_bar.set(0)  # Giá trị mặc định là 0
        progress_bar.pack(side="left", fill="x", expand=True, padx=10)

        return {
            "frame": frame,
            "progress_var": progress_var,
            "progress_bar": progress_bar
        }

    def update_monitors(self):
        while True:
            # Lấy thông tin hệ thống
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            # Cập nhật giá trị cho các thanh trạng thái
            self.cpu_monitor["progress_var"].set(cpu_usage / 100)
            self.ram_monitor["progress_var"].set(ram_usage / 100)
            self.disk_monitor["progress_var"].set(disk_usage / 100)

            # Cập nhật giao diện
            self.cpu_monitor["progress_bar"].update_idletasks()
            self.ram_monitor["progress_bar"].update_idletasks()
            self.disk_monitor["progress_bar"].update_idletasks()

            # Dừng 1 giây trước khi cập nhật tiếp
            time.sleep(1)
            print("Okee")

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()
