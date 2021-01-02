import initrdtool.package.version;
import initrdtool.package.source;
import initrdtool.packages;
import math;
import os.path;
import re;
import pycurl;

class Package:
	def __init__(self):
		pass

	def register(self):
		initrdtool.packages.package_definitions[self.get_name()] = self;

	def deregister(self):
		del initrdtool.packages.package_definitions[self.get_name()];

	def get_name(self):
		return(self._name);

	def get_source_url(self, version):
		pass

	def get_source_sig_url(self, version):
		pass

	def get_url(self):
		return(self._url)

	def get_versions(self):
		return(self._versions.copy())

	def get_latest_version(self):
		version = False
		if (len(self._versions) > 0):
			version = self._versions[-1]
		return(version)

	def _insert_version(self, newversion):
		""" Inserts a new version into the list of versions """
		itermin = 0
		itermax = len(self._versions)
		iter = 0
		while(itermin < itermax):
			iter = itermin + math.floor((itermax - itermin) / 2)
			comparison = self._versions[iter].compare(newversion)
			if (comparison < 0):
				itermin = iter + 1
			elif (comparison > 0):
				itermax = iter
			else:
				return;
		iter = itermin
			
		self._versions.insert(iter, newversion)

	def update_versions(self):
		pass

	def download(self, version):
		if not os.path.isdir(initrdtool.distfiles):
			os.mkdir(initrdtool.distfiles)

		if os.path.isdir(initrdtool.distfiles):

			source_url = self.get_source_url(version)
			source_name = re.sub(r'^.*\/', source_url, r'');
			source_filepath = os.path.join(initrdtool.distfiles, source_name)

			if not os.path.isfile(source_filepath):
				source_file = open(source_filepath, 'wb')

				crl = pycurl.Curl()
				crl.setopt(crl.URL, source_url)
				crl.setopt(crl.WRITEDATA, source_file)

				crl.perform()

				crl.close()

				source_file.close()

# vim: set ts=4 sw=4 noexpandtab :
