from core.portfolio import *
import pandas as pd
import statsmodels.api as sm
import numpy as np
import config
import time
import os
from core.utils import *
from core.adv_utlis import *

period = ('2010-04', '2019-07')
factor_path = os.path.join(config.raw_directory, 'STK_MKT_FivefacDay.txt')
factors = get_factors(factor_path, period, mode='m')

print(1)