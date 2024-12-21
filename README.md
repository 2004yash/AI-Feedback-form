# AI Feedback Form

An intelligent feedback collection system that uses OpenAI to generate dynamic follow-up questions based on user responses.

## Features

- Beautiful UI with Tailwind CSS
- Dynamic question generation
- Progress tracking
- Automated follow-up questions using AI
- Secure data storage

## Setup

1. Clone the repository:

```bash
git clone https://github.com/2004yash/AI-Feedback-form
cd AI-Feedback-form
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env.local` file in the root directory with the following variables:

```plaintext
FLASK_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
DB_HOST=your-database-host
DB_USER=your-database-username
DB_PASSWORD=your-database-password
DB_NAME=your-database-name
```

4. Set up the database:

```sql
CREATE TABLE questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question_text TEXT NOT NULL
);

CREATE TABLE feedback_qna2 (
    id INT PRIMARY KEY AUTO_INCREMENT,
    kid_name VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    ques TEXT NOT NULL,
    ans TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

5. Run the application:

```bash
python app.py
```

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for Flask sessions
- `OPENAI_API_KEY`: Your OpenAI API key
- `DB_HOST`: MySQL database host
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name

## Tech Stack

- Flask
- MySQL
- OpenAI API
- Tailwind CSS

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
