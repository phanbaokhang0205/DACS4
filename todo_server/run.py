from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import socket, threading, time
from datetime import datetime
from call_api import *
from datetime import datetime, timedelta
import os

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# upload file
from werkzeug.utils import secure_filename

# Check ng dùng đăng nhập
# from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# def get_server_ip():
#     hostname = socket.gethostname() 
#     server_ip = socket.gethostbyname(hostname)
#     return server_ip

# server_ip = get_server_ip()

log_list=[]

# Upload file
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    server_ip = "https://flask-api-deploy-e1d2eecd08cb.herokuapp.com/"
    
    # Lấy phương thức HTTP (GET, POST, ...)
    method = request.method
    
    # Lấy mã trạng thái HTTP (200, 404, ...)
    status = response.status
    
    log_entry = f"{current_time}@{method}@{request.path}@{status}@{server_ip}@{client_ip}"
    log_list.append(log_entry)
    
    return response

# API để lấy log
@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(log_list), 200

@app.route('/api/logs/search', methods=['GET'])
def search_logs():
    kw = request.args.get('kw', '').lower()  # Từ khóa lấy từ query parameter
    print(f"Keyword received: {kw}")  # Debug từ khóa nhận được
    if not kw:
        return jsonify({"message": "Please provide a search keyword."}), 400

    filtered_logs = [log for log in log_list if kw in log.lower()]
    print(f"Filtered logs: {filtered_logs}")  # Debug kết quả lọc

    if not filtered_logs:
        return jsonify({"message": "No logs found for the given keyword."}), 404

    return jsonify({"logs": filtered_logs}), 200


# ================================= Define route =================================

# Tạo 1 login_required coi người dùng có đăng nhập hay chưa
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         # Kiem tra co user_id trong session khong:
#         if 'user' not in session:
#             # flash("Vui lòng đăng nhập trước!", "warning")
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user_username')
        password = request.form.get('user_password')
        
        # Lấy danh sách người dùng
        users = getUsers()
        
        # Kiểm tra từng người dùng để tìm user có username và password khớp
        for user in users:
            if user.get('username') == username:
                if check_password_hash(user.get('password'), password):
                    if update_user_status(user.get('id'), True):
                    # Lưu thông tin vào session sau khi xác thực thành công
                        session['user'] = user
                        return redirect("/")

                else:
                    flash("Mật khẩu không đúng!", "danger")
                
        flash("Tên đăng nhập không tồn tại", "danger")
    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            now = datetime.now()
            
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
            # create_at = datetime.now().isoformat()
            create_at = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

            # Chuyển đổi định dạng ngày tháng
            # create_at = datetime.strptime(create_at, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")

            hashed_password = generate_password_hash(password)

            # Kiểm tra nếu password và password_again khớp
            if password != password_again:
                flash("Mật khẩu và xác nhận mật khẩu không khớp!", "danger")
                return redirect(url_for('register'))

            data = {
                "fullname": fullname,
                "age": age,
                "gender": gender,
                "phone": phone,
                "address": address,
                "email": email,
                "username": username,
                "password": hashed_password,
                "avatar": avatar,
                "create_at": create_at,
            }
            
            addUser(**data)
            print(data)

            flash("Đăng kí tài khoản thành công! Hãy đăng nhập nhé", "success")
            return redirect(url_for('login'))
        except Exception as e:
            # Xử lý lỗi, ghi log và thông báo cho người dùng
            print(f"Đã xảy ra lỗi: {e}")
            print(f"Đã xảy ra lỗi trong quá trình xử lý!", "danger")
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    user = session.get('user')  # Lấy thông tin user từ session
    if user:
        # Gọi hàm cập nhật trạng thái offline
        if update_user_status(user.get('id'), False):
            # Xóa thông tin user khỏi session
            session.pop('user', None)

    return redirect(url_for('login'))


@app.route('/')
# @login_required
def dashboard():
    if 'user' in session:
        user = session['user']
        user_id = user.get('id')
        tasks = getTaskByUserId(user_id)
        project_count = len(getProjectByUserId(user_id))
        task_count = len(getTaskByUserId(user_id))
        done_count = sum(1 for task in tasks if task['status'] == 'COMPLETED')
        doing_count = sum(1 for task in tasks if task['status'] == 'IN_PROGRESS')
        todo_count = sum(1 for task in tasks if task['status'] == 'TODO')
        recent_tasks = sorted(tasks, key=lambda x: x['due_day'], reverse=True)[:3]

        return render_template('dashboard.html',
            user = user, project_count = project_count, 
            task_count = task_count, done_count = done_count, 
            doing_count = doing_count, todo_count = todo_count, recent_tasks = recent_tasks
        )
    else:
        return redirect(url_for('login'))
    
