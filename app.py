from flask import Flask, render_template, request
import string
import random

app = Flask(__name__)

def estimate_brute_force_time(password):
    guesses_per_second = 1e9  # تخمينات في الثانية
    possible_characters = len(string.ascii_letters + string.digits + string.punctuation)
    total_guesses = possible_characters ** len(password)
    seconds = total_guesses / guesses_per_second
    if seconds < 60:
        return f"{int(seconds)} ثانية"
    elif seconds < 3600:
        return f"{int(seconds//60)} دقيقة"
    elif seconds < 86400:
        return f"{int(seconds//3600)} ساعة"
    elif seconds < 31536000:
        return f"{int(seconds//86400)} يوم"
    else:
        return f"{min(int(seconds // 31536000), 100)} سنة"

def get_strength_score(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    return score

def analyze_password(password):
    score = get_strength_score(password)
    suggestions = []
    if len(password) < 8:
        suggestions.append("🔒 اجعل طول كلمة المرور 8 أحرف على الأقل.")
    if not any(c.islower() for c in password):
        suggestions.append("🔡 أضف أحرفًا صغيرة (a-z).")
    if not any(c.isupper() for c in password):
        suggestions.append("🔠 أضف أحرفًا كبيرة (A-Z).")
    if not any(c.isdigit() for c in password):
        suggestions.append("🔢 أضف أرقامًا.")
    if not any(c in string.punctuation for c in password):
        suggestions.append("❗ أضف رموزًا مثل (!, @, #).")

    colors = {5: 'green', 4: 'orange', 3: 'orange', 2: 'red', 1: 'red', 0: 'red'}
    labels = {5: 'قوية جدًا', 4: 'قوية', 3: 'متوسطة', 2: 'ضعيفة', 1: 'ضعيفة جدًا', 0: 'ضعيفة جدًا'}

    return {
        "score": score,
        "color": colors[score],
        "label": labels[score],
        "time": estimate_brute_force_time(password)
    }, suggestions

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    suggestions = None
    attacks_info = None
    generated = request.args.get("generated")

    if request.method == 'POST':
        password = request.form['password']
        results, suggestions = analyze_password(password)
        attacks_info = {
            "length": len(password),
            "time": results["time"]
        }

    return render_template('index.html', results=results, suggestions=suggestions, attacks_info=attacks_info, generated=generated)

@app.route('/generate')
def generate_ai_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(16))
    return render_template('index.html', results=None, suggestions=None, attacks_info=None, generated=password)

if __name__ == '__main__':
    app.run(debug=True)