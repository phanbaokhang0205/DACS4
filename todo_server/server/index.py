from tkinter import scrolledtext, messagebox, ttk
import customtkinter as ctk
from PIL import Image
from call_api import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def confirm_exit(app):
    response = messagebox.askyesno(
        "Tắt server", "Bạn có chắc chắn muốn tắt server?")
    if response:
        app.quit()


class App(ctk.CTk):
    def __init__(self, log_list):
        super().__init__()
        self.WIDTH = self.winfo_screenwidth()
        self.HEIGHT = self.winfo_screenheight()
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}+0+0')

        # header
        self.header = HeaderFrame(master=self)

        # sider
        self.sider = SiderFrame(
            master=self, navigate_callback=self.navigate_to_frame)

        # body
        self.body = BodyFrame(master=self, log_list=log_list)

        # Placing widgets
        self.header.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.13)
        self.sider.place(relx=0.01, rely=0.17, relwidth=0.2, relheight=0.82)
        self.body.place(relx=0.22, rely=0.17, relwidth=0.77, relheight=0.82)

        # Default view
        self.navigate_to_frame("dashboard")

    def navigate_to_frame(self, frame_name):
        # Hide all frames
        for frame in self.body.frames.values():
            frame.pack_forget()

        # Show the selected frame
        selected_frame = self.body.frames.get(frame_name)
        if selected_frame:
            selected_frame.pack(fill="both", expand=True)


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')
        # Server Logo
        self.server_logo = self.logo_title()
        self.server_logo.pack(side=ctk.LEFT)
        # Shut down Button
        self.shutdown = self.shut_btn(master)
        self.shutdown.pack(side=ctk.RIGHT)
        
        # refresh button
        self.refresh = self.refresh_btn()
        self.refresh.pack(side=ctk.RIGHT)
        
        
    def logo_title(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        image = ctk.CTkImage(Image.open(
            "server/icons/server.png"), size=(70, 70))
        label = ctk.CTkLabel(frame, image=image, text="")
        label.pack(side=ctk.LEFT, padx=5)
        title = ctk.CTkLabel(frame, text="Todo Server",
                             font=("Arial", 20), text_color='black')
        title.pack(side=ctk.LEFT, padx=5)
        return frame

    def refresh_btn(self):
        frame = ctk.CTkFrame(self, fg_color='transparent')
        image = ctk.CTkImage(Image.open(
            "server/icons/refresh.png"), size=(50, 50))
        button = ctk.CTkButton(frame, image=image, text="", command=self.refresh_data,
                               fg_color="transparent")
        label = ctk.CTkLabel(frame, text="Refresh",
                             font=("Arial", 18), text_color='black')
        button.pack(padx=0, pady=0)
        label.pack(padx=0, pady=0)
        return frame

    def shut_btn(self, app):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        image = ctk.CTkImage(Image.open(
            "server/icons/restart.png"), size=(50, 50))
        button = ctk.CTkButton(frame, image=image, text="",
                               fg_color="transparent", command=lambda: confirm_exit(app))
        label = ctk.CTkLabel(frame, text="Shut down",
                             font=("Arial", 18), text_color='black')
        button.pack(padx=0, pady=0)
        label.pack(padx=0, pady=0)
        return frame
    
    def refresh_data(self):
        # Lấy thông tin hệ thống
        tasks = getTasks()  # Hàm lấy danh sách tasks
        users = getUsers()  # Hàm lấy danh sách users

        # Cập nhật thông tin tasks
        if tasks:
            done_tasks = [task for task in tasks if task["status"] == "COMPLETED"]
            doing_tasks = [task for task in tasks if task["status"] == "IN_PROGRESS"]
            todo_tasks = [task for task in tasks if task["status"] == "TODO"]
            self.tasks_card.done_label.configure(text=f"Done: {done_tasks}")
            self.tasks_card.doing_label.configure(text=f"Doing: {doing_tasks}")
            self.tasks_card.todo_label.configure(text=f"Todo: {todo_tasks}")

        # Cập nhật thông tin users
        if users:
            total_users = len(users)
            # online_users = sum(1 for user in users if user.get("is_online"))
            # offline_users = total_users - online_users

            self.users_statisCard.user_quantity.configure(text=f"Total: {total_users}")
            # self.users_statisCard.online.configure(text=f"Online: {online_users}")
            # self.users_statisCard.offline.configure(text=f"Offline: {offline_users}")



class SiderFrame(ctk.CTkFrame):
    def __init__(self, master, navigate_callback):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')
        self.navigate_callback = navigate_callback

        # Dashboard
        self.dashboard = self.create_button(
            "Dashboard", "server/icons/dashboard.png", "dashboard")
        self.dashboard.pack(fill="x", anchor=ctk.W, padx=10)
        # Requests
        self.requests = self.create_button(
            "Requests", "server/icons/terminal.png", "requests")
        self.requests.pack(fill="x", anchor=ctk.W, padx=10)
        # Users
        self.users = self.create_button(
            "Users", "server/icons/group.png", "users")
        self.users.pack(fill="x", anchor=ctk.W, padx=10)

    def create_button(self, text, icon_path, frame_name):
        frame = ctk.CTkFrame(self, fg_color='transparent', corner_radius=10)
        image = ctk.CTkImage(Image.open(icon_path), size=(45, 45))
        button = ctk.CTkButton(
            frame, image=image, text="", width=45, height=45, fg_color='transparent',
            command=lambda: self.navigate_callback(frame_name)
        )
        label = ctk.CTkLabel(frame, text=text, font=(
            "Aria", 18), text_color='black')
        button.pack(fill="x", side=ctk.LEFT, padx=10, pady=10)
        label.pack(fill="x", side=ctk.LEFT)
        return frame


class BodyFrame(ctk.CTkFrame):
    def __init__(self, master, log_list):
        super().__init__(master, corner_radius=10, fg_color='transparent')
        # Create frame instances and store them in a dictionary for easy access
        self.frames = {
            "requests": Requests_Frame(self, log_list),
            "users": Users_Frame(self),
            "dashboard": Dashboard_Frame(self),
        }


class Dashboard_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='#cfe1b9')

        self.frame = self.dashFrame(self)
        self.frame.pack(fill='both')

    def dashFrame(self, master):
        frame = ctk.CTkFrame(master, fg_color='transparent')
        # System information
        sys_info_title = self.titleLabel(frame, "System Information")
        sys_info_title.pack(fill='both', padx=20, pady=10)

        system_info = get_system_info()  # API call hoặc hàm hệ thống
        user_quantity = getUsers()
        task_quantity = getTasks()
        done_tasks = [task for task in task_quantity if task["status"] == "COMPLETED"]
        doing_tasks = [task for task in task_quantity if task["status"] == "IN_PROGRESS"]
        todo_tasks = [task for task in task_quantity if task["status"] == "TODO"]

        # Lấy số lg ng dùng on, off
        online_users = sum(1 for user in user_quantity if user.get("isOnline"))
        offline_users = len(user_quantity) - online_users


        if system_info:

            # Frame chứa CPU và RAM
            sys_info_row1 = ctk.CTkFrame(frame, fg_color='transparent')
            sys_info_row1.pack(fill='x', padx=100, pady=10)

            # CPU

            self.cpu_card = self.sys_card(sys_info_row1, "#76CF8C", "server/icons/CPU.png",
                                     "CPU", usage=system_info["cpu_usage"], used=None, total=None)
            self.cpu_card.pack(fill='x', expand=False, side=ctk.LEFT)

            # RAM
            self.ram_card = self.sys_card(sys_info_row1, "#CFCC76", "server/icons/RAM.png", "RAM",
                                    usage=system_info["memory_usage_percent"], used=system_info["used_memory"],
                                    total=system_info["total_memory"])
            self.ram_card.pack(expand=True, anchor=ctk.E)
            


            # Frame chứa DISK và STATUS
            sys_info_row2 = ctk.CTkFrame(frame, fg_color='transparent')
            sys_info_row2.pack(fill='x', padx=100, pady=10)
            # DISK
            self.disk_card = self.sys_card(
                sys_info_row2, "#CF7676", "server/icons/DISK.png",
                "DISK", usage=system_info["disk_usage_percent"], 
                used=system_info["used_disk"], 
                total=system_info["total_disk"]
            )
            self.disk_card.pack(fill='x', expand=False, side=ctk.LEFT)

            # STATUS
            self.status_card = self.sys_card(
                sys_info_row2, "#A776CF", "server/icons/STATUS.png", 
                "STATUS", usage=None, used=None, total=None)
            self.status_card.pack(expand=True, anchor=ctk.E)

            # Tạo một Frame trống để cách top
            spacer = ctk.CTkFrame(frame, fg_color="transparent", height=50)
            spacer.pack(fill='x')

        if user_quantity:
            total_users = len(user_quantity)
            total_tasks = len(task_quantity)
            _done = len(done_tasks)
            _doing = len(doing_tasks)
            _todo = len(todo_tasks)

            # Statistical Information
            statis_info_title = self.titleLabel(frame, "Statistical Information")
            statis_info_title.pack(fill='both', padx=20, pady=10)

            # Statis frame
            statis_frame = ctk.CTkFrame(frame, fg_color='transparent')
            statis_frame.pack(fill='x')

            # users_statisCard
            self.users_statisCard = self.users_card(statis_frame, total_users, online_users, offline_users)
            self.users_statisCard.pack(fill='x', padx=(100,50), pady=10, side=ctk.LEFT, expand=True, anchor=ctk.N)

            # tasks_statisCard
            self.task_statisCard = self.tasks_card(statis_frame, total_tasks, _done, _doing, _todo)
            self.task_statisCard.pack(fill='x', padx=(50,100), pady=10, side=ctk.RIGHT, expand=True, anchor=ctk.N)

        # Lấy tất cả client_ip
        hosts = get_all_host()
        if not hosts:
            print("Không có dữ liệu để hiển thị.")
            return

        # Tính toán tỷ lệ tổng thể
        success_rate, fail_rate = self.calculate_overall_success_rate(hosts)

        # request rate
        request_frame = ctk.CTkFrame(frame, fg_color='transparent')
        request_frame.pack(fill='x', padx=150)
        self.success_rate = self.request_rate(request_frame, "#6DFF9B", "Success Request", "server/icons/success.png", round(success_rate, 2))
        self.success_rate.pack(side=ctk.LEFT,  expand=False)
        
        self.fail_rate = self.request_rate(request_frame, "#FF6D6D", "Fail Request", "server/icons/fail.png", round(fail_rate, 2))
        self.fail_rate.pack( anchor=ctk.E)

        # Bảng dữ liệu clients
        table_client_frame = self.create_client_table(frame)
        table_client_frame.pack(fill="both", expand=True, pady=20)

        return frame