#==========================TASK===============================
@app.route('/tasks', methods=['GET', 'POST'])
# @login_required
def tasks():
    if 'user' in session:
        user = session['user']
        user_id = user.get('id')
        projects = getProjectByUserId(user_id)
        if request.method == 'POST':
            try:    
                user_id = user_id
                project_id = request.form.get('project_id')
                title = request.form.get('title')
                description = request.form.get('description')
                status = request.form.get('Status')
                begin_day = request.form.get('beginDay')
                due_day = request.form.get('dueDay')
                priority = request.form.get('priority')
                file = request.files.get('attachment') # Nhận fileee

                # Xử lí file upload (Nếu có)
                attachment_path = None
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    attachment_path = file_path # Duong dan luu filee

                # Chuyển đổi định dạng ngày tháng
                begin_day = datetime.strptime(begin_day, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")
                due_day = datetime.strptime(due_day, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")

                data = {
                    "user_id": user_id,
                    "project_id": project_id,
                    "title": title,
                    "description": description,
                    "status": status,
                    "begin_day": begin_day,
                    "due_day": due_day,
                    "priority": priority,
                    "attachment": attachment_path
                }
                addTask(**data)

                print("Dữ liệu đã được xử lý thành công!", "success")
                return redirect(url_for('tasks'))
            except Exception as e:
                # Xử lý lỗi, ghi log và thông báo cho người dùng
                print(f"Đã xảy ra lỗi: {e}")
                print(f"Đã xảy ra lỗi trong quá trình xử lý: {e}", "error")
        else:
            title = request.args.get('search')
            if title:
                tasks = getTaskBySearching(user_id, title)
            else:
                tasks = getTaskByUserId(user_id)
        return render_template('tasks.html', projects=projects, tasks = tasks, user = user)
    else:
        return redirect(url_for('login'))


@app.route('/delete_task', methods=['POST'])
def handle_delete_task():
    if 'user' in session:
        user = session['user']
        task_id = request.form.get('idForDelete')
        print("Task id: "+task_id)
        result = delete_task(task_id)
        if 'successfully' in result:
            print(result, 'success')
        else:
            print(result, 'error')
        return redirect(url_for('tasks', user=user))
    else:
        return redirect(url_for('login'))

@app.route('/update_task', methods=['POST'])
def handle_update_task():
    if 'user' in session:
        user = session['user']
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
            print(result, 'success')
        else:
            print(result, 'error')
        return redirect(url_for('tasks', user=user))
    else:
        return redirect(url_for('login'))
    
    
#===========================PROJECT================================
@app.route('/projects', methods=['GET', 'POST'])
# @login_required
def projects():
    if 'user' in session:
        user = session['user']
        user_id = user.get('id')
        
        if request.method == 'POST':
            try:    
                user_id = user_id
                name = request.form.get('name')
                description = request.form.get('description')
                created_at = request.form.get('created_at')
                updated_at = request.form.get('updated_at')

                # Chuyển đổi định dạng ngày tháng
                created_at = datetime.strptime(created_at, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")
                updated_at = datetime.strptime(updated_at, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")
                data = {
                    "user_id": user_id,
                    "name": name,
                    "description": description,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
                print(f"===========================: {created_at}, {updated_at}")
                addProject(**data)

                print("Dữ liệu đã được xử lý thành công!", "success")
                return redirect(url_for('projects'))
            except Exception as e:
                # Xử lý lỗi, ghi log và thông báo cho người dùng
                print(f"===========================: {created_at}, {updated_at}")
                print(f"Đã xảy ra lỗi: {e}")
                print(f"Đã xảy ra lỗi trong quá trình xử lý: {e}", "error")
        else:
            name = request.args.get('search')
            if name:
                projects = getProjectBySearching(user_id, name)
            else:
                projects = getProjectByUserId(user_id)
        return render_template('project.html', projects=projects, user = user)
    else:
        return redirect(url_for('login'))
    
@app.route('/delete_project', methods=['POST'])
def handle_delete_project():
    if 'user' in session:
        user = session['user']
        project_id = request.form.get('idForDelete')
        print("Project id: "+project_id)
        result = delete_project(project_id)
        if 'successfully' in result:
            print(result, 'success')
        else:
            print(result, 'error')
        return redirect(url_for('projects', user=user))
    else:
        return redirect(url_for('login'))

@app.route('/update_project', methods=['POST'])
def handle_update_project():
    if 'user' in session:
        user = session['user']
        project_id = request.form.get('idForUpdate')

        name = request.form.get('name-update')
        description = request.form.get('description-update')
        created_at = request.form.get('created_at-update')
        updated_at = request.form.get('updated_at-update')

        data = {
            "name": name,
            "description": description,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        
        result = update_project(project_id, data=data)
        if 'successfully' in result:
            print(result, 'success')
        else:
            print(result, 'error')
        return redirect(url_for('projects', user=user))
    else:
        return redirect(url_for('login'))
    
#=================================USER HOST================================
def track_client(client_ip):
    user_host = get_host_by_ip(client_ip)
    # Tạo thời gian theo định dạng đúng
    now = datetime.now()
    created_at = updated_at = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    if not user_host:
        # Nếu chưa tồn tại, thêm bản ghi mới
        new_host = addHost(client_ip, 0, 0, created_at, updated_at)
        if new_host:
            print("New host added:", new_host)
        else:
            print("Failed to add new host")
        return new_host
    return user_host

@app.before_request
def track_client_request():
    global client_ip
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    track_client(client_ip)

@app.after_request
def update_request_status(response):
    """
    Cập nhật success hoặc fail dựa trên trạng thái của response.
    """
    global client_ip
    status_code = response.status_code

    if 200 <= status_code < 300:
        # Thành công (2xx)
        user_host = get_host_by_ip(client_ip)
        if user_host:
            update_request(client_ip, True)
    else:
        # Thất bại (không phải 2xx)
        user_host = get_host_by_ip(client_ip)
        if user_host:
            update_request(client_ip, False)

    return response

    
#=================================SYSTEM INFO================================
@app.route('/system_info', methods=['GET'])
def system_info():
    info = get_system_info()
    return jsonify(info)

#=================================MAIN=======================================


if __name__ == '__main__':
    # app.secret_key = 'levanquochuykhangbaokhang2024chungtoideptraivailin'

    # Chay flask server trong thread rieng
    # flask_thread = threading.Thread(target=lambda: app.run(debug=True,host='0.0.0.0', port=5001, use_reloader=False))
    # flask_thread.daemon = True # De khi thoat Tkinter, Flask cung tu tat
    # flask_thread.start()

    app.run(debug=True,host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
