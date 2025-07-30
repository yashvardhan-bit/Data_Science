# Technical AI Interview System

A Flask-based technical interview system that uses Ollama with Gemma 3 to evaluate candidate responses.

## Features

- **Field Selection**: Choose from multiple technical categories (Programming, Web Development, Database, Security, DevOps, etc.)
- **Difficulty Levels**: Easy, Medium, Hard, or All difficulties
- **AI Evaluation**: Gemma 3 provides detailed scoring on Accuracy, Completeness, and Clarity
- **Progress Tracking**: Real-time progress through questions
- **Comprehensive Results**: Detailed analysis with category breakdown

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Ollama**:
   ```bash
   ollama run gemma3
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Open Browser**: Go to `http://localhost:5000`

## How to Use

1. **Configure Interview**: Choose category, difficulty, and question count
2. **Answer Questions**: Provide detailed responses
3. **Get AI Feedback**: Receive scores and improvement suggestions
4. **View Results**: See comprehensive performance analysis

## Files

- `app.py` - Main Flask application
- `Software Questions.csv` - Question database
- `templates/` - HTML templates
- `requirements.txt` - Python dependencies 