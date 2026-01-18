from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file_obj:
            lines=file_obj.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirement_lst

setup(
    name="NetworkSecurity",
    version='1.0.0',
    author='Radhay Krishna',
    author_email="radhaykrishna699@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
