from flask import Flask, request, redirect
import flask

app = Flask(__name__, static_folder="static/", template_folder="templates/")


def get_uuid():
    import uuid
    return str(uuid.uuid1()).replace("-","")

import shelve
shelve_name = "/tmp/code"
def get_code(uuid):
    s = shelve.open(shelve_name)
    source_code = s[str(uuid)]
    s.close()
    return source_code

def add_code(source_code):
    uuid = get_uuid()
    s = shelve.open(shelve_name)
    s[uuid] = source_code
    s.sync()
    s.close()
    return uuid

@app.route("/<filename>")
def static_send(filename):
    return app.send_static_file(filename)

@app.route("/code/<uuid>", methods=["GET", "DEL"])
def get_snippet(uuid):
    code = get_code(uuid)
    return flask.render_template('code.html', source_code=code)

@app.route("/link/<uuid>")
def get_link(uuid):
    new_location = request.base_url[:str(request.base_url).find("link/")] + "code/{0}".format(uuid)
    return flask.render_template('link.html', link=new_location)

@app.route('/', methods=["GET", "POST"])
def poster():
    if request.method == "GET":
        return  app.send_static_file("post.html")
    print request.form["source_code"]
    uuid = add_code(request.form["source_code"])
    new_location = request.base_url + "link/{0}".format(uuid)
    return redirect(new_location)

if __name__ == '__main__':
    app.run(port=9090, debug=True)
