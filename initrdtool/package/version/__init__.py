import re

class Version:
	def __init__(self, string):
		self.__strrep = string
		self._version = re.split(r'[\.-]', string)

	def get_major(self):
		return(self._version[0])

	def get_minor(self):
		return(self._version[1])

	def __str__(self):
		return(self.__strrep)

	def compare(self, other):
		version_a = self._version
		version_b = other._version
		
		comp = 0
		iter = 0
		while (comp == 0) and (iter < len(version_a)) and (iter < len(version_b)):

			# Cast to int if this can be done to both versions.
			if (version_a[iter].isnumeric()) and (version_b[iter].isnumeric()):
				version_a_seg = int(version_a[iter])
				version_b_seg = int(version_b[iter])
			else:
				version_a_seg = version_a[iter]
				version_b_seg = version_b[iter]

				# Numeric values are considered greater.
				# This presumes that versions labeled -rc, -beta, -alpha, etc.
				# are prerelease versions.
				if (version_a_seg[0].isalpha()) and not(version_b_seg[0].isalpha()):
					comp = -1
				elif not(version_a_seg[0].isalpha()) and (version_b_seg[0].isalpha()):
					comp = 1

			# Perform comparison using provided type
			# if comparison hasn't already been performed.
			if (comp == 0):
				if (version_a_seg > version_b_seg):
					comp = 1
				elif (version_a_seg < version_b_seg):
					comp = -1 
			iter = iter + 1

		# If all components that align are equal, make sure one version isn't longer than another.
		if (comp == 0):
			lencomp = 0
			if (len(version_a) > iter) and (len(version_b) <= iter):
				lencomp = 1
				nextseg = version_a[iter]
			elif (len(version_b) > iter) and (len(version_a) <= iter):
				nextseg = version_b[iter]
				lencomp = -1

			# Treat string version components unfavorably.
			# eg. Appending a -rc? to the end.
			if (lencomp != 0) and (len(nextseg) > 0) and nextseg[0].isalpha():
				comp = -1 * lencomp
			else:
				comp = lencomp
				
		return(comp)
		
	def __eq__(self, other):
		comp = self.compare(other)
		if (comp == 0):
			retval = True
		else:
			retval = False
		return (retval)

	def __ne__(self, other):
		comp = self.compare(other)
		if (comp != 0):
			retval = True
		else:
			retval = False
		return (retval)

	def __ge__(self, other):
		comp = self.compare(other)
		if (comp >= 0):
			retval = True
		else:
			retval = False
		return (retval)
		
	def __le__(self, other):
		comp = self.compare(other)
		if (comp <= 0):
			retval = True
		else:
			retval = False
		return (retval)

	def __gt__(self, other):
		comp = self.compare(other)
		if (comp > 0):
			retval = True
		else:
			retval = False
		return (retval)
		
	def __lt__(self, other):
		comp = self.compare(other)
		if (comp < 0):
			retval = True
		else:
			retval = False
		return (retval)

# vim: set ts=4 sw=4 noexpandtab :
