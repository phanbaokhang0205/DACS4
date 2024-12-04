import requests

# BASE_URL = "http://127.0.0.1:5000/"
BASE_URL = "https://flask-api-deploy-e1d2eecd08cb.herokuapp.com/"

# =================================Call api =================================
# ======================= TASK =================================
def getTasks():
    base_url = f'{BASE_URL}/tasks'
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(base_url)
        
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi
    
def getTaskByUserId(user_id):
    url = f'{BASE_URL}/tasks/{user_id}'
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi


def addTask(user_id, project_id, title, description, status, begin_day, due_day, priority):
    url = f'{BASE_URL}/tasks'
    
    # Tạo payload cho các dữ liệu còn lại
    payload = {
        "user_id": user_id,
        "project_id": project_id,
        "title": title,
        "description": description,
        "status": status,
        "begin_day": begin_day,
        "due_day": due_day,
        "priority": priority
    }

    try:
        # Gửi yêu cầu POST với multipart/form-data (cho file)
        response = requests.post(url, data=payload)
        
        if response.status_code == 201:
            print("Task added successfully.")
            return response.json()
        else:
            print(f"Failed to add task: {response.status_code}, {response.text}")
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None



def getTaskBySearching(user_id, keywords):
    # Thêm user_id vào URL
    base_url = f'{BASE_URL}/tasks/search/{user_id}'
    params = {
        'title': keywords  # Thêm từ khóa tìm kiếm vào query parameters
    }
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            return response.json()  # Trả về danh sách task dưới dạng JSON
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []  # Trả về danh sách rỗng nếu lỗi HTTP

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về danh sách rỗng nếu xảy ra lỗi yêu cầu

    
def delete_task(task_id):
    try:
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        if response.status_code == 200:
            return response.json()['message']
        else:
            return response.json()['error']
    except Exception as e:
        return f"An error occurred: {e}"
    
def update_task(task_id, data):
    try:
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=data)
        if response.status_code == 200:
            return response.json()['message']
        else:
            return response.json()['error']
    except Exception as e:
        return f"An error occurred: {e}"
    
def update_user(id, data):
    try:
        response = requests.put(f'{BASE_URL}/users/{id}', json=data)
        if response.status_code == 200:
            return response.json()['message']
        else:
            return response.json()['error']
    except Exception as e:
        return f"An error occurred: {e}"

def get_user_by_id(id):
    response = requests.get(f'{BASE_URL}/users/{id}')
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()['error']

    
# ======================= PROJECT =================================
def getProjects():
    base_url = f'{BASE_URL}/projects'

    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(base_url)
        
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi
    
def getProjectByUserId(user_id):
    url = f'{BASE_URL}/projects/{user_id}'
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi

def addProject(user_id, name, description, created_at, updated_at):
    url = f'{BASE_URL}/projects'
    payload = {
        "user_id": user_id,
        "name": name,
        "description": description,
        "created_at": created_at,
        "updated_at": updated_at
    }

    try:
        # Gửi yêu cầu POST
        response = requests.post(url, json=payload)
        
        if response.status_code == 201:
            print("Project added successfully.")
            return response.json()
        else:
            print(f"Failed to add project: {response.status_code}")
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    
def getProjectBySearching(user_id, keywords):
    base_url = f'{BASE_URL}/projects/search/{user_id}'
    params = {
        'name': keywords
    }
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi


def delete_project(project_id):
    try:
        response = requests.delete(f'{BASE_URL}/projects/{project_id}')
        if response.status_code == 200:
            return response.json()['message']
        else:
            return response.json()['error']
    except Exception as e:
        return f"An error occurred: {e}"
    
def update_project(project_id, data):
    try:
        response = requests.put(f'{BASE_URL}/projects/{project_id}', json=data)
        if response.status_code == 200:
            return response.json()['message']
        else:
            return response.json()['error']
    except Exception as e:
        return f"An error occurred: {e}"
    

# ======================= USER =================================
def getUsers():
    base_url = f'{BASE_URL}/users'

    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(base_url)
        
        # Kiểm tra mã trạng thái
        if response.status_code == 200:
            # Chuyển đổi dữ liệu từ JSON thành Python dictionary
            data = response.json()
            users = data.get('users', [])
            online_count = data.get('online_count', 0)
            offline_count = data.get('offline_count', 0)
            print(f"Số lượng online: {online_count}, offline: {offline_count}")
            return users  # Trả về danh sách người dùng
        else:
            print(f"Không thể lấy dữ liệu111: {response.status_code}")
            return []  # Trả về mảng rỗng nếu có lỗi

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi
    

def addUser(fullname, age, gender, phone, address, email, username, password, avatar, create_at):
    url = 'https://flask-api-deploy-e1d2eecd08cb.herokuapp.com/users'
    payload = {
        "fullname": fullname,
        "age": age,
        "gender": gender,
        "phone": phone,
        "address": address,
        "email": email,
        "username": username,
        "password": password,
        "avatar": avatar,
        "create_at": create_at
    }
    # Gui yeu cau post
    try:
        response = requests.post(url, json=payload)
        print(payload)
        if response.status_code == 201:
            print("User register successfully.")
            return response.json()
        else:
            print(f"Failed to register: {response.status_code}")
            return response.json()
    except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None
    

def update_user_status(user_id, is_online):
    url = f"{BASE_URL}/users/{user_id}/status"
    try:
        response = requests.put(url, json={'isOnline': is_online})
        if response.status_code == 200:
            return True  # Thành công
        else:
            print(f"Không thể cập nhật trạng thái: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        return False

# ======================= System Info =================================
def get_system_info():
    base_url = f'{BASE_URL}/system_info'
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []  # Trả về mảng rỗng nếu có lỗi
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

# ======================= USER HOST =================================
def get_all_host():
    url = f'{BASE_URL}/user_host'
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Không thể lấy dữ liệu user_host: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi


def get_host_by_ip(client_ip):
    url = f'{BASE_URL}/user_host/{client_ip}'
    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json() 
        else:
            print(f"Không thể lấy dữ liệu user_host: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi
    
def addHost(client_ip, success, fail, created_at, updated_at):
    url = f'{BASE_URL}/user_host'
    payload = {
        "client_ip": client_ip,
        "success": success,
        "fail": fail,
        "created_at": created_at,
        "updated_at": updated_at
    }
    print("Payload being sent:", payload)  # Thêm dòng log để kiểm tra payload

    try:
        # Gửi yêu cầu POST
        response = requests.post(url, json=payload)
        
        if response.status_code == 201:
            print("Host added successfully.")
            return response.json()
        else:
            print(f"Failed to add Host: {response.status_code}")
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None 

def update_request(client_ip, isSuccess):
    url = f"{BASE_URL}/user_host/{client_ip}/status"
    try:
        response = requests.put(url, json={
            'isSuccess': isSuccess,
        })
        if response.status_code == 200:
            print(f"cập nhật trạng thái user_host thành công: {response.status_code}")
            return True  # Thành công
        else:
            print(f"Không thể cập nhật trạng thái user_host: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        return False
