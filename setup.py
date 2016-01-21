from setuptools import setup, find_packages

setup(
    name='miniboa',
    version='0.0.1',
    packages=find_packages(exclude=['docs', 'tests', 'examples']),
    description='A bare-bones Telnet server',
    author='Jim Storch',
    author_email='jimstorch@gmail.com',
    maintainer='Jared Miller',
    maintainer_email='jtmiller@gmail.com',
    url='https://github.com/shmup/miniboa',
    download_url='https://github.com/shmup/miniboa/archive/v0.0.1.tar.gz',
    keywords=['mud', 'tcp', 'telnet'],
    license='Apache 2'
)
