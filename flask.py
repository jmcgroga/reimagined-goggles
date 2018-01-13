#!/usr/bin/env python

import os
import re
from jinja2 import Template

class FlaskCreator(object):

    def __init__(self, appname):
        self.appname = appname
        self.app_root = os.path.join('blueprints', self.appname)
        self.app_module_root = os.path.join('blueprints', self.appname, self.appname)

    def exists(self, module=None):
        if module is not None:
            return os.path.exists(self.module_root(module))
        return os.path.exists(self.app_module_root)

    def module_root(self, module):
        return os.path.join('blueprints', self.appname, self.appname, module)

    def makedirs(self, *args):
        path = os.path.join(*args)
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        return path

    def file(self, path, filename):
        return os.path.join(path, filename)

    def write_file(self, *args, **kws):
        path = args[:-2]
        filename = args[-2]
        content = args[-1]
        if 'mode' in kws:
            mode = kws['mode']
        else:
            mode = 'w'

        with open(self.file(self.makedirs(*path), filename), mode) as f:
            print(content, file=f)

    def write_file_template(self, *args, **kws):
        path = args[:-2]
        filename = args[-2]
        template_file = args[-1]

        full_path = os.path.join(self.makedirs(*path), filename)

        with open(template_file, 'r') as f:
            Template(f.read()).stream(**kws).dump(full_path)

    def update_file(self, *args, **kws):
        path = args[:-1]
        filename = args[-1]

        full_path = os.path.join(self.makedirs(*path), filename)

        with open(full_path, 'r') as f:
            template = f.read()
            for k in kws:
                template = re.sub('# {{ %s }}' % (k),
                                  '{{ %s }}' % (k),
                                  template,
                                  re.MULTILINE)
        
        Template(template).stream(**kws).dump(full_path)

    def initialize(self):
        self.write_file_template(self.app_root,
                                 'config.py',
                                 'template_config.py',
                                 appname=self.appname)

        self.write_file(self.app_root,
                        'requirements.txt',
                        """""")

        self.write_file_template(self.app_root,
                                 'run.py',
                                 'template_run.py',
                                 appname=self.appname)
        
        self.write_file_template(self.app_module_root,
                                 '__init__.py',
                                 'template_init.py')

        self.write_file(self.app_module_root,
                        'models.py',
                        """""")

        self.makedirs(self.app_module_root,
                      'tests')
        
    def add_module(self, module, module_prefix=None):
        if module_prefix is None:
            module_prefix = '/' + module

        self.update_file(self.app_module_root,
                         '__init__.py',
                         module_import="""from .%s import %s
# {{ module_import }}""" % (module, module),
                         module_blueprint="""app.register_blueprint(%s)
# {{ module_blueprint }}""" % (module))

        self.write_file_template(self.module_root(module),
                                 '__init__.py',
                                 'template_module_init.py',
                                 module=module,
                                 module_prefix=module_prefix)
                        
        self.write_file_template(self.module_root(module),
                                 'views.py',
                                 'template_module_views.py',
                                 appname=self.appname,
                                 module=module)

        self.makedirs(self.module_root(module),
                      'static')

        self.write_file_template(self.module_root(module),
                                 'templates',
                                 module,
                                 'index.html',
                                 'template_module_index.html',
                                 appname=self.appname,
                                 module=module)

    def create_flask_config(self):
        pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('appname', help="Application name")
    parser.add_argument('module', help="Module name", nargs='?', default=None)

    args = parser.parse_args()

    creator = FlaskCreator(args.appname)

    if creator.exists():
        if args.module is None:
            print('App "%s" already exists' % (args.appname))
    else:
        creator.initialize()
        creator.add_module('root', '/')

    if args.module is not None:
        if creator.exists(args.module):
            print('Module "%s" already exists!' % (args.module))
        else:
            creator.add_module(args.module)