# ============= system infomation =========================
    def update_dashboard(self, system_info):
        # Cập nhật các giá trị CPU, RAM, DISK
        global cpu_card, ram_card, disk_card

            # Cập nhật CPU
        self.cpu_card.usage_label.configure(text=f"{system_info['cpu_usage']} %")
        self.cpu_card.monitor["progress_var"].set(system_info["cpu_usage"] / 100)

        # Cập nhật RAM
        self.ram_card.usage_label.configure(text=f"{system_info['memory_usage_percent']} %")
        if self.ram_card.used_label:
            self.ram_card.used_label.configure(
                text=f"{system_info['used_memory']} GB / {system_info['total_memory']} GB"
            )
        self.ram_card.monitor["progress_var"].set(system_info["memory_usage_percent"] / 100)

        # Cập nhật DISK
        self.disk_card.usage_label.configure(text=f"{system_info['disk_usage_percent']} %")
        if self.disk_card.used_label:
            self.disk_card.used_label.configure(
                text=f"{system_info['used_disk']} GB / {system_info['total_disk']} GB"
            )
        self.disk_card.monitor["progress_var"].set(system_info["disk_usage_percent"] / 100)

    def create_monitor_frame(self, master, color, var):
        frame = ctk.CTkFrame(master, fg_color="transparent")

        min_value = 0.0
        max_value = 100.0
        normalized_var = (var - min_value) / (max_value - min_value)
        # Thanh trạng thái
        progress_var = ctk.DoubleVar()
        progress_bar = ctk.CTkProgressBar(
            frame, variable=progress_var, fg_color="#DDDDDD", progress_color=color, height=20, width=250, corner_radius=0, border_width=2)
        progress_bar.set(normalized_var)  # Giá trị mặc định là 0
        progress_bar.pack(side="left", fill="x", expand=True, padx=10)

        return {
            "frame": frame,
            "progress_var": progress_var,
            "progress_bar": progress_bar
        }
    
    def titleLabel(self, master, content):
        frame = ctk.CTkFrame(master, fg_color="#6D96FF",
                             border_width=2, border_color='black', corner_radius=20)
        label = ctk.CTkLabel(frame, text=content, font=(
            'Arial', 32, 'bold'), text_color='black', anchor='center')
        label.pack(fill='x', padx=20, pady=10)
        return frame

    def sys_card(self, master, color, img_src, title, usage, used, total):
        card = ctk.CTkFrame(master, fg_color=color, corner_radius=10)
        
        # Left: Ảnh và tiêu đề
        left = ctk.CTkFrame(card, fg_color='transparent')
        left.pack(side=ctk.LEFT, padx=(30,15), pady=10)
        image_src = ctk.CTkImage(Image.open(img_src), size=(100, 100))
        image = ctk.CTkLabel(left, text='', image=image_src)
        image.pack(pady=10)
        title_label = ctk.CTkLabel(left, text=title, font=("Arial", 22, "bold"), text_color='white')
        title_label.pack()

        # Right: Usage và thanh tiến trình
        right = ctk.CTkFrame(card, fg_color='transparent')
        right.pack(side=ctk.RIGHT, padx=(15, 30), pady=5)
        

        if (title != "STATUS"):
            if used is not None and total is not None:
                used_label = ctk.CTkLabel(right, text=f"{used} GB / {total} GB", font=("Arial", 22, 'bold'), text_color='white')
                used_label.pack(pady=10)

            usage_label = ctk.CTkLabel(right,text=f"{usage} %", font=("Arial", 52, 'bold'), text_color='white')
            usage_label.pack(pady=5)
            self.monitor = self.create_monitor_frame(right, color, usage)
            self.monitor["frame"].pack(pady=10)
            card.monitor = self.monitor  # Lưu monitor để sử dụng sau

            # Lưu tham chiếu
            card.usage_label = usage_label
            card.used_label = used_label if used is not None else None
        else:
            label = ctk.CTkLabel(right, text="ON", font=(
                "Arial", 52, 'bold'), text_color='white', width=270)
            label.pack(pady=5)
        return card
    
