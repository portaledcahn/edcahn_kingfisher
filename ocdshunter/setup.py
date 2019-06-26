"""
"""
from setuptools import setup

install_requires = []

with open('./requirements.txt') as requirements_txt:
    requirements = requirements_txt.read().strip().splitlines()
    for requirement in requirements:
        if requirement.startswith('#'):
            continue
        elif requirement.startswith('-e '):
            install_requires.append(requirement.split('=')[1])
        else:
            install_requires.append(requirement)

setup(
    name='edcahn',
    version='1.0.0',
    author='EDCA HN',
    author_email='ocdshunter@edca.gob.hn',
    url='https://github.com/portaledcahn/edcahn_kingfisher',
    description='',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
    install_requires=install_requires,
)
