"""
Setup script for the Wavefront collector tools.
"""

import os
import setuptools
import setuptools.command.install
from shutil import copyfile
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
                                             extra_args=['-s', '--columns=1000'])
except (IOError, ImportError):
    LONG_DESCRIPTION = ''

class PostInstallCommand(install):

  def run(self):
    config_dir = '/opt/wavefront/dynatrace/config/'
    log_dir = '/tmp/wavefront/dynatrace/log/'
    pid_dir = '/tmp/wavefront/dynatrace/pid/'

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    copyfile('config/config.json', config_dir+'config.json')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    open(log_dir+'dynatrace.log', 'w+')

    if not os.path.exists(pid_dir):
        os.makedirs(pid_dir)

    install.run(self)

setuptools.setup(
    name='dynatrace_collector',
    version='0.0.1',
    author='Wavefront',
    author_email='mike@wavefront.com',
    description=('Dynatrace Collector'),
    license='BSD',
    long_description=LONG_DESCRIPTION,
    keywords='wavefront wavefront_integration collector metrics',
    url='https://www.wavefront.com',
    install_requires=['wavefront-sdk-python', 'python-daemon>=2.1.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
    package_data={'wavefront': ['config/*']},
    cmdclass={'install': PostInstallCommand},
    scripts=['wf-dynatrace', 'dynatrace-collector']
)
