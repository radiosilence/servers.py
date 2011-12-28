#!/usr/bin/python

from string import atoi
import os, sys, stat
import ConfigParser, os
import pprint

servers = []
skels = {}

for skel in os.listdir('skeletons'):
    skels['.'.join(skel.split('.')[:-1])] = open('skeletons/%s' % skel, 'r').readlines()

def main():
    config = ConfigParser.SafeConfigParser()
    config.read('servers.cfg')
    paths = config.defaults()

    for section in config.sections():
        server = {
            'name': section,
            'type': config.get(section, 'type'),
        }
        for p in ['aliases', 'app']:
            try:
                server[p] = config.get(section, p)
            except ConfigParser.NoOptionError:
                server[p] = ''
        
        servers.append(server)

    for k,v in paths.items():
        paths[k] = os.path.abspath(v)

    for server in servers:
        server['path'] = paths['vhosts_dir']
        t = server['type']
        server['appname'] = server['app'].split(':')[0]
        server['primary'] = server['aliases'].split(' ')[0]
        nginx_name = '%s' % server['name']
        with open(paths['sites_dir'] % nginx_name, 'w') as f:
            f.write("".join(skels['nginx_%s' % t]) % server)
            print "Written nginx conf for %s." % nginx_name
        f.closed

if __name__ == '__main__':
    main()
