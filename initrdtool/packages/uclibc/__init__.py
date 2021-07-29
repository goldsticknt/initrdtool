import initrdtool.package
from initrdtool.package import Package
import initrdtool.package.version
import initrdtool.packages;
from bisect import bisect_left
import pycurl;
from io import BytesIO;
import re;

PACKAGE_NAME = 'uClibc'

class Uclibc(Package):
	def __init__(self):
		self._name = PACKAGE_NAME
		self._url = 'https://www.uclibc.org/'
		self._versions = [];

	def _source_url_to_sig_url(self, url):
		sig_url = url + '.sig'
		return(sig_url);

	def get_source_dir(self):
		source_dir = 'https://www.uclibc.org/downloads/'
		return(source_dir);

	def get_source_urls(self, version):
		source_url = self.get_source_dir() + str(version) + '.tar.xz'
		return([source_url]);

	def get_sig_urls(self, version):
		sig_url = self.get_source_dir() + str(version) + '.tar.xz.sign'
		return([sig_url]);

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

		file_pattern = re.compile('href="' + self.get_name() + r'-[^"]*\.tar\.xz"')
		file_list = file_pattern.findall(get_body_utf8)

		version_pattern = re.compile('^.*' + self.get_name() + r'-(.*)\.tar\.xz.*$')
		for file_name in file_list:
			version_str = version_pattern.sub(r'\1', file_name);
			version = initrdtool.package.version.Version(version_str);
			self._insert_version(version);

# Create an instance and register on module load.
Uclibc().register()

# vim: set ts=4 sw=4 noexpandtab :
