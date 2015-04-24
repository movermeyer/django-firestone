from setuptools import setup
from firestone import __version__

setup(
    name='django-firestone',
    packages=('firestone', ),
    version=__version__,
    description='REST API Framework',
    author='C. Paschalides',
    author_email='already.late@gmail.com',
    license='WTFPL',
    url='http://github.com/stargazer/django-firestone',
    keywords=('firestone', 'django-firestone', 'rest', 'restful', 'api', 'crud'),
    install_requires=(
        'Django',
        'django-deserializer',
    ),
    tests_require=(),       
    test_suite='runtests.run',
    zip_safe=False,
    classifiers=(
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Development Status :: 4 - Beta',
    ),
)                                                    

