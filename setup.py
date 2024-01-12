# the presence of which is an indication that the module/package you are about to install has likely been packaged and 
# distributed with Distutils, which is the standard for distributing Python Modules.

# setuptools is a package that helps you build and distribute Python packages

# find_packages() is a function that automatically discovers all the packages in your project and returns them as a list. 
# You can use this function to avoid having to manually specify all the packages in your project.

# setup() is a function that configures your package for distribution. It takes several arguments,  
# including the name of your package, its version, and a list of packages to include




from setuptools import find_packages,setup

setup(
    name='mcqGenerator',
    version='0.0.1',
    author='Ranadip Munda',
    author_email='ranadip01.in@gmail.com',
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()
)