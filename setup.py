from setuptools import setup, find_packages

setup(
    name='gplume',
    version='0.0.7',
    description='The Gaussian Plume Model for atmospheric dispersion and inverse modeling of contaminants with support for multiple sources and receptors.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VaibhavVasdev/Gaussian-Plume_Model',  
    author='Vaibhav Vasdev',
    author_email='vaibhavvasdev63@gmail.com',
    license='MIT',
    keywords='GaussianPlumeModel', 
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
        'scipy',
        'python-dateutil',
        'matplotlib'
    ],
)
