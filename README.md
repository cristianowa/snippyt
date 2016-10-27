#snipPYt

one click install self-hosted code snippets

## Motivation

I just wanted to share some snippets in my local network without having to send it to gist, pastebin, etc. I also did not want to install and configure a network server to run a one page application, so I wrote this piece of code that hold code snippets on my PC until it reboots (or forever, if the shelve file is outside /tmp).

## Instalation

Install requirements:

`pip install -r requirements.txt`

Download the repository and run

`python setup build`

and

`python setup.py install`

alternativally use pip:

`pip install snippyt`

to use client application with pasting, install xclip

` 

## Server Execution
Launch with defaults:
`python main.py serve`
and it will store snippets in /tmp/snippyt and listen on port 9090.

If you want specificy port and storage file, use:
`./snippyt.py serve -p 9090 -storage /tmp/youdatabase`

For daemonizing it, just lauch it with the `-b` flag.

## Client Execution



