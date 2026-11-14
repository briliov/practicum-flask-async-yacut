"""Views for YaCut project."""

from flask import redirect, render_template, url_for

from . import app, db
from .forms import URLCreateForm, URlUploadFileForm
from .models import URLMap
from .utils.short_id import get_unique_short_id
from .utils.yandex_disk import upload_files_to_yandex_disk


@app.route('/<string:short>')
def redirect_view(short: str):
    """Redirects the user to the original link using the short ID."""
    return redirect(URLMap.get_original_link(short))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Displays the home page and handles the creation of short links."""
    short_link = None
    form: URLCreateForm = URLCreateForm()
    if form.validate_on_submit():
        original: str | None = form.original_link.data
        if not (short := form.custom_id.data):
            short = get_unique_short()
        try:
            URLMap.create(
                original=original,  # type: ignore
                short=short,
            )
        except ValueError as error:
            flash(f'Не удалось создать ссылку: {error}')
            return render_template('index.html', form=form)
        short_link = URLMap.get_short_link(short=short)
    return render_template(
        'index.html',
        form=form,
        short_link=short_link,
    )


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    """Displays the file upload page and handles the creation of short
    links to them."""
    form: URlUploadFileForm = URlUploadFileForm()
    uploaded_files: list = []
    if form.validate_on_submit():
        files_upload_data: list[
            dict[str, str]
        ] = await upload_files_to_yandex_disk(form.files.data)
        for file_data in files_upload_data:
            if 'file_url' in file_data.keys():
                file_name: str = file_data['file_name']
                file_url: str = file_data['file_url']
                short_id: str = get_unique_short_id()
                url_map: URLMap = URLMap(
                    original=file_url,  # type: ignore
                    short=short_id,  # type: ignore
                )
                uploaded_files.append(
                    {
                        'name': file_name,
                        'short_link': url_for(
                            'redirect_view',
                            short_id=short_id,
                            _external=True,
                        ),
                    },
                )
                db.session.add(url_map)
        db.session.commit()
    return render_template('upload.html', form=form, files=uploaded_files)
