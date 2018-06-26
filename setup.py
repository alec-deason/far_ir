from setuptools import setup, find_packages

setup(
    name='FarIR',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    extras_require={
        'testing': [
            'pytest',
            'pytest-mock',
        ],
    },
)
