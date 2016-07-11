from setuptools import setup, find_packages

desc = ''
with open('README.rst') as f:
    desc = f.read()

setup(
    name='ansible-flow',
    version='0.2.0',
    description=('Workflow tool to speed up interactions with Ansible'),
    long_description=desc,
    url='https://github.com/jmvrbanac/ansible-flow',
    author='John Vrbanac',
    author_email='john.vrbanac@linux.com',
    license='Apache v2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='ansible management workflow',
    packages=find_packages(exclude=['contrib', 'docs', 'spec*']),
    install_requires=['ansible>=2.0', 'pyyaml', 'virtualenv', 'capturer'],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': ['ansible-flow = ansibleflow.app:main'],
    },
)
