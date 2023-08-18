from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, openai
from urllib.parse import quote, unquote
openai.api_key = ""

app = Flask(__name__)
app.secret_key = 'hello123'  # Set your secret key here

# MySQL configuration (replace with your actual credentials)
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''}

# Function to fetch questions from the MySQL database
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/question', methods=['GET'])
def question():
        kid_name = request.args.get('kid_name')
        phone_no = request.args.get('phone_no')
        ques_no = request.args.get('ques_no',1)
        def fetch_questions():
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT question_text FROM questions where id = %s", (ques_no,))
            questions = cursor.fetchall()
            cursor.close()
            conn.close()
            ques = questions[0]
            return ques
        fetch_questions()
        a=fetch_questions()
        b=str(a[0])
        encoded_text = quote(b)
        ques_no = str(ques_no)
        encoded_ques_no = quote(ques_no)
        print(ques_no)
        return render_template('question_page.html', question=a[0], kid_name=kid_name, phone_no=phone_no, encoded_text=encoded_text, encoded_ques_no = encoded_ques_no)

    # Route to display the question pages and process user's answers
total_questions = 10

@app.route('/question2', methods=['GET'])
def question2():
        kid_name = request.args.get('kid_name')
        phone_no = request.args.get('phone_no')
        question = request.args.get('question')
        ques_no = request.args.get('ques_no',11)
        ques_no = str(ques_no)
        encoded_ques_no = quote(ques_no)
        b=str(question)
        encoded_text = quote(b)
        return render_template('question_page.html', question=question, kid_name=kid_name, phone_no=phone_no, encoded_text=encoded_text, encoded_ques_no=encoded_ques_no)


@app.route('/store_in_sql', methods=['GET'])
def question_page():
        kid_name = request.args.get('kid_name')
        phone_no = request.args.get('phone_no')
        question_no = request.args.get('encoded_text')
        a=str(question_no)
        decoded_text = unquote(a)
        ans = request.args.get('answer')
        no = int(request.args.get('ques_no'))
        # Use the retrieved values in your MySQL Connector query
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Example query with kid_name and phone_no
        query = "INSERT INTO feedback_qna2 (kid_name, phone_no,ques,ans) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (kid_name, phone_no, decoded_text, ans))
        conn.commit()
        next_question_no = no + 1
        i = no + 1
        if next_question_no > total_questions:
            def generate_follow_up_questions(list):
                prompt = f"{list} I have a startup named Hoopstar Academy, this list contains question and answers asked to the parent of a kid who enrolled in our courses. Generate a follow-up question to ask them based on these responses:"
    
                response = openai.Completion.create(
                    engine="text-davinci-003",  # You can experiment with different engines
                    prompt=prompt,
                    max_tokens=50,  # You can adjust the token limit based on your requirements
                    temperature=0.7  # You can adjust the temperature for randomness
                )
                follow_up_questions = response.choices[0].text
                #.strip().split("\n")[0:]
                return follow_up_questions

            def fetch_questions():
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT ques, ans FROM feedback_qna2 where phone_no = %s",(phone_no,))
                questions = cursor.fetchall()
                cursor.close()
                conn.close()
                list = []
                for i in range():
                    pair=questions[i]
                    question = pair[0]
                    answer = pair[1]
                    save = question,answer
                    list.append(save)
                return list
            
            a = fetch_questions
            follow_up_questions = generate_follow_up_questions(a)
            if i in range(11,16):
                 questions = follow_up_questions.split('\n')
                 question = questions[2]
                 return redirect(url_for('question2', ques_no = i, question=question, kid_name=kid_name, phone_no=phone_no))
            return "Question process completed. Thank you!"
        return redirect(url_for('question', ques_no=next_question_no, kid_name=kid_name, phone_no=phone_no))

if __name__ == '__main__':
    app.run(debug=True)

       
        




        


