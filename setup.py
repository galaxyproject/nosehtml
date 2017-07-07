from setuptools import setup

setup(
    name="NoseHTML",
    version="0.4.3",
    description="""HTML Output plugin for Nose / Nosetests""",
    url='https://bitbucket.org/james_taylor/nosehtml/',
    author='James Taylor, Nate Coraor, Dave Bouvier',
    license='MIT',
    install_requires=['nose'],
    packages=['nosehtml'],
    entry_points={'nose.plugins.0.10': [ 'nosehtml = nosehtml.plugin:NoseHTML' ] }
)
