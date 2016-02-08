from setuptools import setup

setup(
    name='pyfocal',
    version='0.1a1',
    packages=['pyfocal', 'pyfocal.ui', 'pyfocal.ui.qt',
              'pyfocal.ui.qt.uic.source.qdarkstyle', 'pyfocal.ui.widgets',
              'pyfocal.ui.widgets.plots', 'pyfocal.core', 'pyfocal.analysis',
              'pyfocal.interfaces'],
    url='http://pyfocal.readthedocs.org',
    license='',
    author='Nicholas Earl',
    author_email='nmearl@protonmail.com',
    description='An interactive astronomical analysis tool.',
    include_package_data=True,
    install_requires=[
        "qtpy",
        "astropy",
        "numpy",
        "py_expression_eval"
    ],
    entry_points={
        'console_scripts': [
            'pyfocal = pyfocal.app:main'
        ]
    }
)