from flask import abort, redirect, render_template, request

from . import app
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
        except URLMap.ObjectCreateError as exc:
            form.custom_id.errors.append(str(exc))
            return render_template(
                'index.html',
                form=form)
        return render_template(
            'index.html',
            form=form,
            short_link=request.host_url + url_map.short)
    return render_template(
        'index.html',
        form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = LoadForm()
    if not form.validate_on_submit():
        return render_template('upload.html', form=form)
    return render_template(
        'upload.html',
        form=form,
        short_urls_and_filenames=[
            dict(short_url=URLMap.create(file_info['url']).
                 get_unique_short_id(),
                 filename=file_info['filename']
                 ) for file_info in await async_upload_files_to_yandexdisk(
                     form.files.data)])


@app.route('/<string:short>', methods=['GET'])
def short_view(short):
    """Функция переадресации с короткой ссылки."""
    url_map = URLMap.get(short)
    if not url_map:
        abort(404)
    return redirect(url_map.original)
