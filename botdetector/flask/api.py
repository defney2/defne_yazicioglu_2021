from flask import Flask, request, render_template,jsonify
from train import detector
app = Flask(__name__)

def do_something(text1):
   text1 = text1.upper()
#   text2 = text2.upper()
   combine = text1 
   combine = detector(combine)
   return combine

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    text1 = request.form['text1']
    word = request.args.get('text1')
    #text2 = request.form['text2']
    #combine = do_something(text1)
    combine = detector(text1)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)
#    return jsonify(result=combine)

if __name__ == '__main__':
    app.run(debug=True)
