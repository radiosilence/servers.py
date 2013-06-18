#!/usr/bin/env python2
import os
from yaml import load
from jinja2 import Environment, PackageLoader
from unipath import Path
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
            config['parent'] = 'base'

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
    return rendered


def write_config(name, instance_name, config, config_type):
    path = Path(config_type.format(
        name=name,
        instance=instance_name,
    ))
    try:
        os.makedirs(path.ancestor(1))
    except OSError as (id, e):
        if id != 17:
            raise
    with open(path, 'w') as f:
        f.write(config)
        print('Written {path}'.format(path=path))


def process_site(name, site, types, settings):
    for instance in site['instances']:
        for config in site['configs']:
            config_type = types[config['type']]
            for setting, value in settings.items():
                config[setting] = config.get(setting, value).format(
                    name=name,
                    instance=instance['name']
                )

            config = generate_config(
                name,
                site,
                instance,
                config,
                config_type
            )
            write_config(
                name, instance['name'], config, config_type
            )


def generate(path):
    config_path = Path(path)
    with open(config_path, 'r') as config_file:
        config = load(config_file.read())

    for name, site in config['sites'].items():
        process_site(name, site, config['types'], config['settings'])
