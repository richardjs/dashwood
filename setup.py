from setuptools import setup, Extension

setup(
    name='Dashwood',
    version='0.1.0',
    description='Quarto engine',
    url='https://github.com/richardjs/dashwood',
    author='Richard Schneider',
    author_email='richard@schneiderbox.net',

    package_dir={'': 'src',},
    packages=['dashwood',],

    ext_modules=[
        Extension('dashwood.c', sources=['src/dashwood/c/c.c',],),
    ],
)
