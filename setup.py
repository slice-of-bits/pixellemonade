from setuptools import setup, find_packages

setup(
    packages=find_packages(where="pixellemonade"),
    package_dir={"": "pixellemonade"},
    include_package_data=True,
)