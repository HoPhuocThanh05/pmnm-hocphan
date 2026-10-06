from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A", 
                   "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A", 
                   "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B", 
                   "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B", 
                   "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", 
                   "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C", 
                   "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

def tinh_dtb_va_xep_loai(scores):
    if not scores:
        return None, "-"
    dtb = round(sum(scores.values()) / len(scores), 2)
    if dtb >= 8.5: xl = "Xuất sắc"
    elif dtb >= 7.0: xl = "Giỏi"
    elif dtb >= 5.5: xl = "Khá"
    elif dtb >= 4.0: xl = "Trung bình"
    else: xl = "Yếu"
    return dtb, xl


@app.route("/")
def index():
    total_students = len(STUDENTS)
    unique_classes = set(st["lop"] for st in STUDENTS.values())
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Trang chủ</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>Trang chủ - Tổng quan</h2>
        <ul>
            <li>Tổng số sinh viên: <strong>{{ total_students }}</strong></li>
            <li>Số lớp (không trùng): <strong>{{ total_classes }}</strong></li>
        </ul>
        <p><a href="/students">Xem danh sách sinh viên (/students)</a> | <a href="/api/students">API Sinh viên</a></p>
    </body>
    </html>
    """
    return render_template_string(html_content, total_students=total_students, total_classes=len(unique_classes))


@app.route("/students", endpoint="student_list")
def student_list():
    selected_lop = request.args.get("lop", "").strip()
    all_classes = sorted(list(set(st["lop"] for st in STUDENTS.values())))
    
    student_results = []
    for mssv, info in STUDENTS.items():
        if selected_lop and info["lop"].lower() != selected_lop.lower():
            continue
        dtb, xep_loai = tinh_dtb_va_xep_loai(info.get("scores", {}))
        student_results.append({
            "mssv": mssv,
            "name": info["name"],
            "lop": info["lop"],
            "dtb": dtb if dtb is not None else "-",
            "xep_loai": xep_loai
        })
        
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Danh sách sinh viên</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>Danh sách Sinh viên</h2>
        <div>
            <strong>Lọc theo lớp: </strong>
            <a href="/students">Tất cả</a>
            {% for cls in all_classes %}
                | <a href="/students?lop={{ cls }}">{{ cls }}</a>
            {% endfor %}
        </div>
        <br>
        <table border="1" cellpadding="8" style="border-collapse: collapse;">
            <tr style="background-color: #f2f2f2;">
                <th>MSSV</th><th>Họ tên</th><th>Lớp</th><th>Điểm TB</th><th>Xếp loại</th>
            </tr>
            {% for st in student_results %}
            <tr>
                <td>{{ st.mssv }}</td>
                <td>{{ st.name }}</td>
                <td>{{ st.lop }}</td>
                <td>{{ st.dtb }}</td>
                <td>{{ st.xep_loai }}</td>
            </tr>
            {% endfor %}
        </table>
        <p><a href="/">Quay lại trang chủ</a></p>
    </body>
    </html>
    """
    return render_template_string(html_content, student_results=student_results, all_classes=all_classes)

# API JSON
@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)

if __name__ == "__main__":
    app.run(debug=True, port=8000)