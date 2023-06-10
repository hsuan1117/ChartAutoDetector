import os
from tempfile import TemporaryDirectory

from flask import Flask, render_template, session, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField

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
        f.save(os.path.join(
            app.instance_path, 'files', filename
        ))
        return redirect(url_for('success'))
    return render_template('use.html', form=form)


if __name__ == '__main__':
    app.run()
