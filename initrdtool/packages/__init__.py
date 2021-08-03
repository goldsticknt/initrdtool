import initrdtool.package
import os
import os.path
import importlib
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

package_definitions={}
package_modules={}
engine = None
Session = None
session = None
Base = declarative_base()

def open_db():
	global engine
	global Session
	global session
	engine = create_engine(initrdtool.initrdtooldb)
	Session = sessionmaker(bind=engine)
	session = Session()

def flush_db():
	global session
	session.commit();

def close_db():
	global Session
	session.close();

def unload():
	""" Unloads all packages. """
	package_definitions = {}
	package_modules = {}

def load():
	""" Loads all packages. """
	package_modules = {}
	package_definitions = {}

	# Load all defined package definitions.
	for dirname in __path__:
		for dirent in os.listdir(dirname):
			if (len(dirent) > 0) and (dirent[0].isalpha()) and os.path.isdir(os.path.join(dirname, dirent)):
				package_fqn = "initrdtool.packages." + dirent
				package_module = importlib.import_module(package_fqn)
				package_modules[dirent] = package_module

	# Populate database if not already done.
	Base.metadata.create_all(engine)

def restore_all():
	for name,obj in package_definitions.items():
		obj.restore()

def preserve_all():
	for name,obj in package_definitions.items():
		obj.preserve()
	flush_db();

def update_versions():
	for name,obj in package_definitions.items():
		obj.update_versions()

# vim: set ts=4 sw=4 noexpandtab :
