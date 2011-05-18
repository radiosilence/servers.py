#!/usr/bin/python

from string import atoi
import os, sys, stat
import ConfigParser, os
import pprint

servers = []
skels = {}

for skel in ['nginx_php5', 'nginx_flat', 'nginx_php5_test', 'nginx_wsgi', 'nginx_php5_ssl', 'supervisor_gunicorn']:
    skels[skel] = open('skeletons/%s.skel' % skel, 'r').readlines()

def main():
    config = ConfigParser.SafeConfigParser()
    config.read('servers.cfg')
    paths = config.defaults()

    for section in config.sections():
        server = {
            'name': section,
            'type': config.get(section, 'type'),
        }
        for p in ['aliases', 'primary', 'app']:
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
            with open(paths['supervisor_conf_dir'] % server['name'] + '.conf', 'w') as f:
                f.write("".join(skels['supervisor_gunicorn']) % server)
                print "Written supervisor config for %s." % server['name']
            f.closed

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
