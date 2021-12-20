# -*- coding: utf-8 -*-
__author__ = "Markus Neubauer"
__copyright__ = "see GPLv3"
__license__ = "GPLv3"
__version__ = "0.1.5"
__maintainer__ = "Markus Neubauer"
__email__ = "neubauer@invalid.email-online.org"
__status__ = "Development"

# pylint: disable=import-error
from .config import DBConfig  # pylint disable=import-error
from .database import DBConnect  # pylint disable=import-error
from .tables import MODELS, WGData, WGRelation
