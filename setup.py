from setuptools import find_packages, setup
from  typing import List


e_dot = '-e .'

def get_req(filename: str)-> List[str]:
    '''
    This function finds the modules which need to be imported.
    '''

    requirements = []
    with open(filename) as fileobj:
        requirements = fileobj.readlines()
        requirements = [req.replace('\n','') for req in requirements]

        if e_dot in requirements:
            requirements.remove('-e .')

    return requirements


setup(
name= "Mantainance Prediciton"
version= "0.0.1"
author= "Pranav"
author_email= "pranavp1712@gmail.com"
packages= find_packages()
install_requires = get_req('requirements.txt')
)