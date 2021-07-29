import initrdtool.package
from initrdtool.package import Package
import initrdtool.package.version
import initrdtool.packages;
from bisect import bisect_left
import pycurl;
from io import BytesIO;
import re;

PACKAGE_NAME = 'linux'

class Linux(Package):
	def __init__(self):
		self._name = PACKAGE_NAME
		self._url = 'https://www.gnu.org/software/' + PACKAGE_NAME + '/'
		self._versions = [];

	def __insert_version(self, newversion):
		""" Inserts a new version into the list of versions """
		iter = bisect_left(self._versions, newversion)
		if (iter >= len(self._versions)) or (self._versions[iter] != newversion):
			self._versions.insert(iter, newversion)

	def _source_url_to_sig_url(self, url):
		sig_url = re.sub(r'(\.tar)(\.xz|\.bz2)$', r'\1\.sig', url);
		return(sig_url);

	def get_source_dir(self):
		source_dir = 'https://mirrors.edge.kernel.org/pub/linux/kernel/'
		return(source_dir);

	def get_source_urls(self, version):
		source_url = self.get_source_dir() + "v" + str(version.get_major()) + ".x/linux-" + str(version) + '.tar.xz'
		return([source_url]);

	def get_sig_urls(self, version):
		sig_urls = []
		for source_url in self.get_source_urls(version):
			sig_urls.append(self._source_url_to_sig_url(source_url))
		return(sig_urls)

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

		dir_pattern = re.compile(r'href="(v[0-9]\.x\/)"')
		dir_list = dir_pattern.findall(get_body_utf8)

		for dir_name in dir_list:
			sub_source_dir = self.get_source_dir() + dir_pattern.sub(r'\1', dir_name);

			crl = pycurl.Curl()
			b_obj = BytesIO()

			crl.setopt(crl.URL, sub_source_dir)
			crl.setopt(crl.WRITEDATA, b_obj)

			crl.perform();
			crl.close();

			get_body = b_obj.getvalue();
			get_body_utf8 = get_body.decode('utf8');

			file_pattern = re.compile('href="' + self.get_name() + r'-[^"]+\.tar\.xz"')
			file_list = file_pattern.findall(get_body_utf8)

			version_pattern = re.compile('^.*' + self.get_name() + r'-(.+)\.tar\.xz.*$')
			for file_name in file_list:
				version_str = version_pattern.sub(r'\1', file_name);
				version = initrdtool.package.version.Version(version_str);
				self.__insert_version(version);

# Create an instance and register on module load.
Linux().register()

# vim: set ts=4 sw=4 noexpandtab :
