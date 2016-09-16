from setuptools import setup

setup(
    name='django-date-range-filter',
    version='0.0.1',
    description='Simplest possible date range filter for Django admin',
    packages=['date_range_filter'],
    install_requires=[
        'Django',
        'pytz',
        'django-suit',
    ],
    setup_requires=[
        'nose>=1.0',
    ],
    url='https://github.com/f213/django-suit-daterange-filter',
    author='Fedor Borshev',
    author_email='f@f213.in',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Environment :: Web Environment',
        'Operating System :: OS Independent'
    ],
    include_package_data=True,
)
