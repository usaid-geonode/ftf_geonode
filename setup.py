import os
from distutils.core import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="usaid_nepal_geonode",
    version="0.1",
    author="pjdufour",
    author_email="pjdufour.dev@gmail.com",
    description="USAID Nepal GeoNode, based on GeoNode",
    long_description=(read('README.rst')),
    # Full list of classifiers can be found at:
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
    license="BSD",
    keywords="usaid_nepal_geonode geonode django gis",
    url='https://github.com/usaid-nepal-geonode/usaid_nepal_geonode',
    packages=['usaid_nepal_geonode',],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
       'geonode>=2.5.6',
    ],
)