# ============= Statistical Information =========================
    def statisCard(self, master, title):
        card = ctk.CTkFrame(master, fg_color="transparent")
        # Header
        title_label = ctk.CTkLabel(card, text=title, font=("Aria", 25), text_color='black')
        title_label.pack(fill='x')
        # image
        # image_src = ctk.CTkImage(Image.open(image), size=(100, 100))
        # image = ctk.CTkLabel(card, text='', image=image_src)
        # image.pack(pady=10)
        
        return card
    
    def users_card(self, master, quantity, online, offline):
        frame = ctk.CTkFrame(master, fg_color='#C3C7F4', corner_radius=10, width=170, height=100)
        frame.pack_propagate(False)  # Ngăn frame tự động điều chỉnh kích thước theo nội dung

        # Header
        header = self.statisCard(frame, f"Total Users: {quantity}")
        header.pack(fill='x', pady=10)
        # Quantity
        # self.user_quantity = ctk.CTkLabel(frame, text=f"Quantity: {quantity}", font=("Aria", 22, 'bold'), text_color='black')
        # self.user_quantity.pack(fill='x', pady=10, padx=20)

        # Online frame
        total_users_frame = ctk.CTkFrame(frame, fg_color='transparent')
        total_users_frame.pack(fill='x', pady=5)
        # online quantity
        self.total_users = ctk.CTkLabel(total_users_frame, text=f"Online: {online}, Offline: {offline}", font=("Aria", 20), text_color='black', justify='center', anchor='center')
        self.total_users.pack(side=ctk.TOP, expand=True)
        # online image
        # online_src = ctk.CTkImage(Image.open("server/icons/online.png"), size=(50, 50))
        # self.online_img = ctk.CTkLabel(online_frame, text='', image=online_src)
        # self.online_img.pack(side=ctk.LEFT, expand=False, padx=(10, 70))

        # offline frame
        # offline_frame = ctk.CTkFrame(frame, fg_color='transparent')
        # offline_frame.pack(fill='x', pady=10, padx=20)
        # offline quantity
        # self.offline = ctk.CTkLabel(offline_frame, text=f"Offline: {offline}", font=("Aria", 22), text_color='black')
        # self.offline.pack(side=ctk.RIGHT, expand=True, anchor=ctk.W)
        # # offline image
        # offline_src = ctk.CTkImage(Image.open("server/icons/offline.png"), size=(50, 50))
        # self.offline_img = ctk.CTkLabel(offline_frame, text='', image=offline_src)
        # self.offline_img.pack(side=ctk.LEFT, expand=False, padx=(10, 70))
        
        return frame

    def tasks_card(self, master, quantity, done, doing, todo):
        frame = ctk.CTkFrame(master, fg_color='#C3C7F4', corner_radius=10, width=170, height=100)
        frame.pack_propagate(False)  # Ngăn frame tự động điều chỉnh kích thước theo nội dung
        # Header
        header = self.statisCard(frame, f"Total Tasks: {quantity}")
        header.pack(fill='x', pady=10)
        # # Quantity
        # self.tasks_quantity = ctk.CTkLabel(frame, text=f"Quantity: {quantity}", font=("Aria", 22, 'bold'), text_color='black')
        # self.tasks_quantity.pack(fill='x', pady=10, padx=20)

        # done frame
        total_tasks_frame = ctk.CTkFrame(frame, fg_color='transparent')
        total_tasks_frame.pack(fill='x', pady=5)
        # done quantity
        self.total_tasks = ctk.CTkLabel(total_tasks_frame, text=f"Done: {done} - Doing: {doing} - Todo: {todo}", font=("Aria", 20), text_color='black', justify='center', anchor='center')
        self.total_tasks.pack(side=ctk.TOP, expand=True)
        # done image
        # done_src = ctk.CTkImage(Image.open("server/icons/done.png"), size=(50, 50))
        # self.done_img = ctk.CTkLabel(done_frame, text='', image=done_src)
        # self.done_img.pack(side=ctk.LEFT, expand=False, padx=(10, 70))

        # doing frame
        # doing_frame = ctk.CTkFrame(frame, fg_color='transparent')
        # doing_frame.pack(fill='x', pady=10, padx=20)
        # # doing quantity
        # self.doing_label = ctk.CTkLabel(doing_frame, text=f"Doing: {doing}", font=("Aria", 22,), text_color='black')
        # self.doing_label.pack(side=ctk.RIGHT, expand=True, anchor=ctk.W)
        # # doing image
        # doing_src = ctk.CTkImage(Image.open("server/icons/doing.png"), size=(50, 50))
        # self.doing_img = ctk.CTkLabel(doing_frame, text='', image=doing_src)
        # self.doing_img.pack(side=ctk.LEFT, expand=False, padx=(10, 70))

        # # todo frame
        # todo_frame = ctk.CTkFrame(frame, fg_color='transparent')
        # todo_frame.pack(fill='x', pady=10, padx=20)
        # # todo quantity
        # self.todo_label = ctk.CTkLabel(todo_frame, text=f"Todo: {todo}", font=("Aria", 22,), text_color='black')
        # self.todo_label.pack(side=ctk.RIGHT, expand=True, anchor=ctk.W)
        # # todo image
        # todo_src = ctk.CTkImage(Image.open("server/icons/todo.png"), size=(50, 50))
        # self.todo_img = ctk.CTkLabel(todo_frame, text='', image=todo_src)
        # self.todo_img.pack(side=ctk.LEFT, expand=False, padx=(10, 70))
        
        return frame
    
    def create_client_table(self, master):
        # Khung chứa bảng
        frame = ctk.CTkFrame(master, fg_color="white", corner_radius=10)

        # Tạo kiểu tùy chỉnh cho Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="#FFFFFF",
                        font=("Arial", 16))
        style.configure("Treeview.Heading",
                        font=("Arial", 18, "bold"),
                        background="#BDD1C5",
                        foreground="black")
        style.map("Treeview", background=[("selected", "#768FCF")])

        # Cột của bảng
        columns = ("ID", "Host", "Number of Requests", "Date")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", style="Treeview")

        # Định nghĩa tiêu đề và kích thước cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Thêm dữ liệu mẫu
        data = [
            (1, "127.0.0.1", 20, "2024/24/12"),
            (2, "127.0.0.1", 12, "2024/24/12"),
            (3, "127.0.0.1", 25, "2024/25/12"),
            (4, "127.0.0.1", 10, "2024/26/12"),
            (5, "127.0.0.1", 30, "2024/27/12"),
            (6, "127.0.0.1", 15, "2024/28/12"),
            (7, "127.0.0.1", 18, "2024/29/12"),
            (8, "127.0.0.1", 22, "2024/30/12"),
            (9, "127.0.0.1", 16, "2024/01/01"),
            (10, "127.0.0.1", 28, "2024/02/01"),
            (11, "127.0.0.1", 24, "2024/03/01"),
        ]
        for row in data:
            self.tree.insert("", "end", values=row)

        # Tính toán số lượng dòng data
        rows = len(data)
        self.tree.config(height=min(rows, 10)) # Chỉ hiển thị tối đa 10 dòng

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Đặt bảng và thanh cuộn
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Thêm khoảng cách khi đặt frame
        frame.pack(fill="both", expand=True, pady=10, padx=10)

        return frame

