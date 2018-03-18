from setuptools import setup


def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements


setup(
    name='bvh-converter',
    version='1.0.1',
    packages=['bvh_converter'],
    url='',
    license='',
    author='tekulvw',
    author_email='',
    description='Converts BVH files to CSV',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities"
    ],
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'bvh-converter=bvh_converter.__main__:main',
        ]
    }
)
