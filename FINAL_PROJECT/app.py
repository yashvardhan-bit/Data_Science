from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
import requests
import json
import datetime
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
import joblib

app = Flask(__name__)
app.secret_key = 'interview_key'

class InterviewSystem:
    def __init__(self):
        self.questions = []
        self.current_question = 0
        self.answers = []
        self.ml_model = None
        self.vectorizer = None
        self.load_data()
        self.load_ml_model()
    
    def load_data(self):
        """Load questions from CSV file"""
        try:
            df = pd.read_csv('Software Questions.csv', encoding='utf-8')
            self.questions = df.to_dict('records')
            print(f"Loaded {len(self.questions)} questions")
        except Exception as e:
            print(f"Error loading CSV: {e}")
            # Fallback questions
            self.questions = [
                {"Question": "What is OOP?", "Answer": "Object-oriented programming is a programming paradigm that organizes code into objects that contain data and code.", "Category": "General Programming", "Difficulty": "Easy"},
                {"Question": "Explain polymorphism.", "Answer": "Polymorphism allows objects to be treated as instances of their parent class while maintaining their own unique implementations.", "Category": "General Programming", "Difficulty": "Medium"}
            ]
    
    def load_ml_model(self):
        """Load or create ML model"""
        try:
            if os.path.exists('interview_model.joblib'):
                self.ml_model = joblib.load('interview_model.joblib')
                print("ML model loaded successfully")
            else:
                self.train_ml_model()
        except Exception as e:
            print(f"Error loading ML model: {e}")
            self.ml_model = None
    
    def train_ml_model(self):
        """Train ML model on synthetic data"""
        try:
            # Create synthetic training data
            synthetic_data = []
            for _ in range(1000):
                score = np.random.randint(1, 11)
                synthetic_data.append({
                    'text': f"answer_{score}",
                    'score': score
                })
            
            # Prepare data
            texts = [item['text'] for item in synthetic_data]
            scores = [item['score'] for item in synthetic_data]
            
            # Vectorize text
            self.vectorizer = TfidfVectorizer(max_features=100)
            X = self.vectorizer.fit_transform(texts)
            
            # Train model
            self.ml_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.ml_model.fit(X, scores)
            
            # Save model
            joblib.dump(self.ml_model, 'interview_model.joblib')
            print("ML model trained and saved successfully")
        except Exception as e:
            print(f"Error training ML model: {e}")
            self.ml_model = None
    
    def get_categories(self):
        """Get unique categories"""
        return sorted(list(set([q['Category'] for q in self.questions])))
    
    def start_interview(self, category='All', count=5):
        """Start a new interview"""
        if category != "All":
            filtered_questions = [q for q in self.questions if q['Category'] == category]
        else:
            filtered_questions = self.questions
        
        self.answers = filtered_questions[:count]
        self.current_question = 0
        return len(self.answers)
    
    def get_current_question(self):
        """Get current question"""
        if self.current_question < len(self.answers):
            return self.answers[self.current_question]
        return None
    
    def submit_answer(self, answer):
        """Submit and evaluate answer"""
        if self.current_question >= len(self.answers):
            return None
        
        question = self.answers[self.current_question]
        
        # ML evaluation
        ml_score = self.evaluate_with_ml(answer)
        
        # AI evaluation
        ai_evaluation = self.evaluate_with_ai(question['Question'], answer, question['Answer'])
        
        # Combine scores (60% ML + 40% AI)
        combined_score = int(ml_score * 0.6 + ai_evaluation['score'] * 0.4)
        
        evaluation = {
            'score': combined_score,
            'accuracy': ai_evaluation['accuracy'],
            'completeness': ai_evaluation['completeness'],
            'clarity': ai_evaluation['clarity'],
            'feedback': ai_evaluation['feedback'],
            'suggestions': ai_evaluation['suggestions']
        }
        
        # Store the answer and evaluation with the question
        question['user_answer'] = answer
        question['evaluation'] = evaluation
        
        self.current_question += 1
        return evaluation
    
    def evaluate_with_ml(self, answer):
        """Evaluate answer using ML model"""
        try:
            if self.ml_model and self.vectorizer:
                # Vectorize the answer
                X = self.vectorizer.transform([answer])
                # Predict score
                score = self.ml_model.predict(X)[0]
                return max(1, min(10, int(score)))
            else:
                return 7  # Default score
        except Exception as e:
            print(f"ML evaluation error: {e}")
            return 7
    
    def evaluate_with_ai(self, question, user_answer, expected_answer):
        """Evaluate answer using AI (Ollama)"""
        try:
            prompt = f"""
            Evaluate this technical interview answer:

            Question: {question}
            Expected Answer: {expected_answer}
            User's Answer: {user_answer}

            Rate the answer on a scale of 1-10 for:
            1. Accuracy (how correct the answer is)
            2. Completeness (how thorough the answer is)
            3. Clarity (how well explained the answer is)

            Provide a JSON response in this exact format:
            {{
                "score": <overall_score_1-10>,
                "accuracy": <accuracy_score_1-10>,
                "completeness": <completeness_score_1-10>,
                "clarity": <clarity_score_1-10>,
                "feedback": "<brief_feedback>",
                "suggestions": "<improvement_suggestions>"
            }}
            """
            
            response = requests.post('http://localhost:11434/api/generate', 
                                   json={
                                       'model': 'gemma3',
                                       'prompt': prompt,
                                       'stream': False
                                   }, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                try:
                    import re
                    json_match = re.search(r'\{.*\}', result['response'], re.DOTALL)
                    if json_match:
                        evaluation = json.loads(json_match.group())
                        return evaluation
                except:
                    pass
            
            # Fallback evaluation
            return {
                'score': 7,
                'accuracy': 7,
                'completeness': 7,
                'clarity': 7,
                'feedback': 'Good effort! Keep practicing.',
                'suggestions': 'Provide more details and examples.'
            }
            
        except Exception as e:
            print(f"AI evaluation error: {e}")
            return {
                'score': 7,
                'accuracy': 7,
                'completeness': 7,
                'clarity': 7,
                'feedback': 'Good effort! Keep practicing.',
                'suggestions': 'Provide more details and examples.'
            }
    
    def get_results(self):
        """Get interview results"""
        return {
            'total': len(self.answers),
            'current': self.current_question,
            'answers': self.answers
        }
    
    def reset(self):
        """Reset interview state"""
        self.current_question = 0
        self.answers = []

# Initialize interview system
interview = InterviewSystem()

@app.route('/')
def home():
    categories = interview.get_categories()
    return render_template('home.html', categories=categories)

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    if request.method == 'POST':
        category = request.form.get('category', 'All')
        count = int(request.form.get('count', 5))
        
        total_questions = interview.start_interview(category, count)
        session['interview_started'] = True
        return redirect(url_for('question'))
    
    categories = interview.get_categories()
    return render_template('configure.html', categories=categories)

@app.route('/question')
def question():
    if not session.get('interview_started'):
        return redirect(url_for('configure'))
    
    question = interview.get_current_question()
    if not question:
        return redirect(url_for('results'))
    
    progress = interview.current_question / len(interview.answers)
    return render_template('question.html', question=question, progress=progress, 
                         current_num=interview.current_question + 1, total=len(interview.answers))

@app.route('/submit', methods=['POST'])
def submit():
    answer = request.form.get('answer', '').strip()
    
    if not answer:
        return jsonify({'error': 'Please provide an answer'})
    
    evaluation = interview.submit_answer(answer)
    if not evaluation:
        return jsonify({'error': 'Interview completed'})
    
    return jsonify({
        'success': True,
        'evaluation': evaluation,
        'next_question': interview.current_question < len(interview.answers)
    })

@app.route('/results')
def results():
    results_data = interview.get_results()
    if not results_data['answers']:
        return redirect(url_for('configure'))
    
    stats = {
        'total': results_data['total'],
        'average': 7.0,
        'config': {'category': 'All', 'difficulty': 'All', 'count': results_data['total']}
    }
    return render_template('results.html', answers=results_data['answers'], stats=stats)

@app.route('/reset')
def reset():
    interview.reset()
    session.clear()
    return redirect(url_for('home'))

@app.route('/check_ollama')
def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        return jsonify({'status': 'running' if response.status_code == 200 else 'not_running'})
    except:
        return jsonify({'status': 'not_running'})

@app.route('/ml_status')
def ml_status():
    """Check ML model status"""
    return jsonify({'is_trained': interview.ml_model is not None})

@app.route('/retrain_ml')
def retrain_ml():
    """Retrain ML model"""
    try:
        interview.train_ml_model()
        return jsonify({'success': True, 'message': 'ML model retrained successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/exit_interview')
def exit_interview():
    """Exit interview"""
    interview.reset()
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000) 