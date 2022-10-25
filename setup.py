from setuptools import find_packages, setup
from typing import List


REQUIREMENTS_FILE = 'requirements.txt'
PROJECT_NAME = "CNN_Classifier_App"
USER_NAME = 'anilans029'
USER_EMAIL = 'anilsai029@gmail.com'
PACKAGE_NAME = "classifier_app"




with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_requirements()->List[str]:
    with open(REQUIREMENTS_FILE, "r") as req:
         requirements =  req.readlines().remove("-e .")
         return requirements



setup(
    name= PACKAGE_NAME,
    version="0.0.1",
    author=USER_NAME,
    author_email="anilsai029@gmail.com",
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
     project_urls={
        "Bug Tracker": f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=get_requirements()
)