import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tactile_map",
    version="0.0.1",
    author="Mateusz Konieczny",
    author_email="matkoniecz@gmail.com",
    description="Generates designs of tactile maps recognisable by touch. For small scale production using laser cutters. For people who are blind or with a poor eyesight.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkoniecz/tactile_map",
    packages=setuptools.find_packages(),
    install_requires = [
        'jsbeautifier>=1.13.5, <2.0',
        'shapely>=1..7.0, <2.0',
        'osm-bot-abstraction-layer>=0.0.10',
        'tactile-patterns>=0.0.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

