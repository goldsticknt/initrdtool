import initrdtool.package
import os
import os.path
import importlib

package_definitions={}
package_modules={}

def unload():
	""" Unloads all packages. """
	package_definitions = {}
	package_modules = {}

def load():
	""" Loads all packages. """
	package_modules = {}
	package_definitions = {}

	package_name_list = []
	for dirname in __path__:
		for dirent in os.listdir(dirname):
			if (len(dirent) > 0) and (dirent[0].isalpha()) and os.path.isdir(os.path.join(dirname, dirent)):
				package_fqn = "initrdtool.packages." + dirent
				package_module = importlib.import_module(package_fqn)
				package_modules[dirent] = package_module

def update_versions():
	for name,obj in package_definitions.items():
		obj.update_versions()

# vim: set ts=4 sw=4 noexpandtab :
