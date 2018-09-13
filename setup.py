from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='scorer',
    version=0.1,
    description='A simple script to show desktop notifications for cricket scores',
    long_description=readme(),
    url='https://github.com/neo1691/scorer.py',
    author='Anubhav Yadav',
    author_email='anubhav1691@gmail.com',
    license='GPLv2',
    packages=['scorer'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'notify22'
    ],
    entry_points={
        'console_scripts': [
            'scorer = scorer.app:main'
        ]
    },
    zip_safe=False
)
