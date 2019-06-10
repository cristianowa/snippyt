from flask import Flask, request, redirect, jsonify
import flask
import traceback
app = Flask(__name__, static_folder="static/", template_folder="templates/")


def get_uuid():
    import uuid
    return str(uuid.uuid1()).replace("-","")

import shelve

shelve_name = None

def get_code(uuid):
    s = shelve.open(shelve_name)
    source_code, title = s[str(uuid)]
    s.close()
    return source_code, title

def add_code(source_code, title):
    uuid = get_uuid()
    s = shelve.open(shelve_name)
    s[uuid] = (source_code, title)
    s.sync()
    s.close()
    return uuid

@app.route("/<filename>")
def static_send(filename):
    return app.send_static_file(filename)

@app.route("/code/<uuid>", methods=["GET", "DEL"])
def get_snippet(uuid):
    code, title = get_code(uuid)
    return flask.render_template('code.html', source_code=code, source_title=title)

@app.route("/link/<uuid>")
def get_link(uuid):
    new_location = request.base_url[:str(request.base_url).find("link/")] + "code/{0}".format(uuid)
    return flask.render_template('link.html', link=new_location)

@app.route('/', methods=["GET", "POST"])
def poster():
    if request.method == "GET":
        return  app.send_static_file("post.html")
    print request.form["source_code"]
    uuid = add_code(request.form["source_code"], request.form["title"])
    try:
        if request.form["script"].lower() == 'true':
            return jsonify(dict(link=request.base_url + "code/{0}".format(uuid)))
    except:
        pass
    return redirect(request.base_url + "link/{0}".format(uuid))

def post_snippet(host, content, title):
    if host.find("http://") != 0:
        host = "http://" + host
    import requests
    ans = requests.post(host, data=dict(source_code=content, title=title, script=True))
    return ans

