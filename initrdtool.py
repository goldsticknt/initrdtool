#!/usr/bin/python3

import initrdtool

print("Open database connection.")
initrdtool.packages.open_db()

print("Loading package definitions...")
initrdtool.packages.load()

print("Loading package information.")
initrdtool.packages.restore_all()

print("Updating package version lists...")
initrdtool.packages.update_versions()

print("Package source lists:")
package_list = initrdtool.packages.package_definitions.keys()
for package in package_list:
	package_def = initrdtool.packages.package_definitions[package]
	package_ver = package_def.get_latest_version()
	package_src_urls = list(package_def.get_src_urls(package_ver).values())
	package_sig_urls = list(package_def.get_sig_urls(package_ver).values())
	print("==========")
	print("Package: %s" % package_def.get_name())
	print("Version: %s" % str(package_ver))
	for package_src_url in package_src_urls:
		print("Source: %s" % package_src_url)
	for package_sig_url in package_sig_urls:
		print("Signature: %s" % package_sig_url)
	print("Downloading...")
	package_def.download(package_ver)

print("Calculating install dependencies...")
print("TODO: Implement")

print("Performing installations...")
print("TODO: Implement")

print("Saving package information.")
initrdtool.packages.preserve_all()

print("Close database connection.")
initrdtool.packages.close_db()

# vim: set ts=4 sw=4 noexpandtab :

