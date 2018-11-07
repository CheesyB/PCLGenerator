from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pcgen',
      version='0.1',
      description='generate point clouds from mesh files',
      long_description=readme(),
      classifiers=[
        'Development Status :: 0 - Alpha',
        'License :: ?? :: ?? ',
        'Programming Language :: Python :: 3.7',
        'Topic :: point clouds  :: deep learning :: pointnet',
      ],
      keywords='point cloud',
      url='https://gitlab.lrz.de/ga67caf/PCLGenerator.git',
      author='Tim Breu',
      author_email='tim.breu@mailbox.org',
      license='??')
#      packages=['funniest'],
#      install_requires=[
#          'markdown',
#      ],
#      test_suite='nose.collector',
#      tests_require=['nose', 'nose-cover3'],
#      entry_points={
#          'console_scripts': ['funniest-joke=funniest.command_line:main'],
#      },
#      include_package_data=True,
#      zip_safe=False)
#
