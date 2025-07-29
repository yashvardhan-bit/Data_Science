from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pandas as pd
import requests
import json
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

app = Flask(__name__)
app.secret_key = 'interview_key'

class InterviewSystem:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.questions_df = None
        self.interview_questions = []
        self.current_question = 0
        self.answers = []
        self.vectorizer = None
        self.models = {}
        self.load_data()
    
    def load_data(self):
        """Load questions and train/load ML model"""
        try:
            self.questions_df = pd.read_csv('Software Questions.csv', encoding='latin-1')
            print(f"Loaded {len(self.questions_df)} questions")
            
            # Load or train ML model
            if not self.load_ml_model():
                self.train_ml_model()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.questions_df = pd.DataFrame([
                {"Question": "What is OOP?", "Answer": "Object-oriented programming...", "Category": "General Programming", "Difficulty": "Easy"},
                {"Question": "Explain polymorphism.", "Answer": "Polymorphism allows...", "Category": "General Programming", "Difficulty": "Medium"}
            ])
            self.train_ml_model()
    
    def train_ml_model(self):
        """Train ML model on synthetic data"""
        try:
            # Generate synthetic training data
            training_data = []
            for _, row in self.questions_df.iterrows():
                q, a = row['Question'], row['Answer']
                # Create 5 quality levels per question
                answers = [
                    (f"{a} Comprehensive explanation with examples.", {'accuracy': 9, 'completeness': 9, 'clarity': 9, 'score': 9}),
                    (f"{a} Good explanation with details.", {'accuracy': 8, 'completeness': 7, 'clarity': 7, 'score': 7.3}),
                    (f"{a[:len(a)//2]} Basic understanding.", {'accuracy': 6, 'completeness': 5, 'clarity': 5, 'score': 5.3}),
                    (f"I think it's about {a.split()[0]}.", {'accuracy': 4, 'completeness': 3, 'clarity': 3, 'score': 3.3}),
                    ("I'm not sure.", {'accuracy': 2, 'completeness': 1, 'clarity': 1, 'score': 1.3})
                ]
                for answer, scores in answers:
                    training_data.append({'text': f"{q} {answer} {a}", **scores})
            
            df = pd.DataFrame(training_data)
            self.vectorizer = TfidfVectorizer(max_features=500)
            X = self.vectorizer.fit_transform(df['text'])
            
            # Train models for each score component
            for col in ['accuracy', 'completeness', 'clarity', 'score']:
                model = RandomForestRegressor(n_estimators=50, random_state=42)
                model.fit(X, df[col])
                self.models[col] = model
            
            # Save model
            joblib.dump({'vectorizer': self.vectorizer, 'models': self.models}, 'interview_model.joblib')
            print("ML model trained successfully")
            
        except Exception as e:
            print(f"Error training ML model: {e}")
    
    def load_ml_model(self):
        """Load existing ML model"""
        try:
            if os.path.exists('interview_model.joblib'):
                data = joblib.load('interview_model.joblib')
                self.vectorizer = data['vectorizer']
                self.models = data['models']
                print("ML model loaded successfully")
                return True
        except Exception as e:
            print(f"Error loading ML model: {e}")
        return False
    
    def predict_score(self, question, answer, expected):
        """Predict score using ML"""
        try:
            text = f"{question} {answer} {expected}"
            X = self.vectorizer.transform([text])
            scores = {}
            for component, model in self.models.items():
                pred = model.predict(X)[0]
                scores[component] = max(1, min(10, pred))
            return scores
        except Exception as e:
            print(f"ML prediction error: {e}")
            return None
    
    def get_ai_evaluation(self, question, answer, expected):
        """Get AI evaluation using Ollama"""
        try:
            prompt = f"""Evaluate this answer realistically:
            Q: {question}
            Expected: {expected}
            Answer: {answer}
            
            Score 1-10 for: accuracy, completeness, clarity. Calculate weighted overall score.
            Return JSON: {{"accuracy": score, "completeness": score, "clarity": score, "score": overall, "feedback": "text", "suggestions": "text"}}"""
            
            response = requests.post(self.ollama_url, json={
                "model": "gemma3",
                "prompt": prompt,
                "stream": False
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()['response']
                try:
                    json_start = result.find('{')
                    json_end = result.rfind('}') + 1
                    if json_start != -1:
                        return json.loads(result[json_start:json_end])
                except:
                    pass
        except Exception as e:
            print(f"AI evaluation error: {e}")
        return None
    
    def evaluate_answer(self, question, answer, expected):
        """Hybrid ML+AI evaluation"""
        ml_scores = self.predict_score(question, answer, expected)
        ai_scores = self.get_ai_evaluation(question, answer, expected)
        
        if ml_scores and ai_scores:
            # Combine ML (60%) and AI (40%)
            final = {}
            for key in ['accuracy', 'completeness', 'clarity']:
                final[key] = round((ml_scores.get(key, 5) * 0.6) + (ai_scores.get(key, 5) * 0.4), 1)
            final['score'] = round((final['accuracy'] * 0.4) + (final['completeness'] * 0.35) + (final['clarity'] * 0.25), 1)
            final['feedback'] = f"ML-AI Hybrid: {ai_scores.get('feedback', 'Good effort!')}"
            final['suggestions'] = ai_scores.get('suggestions', 'Provide more details and examples.')
            return final
        elif ml_scores:
            return {**ml_scores, 'feedback': 'ML-based evaluation', 'suggestions': 'Add more details and examples.'}
        elif ai_scores:
            return ai_scores
        else:
            return {'score': 6, 'accuracy': 6, 'completeness': 6, 'clarity': 6, 'feedback': 'Good effort!', 'suggestions': 'Provide more details.'}
    
    def get_categories(self):
        """Get available categories"""
        if self.questions_df is not None:
            return sorted(self.questions_df['Category'].unique())
        return ["General Programming"]
    
    def get_questions(self, category="All", count=10):
        """Get questions from CSV, generate AI questions if needed"""
        if self.questions_df is None:
            return []
        
        df = self.questions_df.copy()
        
        # Apply category filter
        if category != "All":
            df = df[df['Category'] == category]
        
        questions = []
        
        # Get questions from CSV
        if len(df) > 0:
            csv_questions = df.sample(n=min(count, len(df))).to_dict('records')
            questions.extend(csv_questions)
        
        # Generate AI questions if needed
        remaining_count = count - len(questions)
        if remaining_count > 0:
            ai_questions = self.generate_ai_questions(category, remaining_count)
            questions.extend(ai_questions)
        
        return questions
    
    def generate_ai_questions(self, category, count):
        """Generate AI questions for the specified category"""
        try:
            prompt = f"""Generate {count} technical interview questions for the category: {category}
            
            For each question, provide:
            1. A clear, specific technical question
            2. A comprehensive answer that demonstrates expertise
            3. Appropriate difficulty level (Easy/Medium/Hard)
            
            Format as JSON array:
            [
                {{
                    "Question": "question text",
                    "Answer": "detailed answer",
                    "Category": "{category}",
                    "Difficulty": "Easy/Medium/Hard"
                }}
            ]
            
            Make questions relevant to {category} and vary the difficulty levels."""
            
            response = requests.post(self.ollama_url, json={
                "model": "gemma3",
                "prompt": prompt,
                "stream": False
            }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()['response']
                try:
                    # Extract JSON from response
                    json_start = result.find('[')
                    json_end = result.rfind(']') + 1
                    if json_start != -1:
                        questions = json.loads(result[json_start:json_end])
                        return questions
                except:
                    pass
            
            # Fallback: Generate simple questions
            return self._generate_fallback_questions(category, count)
            
        except Exception as e:
            print(f"Error generating AI questions: {e}")
            return self._generate_fallback_questions(category, count)
    
    def _generate_fallback_questions(self, category, count):
        """Generate fallback questions if AI fails"""
        fallback_questions = []
        
        # Template questions based on category
        templates = {
            "General Programming": [
                ("What are the key principles of object-oriented programming?", "OOP principles include encapsulation, inheritance, polymorphism, and abstraction. Encapsulation bundles data and methods, inheritance allows code reuse, polymorphism enables flexible design, and abstraction simplifies complex systems."),
                ("Explain the difference between stack and heap memory.", "Stack memory stores local variables and function calls with automatic management. Heap memory is for dynamic allocation with manual management. Stack is faster but limited in size, while heap is larger but slower."),
                ("What is the purpose of a constructor in programming?", "A constructor initializes object properties when a class is instantiated, ensuring the object starts in a valid state. It can accept parameters to set initial values and is called automatically when creating new objects.")
            ],
            "Data Structures": [
                ("What is the difference between an array and a linked list?", "Arrays store elements in contiguous memory with fixed size and O(1) access. Linked lists use nodes with pointers, allowing dynamic size and O(n) access but efficient insertions/deletions."),
                ("Explain how a binary search tree works.", "A BST is a hierarchical data structure where each node has at most two children. Left subtree contains smaller values, right subtree contains larger values, enabling efficient search, insertion, and deletion operations."),
                ("What is the time complexity of binary search?", "Binary search has O(log n) time complexity. It repeatedly divides the search interval in half, making it very efficient for searching in sorted arrays.")
            ],
            "Database and SQL": [
                ("What is normalization in database design?", "Normalization organizes data to reduce redundancy and improve integrity. It follows normal forms (1NF, 2NF, 3NF) to eliminate data anomalies and ensure data consistency."),
                ("Explain the difference between INNER JOIN and LEFT JOIN.", "INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table and matching rows from the right table, with NULLs for non-matches."),
                ("What are ACID properties in database transactions?", "ACID ensures reliable transactions: Atomicity (all-or-nothing), Consistency (valid state transitions), Isolation (independent transactions), and Durability (persisted changes).")
            ]
        }
        
        # Get templates for the category or use general ones
        category_templates = templates.get(category, templates["General Programming"])
        
        for i in range(min(count, len(category_templates))):
            question, answer = category_templates[i]
            fallback_questions.append({
                "Question": question,
                "Answer": answer,
                "Category": category,
                "Difficulty": "Medium"
            })
        
        return fallback_questions
    
    def get_available_combinations(self):
        """Get available category-difficulty combinations"""
        if self.questions_df is None:
            return {}
        
        combinations = {}
        for category in self.questions_df['Category'].unique():
            cat_df = self.questions_df[self.questions_df['Category'] == category]
            difficulties = cat_df['Difficulty'].unique()
            combinations[category] = list(difficulties)
        
        return combinations
    
    def start_interview(self, category="All", count=10):
        """Start interview with simplified configuration"""
        self.interview_questions = self.get_questions(category, count)
        self.current_question = 0
        self.answers = []
        
        if len(self.interview_questions) == 0:
            return False
        
        return True
    
    def get_current_question(self):
        """Get current question"""
        if self.current_question < len(self.interview_questions):
            return self.interview_questions[self.current_question]
        return None
    
    def submit_answer(self, answer):
        """Submit and evaluate answer"""
        if self.current_question < len(self.interview_questions):
            question = self.interview_questions[self.current_question]
            evaluation = self.evaluate_answer(question['Question'], answer, question['Answer'])
            
            self.answers.append({
                'question': question['Question'],
                'answer': answer,
                'expected': question['Answer'],
                'category': question['Category'],
                'difficulty': question['Difficulty'],
                'evaluation': evaluation,
                'timestamp': datetime.now().isoformat()
            })
            
            self.current_question += 1
            return evaluation
        return None
    
    def get_stats(self):
        """Get interview statistics"""
        if not self.answers:
            return {}
        
        scores = [ans['evaluation'].get('score', 0) for ans in self.answers]
        return {
            'total': len(self.answers),
            'average': sum(scores) / len(scores),
            'config': {'category': 'All', 'difficulty': 'All', 'count': len(self.answers)}
        }

# Initialize system
interview = InterviewSystem()

@app.route('/')
def home():
    return render_template('home.html', categories=interview.get_categories())

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    if request.method == 'POST':
        category = request.form.get('category', 'All')
        count = int(request.form.get('count', 10))
        
        # Handle empty values
        if not category or category.strip() == '':
            category = 'All'
        
        if interview.start_interview(category, count):
            session['interview_started'] = True
            return redirect(url_for('question'))
        else:
            error_msg = f"Unable to start interview for Category: '{category}'. Please try a different category."
            return render_template('configure.html', error=error_msg, categories=interview.get_categories())
    
    return render_template('configure.html', categories=interview.get_categories())

@app.route('/question')
def question():
    if not session.get('interview_started'):
        return redirect(url_for('configure'))
    
    current = interview.get_current_question()
    if not current:
        return redirect(url_for('results'))
    
    progress = interview.current_question / len(interview.interview_questions)
    return render_template('question.html', question=current, progress=progress, 
                         current_num=interview.current_question + 1, total=len(interview.interview_questions))

@app.route('/submit', methods=['POST'])
def submit():
    answer = request.form.get('answer', '').strip()
    if not answer:
        return jsonify({'error': 'Please provide an answer'})
    
    evaluation = interview.submit_answer(answer)
    if evaluation:
        return jsonify({
            'success': True,
            'evaluation': evaluation,
            'next_question': interview.get_current_question() is not None
        })
    else:
        return jsonify({'error': 'Failed to evaluate answer'})

@app.route('/results')
def results():
    if not interview.answers:
        return redirect(url_for('configure'))
    
    stats = interview.get_stats()
    return render_template('results.html', answers=interview.answers, stats=stats)

@app.route('/check_ollama')
def check_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return jsonify({'status': 'running' if response.status_code == 200 else 'error'})
    except:
        return jsonify({'status': 'error'})

@app.route('/ml_status')
def ml_status():
    return jsonify({'is_trained': len(interview.models) > 0})

@app.route('/retrain_ml')
def retrain_ml():
    interview.train_ml_model()
    return jsonify({'status': 'success'})

@app.route('/exit_interview')
def exit_interview():
    """Exit interview and return to homepage"""
    session.clear()
    interview.current_question = 0
    interview.answers = []
    interview.interview_questions = []
    return redirect(url_for('home'))

@app.route('/reset')
def reset():
    session.clear()
    interview.current_question = 0
    interview.answers = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000) 