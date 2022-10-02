# project/server/main/views.py
import os

from celery.result import AsyncResult
from flask import render_template, Blueprint, jsonify, request, flash, redirect, send_from_directory, make_response, current_app as app

from project.server.tasks import check_size_file, reformat_file


main_blueprint = Blueprint("main", __name__,)
ALLOWED_EXTENSIONS = ['csv']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_blueprint.route('/files', methods=['POST'])
def upload_file():
    upload = os.path.join(app.config["UPLOAD_PATH"])
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        file_length = file.seek(0, os.SEEK_END)
        if check_size_file(file_length):
            file.stream.seek(0)
            file.save(os.path.join(upload, file.filename))
        else:
            resp = jsonify({'message': 'File too big'})
            resp.status_code = 412
            return resp

        file = reformat_file.delay(os.path.join(upload, file.filename), upload)
        return jsonify({"file_id": file.id}), 202


@main_blueprint.route("/files/<file_id>", methods=["GET"])
def get_file_by_id(file_id):
    task_result = AsyncResult(file_id)
    result = {
        "task_id": file_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }

    if task_result.status == "SUCCESS":
        uploads = os.path.join(app.root_path.rsplit('/', 2)[0], app.config["UPLOAD_PATH"])
        response = make_response(send_from_directory(uploads, task_result.result))

        return response
    return result

