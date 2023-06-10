import os
from tempfile import TemporaryDirectory

from flask import Flask, render_template, session, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'


class DataForm(FlaskForm):
    file = FileField('file', validators=[
        FileRequired(),
        FileAllowed(['csv', 'xls', 'xlsx'], '僅限上傳資料檔!')
    ])
    about = StringField('about', validators=[
        DataRequired()
    ])
    submit = SubmitField("送出")


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
        print(f)
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
            session['upload'].append(data)
        else:
            session['upload'] = [data]
        return redirect(url_for('my'))
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
                return render_template('show.html', data=data)
    return redirect(url_for('my'))


if __name__ == '__main__':
    app.run()
