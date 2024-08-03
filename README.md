# Feedback Form Web Application

Welcome to the Feedback Form web application repository! This project leverages HTML, CSS, Python (Flask), the OpenAI API, and MySQL to create an interactive and dynamic feedback system.

## Features

- **User-Friendly Interface**: Developed using HTML and CSS to provide an intuitive and accessible user interface.
- **Efficient Data Processing**: Implemented with Python and the Flask framework for efficient backend processing and data handling.
- **Dynamic Question Generation**: Integrated the OpenAI API to generate contextually relevant questions based on user-provided answers.
- **Database Integration**: Established a connection with MySQL to fetch questions and store user-generated questions along with their answers.

## Technologies Used

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask)
- **API**: OpenAI API
- **Database**: MySQL

## Getting Started

To get a local copy up and running, follow these simple steps:

### Prerequisites

- Python 3.x
- MySQL
- OpenAI API key

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/feedback-form-web-app.git
   ```
2. Navigate to the project directory:
   ```sh
   cd feedback-form-web-app
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the MySQL database:
   - Create a new database and note its name.
   - Update the database configuration in the `config.py` file with your database credentials.
   - Initialize the database schema:
     ```sh
     python init_db.py
     ```
5. Set your OpenAI API key in the `config.py` file.

### Running the Application

1. Start the Flask server:
   ```sh
   flask run
   ```
2. Open your web browser and navigate to `http://127.0.0.1:8000`.

## Usage

- **Providing Feedback**: Fill out the feedback form on the home page. The OpenAI API will generate contextually relevant questions based on your answers.
- **Viewing Responses**: Responses are stored in the MySQL database and can be retrieved as needed.

## Contributing

Contributions are welcome! Here's how you can contribute:
- Fork the repository
- Create a new branch (`git checkout -b feature`)
- Make changes and commit (`git commit -am 'Add new feature'`)
- Push to the branch (`git push origin feature`)
- Create a pull request


