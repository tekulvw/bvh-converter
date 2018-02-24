from setuptools import setup


def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name='bvh-converter',
    version='1.0',
    packages=['bvh_converter'],
    url='',
    license='',
    author='tekulvw',
    author_email='',
    description='Converts BVH files to CSV',
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'bvh-converter=bvh_converter.__main__:main',
        ]
    }
)
