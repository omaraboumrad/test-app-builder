import argparse
import os
import random


class Field(object):
    TEMPLATE = """{name} = models.{tp}({options})"""

    def __init__(self, name, tp, *args, **kwargs):
        self.name = name
        self.tp = tp
        self.args = args
        self.kwargs = kwargs

    def as_str(self):
        options = ''

        if self.args:
            args = ', '.join(self.args)
            options = args

        if self.kwargs:
            kwargs_list = map(lambda (x,y): '{}={}'.format(x,y),
                              self.kwargs.items())
            kwargs = ', '.join(kwargs_list)
            if self.args:
                options = '{}, {}'.format(options, kwargs)
            else:
                options = kwargs

        return self.TEMPLATE.format(
            name=self.name,
            tp=self.tp,
            options=options)


class Model(object):

    TEMPLATE = """class {name}(models.Model):\n{content}"""

    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def as_str(self):
        pad4 = lambda x: '    {}'.format(x.as_str())
        content = '\n'.join(map(pad4, self.fields))
        return self.TEMPLATE.format(
            name=self.name,
            content=content or '    pass')


class Module(object):

    TEMPLATE = """from django.db import models\n\n\n{content}"""

    def __init__(self, name, models):
        self.name = name
        self.models = models

    def as_str(self):
        content = '\n\n\n'.join(m.as_str() for m in self.models)
        return self.TEMPLATE.format(content=content)


def module_builder(num_modules, num_models, max_fields):
    modules = []
    mf = 'M{}' # model format
    mc = 0; # model counter

    ff = 'f{}' # field format
    fc = 0 # field counter

    fields = (
        ('CharField', [], dict(max_length=200)),
        ('TextField', [], {}),
        ('IntegerField', [], dict(default=1)),
    )

    for i in range(num_modules):
        models = []
        for j in range(num_models//num_modules):
            _max_fields = random.randrange(1, max_fields+1)
            _fields = []
            for idx in range(fc+1, fc+_max_fields):
                _type, args, kwargs = random.choice(fields)
                _fields.append(Field(ff.format(idx), _type, *args, **kwargs))

            fc += _max_fields-1
            mc += 1
            models.append(Model(mf.format(mc), _fields))

        modules.append(Module('models.py', models))

    return modules

def apps_builder(target, num_apps, num_models, max_fields):
    modules = module_builder(num_apps, num_models, max_fields)
    pad4 = lambda x: '    {}'.format(x)

    if not os.path.exists(target):
        os.makedirs(target)

    app_counter = 0
    app_format = 'app{}'
    apps = []

    for module in modules:
        app_counter += 1
        app_name = app_format.format(app_counter)
        apps.append("'{}'".format(app_name))

        app_path = os.path.join(target, app_name)
        init_file = os.path.join(app_path, '__init__.py')
        models_file = os.path.join(app_path, module.name)

        if not os.path.exists(app_path):
            os.makedirs(app_path)
            open(init_file, 'a').close()

        with open(models_file, 'a') as f:
            f.write(module.as_str())

    with open(os.path.join(target, 'apps_settings.txt'), 'a') as f:
        installed_apps = 'INSTALLED_APPS += [\n{}\n]'
        f.write(installed_apps.format(',\n'.join(map(pad4, apps))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='target django directory')
    parser.add_argument('-a', '--apps', default=1, type=int)
    parser.add_argument('-m', '--models', default=1, type=int)
    parser.add_argument('-f', '--max-fields', default=1, type=int)

    args = parser.parse_args()

    apps = apps_builder(args.target, args.apps, args.models, args.max_fields)

