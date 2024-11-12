from setuptools import setup, find_packages

setup(
	name='reactbuilder',
	version='0.1.1',
	package_dir={'': 'src'},
	packages=find_packages(where='src'),
	install_requires=[
		# List your package dependencies here
	],
	entry_points={
		'console_scripts': [
			'reactbuild=reactbuilder.cli:main',
		],
	},
	author='Tom Bertalan',
	author_email='reactbuilder@tombertalan.com',
	description='Some scripts to make React setup and building OUTSIDE OF YOUR LOCAL WORKSPACE easier.',
	url='https://github.com/tsbertalan/reactbuilder',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
)