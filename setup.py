from setuptools import setup, find_packages

setup( name="NoseHTML",
	version="0.3.1",
	description="""HTML Output plugin for Nose / Nosetests""",
	packages=['nosehtml'],
	entry_points = {'nose.plugins.0.10': [ 'nosehtml = nosehtml.plugin:NoseHTML' ] }
	)
