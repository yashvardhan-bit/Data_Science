from flask import Flask,render_template,request,url_for
app = Flask(__name__)

@app.route('/hello')
def home():
    return 'learning is fun'

if __name__=="__main__":
    app.run(debug=True)

