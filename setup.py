from setuptools import setup


setup(
    name='jsonfield2',
    version='4.0.0',
    packages=['jsonfield'],
    license='MIT',
    include_package_data=True,
    author='Ryan P Kilby',
    author_email='rpkilby@ncsu.edu',
    url='https://github.com/rpkilby/jsonfield2/',
    description='A reusable Django field that allows you to store validated JSON in your model.',
    long_description=open("README.rst").read(),
    install_requires=['Django >= 2.2'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
    ],
)
