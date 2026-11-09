# pyright: reportCallIssue=false

from flask import redirect, render_template, url_for

from . import app, db
from .forms import URLCreateForm, URlUploadFileForm
from .models import URLMap
from .utils.short_id import get_unique_short_id
from .utils.yandex_disk import upload_files_to_yandex_disk


@app.route('/<string:short_id>')
def redirect_view(short_id: str):
    url_map: URLMap = URLMap.query.filter_by(short=short_id).first_or_404()
    original: str = url_map.original
    return redirect(original)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    short_link = None
    form: URLCreateForm = URLCreateForm()
    if form.validate_on_submit():
        original_link: str | None = form.original_link.data
        if not (custom_id := form.custom_id.data):
            custom_id = get_unique_short_id()
        url_map: URLMap = URLMap(
            original=original_link,
            short=custom_id,
        )
        db.session.add(url_map)
        db.session.commit()
        short_link: str | None = url_for(
            'redirect_view',
            short_id=custom_id,
            _external=True,
        )
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/files')
def files_view():
    form: URlUploadFileForm = URlUploadFileForm()
    return render_template('upload.html', form=form)
