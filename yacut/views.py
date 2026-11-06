from flask import render_template

from . import app
from .forms import URLCreateForm, URlUploadFileForm


@app.route('/')
def index_view():
    form: URLCreateForm = URLCreateForm()
    return render_template('index.html', form=form)


@app.route('/files')
def files_view():
    form: URlUploadFileForm = URlUploadFileForm()
    return render_template('upload.html', form=form)
