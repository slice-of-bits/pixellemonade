from setuptools import setup, find_packages

setup(
    name="pixellemonade",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-hashid-field>=3.3.7',
        'django-imagekit>=5.0.0',
        'Pillow>=9.4.0',
        'django-ninja>=0.22.2',
        'exif>=1.6.0',
        'IPTCInfo3>=2.1.4',
        'user-agents>=2.2.0',
        'django-treebeard>=4.7',
    ]
)
