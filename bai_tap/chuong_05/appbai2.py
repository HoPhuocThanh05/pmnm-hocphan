from flask import Flask, render_template, request
app = Flask(__name__)
def validate_score(text):
    text = text.strip()
    if not text:
        return None, "Vui lòng nhập một số."
    clean_text = text.replace(",", ".")
    try:
        score = float(clean_text)
    except ValueError:
        return None, "Vui lòng nhập một số."
    if score < 0 or score > 10:
        return None, "Điểm phải từ 0 đến 10."    
    return score, None
def get_letter_grade(final_score, ck_score):
    if ck_score < 1:
        return "F (điểm thi dưới 1)"
    
    if final_score >= 8.5:
        return "A"
    elif final_score >= 7.0:
        return "B"
    elif final_score >= 5.5:
        return "C"
    elif final_score >= 4.0:
        return "D"
    else:
        return "F"
@app.route("/", methods=["GET", "POST"])
def grade_calculator():
    values = {"cc": "", "gk": "", "ck": ""}
    errors = {}
    result = None
    if request.method == "POST":
        values = {k: request.form.get(k, "") for k in values}
        scores = {}

        for key in ["cc", "gk", "ck"]:
            score_val, err_msg = validate_score(values[key])
            if err_msg:
                errors[key] = err_msg
            else:
                scores[key] = score_val
        if not errors:
            cc = scores["cc"]
            gk = scores["gk"]
            ck = scores["ck"]
            final_score = round(cc * 0.1 + gk * 0.3 + ck * 0.6, 1)
            letter_grade = get_letter_grade(final_score, ck)
            result = f"{final_score} - {letter_grade}"
    return render_template("indexbai2.html", values=values, errors=errors, result=result)
if __name__ == "__main__":
    app.run(debug=True)