# ============= request rate =========================
    def calculate_overall_success_rate(self, hosts):
        total_success = sum(host['success'] for host in hosts)
        total_fail = sum(host['fail'] for host in hosts)
        total_requests = total_success + total_fail

        if total_requests == 0:
            return 0, 0

        success_rate = (total_success / total_requests) * 100
        fail_rate = (total_fail / total_requests) * 100
        return success_rate, fail_rate


    def request_rate(self, master, color, title, img, rate):
        frame = ctk.CTkFrame(master, fg_color=color, corner_radius=10, width=320, height=160)
        frame.pack_propagate(False)  # Ngăn frame tự điều chỉnh kích thước theo nội dung
        
        # title
        title_label = ctk.CTkLabel(frame, text=f"{title}: {rate}%", text_color='black', font=("Aria", 25))
        title_label.pack(fill='x' ,padx=5, pady=10)

        # image 
        rate_src = ctk.CTkImage(Image.open(img), size=(85,85))
        self.rate_img = ctk.CTkLabel(frame, text='', image=rate_src)
        self.rate_img.pack(padx=5)

        return frame
    


class Requests_Frame(ctk.CTkFrame):
    def __init__(self, master, log_list):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')

        # # search_frame
        self.search = self.search_frame(self, log_list)
        self.search.pack(fill='x', expand=False, padx=10, pady=10)

        # ScrolledText để hiển thị log
        self.log_display = self.log_frame(self)
        self.log_display.pack(fill='both', expand=True, pady=(0, 10), padx=10)

    def search_frame(self, master, log_list):
        frame = ctk.CTkFrame(master, fg_color='transparent')

        global search_img
        search_img = ctk.CTkImage(Image.open(
            'server/icons/search.png'), size=(20, 20))
        refresh_img = ctk.CTkImage(Image.open(
            'server/icons/refresh.png'), size=(20, 20))
        self.title = ctk.CTkLabel(frame, text="Requests List", font=(
            "Aria", 34, "bold"), text_color='black')
        self.title.pack(side=ctk.LEFT, expand=True,
                        anchor=ctk.W, padx=(5, 10), pady=5)

        # Trường nhập liệu tìm kiếm
        self.search_entry = ctk.CTkEntry(frame, height=35, placeholder_text="Searching...",
                                         placeholder_text_color="gray", fg_color='black', corner_radius=20, border_width=0)
        self.search_entry.pack(side=ctk.LEFT, padx=(
            5, 15), fill='x', expand=True)

        # Nút Refresh để cập nhật log
        refresh_button = ctk.CTkButton(frame, fg_color="#79FDA5", text="Refresh", width=100, text_color='black',
                                       image=refresh_img, compound=ctk.LEFT, height=35, command=lambda: self.update_logs(log_list))
        refresh_button.pack(padx=5, side=ctk.LEFT, expand=False)

        # Nút tìm kiếm
        search_button = ctk.CTkButton(frame, width=100, text_color='black', fg_color='#79E2FD', text="Search",
                                      height=35, image=search_img, compound=ctk.LEFT, command=lambda: self.search_logs(log_list))
        search_button.pack(padx=5, side=ctk.LEFT, expand=False)
        return frame

    def log_frame(self, master):
        frame = ctk.CTkScrollableFrame(
            master, fg_color='black', corner_radius=10)
        return frame

    # Request item
    def request_item(self, master, method, content, color):
        frame = ctk.CTkFrame(master, fg_color='transparent', corner_radius=20)

        # request method
        self.method = self.method_item(frame, color, method)
        self.method.pack(expand=False, side=ctk.LEFT, anchor=ctk.N)

        # request content
        self.content = self.request_content(frame, color, content)
        self.content.pack(expand=True, side=ctk.LEFT, ipadx=10,
                          ipady=15, anchor=ctk.W, padx=(20, 0))

        return frame

    # request method item
    def method_item(self, master, fg_color, method):
        self.label = ctk.CTkLabel(
            master=master, text=method, text_color='black',
            font=('Aria', 16, 'bold'), corner_radius=20, fg_color=fg_color,
            width=120, height=50
        )
        return self.label

    # request content
    def request_content(self, master, fg_color, content):
        self.label = ctk.CTkLabel(
            master, text=content,
            font=('Aria', 16), text_color='black',
            fg_color=fg_color, corner_radius=20, anchor=ctk.W, justify=ctk.LEFT
        )
        return self.label

    # Hàm cập nhật log
    def update_logs(self, filtered_logs=None, log_list=None):
        # Xóa nội dung cũ
        for widget in self.log_display.winfo_children():
            widget.destroy()

        # Lấy danh sách log cần hiển thị
        logs_to_display = filtered_logs if filtered_logs else log_list

        # Duyệt qua từng log và tạo request item cho mỗi log
        for log in logs_to_display:
            parts = log.split("@")

            if len(parts) >= 6:
                times = parts[0]
                method = parts[1]
                path = parts[2]
                status = parts[3]
                server_ip = parts[4]
                client_ip = parts[5]
                content = f"[{times}]\n\nMethod: {method}\nPath: {path}\nServer IP: {server_ip}\nClient IP: {client_ip}\nStatus: {status}"
                color = "#79FDA5" if method == "GET" else "#79E2FD" if method == "POST" else "#FD797B" if method == "DELETE" else "#FDEF79"
                request_item = self.request_item(
                    master=self.log_display,
                    method=method,
                    content=content,
                    color=color
                )
                if self.filterRequest(path):
                    request_item.pack(fill='x', padx=10, pady=10)

        # Tự động cuộn xuống cuối
        self.log_display.update_idletasks()
        self.log_display._parent_canvas.yview_moveto(1.0)

    def filterRequest(self, content):
        if ("/static/assets" in content):
            return False
        else:
            return True

    # Hàm tìm kiếm log dựa trên từ khóa
    def search_logs(self,  log_list=None):
        # Lấy từ khóa tìm kiếm và chuyển thành chữ thường
        search_term = self.search_entry.get().lower()
        # Lọc log chứa từ khóa
        filtered_logs = [log for log in log_list if search_term in log.lower()]
        self.update_logs(filtered_logs)


