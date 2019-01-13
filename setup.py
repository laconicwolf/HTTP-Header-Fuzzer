from setuptools import setup, find_packages

setup(
    name='HTTP Header Fuzzer',
    version='0.0.2',
    description='Multi-threaded website scanner that fuzzes HTTP headers.',
    url='https://github.com/laconicwolf/HTTP-Header-Fuzzer/',
    author='Jake Miller (@LaconicWolf)',
    author_contact='https://laconicwolf.com/contact-us/',

    packages=find_packages(),

    install_requires=['requests', 'urllib3', 'colorama'],

    project_urls={
        'Bug Reports': 'https://github.com/laconicwolf/HTTP-Header-Fuzzer/issues',
        'Source': 'https://github.com/laconicwolf/HTTP-Header-Fuzzer/',
        'Author Homepage': 'https://laconicwolf.com'
    },
)
