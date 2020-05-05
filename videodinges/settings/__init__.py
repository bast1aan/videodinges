try:
	from .localsettings import *
except ImportError:
	from .defaultsettings import *