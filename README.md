# 🤖 AI-Based Plagiarism Checker with Paraphrase Detection

The AI-Based Plagiarism Checker is a web-based application developed to detect both exact and paraphrased plagiarism using Natural Language Processing and machine learning techniques.

The system combines **TF-IDF** for lexical similarity and **SBERT (Sentence-BERT)** for semantic similarity to identify text that may be copied or paraphrased.

## ✨ Features

- Detects exact plagiarism
- Detects paraphrased content
- Uses TF-IDF for lexical similarity
- Uses SBERT for semantic similarity
- Calculates similarity using cosine similarity
- Displays plagiarism percentage
- Supports document and text analysis
- Django-based web application
- User-friendly web interface

## 🛠️ Technologies Used

### Programming Language
- Python

### Backend
- Django

### Machine Learning & NLP
- Scikit-learn
- Sentence Transformers (SBERT)
- TF-IDF
- Cosine Similarity

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- SQLite

## 🏗️ Project Architecture

User
↓
Django Web Interface
↓
Text / Document Upload
↓
Text Preprocessing
↓
TF-IDF + SBERT Analysis
↓
Cosine Similarity
↓
Plagiarism Detection
↓
Plagiarism Percentage / Result

## 📁 Project Structure

Plagiarism-checker-/
│
├── plagiarism/
│   └── Django project configuration
│
├── plagiarism_checking/
│   └── Plagiarism detection application
│
├── static/
│   └── CSS, JavaScript and static assets
│
├── templates/
│   └── HTML templates
│
├── db.sqlite3
│   └── SQLite database
│
├── manage.py
│   └── Django project management script
│
├── requirements.txt
│   └── Python project dependencies
│
└── README.md

## ⚙️ How to Run the Project

### 1. Clone the repository

git clone https://github.com/farjana-sk/Plagiarism-checker-.git

### 2. Open the project

cd Plagiarism-checker-

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the Django server

python manage.py runserver

### 5. Open in browser

http://127.0.0.1:8000/

## 🔄 Application Workflow

1. User opens the plagiarism checker application.
2. User enters text or uploads a document.
3. The system extracts and preprocesses the text.
4. TF-IDF is used to measure lexical similarity.
5. SBERT is used to identify semantic similarity.
6. Cosine similarity is calculated.
7. The system analyzes the similarity results.
8. The plagiarism percentage and result are displayed.

## 🧠 Plagiarism Detection Approach

### TF-IDF

TF-IDF is used to measure lexical similarity by analyzing the importance of words within the given text.

### SBERT

Sentence-BERT is used to understand the semantic meaning of sentences and identify paraphrased content even when different words are used.

### Cosine Similarity

Cosine similarity is used to compare the text representations and determine how similar the content is.

## 🗄️ Database

The application uses **SQLite** for storing application data.

Django provides database management through its built-in ORM, allowing the application to work with stored data efficiently.

## 🎯 Project Objectives

- Develop an AI-based plagiarism detection system.
- Detect both exact and paraphrased plagiarism.
- Apply Natural Language Processing techniques to text comparison.
- Combine lexical and semantic similarity approaches.
- Calculate and display plagiarism percentage.
- Develop a practical Django-based web application.

## 📸 Screenshots

Screenshots of the AI-Based Plagiarism Checker can be added to the repository to demonstrate the application interface and plagiarism detection results.

## 🚀 Future Enhancements

- Multi-document plagiarism comparison
- Improved paraphrase detection
- PDF and DOCX document support
- Larger reference document database
- Advanced NLP models
- Real-time plagiarism checking
- Detailed plagiarism reports
- Downloadable plagiarism reports
- User authentication
- Cloud deployment

## 👩‍💻 Developer

SK Farjana

B.Tech - Computer Science and Engineering
Specialization: Artificial Intelligence & Machine Learning

## 📄 License

This project is developed for educational and portfolio purposes.
