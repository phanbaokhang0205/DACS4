import requests

BASE_URL = "http://127.0.0.1:5000"
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
    
def addTask(user_id, project_id, title, description, status, begin_day, due_day, priority):
    url = f'{BASE_URL}/tasks'
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
        # Gửi yêu cầu POST
        response = requests.post(url, json=payload)
        
        if response.status_code == 201:
            print("Task added successfully.")
            return response.json()
        else:
            print(f"Failed to add task: {response.status_code}")
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def getTaskBySearching(keywords):
    base_url = f'{BASE_URL}/tasks/search'
    params = {
        'title': keywords
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
        return []  # Trả về mảng rỗng nế    u có lỗi
    
def delete_task(task_id):
    try:
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        if response.status_code == 200:
            return response.json()['message']
        else:
            return response.json()['error']
    except Exception as e:
        return f"An error occurred: {e}"
    
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
    

# ======================= USER =================================
def getUsers():
    base_url = f'{BASE_URL}/users'

    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(base_url)
        
        # Kiểm tra mã trạng thái
        if response.status_code == 200:
            # Chuyển đổi dữ liệu từ JSON thành Python dictionary
            return response.json()  # Trả về danh sách người dùng
        else:
            print(f"Không thể lấy dữ liệu: {response.status_code}")
            return []  # Trả về mảng rỗng nếu có lỗi

    except requests.exceptions.RequestException as e:
        print(f"Có lỗi xảy ra: {e}")
        return []  # Trả về mảng rỗng nếu có lỗi
    
def addUser():
    pass

def checkUser():
    pass

