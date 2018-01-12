#!/usr/bin/env python

import os
import re
from jinja2 import Template

class FlaskCreator(object):

    def __init__(self, appname):
        self.appname = appname

    def path(self, *args):
        path = os.path.join('blueprints', *args)
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

        with open(self.file(self.path(*path), filename), mode) as f:
            print(content, file=f)

    def write_file_template(self, *args, **kws):
        path = args[:-2]
        filename = args[-2]
        template_file = args[-1]

        full_path = os.path.join(self.path(*path), filename)

        with open(template_file, 'r') as f:
            Template(f.read()).stream(**kws).dump(full_path)

    def update_file(self, *args, **kws):
        path = args[:-1]
        filename = args[-1]

        full_path = os.path.join(self.path(*path), filename)


        with open(full_path, 'r') as f:
            template = f.read()
            for k in kws:
                template = re.sub('# {{ %s }}' % (k),
                                  '{{ %s }}' % (k),
                                  template,
                                  re.MULTILINE)
        
        Template(template).stream(**kws).dump(full_path)

    def initialize(self):
        self.write_file_template(self.appname,
                                 'config.py',
                                 'template_config.py',
                                 appname=self.appname)

        self.write_file(self.appname,
                        'requirements.txt',
                        """""")

        self.write_file_template(self.appname,
                                 'run.py',
                                 'template_run.py',
                                 appname=self.appname)
        
        self.write_file_template(self.appname,
                                 self.appname,
                                 '__init__.py',
                                 'template_init.py')

        self.write_file(self.appname,
                        self.appname,
                        'models.py',
                        """""")

        self.path(self.appname,
                  self.appname,
                  'tests')
        
    def add_module(self, module):
        self.update_file(self.appname,
                        self.appname,
                        '__init__.py',
                         module_import="""from .%s import %s
# {{ module_import }}""" % (module, module),
                         module_blueprint="""app.register_blueprint(%s)
# {{ module_blueprint }}""" % (module))

        self.write_file_template(self.appname,
                                 self.appname,
                                 module,
                                 '__init__.py',
                                 'template_module_init.py',
                                 module=module)
                        
        self.write_file_template(self.appname,
                                 self.appname,
                                 module,
                                 'views.py',
                                 'template_module_views.py',
                                 module=module)

        self.path(self.appname,
                  self.appname,
                  module,
                  'static')

        self.write_file_template(self.appname,
                                 self.appname,
                                 module,
                                 'templates',
                                 module,
                                 'index.html',
                                 'template_module_index.html',
                                 appname=self.appname,
                                 module=module)

    def create_flask_config(self):
        pass


if __name__ == '__main__':
    creator = FlaskCreator('testapp')
    creator.initialize()
    creator.add_module('site')
    creator.add_module('admin')
