from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import openai
from urllib.parse import quote, unquote
from dotenv import load_dotenv
import os

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question', methods=['GET'])
def question():
    try:
        kid_name = request.args.get('kid_name')
        phone_no = request.args.get('phone_no')
        ques_no = int(request.args.get('ques_no', 1))
        
        conn = get_db_connection()
        if not conn:
            return "Database connection error", 500
            
        cursor = conn.cursor()
        cursor.execute("SELECT question_text FROM questions WHERE id = %s", (ques_no,))
        question = cursor.fetchone()
        cursor.close()
        conn.close()

        if not question:
            return "Question not found", 404

        encoded_text = quote(question[0])
        encoded_ques_no = quote(str(ques_no))
        
        return render_template('question_page.html',
                             question=question[0],
                             kid_name=kid_name,
                             phone_no=phone_no,
                             encoded_text=encoded_text,
                             encoded_ques_no=encoded_ques_no,
                             current_question=ques_no,
                             total_questions=total_questions)
    except Exception as e:
        print(f"Error in question route: {e}")
        return "An error occurred", 500

@app.route('/store_in_sql', methods=['GET'])
def store_answer():
    try:
        kid_name = request.args.get('kid_name')
        phone_no = request.args.get('phone_no')
        question = unquote(request.args.get('encoded_text'))
        answer = request.args.get('answer')
        current_question = int(request.args.get('ques_no'))

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

        next_question = current_question + 1
        
        if next_question <= total_questions:
            return redirect(url_for('question',
                                  kid_name=kid_name,
                                  phone_no=phone_no,
                                  ques_no=next_question))
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
        
        return redirect(url_for('question2',
                              question=follow_up_question,
                              kid_name=kid_name,
                              phone_no=phone_no,
                              ques_no=total_questions + 1))
    except Exception as e:
        print(f"Error generating follow-up questions: {e}")
        return "Survey completed. Thank you!"

@app.route('/question2', methods=['GET'])
def question2():
    return render_template('question_page.html',
                         question=request.args.get('question'),
                         kid_name=request.args.get('kid_name'),
                         phone_no=request.args.get('phone_no'),
                         encoded_text=quote(request.args.get('question')),
                         encoded_ques_no=quote(request.args.get('ques_no')),
                         current_question=int(request.args.get('ques_no')),
                         total_questions=total_questions + 5)  # Adding 5 follow-up questions

if __name__ == '__main__':
    app.run(debug=True)










