from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requires = f.read().strip().split('\n')

with open('dependency_links.txt') as f:
    links = f.read().strip().split('\n')

setup(
    name='projectile',
    url='https://github.com/Vayel/projectile',
    author='Vincent Lefoulon',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    dependency_links=links,
)
