from tkinter import scrolledtext, messagebox, ttk
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

    
def confirm_exit(app):
    response = messagebox.askyesno("Tắt server", "Bạn có chắc chắn muốn tắt server?")
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
        self.sider = SiderFrame(master=self, navigate_callback=self.navigate_to_frame)

        # body
        self.body = BodyFrame(master=self, log_list=log_list)

        # Placing widgets
        self.header.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.13)
        self.sider.place(relx=0.01, rely=0.17, relwidth=0.2, relheight=0.82)
        self.body.place(relx=0.22, rely=0.17, relwidth=0.77, relheight=0.82)

        # Default view
        self.navigate_to_frame("requests")

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

    def logo_title(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        image = ctk.CTkImage(Image.open("server/icons/server.png"), size=(70, 70))
        label = ctk.CTkLabel(frame, image=image, text="")
        label.pack(side=ctk.LEFT, padx=5)
        title = ctk.CTkLabel(frame, text="Todo Server", font=("Arial", 20), text_color='black')
        title.pack(side=ctk.LEFT, padx=5)
        return frame

    def shut_btn(self, app):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        image = ctk.CTkImage(Image.open("server/icons/restart.png"), size=(50, 50))
        button = ctk.CTkButton(frame, image=image, text="", fg_color="transparent", command=lambda: confirm_exit(app))
        label = ctk.CTkLabel(frame, text="Shut down", font=("Arial", 18), text_color='black')
        button.pack(padx=0, pady=0)
        label.pack(padx=0, pady=0)
        return frame



class SiderFrame(ctk.CTkFrame):
    def __init__(self, master, navigate_callback):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')
        self.navigate_callback = navigate_callback

        # Dashboard
        self.dashboard = self.create_button("Dashboard", "server/icons/dashboard.png", "dashboard")
        self.dashboard.pack(fill="x", anchor=ctk.W, padx=10)
        # Requests
        self.requests = self.create_button("Requests", "server/icons/terminal.png", "requests")
        self.requests.pack(fill="x", anchor=ctk.W, padx=10)
        # Users
        self.users = self.create_button("Users", "server/icons/group.png", "users")
        self.users.pack(fill="x", anchor=ctk.W, padx=10)
        # Notifications
        self.notis = self.create_button("Notification", "server/icons/notification.png", "notis")
        self.notis.pack(fill="x", anchor=ctk.W, padx=10)

    def create_button(self, text, icon_path, frame_name):
        frame = ctk.CTkFrame(self, fg_color='transparent', corner_radius=10)
        image = ctk.CTkImage(Image.open(icon_path), size=(45, 45))
        button = ctk.CTkButton(
            frame, image=image, text="", width=45, height=45, fg_color='transparent',
            command=lambda: self.navigate_callback(frame_name)
        )
        label = ctk.CTkLabel(frame, text=text, font=("Aria", 18), text_color='black')
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
            "notis": Notis_Frame(self)
        }


class Dashboard_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='red')
        label = ctk.CTkLabel(self, text="Dashboard Content", font=("Arial", 20), text_color="white")
        label.pack(pady=20)



