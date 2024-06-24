from setuptools import setup, find_packages

setup(
    name="oven-cli",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'jinja2',
        'markdown',
        'pytz',
        'polib'
    ],
    entry_points={
        'console_scripts': [
            'oven=oven.__main__:main',
        ],
    },
    author="Kamil Tokarski",
    author_email="kamil@tokarski.xyz",
    description="A static site generator with markdown support",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ktxyz/oven",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

