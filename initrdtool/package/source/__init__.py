from enum import Enum;

class Type(Enum):
    WEB = 0
    GIT = 1
    SVN = 2
    HG = 3

class Source:
	def __init__(self):
		pass;

	def __str__(self):
		pass;

	def get_type(self):
		return self._type;

class Web(Source):
	def __init__(self, url):
		self._type = Type.WEB;
		self._url = url;

	def __str__(self):
		return(str(self._url))

def construct(newurl, origtype):
	"Create a new source object from a url and type"
	if (origtype == Type.WEB):
		return Web(newurl)
	else:
		pass

# vim: set ts=4 sw=4 noexpandtab :
