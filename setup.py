from setuptools import find_packages, setup


setup(
    name='jsonfield',
    version='3.1.0',
    license='MIT',
    include_package_data=True,
    author='Brad Jasper',
    author_email='contact@bradjasper.com',
    maintainer='Ryan P Kilby',
    maintainer_email='kilbyr@gmail.com',
    url='https://github.com/rpkilby/jsonfield/',
    description='A reusable Django field that allows you to store validated JSON in your model.',
    long_description=open("README.rst").read(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['Django >= 2.2'],
    python_requires='>=3.6',
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
    ],
)
