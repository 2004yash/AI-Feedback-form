from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import openai
from urllib.parse import quote, unquote
from dotenv import load_dotenv
import os
import json
import base64

# Load environment variables
load_dotenv('.env.local')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

total_questions = 10

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def get_questions():
    with open('questions.json', 'r') as f:
        return json.load(f)['questions']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question', methods=['GET'])
def question():
    try:
        kid_name = request.args.get('kid_name')
        phone_no = request.args.get('phone_no')
        ques_no = int(request.args.get('ques_no', 1))
        custom_question = request.args.get('question')  # For follow-up questions
        
        # Calculate progress percentage
        if custom_question:
            total = total_questions + 5
            progress_percentage = round((ques_no / total) * 100)
            # Handle follow-up question
            return render_template('question.html',
                                question=custom_question,
                                kid_name=kid_name,
                                phone_no=phone_no,
                                encoded_text=quote(custom_question),
                                encoded_ques_no=quote(str(ques_no)),
                                current_question=ques_no,
                                total_questions=total,
                                progress_percentage=progress_percentage)
        else:
            # Handle regular questions from questions.json
            questions = get_questions()
            if ques_no > len(questions):
                return redirect('/')
            
            progress_percentage = round((ques_no / len(questions)) * 100)
            current_question = questions[ques_no - 1]
            encoded_text = base64.b64encode(current_question.encode()).decode()
            encoded_ques_no = base64.b64encode(str(ques_no).encode()).decode()
            
            return render_template('question.html',
                                question=current_question,
                                kid_name=kid_name,
                                phone_no=phone_no,
                                encoded_text=encoded_text,
                                encoded_ques_no=encoded_ques_no,
                                current_question=ques_no,
                                total_questions=len(questions),
                                progress_percentage=progress_percentage)
    except Exception as e:
        print(f"Error in question route: {e}")
        return "An error occurred", 500

@app.route('/store_in_sql', methods=['GET'])
def store_answer():
    try:
        kid_name = request.args.get('kid_name')
        phone_no = request.args.get('phone_no')
        answer = request.args.get('answer')
        encoded_text = request.args.get('encoded_text')
        encoded_ques_no = request.args.get('encoded_ques_no')
        
        question = base64.b64decode(encoded_text).decode()
        ques_no = int(base64.b64decode(encoded_ques_no).decode())

        conn = get_db_connection()
        if not conn:
            return "Database connection error", 500

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback_qna2 (kid_name, phone_no, ques, ans)
            VALUES (%s, %s, %s, %s)
        """, (kid_name, phone_no, question, answer))
        conn.commit()
        cursor.close()
        conn.close()

        questions = get_questions()
        if ques_no < len(questions):
            return redirect(url_for('question',
                                  kid_name=kid_name,
                                  phone_no=phone_no,
                                  ques_no=ques_no + 1))
        else:
            # Generate follow-up questions using OpenAI
            return generate_followup_questions(kid_name, phone_no)
            
    except Exception as e:
        print(f"Error in store_answer route: {e}")
        return "An error occurred", 500

def generate_followup_questions(kid_name, phone_no):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ques, ans FROM feedback_qna2 
            WHERE phone_no = %s 
            ORDER BY id
        """, (phone_no,))
        responses = cursor.fetchall()
        cursor.close()
        conn.close()

        # Format responses for OpenAI
        conversation_history = "\n".join([f"Q: {q}\nA: {a}" for q, a in responses])
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Based on these responses:\n{conversation_history}\n\nGenerate a relevant follow-up question:",
            max_tokens=50,
            temperature=0.7
        )
        
        follow_up_question = response.choices[0].text.strip()
        
        return redirect(url_for('question',
                              question=follow_up_question,
                              kid_name=kid_name,
                              phone_no=phone_no,
                              ques_no=total_questions + 1))
    except Exception as e:
        print(f"Error generating follow-up questions: {e}")
        return "Survey completed. Thank you!"

if __name__ == '__main__':
    app.run(debug=True)










