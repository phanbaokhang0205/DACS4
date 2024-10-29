from flask import Flask, render_template, request, redirect, url_for
import socket, threading
from datetime import datetime
from call_api import *
from server.index import App

app = Flask(__name__)

def get_server_ip():
    hostname = socket.gethostname() 
    server_ip = socket.gethostbyname(hostname)
    return server_ip

server_ip = get_server_ip()


log_list=[]

# Hàm log request vào log_list
# Log request thông tin sau khi xử lý request
@app.after_request
def log_request_info(response):
    # Lấy thời gian hiện tại
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Lấy địa chỉ IP của client, kiểm tra header 'X-Forwarded-For' nếu có
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Lấy địa chỉ IP của server
    server_ip = get_server_ip()
    
    # Lấy phương thức HTTP (GET, POST, ...)
    method = request.method
    
    # Lấy mã trạng thái HTTP (200, 404, ...)
    status = response.status
    
    log_entry = f"{current_time}@{method}@{request.path}@{status}@{server_ip}@{client_ip}"
    log_list.append(log_entry)
    
    return response


# ================================= Define route =================================
@app.route('/')
@app.route('/login')
def login():
    
    return render_template('auth/login.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    pass

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')

@app.route('/tasks')
def tasks():
    
    return render_template('tasks.html')
@app.route('/users')
def users():
    users= getUsers()
    return render_template('users.html', users=users)

if __name__ == '__main__':
        

    # app.run(debug=True)
    # Chay flask server trong thread rieng
    flask_thread = threading.Thread(target=lambda: app.run(debug=True,host=server_ip, port=5001, use_reloader=False))
    flask_thread.daemon = True # De khi thoat Tkinter, Flask cung tu tat
    flask_thread.start()

    # Khoi chay giao dien tkinter
    server_ui = App(log_list=log_list)
    server_ui.mainloop()