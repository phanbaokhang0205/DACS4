from flask import Flask, render_template, request, redirect, url_for, flash
import socket, threading
from datetime import datetime
from call_api import *
from server.index import App
from datetime import datetime

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            fullname = request.form.get('fullname')
            age = request.form.get('age')
            gender = request.form.get('gender')
            phone = request.form.get('phone')
            address = request.form.get('address')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            password_again = request.form.get('pass_again')
            avatar = request.form.get('avatar')
            create_at = datetime.now().isoformat()

             # Kiểm tra nếu password và password_again khớp
            if password != password_again:
                flash("Mật khẩu và xác nhận mật khẩu không khớp!", "error")
                return redirect(url_for('register'))

            data = {
                "fullname": fullname,
                "age": age,
                "gender": gender,
                "phone": phone,
                "address": address,
                "email": email,
                "username": username,
                "password": password,
                "avatar": avatar,
                "create_at": create_at,
            }
            addUser(**data)

            flash("Dữ liệu đã được xử lý thành công!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            # Xử lý lỗi, ghi log và thông báo cho người dùng
            print(f"Đã xảy ra lỗi: {e}")
            flash(f"Đã xảy ra lỗi trong quá trình xử lý: {e}", "error")
    
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

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    projects = getProjects()

    if request.method == 'POST':
        try:    
            user_id = 1
            project_id = request.form.get('project_id')
            title = request.form.get('title')
            description = request.form.get('description')
            status = request.form.get('Status')
            begin_day = request.form.get('beginDay')
            due_day = request.form.get('dueDay')
            priority = request.form.get('priority')

            data = {
                "user_id": user_id,
                "project_id": project_id,
                "title": title,
                "description": description,
                "status": status,
                "begin_day": begin_day,
                "due_day": due_day,
                "priority": priority
            }
            addTask(**data)

            flash("Dữ liệu đã được xử lý thành công!", "success")
            return redirect(url_for('tasks'))
        except Exception as e:
            # Xử lý lỗi, ghi log và thông báo cho người dùng
            print(f"Đã xảy ra lỗi: {e}")
            flash(f"Đã xảy ra lỗi trong quá trình xử lý: {e}", "error")
    else:
        title = request.args.get('search')
        if title:
            tasks = getTaskBySearching(title)
        else:
            tasks = getTasks()
    return render_template('tasks.html', projects=projects, tasks = tasks)

# @app.route('/users', methods=['GET','POST'])
# def users():
#     if request.method == 'POST':
#         pio = request.form.get('priority')
#         print(pio)
#     users= getUsers()
#     return render_template('users.html', users=users)



if __name__ == '__main__':
    app.secret_key = 'your_secret_key'  # Thay thế bằng chuỗi bí mật của bạn

    # app.run(debug=True)
    # Chay flask server trong thread rieng
    flask_thread = threading.Thread(target=lambda: app.run(debug=True,host=server_ip, port=5001, use_reloader=False))
    flask_thread.daemon = True # De khi thoat Tkinter, Flask cung tu tat
    flask_thread.start()

    # Khoi chay giao dien tkinter
    server_ui = App(log_list=log_list)
    server_ui.mainloop()