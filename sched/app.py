from flask import Flask, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from sched.models import Base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'

# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/test')
def test():
    return 'This is a \'test\' page'

@app.route('/appointments/')
def appointment_list():
    return 'Listing of all appointments we have.'

@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    edit_url = url_for('appointment_list')
    return edit_url



if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
