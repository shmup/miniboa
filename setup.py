from setuptools import setup, find_packages

setup(
    name='miniboa',
    version='1.0.0',
    packages=find_packages(exclude=['docs', 'tests', 'examples']),
    description='A bare-bones Telnet server',
    author='Jim Storch',
    author_email='jimstorch@gmail.com',
    maintainer='Jared Miller',
    maintainer_email='jtmiller@gmail.com',
    url='https://github.com/shmup/miniboa',
    download_url='https://github.com/shmup/miniboa/archive/v1.0.0.tar.gz',
    keywords=['mud', 'tcp', 'telnet'],
    license='Apache 2'
)