class Requests_Frame(ctk.CTkFrame):
    def __init__(self, master, log_list):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')

        # # search_frame
        self.search = self.search_frame(self,log_list)
        self.search.pack(fill='x', expand=False, padx=10, pady=10)

        # ScrolledText để hiển thị log
        self.log_display = self.log_frame(self)
        self.log_display.pack(fill='both', expand=True, pady=(0,10), padx=10)

    def search_frame(self,master, log_list):
        frame = ctk.CTkFrame(master, fg_color='transparent')

        global search_img
        search_img = ctk.CTkImage(Image.open('server/icons/search.png'), size=(20, 20))
        refresh_img = ctk.CTkImage(Image.open('server/icons/refresh.png'), size=(20, 20))
        self.title = ctk.CTkLabel(frame, text="Requests List", font=("Aria", 34, "bold"), text_color='black')
        self.title.pack(side=ctk.LEFT,expand=True, anchor=ctk.W, padx=(5,10), pady=5)

        # Trường nhập liệu tìm kiếm
        self.search_entry = ctk.CTkEntry(frame, height=35, placeholder_text="Searching...", placeholder_text_color="gray", fg_color='black', corner_radius=20, border_width=0)
        self.search_entry.pack(side=ctk.LEFT, padx=(5,15), fill='x', expand=True)

        # Nút Refresh để cập nhật log
        refresh_button = ctk.CTkButton(frame, fg_color="#79FDA5", text="Refresh",width=100, text_color='black', image=refresh_img, compound=ctk.LEFT, height=35, command=lambda: self.update_logs(log_list))
        refresh_button.pack(padx=5,side=ctk.LEFT, expand=False)

        # Nút tìm kiếm
        search_button = ctk.CTkButton(frame, width=100, text_color='black', fg_color='#79E2FD',text="Search", height=35 ,image=search_img, compound=ctk.LEFT, command=lambda: self.search_logs(log_list))
        search_button.pack(padx=5,side=ctk.LEFT, expand=False)
        return frame
        
    def log_frame(self, master):
        frame = ctk.CTkScrollableFrame(master, fg_color='black', corner_radius=10)
        return frame
    
    # Request item
    def request_item(self, master, method, content, color):
        frame = ctk.CTkFrame(master, fg_color='transparent', corner_radius=20)

        # request method
        self.method = self.method_item(frame, color, method)
        self.method.pack(expand=False, side=ctk.LEFT, anchor=ctk.N)

        # request content
        self.content = self.request_content(frame, color, content)
        self.content.pack(expand=True, side=ctk.LEFT, ipadx=10, ipady=15, anchor=ctk.W, padx=(20,0))

        return frame
    
    # request method item
    def method_item(self,master, fg_color, method):
        self.label = ctk.CTkLabel(
            master=master, text=method, text_color='black',
            font=('Aria', 16, 'bold'), corner_radius=20, fg_color=fg_color, 
            width=120,height=50
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
                
                color = "#79FDA5" if method == "GET" else "#79E2FD" if method == "POST" else "#FD797B" if method == "DELETE" else "#FDEF79"
                request_item = self.request_item(
                    master=self.log_display,
                    method=method,
                    content=f" [{times}]\n\nMethod: {method}\nPath: {path}\nServer IP: {server_ip}\nClient IP: {client_ip}\nStatus: {status}",
                    color=color
                )
                request_item.pack(fill='x', padx=10, pady=10)
        
        # Tự động cuộn xuống cuối
        self.log_display.update_idletasks()
        self.log_display._parent_canvas.yview_moveto(1.0)


    # Hàm tìm kiếm log dựa trên từ khóa
    def search_logs(self,  log_list=None):
        search_term = self.search_entry.get().lower()  # Lấy từ khóa tìm kiếm và chuyển thành chữ thường
        filtered_logs = [log for log in log_list if search_term in log.lower()]  # Lọc log chứa từ khóa
        self.update_logs(filtered_logs)

    
class Users_Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.content = self.user_table(self)
        self.search = self.search_user(self)
        self.search.grid(row=0, column=0, sticky=ctk.NSEW, padx=10)
        self.content.grid(row=1, column=0, sticky=ctk.NSEW, padx=10, pady=10)

    def search_user(self, master):
        frame = ctk.CTkFrame(master, fg_color='transparent')

        self.title = ctk.CTkLabel(frame, text="Users List", font=("Aria", 34, "bold"), text_color='black')
        self.title.pack(side=ctk.LEFT,expand=True, anchor=ctk.W, padx=(5,10))
        # Trường nhập liệu tìm kiếm
        self.search_entry = ctk.CTkEntry(frame, height=35, placeholder_text="Searching...", placeholder_text_color="gray", fg_color='black', corner_radius=20, border_width=0)
        self.search_entry.pack(side=ctk.LEFT, padx=(5,15), fill='x', expand=True)

        # Nút tìm kiếm
        search_button = ctk.CTkButton(frame, text="Search", width=100, text_color='black', fg_color='#79E2FD', height=35 ,image=search_img, compound=ctk.LEFT)
        search_button.pack(padx=5,side=ctk.LEFT, expand=False)

        del_img = ctk.CTkImage(Image.open('server/icons/delete.png'), size=(20, 20))
        delete_button = ctk.CTkButton(frame, text="Delete", width=100, text_color='black', fg_color='#FD797B', height=35 ,image=del_img, compound=ctk.LEFT)
        delete_button.pack(padx=5,side=ctk.LEFT, expand=False)
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
                        font=("Arial", 12),     # tăng kích thước font chữ nội dung
                        fieldbackground="#E6E6FA")  # màu nền cho các trường trống
        style.configure("Treeview.Heading", 
                        font=("Arial", 14, "bold"), # tăng kích thước và đậm cho tiêu đề
                        background="#B0C4DE",  # màu nền cho tiêu đề
                        foreground="black")    # màu chữ cho tiêu đề
        style.map("Treeview", background=[("selected", "#768FCF")])  # màu dòng được chọn

        # Tạo Treeview
        columns = ("ID", "Fullname", "Age", "Gender", "Phone", "Address", "Email", "Username", "Password")
        tree = ttk.Treeview(frame, columns=columns, show="headings", style="Treeview")
        
        # Định nghĩa tiêu đề các cột và thiết lập kích thước cột
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=ctk.CENTER)  # tăng kích thước mỗi cột

        # Thêm dữ liệu mẫu vào Treeview
        sample_data = [
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),

            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
            (1, "John Doe", 25, "Male", "123-456-789", "123 Example St.", "john@example.com", "johndoe", "password"),
            (2, "Jane Smith", 30, "Female", "987-654-321", "456 Sample Ave.", "jane@example.com", "janesmith", "password123"),
        ]
        for data in sample_data:
            tree.insert("", "end", values=data)
        
        # Tạo thanh cuộn dọc (không tạo thanh cuộn ngang)
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=vsb.set)
        
        # Đặt Treeview và thanh cuộn dọc vào frame
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        return frame  # Trả về frame để tránh lỗi AttributeError




class Notis_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='pink')
        label = ctk.CTkLabel(self, text="Notifications Content", font=("Arial", 20), text_color="white")
        label.pack(pady=20)

