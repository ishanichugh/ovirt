#!/usr/bin/python
"""
This script is a Flask app with implementation of prototype of tool
"""
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from parser import Parser
from binary_search import Searcher
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['log'])

def allowed_file(filename):
    """
    Checks for consistency of file type
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route("/")
def hello():
    """
    Renders Start Page
    """
    return render_template("index.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    """
    Module to take input search parameters from form.
    """
    filenames = []
    if request.method == 'POST':
        engine_file = request.files['engine_file']
        vdsm_file1 = request.files['vdsm_file1']
        vdsm_file2 = request.files['vdsm_file2']
        if engine_file and allowed_file(engine_file.filename):
            filenames.append(secure_filename(engine_file.filename))
            engine_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(engine_file.filename)))
        if vdsm_file1 and allowed_file(vdsm_file1.filename):
            filenames.append(secure_filename(vdsm_file1.filename))
            vdsm_file1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(vdsm_file1.filename)))
        if vdsm_file2 and allowed_file(vdsm_file2.filename):
            filenames.append(secure_filename(vdsm_file2.filename))
            vdsm_file2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(vdsm_file2.filename)))
        print "yolo"
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        print "lets go"
        print filenames
        return redirect(url_for("displ", engine=filenames[0], vdsm1=filenames[1], vdsm2=filenames[2], start_time=start_time, end_time=end_time))

    if request.method == "GET":
        return render_template("search.html")

@app.route("/display", methods=['GET', 'POST'])
def displ():
    """
    Module to display logs given search criteria parameters
    """
    # filenames = request.args['filenames']
    # print filenames
    # engine_file = request.files['engine_file']
    # vdsm_file1 = request.files['vdsm_file1']
    # vdsm_file2 = request.files['vdsm_file2']
    #     # print secure_filename(engine_file.filename)
    # filename =""
    # if engine_file and allowed_file(engine_file.filename):
    #     filenames.append(secure_filename(engine_file.filename))
    #     engine_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(engine_file.filename)))
    # if vdsm_file1 and allowed_file(vdsm_file1.filename):
    #     filenames.append(secure_filename(vdsm_file1.filename))
    #     vdsm_file1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(vdsm_file1.filename)))
    # if vdsm_file2 and allowed_file(vdsm_file2.filename):
    #     filenames.append(secure_filename(vdsm_file2.filename))
    #     vdsm_file2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(vdsm_file2.filename)))
    filename = "uploads/"+request.args['engine']
    print filename
    # start_time = Parser("2017-02-23 09:28:30,576Z").get_timestamp()
    # end_time = Parser("2017-02-23 09:28:30,660Z").get_timestamp()
    start_time = Parser(request.args['start_time']).get_timestamp()
    end_time = Parser(request.args['end_time']).get_timestamp()
    logs = Searcher(filename).find(start_time, end_time)
    log_array = []
    log = None
    for line in logs:
        elog = Parser(line).engine_parser()
        if elog is not None:
            log_array.append(elog)
            log = elog
        if elog is None and log is not None:
            log.message = log.message + line
    # for elog in log_array:
    #     print elog.message

    filename = "uploads/"+request.args['vdsm1']
    # start_time = Parser("2017-02-23 09:28:30,576Z").get_timestamp()
    # end_time = Parser("2017-02-23 09:28:30,660Z").get_timestamp()
    start_time = Parser(request.args['start_time']).get_timestamp()
    end_time = Parser(request.args['end_time']).get_timestamp()
    logs = Searcher(filename).find(start_time, end_time)
    log_array1 = []
    log = None
    for line in logs:
        vlog = Parser(line).vdsm_parser()
        if vlog is not None:
            log_array1.append(vlog)
            log = vlog
        if vlog is None and log is not None:
            log.message = log.message + line
    # for vlog in log_array1:
    #     print vlog.message

    filename = "uploads/"+request.args['vdsm2']
    start_time = Parser(request.args['start_time']).get_timestamp()
    end_time = Parser(request.args['end_time']).get_timestamp()
    logs = Searcher(filename).find(start_time, end_time)
    log_array2 = []
    log = None
    for line in logs:
        vlog = Parser(line).vdsm_parser()
        if vlog is not None:
            log_array2.append(vlog)
            log = vlog
        if vlog is None and log is not None:
            log.message = log.message + line
    # for vlog in log_array2:
    #     print vlog.message

    return render_template("dd.html", logs=log_array, vdsm1=log_array1, vdsm2=log_array2)

if __name__ == "__main__":
    app.run(debug=True)
