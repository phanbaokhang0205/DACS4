from datetime import datetime

def countTasksByMonth(tasks):
    # Khởi tạo dữ liệu trống cho 12 tháng
    months = {month: {"completed": 0, "in_progress": 0, "todo": 0} for month in range(1, 13)}

    for task in tasks:
        # Chuyển đổi chuỗi ngày tháng từ API sang datetime
        try:
            due_date = datetime.strptime(task["due_day"], "%a, %d %b %Y %H:%M:%S %Z")
            month = due_date.month  # Lấy tháng từ ngày
        except ValueError:
            print(f"Không thể chuyển đổi ngày: {task['due_day']}")
            continue

        # Đếm số lượng task theo trạng thái
        if task["status"] == "COMPLETED":
            months[month]["completed"] += 1
        elif task["status"] == "IN_PROGRESS":
            months[month]["in_progress"] += 1
        elif task["status"] == "TODO":
            months[month]["todo"] += 1

    return months
