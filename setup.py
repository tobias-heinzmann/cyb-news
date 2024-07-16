import os
from setuptools import find_packages
from setuptools import setup
from packaging.version import Version


#requirements = []
#
# if os.path.isfile('requirements.txt'):
#     with open('requirements.txt') as f:
#         content = f.readlines()
#     requirements.extend([x.strip() for x in content if 'git+' not in x])

# if os.path.isfile('requirements_dev.txt'):
#     with open('requirements_dev.txt') as f:
#         content = f.readlines()
#     requirements.extend([x.strip() for x in content if 'git+' not in x])


version_file_name = '.version'
new_version = None
if os.path.isfile(version_file_name) and new_version is None:
    with open(version_file_name, 'r+') as f:
        old = Version(f.read().strip())
        #print(f'old version of cybnews: {old}')
        
        # new version: increment micro
        new_version = str(Version(f'{old.major}.{old.minor}.{old.micro + 1 }'))
        #print(f'new version of cybnews: {new_version}')
        f.seek(0)
        f.write(new_version)
        f.truncate()


setup(
    name='cybnews',
    version=new_version,
    description="Check Your Bias News",
    packages=find_packages(),
    # install_requires=requirements,
    # include_package_data: to install data from MANIFEST.in
    # include_package_data=True,
    # scripts=['scripts/packagename-run'],
    zip_safe=False
)
