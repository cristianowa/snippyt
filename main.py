from flask import Flask, request, redirect, jsonify
import flask
import argparse
import traceback
app = Flask(__name__, static_folder="static/", template_folder="templates/")


def get_uuid():
    import uuid
    return str(uuid.uuid1()).replace("-","")

import shelve

shelve_name = None

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

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-d", '--debug', help="Enables debug", dest='debug', action="store_true")
    subparsers = p.add_subparsers(help="", dest="command")

    serve = subparsers.add_parser("serve")
    serve.add_argument("-p","-port", type=int, help="Server ports", dest="port", default="9090")
    serve.add_argument("-storage", help="File to store snippets", dest="storage", default="/tmp/snippyt")
    serve.add_argument('-b','--bg', help="send server to background", dest='background', action="store_true")

    post = subparsers.add_parser("post")
    post.add_argument("-a", "-address", help="Server to post content to", dest="post_server", default="localhost:9090")
    post.add_argument("-c", "-content", help="Content to be posted", dest="post_content")
    post.add_argument("-t", "-title", help="Title of content to be posted", dest="post_title", default="")

    args = p.parse_args()
    if args.command == "serve":
        try:
            shelve_name = args.storage
            if args.background:
                import daemon
                with daemon.DaemonContext():
                    app.run(port=args.port, debug=args.debug)
            else:
                app.run(port=args.port, debug=args.debug)
        except:
            if args.debug:
                traceback.print_exc()
            print serve.format_usage()
    elif args.command ==  "post":
        try:
            ans = post_snippet(args.post_server, args.post_content, args.post_title)
            if ans.status_code >= 400:
                print "Error posting, code: {0}".format(ans.status_code)
            print ans.content
        except:
            if args.debug:
                traceback.print_exc()
            print post.format_usage()

    else:
        print p.format_usage()
