from .infras import *
from .envtypes import *
from .version import *

from nory import WebBuilder, logger_factory, auth_factory, data_factory, response_factory

import os

def create_default_app(name):
  root_path = os.path.abspath(os.curdir)

  web_builder = WebBuilder(name, root_path)
  web_builder.env.configuration.add_file_by_prefix('appsettings', follow_mode=False)
  web_builder.use_middlewares([logger_factory, auth_factory, data_factory, response_factory])
  web_builder.use_ext_manager([name])
  
  return web_builder.build()