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
		self._src_suffix_pattern = r'(\.tar)(\.xz|\.bz2)$';
		self._sig_suffix_patterm = r'\1\.sig';

	def __insert_version(self, newversion):
		""" Inserts a new version into the list of versions """
		iter = bisect_left(self._versions, newversion)
		if (iter >= len(self._versions)) or (self._versions[iter] != newversion):
			self._versions.insert(iter, newversion)

	def get_src_dir(self):
		src_dir = 'https://mirrors.edge.kernel.org/pub/linux/kernel/'
		return(src_dir);

	def get_src_urls(self, version):
		src_url = self.get_src_dir() + "v" + str(version.get_major()) + ".x/linux-" + str(version) + '.tar.xz'
		return([src_url]);

	def get_sig_urls(self, version):
		sig_urls = []
		for src_url in self.get_src_urls(version):
			sig_urls.append(self.src_url_to_sig_url(src_url))
		return(sig_urls)

	def update_versions(self):
		""" Downloads the list of versions from upstream. """
		crl = pycurl.Curl()
		b_obj = BytesIO()

		crl.setopt(crl.URL, self.get_src_dir())
		crl.setopt(crl.WRITEDATA, b_obj)

		crl.perform();
		crl.close();

		get_body = b_obj.getvalue();
		get_body_utf8 = get_body.decode('utf8');

		dir_pattern = re.compile(r'href="(v[0-9]\.x\/)"')
		dir_list = dir_pattern.findall(get_body_utf8)

		for dir_name in dir_list:
			sub_src_dir = self.get_src_dir() + dir_pattern.sub(r'\1', dir_name);

			crl = pycurl.Curl()
			b_obj = BytesIO()

			crl.setopt(crl.URL, sub_src_dir)
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
