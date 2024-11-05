from flask import Flask, render_template, request, redirect, url_for, flash
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

def format_date(date_string):
    # Giả sử date_string có định dạng Thu, 28 Nov 2024 00:00:00 GMT
    date_object = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %Z')
    return date_object.strftime('%Y-%m-%d')

@app.template_filter('format_date')
def format_date(date_string):
    date_object = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %Z')
    return date_object.strftime('%Y-%m-%d')

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

@app.route('/delete_task', methods=['POST'])
def handle_delete_task():
    task_id = request.form.get('idForDelete')
    print("Task id: "+task_id)
    result = delete_task(task_id)
    if 'successfully' in result:
        flash(result, 'success')
    else:
        flash(result, 'error')
    return redirect(url_for('tasks'))

@app.route('/update_task', methods=['POST'])
def handle_update_task():
    task_id = request.form.get('idForUpdate')

    title = request.form.get('title-update')
    description = request.form.get('description-update')
    status = request.form.get('Status-update')
    begin_day = request.form.get('beginDay-update')
    due_day = request.form.get('dueDay-update')
    priority = request.form.get('priority-update')

    data = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "begin_day": begin_day,
        "due_day": due_day
    }
    
    result = update_task(task_id, data=data)
    if 'successfully' in result:
        flash(result, 'success')
    else:
        flash(result, 'error')
    return redirect(url_for('tasks'))

@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'POST':
        pio = request.form.get('priority')
        print(pio)
    users= getUsers()
    return render_template('users.html', users=users)

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