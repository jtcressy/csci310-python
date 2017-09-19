from setuptools import setup
setup(
        name='hangman',
        packages=['hangman'],
        include_package_data=True,
        install_requires=[
            'xtermcolor',
            'urwid',
            'fysom'
        ],
)
