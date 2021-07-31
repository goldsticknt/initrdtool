import initrdtool.package.version;
import initrdtool.package.source;
import initrdtool.packages;
import math;
import os.path;
import re;
import pycurl;

class Package:
	def __init__(self):
		self._src_url_suffix_pattern = None;
		self._sig_url_suffix_pattern = None;
		pass

	def _url_to_filename(self, url):
		package_name = self.get_name()
		file_name = re.sub(r'^.*/', r'', url)
		if not ( package_name.lower() in file_name.lower() ):
			file_name = re.sub(r'^.*/([^/]*)/', r'\1-', url)
		return(file_name);

	def register(self):
		initrdtool.packages.package_definitions[self.get_name()] = self;

	def deregister(self):
		del initrdtool.packages.package_definitions[self.get_name()];

	def get_name(self):
		return(self._name);

	def src_url_to_sig_url(self, url):
		if (self._src_suffix_pattern == None):
			sig_url = url + self._sig_suffix_pattern;
		else:
			sig_url = re.sub(self._src_suffix_pattern, self._sig_suffix_patterm, url);
		return(sig_url);

	def get_src_urls(self, version):
		pass

	def get_sig_urls(self, version):
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

	def get_sig_filenames(self):
		package_name = self.get_name()
		urls = self.get_sig_urls(version)
		file_names = {}

		for url in urls:
		    file_name = _url_to_filename(url)
		    file_names.append(file_name)

		return file_names

	def get_src_filenames(self):
		package_name = self.get_name()
		urls = self.get_src_urls(version)
		file_names = {}

		for url in urls:
		    file_name = _url_to_filename(url)
		    file_names.append(file_name)

		return file_names

	def download(self, version):
		package_name = self.get_name()

		if not os.path.isdir(initrdtool.distfiles):
			os.mkdir(initrdtool.distfiles)

		if os.path.isdir(initrdtool.distfiles):

			sig_urls = self.get_sig_urls(version)
			src_urls = self.get_src_urls(version)
			for url in ( list(sig_urls) + list(src_urls) ):
				file_name = self._url_to_filename(url)
				file_path = os.path.join(initrdtool.distfiles, file_name)

				if not os.path.isfile(file_path):
					print("Downloading %s to %s\n" %(url, file_path))
					file_handle = open(file_path, 'wb')

					crl = pycurl.Curl()
					crl.setopt(crl.URL, url)
					crl.setopt(crl.WRITEDATA, file_handle)

					crl.perform()

					crl.close()

					file_handle.close()
				else:
					print("File %s already exists.\n" % file_path)

	def verify(self, version):
		package_name = self.get_name()

		#if not os.path.isdir(initrdtool.distfiles):
		#	os.mkdir(initrdtool.distfiles)

		#if os.path.isdir(initrdtool.distfiles):
		#	sig_url = self.get_sig_urls(version)

# vim: set ts=4 sw=4 noexpandtab :
