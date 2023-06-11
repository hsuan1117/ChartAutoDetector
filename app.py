import os
from tempfile import TemporaryDirectory

from flask import Flask, render_template, session, redirect, url_for, send_file
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
from datetime import datetime
import csv as csv
from worker import q

app = Flask(__name__)
app.secret_key = 'secret_key'


class DataForm(FlaskForm):
    file = FileField('file', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'Only Data Files!')
    ])
    about = StringField('about', validators=[
        DataRequired()
    ])
    submit = SubmitField("Submit")


def gen_id():
    import random, string
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


@app.route('/')
def home_landing():
    return render_template('home.html')


@app.route('/use', methods=['GET', 'POST'])
def upload_image():
    form = DataForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        temp_dir = TemporaryDirectory().name
        if not os.path.exists(os.path.join(temp_dir, 'files')):
            os.makedirs(os.path.join(temp_dir, 'files'))
        path = os.path.join(
            temp_dir, 'files', filename
        )
        f.save(path)
        data = {
            "id": gen_id(),
            "about": form.about.data,
            "path": path,
            "time": datetime.now()
        }
        if 'upload' in session:
            origin = session['upload']
            origin.append(data)
            session['upload'] = origin
        else:
            session['upload'] = [data]
        from function.generate import generate_all
        q.enqueue_call(
            func=generate_all, args=(data,), result_ttl=5000
        )
        return redirect(url_for('show', id=data['id']))
    return render_template('use.html', form=form)


@app.get('/my')
def my():
    if 'upload' in session:
        return render_template('my.html', files=session['upload'])
    else:
        return render_template('my.html', files=[])


@app.get('/show/<id>')
def show(id):
    if 'upload' in session:
        for data in session['upload']:
            if data['id'] == id:
                csv_data = csv.reader(open(data['path'], 'r'))
                return render_template('show.html', data=data, csv_data=list(csv_data), enumerate=enumerate)
    return redirect(url_for('my'))


@app.get('/download/<id>')
def download(id):
    if 'upload' in session:
        for data in session['upload']:
            if data['id'] == id:
                return send_file(data['path'], as_attachment=True)
    return redirect(url_for('my'))


@app.post('/delete/<id>')
def delete(id):
    if 'upload' in session:
        origin = session['upload']
        for data in session['upload']:
            if data['id'] == id:
                origin.remove(data)
                session['upload'] = origin
                return redirect(url_for('my'))
    return redirect(url_for('my'))


if __name__ == '__main__':
    app.run()
