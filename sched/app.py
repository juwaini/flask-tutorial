from flask import abort, jsonify, redirect 
from flask import Flask, request, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy

from sched.forms import AppointmentForm
from sched.models import Base, Appointment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'

# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base

def dump_request_detail(request):
    request_detail = """
    # Before Request #
    request.endpoint: {request.endpoint}
    request.method: {request.method}
    request.view_args: {request.view_args}
    request.args: {request.args}
    request.form: {request.form}
    request.user_agent: {request.user_agent}
    request.files: {request.files}
    request.is_xhr: {request.is_xhr}

    ## request.headers  ##
    {request.headers}
    """.format(request=request).strip()
    return request_detail

@app.before_request
def callme_before_every_request():
    # Demo only: the before_request hook.
    app.logger.debug(dump_request_detail(request))

@app.after_request
def callme_after_every_response(response):
    # Demo only: the after_request hook.
    app.logger.debug('# After Request #\n' + repr(response))
    return response

@app.route('/')
def hello():
    return render_template('appointment/index.html')

@app.route('/test')
def test():
    return 'This is a \'test\' page'

@app.route('/appointments/')
def appointment_list():
    """Provide HTML listing of all appointments."""
    #Query: Get all Appointment objects, sorted by date
    appts = (db.session.query(Appointment).order_by(Appointment.start.asc()).all())
    return render_template('appointment/index.html', appts=appts)

@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    """Provide HTML page with a given appointment. """
    #Query: get Appointment object by ID.
    appt = db.session.query(Appointment).get(appointment_id)
    
    if appt is None:
        #Abort with Not Found
        abort(404)
    return render_template('appointment/detail.html', appt=appt)

@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    """Provide HTML form to edit a given appoinment"""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        #Success. Send the user back to detail view
        return redirect(url_for('appointment_detail'), appointment_id=appt.id)
    return render_template('appointment/edit.html', form=form)

@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    """Provide HTML form to create a new appointment"""
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Appointment()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        #Success. Send user back to full appointment list
        return redirect(url_for('appointment_list'))
    #Either first load or validation error
    return render_template('appointment/edit.html', form=form)

@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
def appointment_delete():
    raise NotImplementedError('DELETE')

@app.errorhandler(404)
def error_not_found(error):
    return render_template('error/not_found.html'), 404
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
