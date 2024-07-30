from os import path

from setuptools import setup

REQUIREMENTS = ['pytest', 'six']

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='show-dialog',
    version='1.0.0',
    py_modules=['show_dialog'],
    provides=['show_dialog'],
    description='Show dialog',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Joao Coelho',
    author_email='devs@singular.net',
    url='https://github.com/joaonc/show_dialog',
    keywords='qt, qt6',
    install_requires=REQUIREMENTS,
    license='MIT License',
    python_requires='>=3.10',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