class Users_Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='#E7F5DC')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.content = self.user_table(self)
        self.search = self.search_user(self)
        self.search.grid(row=0, column=0, sticky=ctk.NSEW, padx=10)
        self.content.grid(row=1, column=0, sticky=ctk.NSEW, padx=10, pady=10)

    def search_user(self, master):
        frame = ctk.CTkFrame(master, fg_color='transparent')

        self.title = ctk.CTkLabel(frame, text="Users List", font=(
            "Aria", 34, "bold"), text_color='black')
        self.title.pack(side=ctk.LEFT, expand=True, anchor=ctk.W, padx=(5, 10))
        # Trường nhập liệu tìm kiếm
        self.search_entry = ctk.CTkEntry(frame, height=35, placeholder_text="Searching...",
                                         placeholder_text_color="gray", fg_color='black', corner_radius=20, border_width=0)
        self.search_entry.pack(side=ctk.LEFT, padx=(
            5, 15), fill='x', expand=True)

        # Nút tìm kiếm
        search_button = ctk.CTkButton(frame, text="Search", width=100, text_color='black',
                                      fg_color='#79E2FD', height=35, image=search_img, compound=ctk.LEFT)
        search_button.pack(padx=5, side=ctk.LEFT, expand=False)

        del_img = ctk.CTkImage(Image.open(
            'server/icons/delete.png'), size=(20, 20))
        delete_button = ctk.CTkButton(frame, text="Delete", width=100, text_color='black',
                                      fg_color='#FD797B', height=35, image=del_img, compound=ctk.LEFT)
        delete_button.pack(padx=5, side=ctk.LEFT, expand=False)
        # Nút xóa
        return frame

    def user_table(self, master):
        frame = ctk.CTkFrame(master, fg_color="transparent")

        # Thiết lập kiểu tùy chỉnh cho Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#D9D9D9",   # màu nền cho các hàng
                        foreground="black",     # màu chữ
                        rowheight=30,           # tăng chiều cao dòng
                        borderwidth=0,
                        # tăng kích thước font chữ nội dung
                        font=("Arial", 12),
                        fieldbackground="#768FCF")  # màu nền cho các trường trống
        style.configure("Treeview.Heading",
                        # tăng kích thước và đậm cho tiêu đề
                        font=("Arial", 14, "bold"),
                        background="#CFDDFF",  # màu nền cho tiêu đề
                        rowheight=30,
                        foreground="black")    # màu chữ cho tiêu đề
        # màu dòng được chọn
        style.map("Treeview", background=[("selected", "#768FCF")])

        # Tạo Treeview
        columns = ("ID", "Fullname", "Age", "Gender", "Phone",
                   "Address", "Email", "Username", "Password")
        self.tree = ttk.Treeview(frame, columns=columns,
                                 show="headings", style="Treeview")

        # Định nghĩa tiêu đề các cột và thiết lập kích thước cột
        for col in columns:
            self.tree.heading(col, text=col)
            # tăng kích thước mỗi cột
            self.tree.column(col, width=150, anchor=ctk.CENTER)

        # Thêm dữ liệu mẫu vào Treeview
        sample_data = getUsers()
        for data in sample_data:
            self.tree.insert("", "end",
                             values=(data['id'], data['fullname'], data['age'],
                                     data['gender'], data['phone'], data['address'], data['email'],
                                     data['username'], data['password']))

        # Tạo thanh cuộn dọc (không tạo thanh cuộn ngang)
        # vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        # tree.configure(yscroll=vsb.set)

        # Đặt Treeview và thanh cuộn dọc vào frame
        self.tree.grid(row=0, column=0, sticky="nsew")
        # vsb.grid(row=0, column=1, sticky="ns")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.auto_resize_columns()

        return frame  # Trả về frame để tránh lỗi AttributeError

    def auto_resize_columns(self):
        # Duyệt qua từng cột trong Treeview
        for col in self.tree["columns"]:
            max_width = 0
            # Tính độ rộng lớn nhất của nội dung trong mỗi hàng
            for item in self.tree.get_children():
                cell_value = str(self.tree.item(
                    item)["values"][self.tree["columns"].index(col)])
                max_width = max(max_width, len(cell_value))

            # Đặt chiều rộng của cột bằng độ dài lớn nhất * hệ số pixel (7 hoặc 10)
            self.tree.column(col, width=max_width * 10)
