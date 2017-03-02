
import sys, time

sys.modules['time2'] = time

import time2

del time
del sys.modules['time2']