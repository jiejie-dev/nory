import importlib
import logging

import os
import yaml

from nory.infras.exts.models import ExtensionInfo


class ExtensionInfoLoader(object):
    def load(self, name) -> ExtensionInfo:
        pass


class ExtensionPyInfoLoader(ExtensionInfoLoader):
    """info.py"""

    def load(self, name) -> ExtensionInfo:
        info_m = importlib.import_module('extensions.{}.info'.format(name))
        app_info = ExtensionInfo(
            name=name,
            author=getattr(info_m, '__author__', 'None'),
            version=getattr(info_m, '__version__', 'None'),
            description=getattr(info_m, '__description__', 'None'),
            home_page=getattr(info_m, '__home_page__', 'None'),
            indexs=getattr(info_m, 'INDEXS', []),
            dependency=getattr(info_m, 'dependency', []),
            static=getattr(info_m, 'static', {}),
            enabled=getattr(info_m, 'enabled', False),
            locale=getattr(info_m, 'locale', {})
        )
        return app_info


class ExtensionYamlInfoLoader(ExtensionInfoLoader):
    """app.yaml"""

    def load(self, name) -> ExtensionInfo:
        abs_p = os.path.abspath('.')
        path = os.path.join(abs_p, 'extensions/{}/{}'.format(name, 'app.yaml'))
        app_info = yaml.load(open(path))
        logging.debug('app_info from yaml:{}'.format(app_info))
        app_info = ExtensionInfo(
            name=name,
            author=app_info.get('author', ''),
            version=app_info.get('version', ''),
            description=app_info.get('description', ''),
            home_page=app_info.get('home_page'),
            indexs=app_info.get('indexs', []),
            dependency=app_info.get('dependency', []),
            static=app_info.get('static', {}),
            enabled=app_info.get('enabled', False),
            locale=app_info.get('locale', {})
        )
        return app_info


def load_extension_info(name) -> ExtensionInfo:
    m = {
        'info.py': ExtensionPyInfoLoader(),
        'app.yaml': ExtensionYamlInfoLoader()
    }
    abs_p = os.path.abspath('.')
    filter_path = lambda key: os.path.exists(os.path.join(abs_p, 'extensions/{}/{}'.format(name, key)))
    keys = list(filter(filter_path, m.keys()))
    if keys is None or len(keys) == 0:
        raise FileNotFoundError('app info file not found {}'.format(name))
    elif len(keys) > 1:
        raise Exception('more than one app info file exists')

    loader = m.get(keys[0], None)
    if loader is not None:
        return loader.load(name)
    raise Exception('[load_extension_info] loader not found for [{}]'.format(name))