from flask import Flask, render_template, request

app = Flask(__name__)
OPS = ["+", "-", "*", "/"]


def to_number(text):
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


# Đã kéo hàm calculate ra ngoài cùng cấp với to_number
def calculate(a, op, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return a / b


@app.route("/", methods=["GET", "POST"])
def calculator():
    values = {"a": "", "op": "+", "b": ""}
    errors, result = {}, None

    if request.method == "POST":
        values = {k: request.form.get(k, "").strip() for k in values}
        a = to_number(values["a"])
        b = to_number(values["b"])

        if a is None:
            errors["a"] = "Vui lòng nhập một số."
        if b is None:
            errors["b"] = "Vui lòng nhập một số."

        # Sửa errors[op] thành errors["op"]
        if values["op"] not in OPS:
            errors["op"] = "Phép toán không hợp lệ."
        elif values["op"] == "/" and b == 0:
            errors["b"] = "Không thể chia cho 0."

        if not errors:
            value = calculate(a, values["op"], b)
            result = f"{a:g} {values['op']} {b:g} = {value:g}"

    # Lệnh return nằm ngoài khối if request.method == "POST"
    return render_template(
        "index.html", values=values, errors=errors, result=result, ops=OPS
    )


if __name__ == "__main__":
    app.run(debug=True)