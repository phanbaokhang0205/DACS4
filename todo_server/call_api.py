import requests

# =================================Call api =================================
def getUsers():
    base_url = 'http://127.0.0.1:5000/users'

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
    
def getTasks():
    base_url = 'http://127.0.0.1:5000/tasks'

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