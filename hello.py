from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/test')
def test():
    return 'This is a \'test\' page'

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
