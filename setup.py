from setuptools import setup, find_packages

setup(
    name="ofcourse",
    version="1.2.0",
    url="",
    author="Jonas Hagen",
    author_email="jonas.hagen3@gmail.com",
    description="Tools to manage a course.",
    packages=["ofcourse"],
    entry_points = {
        'console_scripts': ['ofc=ofcourse.ofc_cli:cli'],
    },
    install_requires=[
        "wheel",
        "ruamel.yaml",
        "phonenumbers",
        "docopt",
        "tabulate",
        "click",
        "jinja2",
    ],
)
