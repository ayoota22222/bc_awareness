import random
import string
import os
from dateutil.parser import parse

import logging
_logger = logging.getLogger(__name__)

class Util:
    addons_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    def __init__(self):
        self.addons_path = self.addons_path.replace('bc_awareness/bc_awareness', 'bc_awareness')

    def path(self, *paths):
        ''' Make a path
        '''
        return os.path.join(self.addons_path, *paths)
 

util = Util()