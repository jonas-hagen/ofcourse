from setuptools import setup, find_packages

setup(
    name="ofcourse",
    version="1.0.0",
    url="",
    author="Jonas Hagen",
    author_email="jonas.hagen3@gmail.com",
    description="Tools to manage a course.",
    packages=find_packages(),
    install_requires=["wheel", "pyyaml", "phonenumbers"],
)
