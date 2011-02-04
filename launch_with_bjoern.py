#!/usr/bin/python
#from gevent.wsgi import WSGIServer
import bjoern
import sys

def main():
    if len(sys.argv) < 3:
        exit("Usage: bjoern <app> <port>.")
    sys.path.append("%s" % sys.argv[1])
    from app import app
    bjoern.run(app, '127.0.0.1', int(sys.argv[2]))
    
if __name__ == '__main__':
    main()
