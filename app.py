import re

class CodePreprocess:
    def __init__(self):
        pass

    @staticmethod
    def remove_comment(code):
        return re.sub(r"(\/\/.+)|(#.+)|('.+)|(\/\*[^(\*\/)]+?\*\/)|(\"{3}[^(\"{3})]+?\"{3})", ' ', code)

    @staticmethod
    def remove_space(code):
        return re.sub("\s+", ' ', code.strip())

    def preprocess(self, code):
        code = self.remove_comment(code)
        code = self.remove_space(code)
        return code


from flask import Flask, request, render_template
import traceback
import fasttext as ft

app = Flask(__name__)
 
class CodeIdentify:
    def __init__(self, model_file='topic_detection_fasttext.bin'):
        self.model = ft.load_model(model_file)
        self.tp = CodePreprocess()
 
    def pred(self, txt):
        txt = self.tp.preprocess(txt)
        res = self.model.predict(txt)
        label = res[0][0]
        score = round(res[1][0], 2)
        language_name = label.upper()
        return language_name, score
 
 
ci = CodeIdentify()
 
 
@app.route('/')
def ping():
    return 'ok'
 
 
@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            code = request.form['code']
            if not code or len(code) <= 20:
                return render_template('index.html', error='Please type more than 20 characters!')
            language, score = ci.pred(code)
            return render_template('index.html', language=language, score=score, code=code)
        except:
            traceback.print_exc()
            return render_template('index.html', error='Unknown error has occurred, please try again!')
 
 
if __name__ == '__main__':
    app.run(debug=True)

