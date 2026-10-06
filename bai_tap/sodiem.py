from flask import Flask, request, jsonify, render_template_string, abort, redirect, url_for, make_response

app = Flask(__name__)
app.json.ensure_ascii = False

# Dữ liệu sinh viên mẫu
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

# CÂU 1: Trang chủ
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
        <p><a href="/students">Xem danh sách sinh viên (/students)</a> | <a href="/search">Tìm kiếm (/search)</a></p>
    </body>
    </html>
    """
    return render_template_string(html_content, total_students=total_students, total_classes=len(unique_classes))

# CÂU 2: Danh sách sinh viên
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
            "dtb": str(dtb) if dtb is not None else "-",
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
                <td><a href="/students/{{ st.mssv }}">{{ st.mssv }}</a></td>
                <td>{{ st.name }}</td>
                <td>{{ st.lop }}</td>
                <td>{{ st.dtb }}</td>
                <td>{{ st.xep_loai }}</td>
            </tr>
            {% endfor %}
        </table>
        <p><a href="/">Quay lại trang chủ</a> | <a href="/search">Tìm kiếm sinh viên</a></p>
    </body>
    </html>
    """
    return render_template_string(html_content, student_results=student_results, all_classes=all_classes)

# CÂU 3: Chi tiết sinh viên (/students/<mssv>)
@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    
    st = STUDENTS[mssv]
    dtb, xep_loai = tinh_dtb_va_xep_loai(st.get("scores", {}))
    dtb_str = str(dtb) if dtb is not None else "-"
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Chi tiết sinh viên</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>Thông tin sinh viên: {{ st.name }}</h2>
        <p><strong>MSSV:</strong> {{ mssv }}</p>
        <p><strong>Lớp:</strong> <a href="/students?lop={{ st.lop }}">{{ st.lop }}</a></p>
        <p><strong>Điểm trung bình:</strong> {{ dtb_str }}</p>
        <p><strong>Xếp loại:</strong> {{ xep_loai }}</p>
        
        <h3>Bảng điểm từng học phần</h3>
        {% if st.scores %}
        <table border="1" cellpadding="8" style="border-collapse: collapse;">
            <tr style="background-color: #f2f2f2;">
                <th>Môn học</th>
                <th>Điểm</th>
            </tr>
            {% for subject, score in st.scores.items() %}
            <tr>
                <td>{{ subject }}</td>
                <td>{{ score }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p><em>Sinh viên chưa có điểm học phần nào.</em></p>
        {% endif %}
        
        <br>
        <p>
            <a href="/students/{{ mssv }}/export">Tải bảng điểm (CSV)</a> | 
            <span>Link rút gọn: <a href="/sv/{{ mssv }}">/sv/{{ mssv }}</a></span>
        </p>
        
        <p><a href="/students">← Quay lại danh sách sinh viên</a></p>
    </body>
    </html>
    """
    return render_template_string(html_content, mssv=mssv, st=st, dtb_str=dtb_str, xep_loai=xep_loai)

# CÂU 4: Link rút gọn (/sv/<mssv>) -> Redirect 301
@app.route("/sv/<mssv>")
def short_link(mssv):
    return redirect(url_for('student_detail', mssv=mssv), code=301)

# CÂU 5: Xuất bảng điểm CSV (/students/<mssv>/export)
@app.route("/students/<mssv>/export")
def export_csv(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    
    st = STUDENTS[mssv]
    lines = ["hoc_phan,diem"]
    for subject, score in st.get("scores", {}).items():
        lines.append(f"{subject},{score}")
    
    csv_data = "\n".join(lines)
    
    response = make_response(csv_data)
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    
    return response

# CÂU 6: Tìm kiếm an toàn (/search?q=...)
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    results = []
    
    if query:
        query_lower = query.lower()
        for mssv, info in STUDENTS.items():
            # Tìm kiếm chứa từ khóa trong Họ tên HOẶC MSSV (không phân biệt hoa/thường)
            if query_lower in info["name"].lower() or query_lower in mssv.lower():
                results.append({
                    "mssv": mssv,
                    "name": info["name"],
                    "lop": info["lop"]
                })

    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Tìm kiếm sinh viên</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>Tìm kiếm sinh viên</h2>
        <form action="/search" method="GET">
            <input type="text" name="q" value="{{ query }}" placeholder="Nhập tên hoặc MSSV..." style="padding: 5px; width: 250px;">
            <button type="submit" style="padding: 5px 10px;">Tìm kiếm</button>
        </form>
        <br>
        {% if query %}
            <p>Tìm thấy <strong>{{ results|length }}</strong> kết quả cho "<strong>{{ query }}</strong>"</p>
            {% if results %}
                <ul>
                {% for st in results %}
                    <li><a href="/students/{{ st.mssv }}">{{ st.mssv }} - {{ st.name }}</a> (Lớp {{ st.lop }})</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>Không tìm thấy sinh viên nào phù hợp.</p>
            {% endif %}
        {% endif %}
        
        <p><a href="/students">Quay lại danh sách sinh viên</a> | <a href="/">Trang chủ</a></p>
    </body>
    </html>
    """
    return render_template_string(html_content, query=query, results=results)

# API JSON
@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
