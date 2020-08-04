from setuptools import setup, find_packages

setup(
    name='pmExt',
    version='1.0.0',
    url='https://github.com/yooha1003/pmExt',
    author='Uksu, Choi',
    author_email='qtwing@naver.com',
    description='Pubmed Article Search and Download python script',
    packages=find_packages(),
    install_requires=['selenium', 'argparse', 'tqdm', 'requests', 'urllib3', 'pillow', 'pytextrank', 'reportlab'],
)
