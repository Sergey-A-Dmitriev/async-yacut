from flask import abort, redirect, render_template

from . import app
from .exceptions import ObjectCreateError
from .forms import LoadForm, MainForm
from .models import URLMap
from .yandexdisk import async_upload_files_to_yandexdisk


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        try:
            url_map = URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data or None)
        except ObjectCreateError as exc:
            form.custom_id.errors.append(str(exc))
            return render_template(
                'index.html',
                form=form)
        return render_template(
            'index.html',
            form=form,
            short_link=url_map.get_short_url())
    return render_template(
        'index.html',
        form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = LoadForm()

    if not form.validate_on_submit():
        return render_template('upload.html', form=form)

    uploaded_files = await async_upload_files_to_yandexdisk(
        form.files.data)
    short_urls_and_filenames = []
    for file_info in uploaded_files:
        url_map = URLMap.create(file_info['url'])

        short_urls_and_filenames.append(
            {
                'filename': file_info['filename'],
                'short_link': url_map.get_short_url(),
            })
    return render_template(
        'upload.html',
        form=form,
        short_urls_and_filenames=short_urls_and_filenames)


@app.route('/<string:short>', methods=['GET'])
def short_view(short):
    """Функция переадресации с короткой ссылки."""
    url_map = URLMap.get(short)
    if not url_map:
        abort(404)
    return redirect(url_map.original)
