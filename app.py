import time
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from core.engine import build_scenario_list, get_scenario_by_index, validate_command

app = Flask(__name__)
app.secret_key = 'g5live_labs_super_secret'


@app.route('/')
def home():
    return render_template('menu.html')


@app.route('/start', methods=['POST'])
def start_lab():
    # 1. Capture Form Data
    session['difficulty'] = request.form.get('difficulty')
    session['time_limit'] = int(request.form.get('time_limit'))

    # Capture the list of selected modules (checkboxes)
    selected_modules = request.form.getlist('modules')
    if not selected_modules:
        selected_modules = ['security_plus']  # Fallback if none selected
    session['modules'] = selected_modules

    # 2. Build the dynamic queue to get the total question count
    scenarios = build_scenario_list(session['modules'], session['difficulty'])
    session['total_questions'] = len(scenarios)
    session['solved'] = []
    session['end_time'] = time.time() + session['time_limit']

    # Prevent crash if a combination yields 0 questions
    if session['total_questions'] == 0:
        return "Error: No scenarios found for this module/difficulty combination. Please add questions to the JSON files.", 400

    # Start at the 0th index of the compiled list
    return redirect(url_for('scenario', index=0))


@app.route('/scenario/<int:index>')
def scenario(index):
    if 'end_time' not in session or time.time() >= session['end_time']:
        return redirect(url_for('results'))

    scenario_data = get_scenario_by_index(session['modules'], session['difficulty'], index)
    if not scenario_data:
        return redirect(url_for('results'))

    time_left = int(session['end_time'] - time.time())

    # Determine if there is a next question
    next_index = index + 1 if (index + 1) < session['total_questions'] else None

    return render_template('index.html', scenario=scenario_data, index=index, next_index=next_index,
                           time_left=time_left)


@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.get_json()
    user_command = data.get('command')
    index = data.get('index')

    result = validate_command(user_command, session['modules'], session['difficulty'], index)

    if result.get('correct'):
        if 'solved' in session and index not in session['solved']:
            session['solved'].append(index)
            session.modified = True

    return jsonify(result)


@app.route('/results')
def results():
    if 'solved' not in session:
        return redirect(url_for('home'))

    score = len(session['solved'])
    total = session.get('total_questions', 1)
    pass_rate = round((score / total) * 100)
    passed = pass_rate >= 80

    return render_template('results.html', score=score, total=total, pass_rate=pass_rate, passed=passed)


if __name__ == '__main__':
    app.run(debug=True)