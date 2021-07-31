import initrdtool.package
from initrdtool.package import Package
import initrdtool.package.version
import initrdtool.packages;
from bisect import bisect_left
import pycurl;
from io import BytesIO;
import re;

PACKAGE_NAME = 'glibc'

class Glibc(Package):
	def __init__(self):
		self._name = PACKAGE_NAME
		self._url = 'https://www.gnu.org/software/libc/'
		self._versions = [];
		self._src_suffix_pattern = None;
		self._sig_suffix_pattern = '.sig';

	def __insert_version(self, newversion):
		""" Inserts a new version into the list of versions """
		iter = bisect_left(self._versions, newversion)
		if (iter >= len(self._versions)) or (self._versions[iter] != newversion):
			self._versions.insert(iter, newversion)

	def get_source_dir(self):
		source_dir = 'https://ftp.gnu.org/gnu/' + PACKAGE_NAME + '/'
		return(source_dir);

	def get_source_urls(self, version):
		source_url = self.get_source_dir() + str(version) + '.tar.xz'
		return([source_url]);

	def get_sig_urls(self, version):
		sig_urls = []
		for source_url in self.get_source_urls(version):
			sig_urls.append(self.src_url_to_sig_url(source_url))
		return(sig_urls);

	def update_versions(self):
		""" Downloads the list of versions from upstream. """
		crl = pycurl.Curl()
		b_obj = BytesIO()

		crl.setopt(crl.URL, self.get_source_dir())
		crl.setopt(crl.WRITEDATA, b_obj)

		crl.perform();
		crl.close();

		get_body = b_obj.getvalue();
		get_body_utf8 = get_body.decode('utf8');

		file_pattern = re.compile('href="' + self.get_name() + r'-[0-9][^"]*\.tar\.xz"')
		file_list = file_pattern.findall(get_body_utf8)

		version_pattern = re.compile('^.*' + self.get_name() + r'-([0-9].*)\.tar\.xz.*$')
		for file_name in file_list:
			version_str = version_pattern.sub(r'\1', file_name);
			version = initrdtool.package.version.Version(version_str);
			self.__insert_version(version);

# Create an instance and register on module load.
Glibc().register()

# vim: set ts=4 sw=4 noexpandtab :
