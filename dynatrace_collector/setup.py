"""Packaging settings."""

import os
from configparser import ConfigParser
from shutil import copyfile

import setuptools
import setuptools.command.install
from setuptools.command.install import install

# The easiest way to convert the markdown to RestructuredText is to use
# pandoc.  There is a Python frontend to that package called pypandoc.
# To use this code you will need to :
#   1. Download and install pandoc  (http://pandoc.org/installing.html)
#   2. pip install pypandoc
# see: https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert_file(source_file='README.md',
                                             format='markdown_github',
                                             to='rst',
                                             extra_args=['-s',
                                                         '--columns=1000'])
except (IOError, ImportError):
    LONG_DESCRIPTION = ''


class PostInstallCommand(install):

    def run(self):
        config = ConfigParser()
        config.read("dynatrace_collector/dtcollector.conf")
        log_dir = config.get('default','log_dir')
        config_dir = '/opt/wavefront/dynatrace/config/'
        pid_dir = '/var/run/'

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        copyfile('dynatrace_collector/config.json', config_dir+'config.json')
        copyfile('dynatrace_collector/dtcollector.conf', config_dir+'dtcollector.conf')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        open(log_dir+'dynatrace.log', 'w+')

        if not os.path.exists(pid_dir):
            os.makedirs(pid_dir)

        install.run(self)


setuptools.setup(
    name='dynatrace_collector',
    version='0.0.2',
    author='Wavefront',
    author_email='mike@wavefront.com',
    description=('Wavefront Dynatrace Collector'),
    license='BSD',
    long_description=LONG_DESCRIPTION,
    keywords='wavefront wavefront_integration collector metrics',
    url='https://github.com/wavefrontHQ/integrations/tree/master/dynatrace_collector',
    install_requires=['wavefront-sdk-python', 'python-daemon>=2.1.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=setuptools.find_packages(include=['dynatrace_collector']),
    include_package_data=True,
    cmdclass={'install': PostInstallCommand},
    scripts=['dynatrace_collector/wf-dynatrace', 'dynatrace_collector/dynatrace-collector']
)
