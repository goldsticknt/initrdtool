import initrdtool.package
from initrdtool.package import Package
import initrdtool.package.version
from initrdtool.package.version import Version
import initrdtool.package.source
from initrdtool.package.source import Web
import initrdtool.packages
import pycurl
from io import BytesIO
import re

PACKAGE_NAME = 'glibc'

class Glibc(Package):
	def __init__(self, *args, **kwargs):
		package_args = kwargs
		package_args["name"] = PACKAGE_NAME
		package_args["url"] = Web('https://www.gnu.org/software/libc/')
		#package_args["src_url_suffix_pattern"] = None
		package_args["sig_url_suffix_pattern"] = '.sig'
		package_args["src_url_pattern"] = 'href="' + PACKAGE_NAME + r'-[0-9][^"]*\.tar\.xz"'
		package_args["src_version_sub_pattern"] = '^.*' + PACKAGE_NAME + r'-([0-9].*)\.tar\.xz.*$'
		super().__init__(*args, **package_args)

	def get_src_dir(self):
		src_dir = 'https://ftp.gnu.org/gnu/' + self.get_name() + '/'
		return(src_dir)

	def get_src_files(self, version):
		src_name = self.get_name() + '-' + str(version) + '.tar.xz'
		return([src_name])

	def get_src_urls(self, version):
		src_urls = {}
		src_files = self.get_src_files(version)
		for src_file in src_files:
			src_urls[src_file] = Web(str(self.get_src_dir() + src_file))
		return(src_urls)

	def update_versions(self):
		""" Downloads the list of versions from upstream. """
		crl = pycurl.Curl()
		b_obj = BytesIO()

		crl.setopt(crl.URL, self.get_src_dir())
		crl.setopt(crl.WRITEDATA, b_obj)

		crl.perform()
		crl.close()

		get_body = b_obj.getvalue()
		get_body_utf8 = get_body.decode('utf8')

		if (self.src_url_pattern == None):
			return

		file_pattern = re.compile(self.src_url_pattern)
		file_list = file_pattern.findall(get_body_utf8)

		if (self.src_version_sub_pattern == None):
			return

		version_pattern = re.compile(self.src_version_sub_pattern)
		for file_name in file_list:
			version_str = version_pattern.sub(r'\1', file_name)
			version = Version(package_name=self.get_name(),version_string=version_str)
			super().insert_version(version)

# Create an instance and register on module load.
Glibc().register()

# vim: set ts=4 sw=4 noexpandtab :
