#!/usr/bin/python

from string import atoi
import os, sys, stat
import ConfigParser, os
import pprint

servers = []
skels = {}

for skel in ['nginx_php5', 'nginx_flat', 'nginx_php5_test', 'nginx_wsgi', 'init_gunicorn', 'nginx_php5_ssl']:
    skels[skel] = open('skeletons/%s.skel' % skel, 'r').readlines()

def main():
    config = ConfigParser.SafeConfigParser()
    config.read('servers.cfg')
    paths = config.defaults()
    wsgi_name = paths['wsgi_server']

    for section in config.sections():
        server = {
            'name': section,
            'type': config.get(section, 'type')
        }
        for p in ['aliases', 'primary']:
            try:
                server[p] = config.get(section, p)
            except ConfigParser.NoOptionError:
                server[p] = ''
        
        servers.append(server)

    for k,v in paths.items():
        paths[k] = os.path.abspath(v)

    for server in servers:
        if server['type'] in ['wsgi']:
            server['path'] = paths['apps_dir']
            init_name = "%s_%s" % (wsgi_name, server['name'])
            server['daemon'] = paths['wsgi_server']
            with open(paths['init_dir'] % init_name, 'w') as f:
                f.write("".join(skels['init_%s' % wsgi_name]) % server)
                print "Written init script for %s." % init_name
            f.closed
            os.chmod(paths['init_dir'] % init_name, stat.S_IRWXU)

        else:
            server['path'] = paths['vhosts_dir']

        t = server['type']
        nginx_name = '%s_%s' % (t, server['name'])
        with open(paths['sites_dir'] % nginx_name, 'w') as f:
            f.write("".join(skels['nginx_%s' % t]) % server)
            print "Written nginx conf for %s." % nginx_name
        f.closed

if __name__ == '__main__':
    main()
