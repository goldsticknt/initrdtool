#!/usr/bin/python3

import initrdtool;

print("Loading package definitions...")
initrdtool.packages.load()

print("Updating package version lists...")
initrdtool.packages.update_versions()

print("Package source lists:")
package_list = initrdtool.packages.package_definitions.keys()
for package in package_list:
	package_def = initrdtool.packages.package_definitions[package]
	package_ver = package_def.get_latest_version()
	package_source_urls = package_def.get_source_urls(package_ver)
	print("==========")
	print("Package: %s" % package_def.get_name())
	print("Version: %s" % str(package_ver))
	for package_source_url in package_source_urls:
		print("Source: %s" % package_source_url)
	print("Downloading...")
	package_def.download(package_ver);

# vim: set ts=4 sw=4 noexpandtab :

