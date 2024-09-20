# pylint: disable=C0114

from io import open

from setuptools import setup

CURRENT_VERSION = "0.4.5"


def read(filename):  # pylint: disable=C0116
    with open(filename, encoding="utf-8") as file:
        return file.read()


setup(
    name="Loglan-Core",
    packages=["loglan_core", "loglan_core.addons"],
    package_data={
        "loglan_core": ["*"],
    },
    include_package_data=True,
    version=CURRENT_VERSION,
    license="MIT",
    description="Loglan Dictionary Database Model for SQLAlchemy",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="torrua",
    author_email="torrua@gmail.com",
    url="https://github.com/torrua/loglan_core",
    download_url=f"https://github.com/torrua/loglan_core/archive/{CURRENT_VERSION}.tar.gz",
    keywords=["Loglan", "Dictionary", "Database", "Model", "LOD"],
    install_requires=[
        "sqlalchemy>=2.0.21",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Database",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
)
