#!/usr/bin/python
import argparse
import traceback
from snippyt import *
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
post.add_argument("-f", "-filename", help="File to be posted", dest="post_file", default=None)
post.add_argument("-t", "-title", help="Title of content to be posted", dest="post_title", default="")

args = p.parse_args()
if args.command == "serve":
    try:
        shelve_name = args.storage
        if args.background:
            import daemon
            with daemon.DaemonContext():
                app.run(host="0.0.0.0", port=args.port, debug=args.debug)
        else:
            app.run(host="0.0.0.0", port=args.port, debug=args.debug)
    except:
        if args.debug:
            traceback.print_exc()
        print serve.format_usage()
elif args.command == "post":
    try:
        import json
        if args.post_file is not None:
            content = open(args.post_file).read()
        else:
            content = args.post_content
        ans = post_snippet(args.post_server, content, args.post_title)

        if ans.status_code >= 400:
            print "Error posting, code: {0}".format(ans.status_code)
        link = json.loads(ans.content)["link"]
        print link
        try:
            import pyperclip
            pyperclip.copy(link)
            print "Text copied to clipboard"
        except:
            pass
    except Exception as e:

        if args.debug:
            traceback.print_exc()
        from requests.exceptions import ConnectionError
        if isinstance(e, ConnectionError):
            print "Server not available"
        else:
            print post.format_usage()

else:
    print p.format_usage()
