#!/usr/bin/python

import os, sys, stat
import ConfigParser, os
import pprint

pp = pprint.PrettyPrinter(indent=4)

output_nginx = '/etc/nginx/sites-available/%s.conf'
output_init = '/etc/init.d/flask_%s'

#servers = [
#    {'port': 5000, 'app': 'flasktest', 'aliases': ''}
#]

servers = []

def generator(object):
    def generate():
        print "hi"

skels = {
    'nginx_php': open('skeletons/nginx_php.skel', 'r').readlines(),
    'nginx_flask': open('skeletons/nginx_flask.skel', 'r').readlines(),
    'nginx_flat': open('skeletons/nginx_flat.skel', 'r').readlines(),
    'init': open('skeletons/init_bjoern.skel', 'r').readlines()
}

def main():
    config = ConfigParser.SafeConfigParser()
    config.read('servers.cfg')
    paths = config.defaults()

    for section in config.sections():
        server = {
            'name': section,
            'type': config.get(section, 'type')
        }
        for p in ['port', 'aliases']:
            try:
                server[p] = config.get(section, p)
            except ConfigParser.NoOptionError:
                server[p] = ''
        
        servers.append(server)

    for server in servers:
        if server['type'] == 'flask':
            nginx_name = "flask_%s" % server['name']

            with open(paths['sites_dir'] % nginx_name, 'w') as f:
                f.write("".join(skels['nginx_flask']) % server)
                print "Written nginx conf for %s." % nginx_name
            f.closed

            init_name = "bjoern_%s" % server['name']
            with open(paths['init_dir'] % init_name, 'w') as f:
                f.write("".join(skels['init']) % server)
                print "Written init script for %s." % init_name
            f.closed
            os.chmod(paths['init_dir'] % init_name, stat.S_IRWXU)

        else:
            t = server['type']
            nginx_name = '%s_%s' % (t, server['name'])
            with open(paths['sites_dir'] % nginx_name, 'w') as f:
                f.write("".join(skels['nginx_%s' % t]) % server)
                print "Written nginx conf for %s." % nginx_name
            f.closed

if __name__ == '__main__':
    main()
