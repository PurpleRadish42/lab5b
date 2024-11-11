from flask import *
# Helper functions
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_primes(start, end):
    return [num for num in range(start, end + 1) if is_prime(num)]

def is_palindrome(s):
    return s == s[::-1]

app = Flask(__name__)

# Helper functions
def check_fill_blank(answer):
    # Check if "nile" (case insensitive) is present in the answer
    return 'nile' in answer.lower()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prime', methods=['GET', 'POST'])
def prime():
    if request.method == 'POST':
        try:
            num1 = int(request.form['num1'])
            num2 = int(request.form['num2'])
            if num1 <= 0 or num2 <= 0:
                message = "Input number should be greater than zero."
            elif num2 < num1:
                message = "The second input number should be greater than the first number."
            else:
                primes = find_primes(num1, num2)
                return render_template('prime.html', primes=primes, num1=num1, num2=num2)
        except ValueError:
            message = "Please enter valid integers."
        return render_template('prime.html', message=message)
    return render_template('prime.html')

@app.route('/palindrome', methods=['GET', 'POST'])
def palindrome():
    if request.method == 'POST':
        input_string = request.form['text']
        if input_string == input_string[::-1]:
            result_message = f"You entered '{input_string}'. It is a palindrome."
        else:
            result_message = f"You entered '{input_string}'. It is not a palindrome."
        return render_template('palindrome.html', message=result_message)
    
    return render_template('palindrome.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = 0
        result_detail = []

        # Check fill-in-the-blank question
        fill_blank_answer = request.form.get('fill_blank', '').strip()
        if check_fill_blank(fill_blank_answer):
            score += 1
            result_detail.append("Correct: The Nile is the longest river in the world, You got 1 mark!.")
        else:
            result_detail.append("Incorrect!: The Nile is the longest river in the world, You got 0 mark.")

        # Check multiple-choice question
        mcq_answer = request.form.get('mcq')
        if mcq_answer == 'Paris':
            score += 1
            result_detail.append("Correct: Paris is the capital of France, You got 1 mark!.")
        else:
            result_detail.append("Incorrect!: Paris is the capital of France, You got 0 mark.")

        # Check multiple-answer question (checkboxes)
        checkbox_answers = request.form.getlist('checkbox')
        correct_answers = {'India', 'Singapore'}
        selected_correct_answers = correct_answers.intersection(checkbox_answers)

        # Award 0.5 for each correct answer
        if len(checkbox_answers) > 2:
            result_detail.append("You have selected more than 2 options, please choose any 2.")
        else:
            if len(selected_correct_answers) == 2:
                score += 1
                result_detail.append("Correct: India & Singapore both have Tamil as one of their official languages, You got 1 mark!.")
            elif len(selected_correct_answers) == 1:
                score += 0.5
                country = selected_correct_answers.pop()
                result_detail.append(f"Partial Mark: Both India & Singapore both have Tamil as one of their official languages, hence you got 0.5 marks for selecting {country}.")
            else:
                result_detail.append("Incorrect!: India & Singapore both have Tamil as one of their official languages, You got 0 mark.")

        # Final result display
        result_summary = f"You scored {score} out of 3."
        return render_template('quiz.html', result_summary=result_summary, result_detail=result_detail)

    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug=True)
