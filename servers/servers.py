#!/usr/bin/env python2
import os
from yaml import load, dump
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('servers', 'skeletons'))


def generate_config(name, site, instance, config, config_type):
    ext = config_type.split('.')[-1]
    def path(type, name=None, application=None, **kwargs):
        template_path = [config['type']]
        if application:
            template_path.extend([
                'applications',
                config['application'],
            ])
        if name:
            template_path.extend([name])
        return u'{path}.{ext}'.format(
            path=u'/'.join(template_path),
            ext=ext
        )
    def parent(config):
        if not 'parent' in config:
            return None
        else:
            return path(
                name=config['parent'],
                type=config['type']
            )

    template = env.get_template(
        path(**config)
    )
    rendered = template.render(
        name=name,
        site=site,
        parent=parent(config),
        instance=instance,
        config=config
    )
    print rendered


def process_site(name, site, types):
    for instance in site['instances']:
        for config in site['configs']:
            generate_config(name, site, instance, config, types[config['type']])

def generate(path):
    config_path = os.path.abspath(path)
    with open(config_path, 'r') as config_file:
        config = load(config_file.read())
    
    for name, site in config['sites'].items():
        process_site(name, site, config['types'])

    # template = env.get_template('.html')