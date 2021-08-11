import initrdtool.package.version
import initrdtool.package.source
import initrdtool.packages
from initrdtool.packages import session, Base
from sqlalchemy import Column, Integer, String
import math
import os.path
import re
import pycurl

MAX_NAME_STR_LEN = 64
MAX_URL_STR_LEN = 256
MAX_SRC_URL_SUFFIX_PATTERN_LEN = 128
MAX_SIG_URL_SUFFIX_PATTERN_LEN = 128

def _download(url, file_path):
	if not os.path.isfile(file_path):
		url_str = str(url)

		print("Downloading %s to %s\n" %(url_str, file_path))
		file_handle = open(file_path, 'wb')

		crl = pycurl.Curl()
		crl.setopt(crl.URL, url_str)
		crl.setopt(crl.WRITEDATA, file_handle)

		crl.perform()

		crl.close()

		file_handle.close()
	else:
		print("File %s already exists.\n" % file_path)

class Package(Base):
	__tablename__ = 'packages'

	id = Column(Integer, primary_key=True)
	name = Column(String(MAX_NAME_STR_LEN))
	url = Column(String(MAX_URL_STR_LEN))

	src_url_suffix_pattern = Column(String(MAX_SRC_URL_SUFFIX_PATTERN_LEN))
	sig_url_suffix_pattern = Column(String(MAX_SIG_URL_SUFFIX_PATTERN_LEN))

	_versions = []

	def register(self):
		initrdtool.packages.package_definitions[self.get_name()] = self

	def deregister(self):
		del initrdtool.packages.package_definitions[self.get_name()]

	def get_name(self):
		return(self.name)

	def _src_filename_to_sig_filename(self, url):
		if (self.src_url_suffix_pattern == None):
			sig_url = url + self.sig_url_suffix_pattern
		else:
			sig_url = re.sub(self.src_url_suffix_pattern, self.sig_url_suffix_pattern, url)
		return(sig_url)

	def get_src_files(self, version):
		pass

	def get_src_urls(self, version):
		pass

	def get_sig_files(self, version):
		src_urls = self.get_src_urls(version)
		sig_files = {}
		for src_file in src_urls.keys():
			sig_file = self._src_filename_to_sig_filename(src_file)
			sig_files[src_file] = sig_file
		return(sig_files)

	def get_sig_urls(self, version):
		src_urls = self.get_src_urls(version)
		sig_urls = {}
		for src_name in src_urls.keys():
			sig_name = self._src_filename_to_sig_filename(src_name)
			src_url = src_urls[src_name]
			src_url_str = str(src_url)
			url_type = src_url.get_type()
			sig_url_str = self._src_filename_to_sig_filename(src_url_str)
			sig_urls[sig_name] = source.construct(sig_url_str, url_type)
		return(sig_urls)

	def get_url(self):
		return(self.url)

	def get_versions(self):
		""" Returns a list of the versions of a package that are available. """
		return(self._versions.copy())

	def set_versions(self, versions):
		""" Sets the current list of versions from a saved copy. """
		self._versions = sorted(versions)

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
				return
		iter = itermin
			
		self._versions.insert(iter, newversion)

	def restore(self):
		""" Load all package versions from database session. """
		pass
		
	def preserve(self):
		""" Add all package versions to database session. """
		pass

	def update_versions(self):
		pass

	def get_src_filenames(self):
		return list(self.get_src_urls().keys())

	def get_sig_filenames(self):
		return list(self.get_sig_urls().keys())

	def download(self, version):
		package_name = self.get_name()

		# Make sure dist dir exists.
		if not os.path.isdir(initrdtool.distfiles):
			os.mkdir(initrdtool.distfiles)

		# If it does,
		if os.path.isdir(initrdtool.distfiles):

			# Get list of files to download.
			src_files = self.get_src_files(version)
			sig_files = self.get_sig_files(version)

                        # Get the corresponding urls.
			src_urls = self.get_src_urls(version)
			sig_urls = self.get_sig_urls(version)

                        # Download each source in turn.
			for src_file in ( src_files ):
				sig_file = sig_files[src_file]
				src_path = os.path.join(initrdtool.distfiles, src_file)
				sig_path = os.path.join(initrdtool.distfiles, sig_file)
				src_url = src_urls[src_file]
				sig_url = sig_urls[sig_file]
				src_url_str = str(src_url)
				sig_url_str = str(sig_url)

				print("Signature %s verifies source %s\n" %(sig_url_str, src_url_str))
				_download(sig_url, sig_path)
				_download(src_url, src_path)

	def verify(self, version):
		package_name = self.get_name()

		#if not os.path.isdir(initrdtool.distfiles):
		#	os.mkdir(initrdtool.distfiles)

		#if os.path.isdir(initrdtool.distfiles):
		#	sig_url = self.get_sig_urls(version)

# vim: set ts=4 sw=4 noexpandtab :
