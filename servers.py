#!/usr/bin/python

import os, sys, stat
import ConfigParser, os
import pprint

servers = []

skels = {
    'nginx_php': open('skeletons/nginx_php.skel', 'r').readlines(),
    'nginx_flask': open('skeletons/nginx_flask.skel', 'r').readlines(),
    'nginx_flat': open('skeletons/nginx_flat.skel', 'r').readlines(),
    'nginx_php_test': open('skeletons/nginx_php_test.skel', 'r').readlines(),
    'init_bjoern': open('skeletons/init_bjoern.skel', 'r').readlines()
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

    for k,v in paths.items():
        paths[k] = os.path.abspath(v)

    for server in servers:
        if server['type'] in ['flask']:
            server['path'] = paths['apps_dir']
            
            init_name = "bjoern_%s" % server['name']
            server['daemon'] = paths['wsgi_server']
            with open(paths['init_dir'] % init_name, 'w') as f:
                f.write("".join(skels['init_bjoern']) % server)
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
