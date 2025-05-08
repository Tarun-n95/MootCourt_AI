from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models.user import User
from models.judge import Judge
from models.case import Case
from ai_engine.tts import speak
from ai_engine.questioning import generate_smart_questions
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models.performance import Performance
from ai_engine.transcriber import transcribe_audio, grade_answer
from ai_engine.fluency import analyze_fluency
import PyPDF2

app = Flask(__name__)
from datetime import timedelta

app.permanent_session_lifetime = timedelta(days=30)  # Keep user logged in for 30 days

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)  # Secret key for sessions

# PDF Reader
def read_pdf(path):
    text = ""
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Home
@app.route('/')
def home():
    return render_template('index.html')

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.find_by_email(email):
            flash('Email already exists!')
            return redirect(url_for('signup'))
        
        User.create_user(username, email, password)
        flash('Signup Successful! Please login.')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("🔐 Login attempt:", email)

        user = User.find_by_email(email)
        print("🧑 User from DB:", user)

        if user:
            print("🧠 Stored password (hashed):", user[3])
            print("🔍 Password match:", check_password_hash(user[3], password))

        if user and check_password_hash(user[3], password):
            session.permanent = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            print("✅ Login successful. Redirecting to dashboard.")
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.')
            print("❌ Login failed. Redirecting back to login.")
            return redirect(url_for('login'))

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        uploaded_cases = Case.get_cases_by_user(session['user_id'])
        
        # --- Fetch challenge badges ---
        challenge_count = Performance.get_challenge_count_by_user(session['user_id'])
        badges = []

        if challenge_count >= 1:
            badges.append("First Battle 🏅")
        if challenge_count >= 5:
            badges.append("Warrior 🛡️")
        if challenge_count >= 10:
            badges.append("Veteran ⚔️")
        if challenge_count >= 25:
            badges.append("Master Advocate 👑")

        return render_template('dashboard.html', username=session['username'],
                               uploaded_cases=uploaded_cases,
                               badges=badges)
    else:
        flash('Please login first!')
        return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Judge Panel
@app.route('/judges', methods=['GET', 'POST'])
def judge_panel():
    judges = None
    if request.method == 'POST':
        num_judges = int(request.form['num_judges'])
        judges = Judge.get_random_judges(num_judges)
    return render_template('judge_panel.html', judges=judges)

# Speech Function
@app.route('/speak/<judge_name>')
def judge_speak(judge_name):
    message = f"I am {judge_name}. Please present your arguments."
    speak(message)
    flash(f"{judge_name} has spoken. Check your speakers!")
    return redirect(url_for('judge_panel'))

# Judge Asks Question Function
@app.route('/ask_questions/<judge_name>')
def ask_questions(judge_name):
    case_text = "This is a dummy case text for now."  # Later we can upload real cases
    questions = generate_smart_questions(case_text, "Civil Law", "Medium")
    
    for q in questions:
        message = f"{judge_name} asks: {q}"
        speak(message)
    
    flash(f"{judge_name} asked {len(questions)} questions!")
    return redirect(url_for('judge_panel'))

# Argue Function
@app.route('/argue', methods=['GET', 'POST'])
def argue():
    result = None
    score_a = 0
    score_b = 0
    feedback_a = ""
    feedback_b = ""

    if request.method == 'POST':
        arg_a = request.form['arg_a']
        arg_b = request.form['arg_b']

        # --- Grading Logic ---
        # Score based on length of argument (basic for now)
        len_a = len(arg_a.split())
        len_b = len(arg_b.split())

        # Basic scoring: longer arguments get more marks, capped at 10
        score_a = min(len_a // 10, 10)  # Every 10 words = 1 mark
        score_b = min(len_b // 10, 10)

        # --- Feedback ---
        feedback_a = "Good depth, but be concise." if score_a >= 7 else "Try to elaborate more on your arguments."
        feedback_b = "Good structure and depth." if score_b >= 7 else "Work on providing more legal reasoning."

        # --- Result ---
        if score_a > score_b:
            result = "Student A wins!"
        elif score_b > score_a:
            result = "Student B wins!"
        else:
            result = "It's a Tie!"
        # --- Performance ---
        if 'user_id' in session:
            Performance.save_performance(session['user_id'], "Student B", score_a, result)

    return render_template('argue.html', result=result, score_a=score_a, score_b=score_b,
                           feedback_a=feedback_a, feedback_b=feedback_b)

# Upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_case', methods=['GET', 'POST'])
def upload_case():
    questions = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        case_type = request.form['case_type']
        difficulty = request.form['difficulty']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if filename.endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    case_text = f.read()
            elif filename.endswith('.pdf'):
                case_text = read_pdf(filepath)
            else:
                case_text = ""

            if 'user_id' in session:
                Case.save_case(session['user_id'], filename, case_text)

            # Pass case_type to generate smarter questions!
            questions = generate_smart_questions(case_text, case_type, difficulty)

    return render_template('upload_case.html', questions=questions)

# Performance
@app.route('/performance')
def performance():
    if 'user_id' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))

    records = Performance.get_performance_by_user(session['user_id'])

    total_battles = len(records)
    average_score = sum([r[1] for r in records]) / total_battles if total_battles > 0 else 0
    best_score = max([r[1] for r in records]) if total_battles > 0 else 0

    # --- Prepare timestamps and scores for graph ---
    timestamps = [str(r[3]) for r in records]  # VERY IMPORTANT: Convert all to strings
    scores = [r[1] for r in records]

    return render_template('performance.html',
                           records=records,
                           total_battles = total_battles,
                           average_score = average_score,
                           best_score = best_score,
                           timestamps = timestamps,
                           scores = scores)


# Audio Saving
@app.route('/save_audio', methods=['POST'])
def save_audio():
    if 'audio_data' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio_data']

    filename = secure_filename(audio_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'audio', filename)
    audio_file.save(filepath)

    return jsonify({'success': True, 'filename': filename})

# Transcriber
@app.route('/transcribe_and_grade/<filename>/<case_type>')
def transcribe_and_grade(filename, case_type):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'audio', filename)
    
    transcribed_text = transcribe_audio(filepath)
    score, feedback = grade_answer(transcribed_text, case_type)

    # --- Fluency Analysis ---
    fluency_score, fluency_feedback = analyze_fluency(transcribed_text)


    # Save to performance history
    if 'user_id' in session:
        Performance.save_performance(
            user_id=session['user_id'],
            opponent_name="Oral Practice",
            score=score,
            result="Oral Answer",
            transcription=transcribed_text,
            feedback=feedback + " | Fluency: " + fluency_feedback
        )

    return render_template('transcription_result.html', transcribed_text=transcribed_text, score=score, feedback=feedback, fluency_score=fluency_score, fluency_feedback=fluency_feedback)

@app.route('/challenge')
def challenge():
    return render_template('challenge.html')

if __name__ == '__main__':
    port = int(os.environ.get('port', 10000))
    app.run(host='0.0.0.0', port=10000)