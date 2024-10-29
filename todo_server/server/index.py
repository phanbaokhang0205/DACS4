from tkinter import scrolledtext, messagebox
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



class SiderFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, navigate_callback):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')
        self.navigate_callback = navigate_callback

        # Dashboard
        self.dashboard = self.create_button("Dashboard", "server/icons/dashboard.png", "dashboard")
        self.dashboard.pack(fill="x", anchor=ctk.W)
        # Requests
        self.requests = self.create_button("Requests", "server/icons/terminal.png", "requests")
        self.requests.pack(fill="x", anchor=ctk.W)
        # Users
        self.users = self.create_button("Users", "server/icons/group.png", "users")
        self.users.pack(fill="x", anchor=ctk.W)
        # Notifications
        self.notis = self.create_button("Notification", "server/icons/notification.png", "notis")
        self.notis.pack(fill="x", anchor=ctk.W)

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
            "dashboard": Dashboard_Frame(self),
            "requests": Requests_Frame(self, log_list),
            "users": Users_Frame(self),
            "notis": Notis_Frame(self)
        }


class Dashboard_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='red')
        label = ctk.CTkLabel(self, text="Dashboard Content", font=("Arial", 20), text_color="white")
        label.pack(pady=20)


class Users_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='blue')
        label = ctk.CTkLabel(self, text="Users Content", font=("Arial", 20), text_color="white")
        label.pack(pady=20)


class Requests_Frame(ctk.CTkFrame):
    def __init__(self, master, log_list):
        super().__init__(master, corner_radius=10, fg_color='#768FCF')

        # # search_frame
        self.search = self.search_frame(self,log_list)
        self.search.pack(fill='x', expand=False, padx=10, pady=10)

        # ScrolledText để hiển thị log
        # self.log_display = scrolledtext.ScrolledText(self, width=80, height=20)
        # self.log_display.pack(fill='both', expand=True, pady=(0,10), padx=10)
        self.log_display = self.log_frame(self)
        self.log_display.pack(fill='both', expand=True, pady=(0,10), padx=10)

    def search_frame(self,master, log_list):
        frame = ctk.CTkFrame(master, fg_color='transparent')

        # Trường nhập liệu tìm kiếm
        self.search_entry = ctk.CTkEntry(frame, height=35, placeholder_text="Searching...", placeholder_text_color="gray", fg_color='black')
        self.search_entry.pack(side=ctk.LEFT, padx=(5,15), fill='x', expand=True)

        # Nút Refresh để cập nhật log
        refresh_button = ctk.CTkButton(frame, text="Refresh", height=35, command=lambda: self.update_logs(log_list))
        refresh_button.pack(padx=5,side=ctk.LEFT, expand=False)

        # Nút tìm kiếm
        search_button = ctk.CTkButton(frame, text="Search", height=35, command=lambda: self.search_logs(log_list))
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

    


class Notis_Frame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10, fg_color='pink')
        label = ctk.CTkLabel(self, text="Notifications Content", font=("Arial", 20), text_color="white")
        label.pack(pady=20)