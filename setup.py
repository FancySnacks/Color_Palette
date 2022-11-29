from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE.md") as f:
    license = f.read()

setup(
    name="Color_Palette_ARaveMistake",
    version="1.0.0",
    description="A tool for artists that allows to create and save color palettes using text and images.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/A-Rave-Mistake/Color_Palette",
    author="A-Rave-Mistake",
    author_email="adrian.urbaniak1336@gmail.com",
    license=license,
    classifiers=[
                    "Topic :: Software Development",
                    "Programming Language :: Python :: 3.10",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                    "Operating System :: Microsoft :: Windows :: Windows 10",
],
    packages=find_packages(exclude=('tests', 'dist', '.git')),
    install_requires=[
                        "extcolors>=1.0.0,<2.0",
                        "matplotlib>=3.6.2,<4.0",
                        "numpy>=1.23.5,<2.0",
                        "opencv_python>=4.6.0.66,<5.0",
                        "Pillow>=9.3.0,<10.0",
                        "PyAutoGUI>=0.9.53,<1.0",
                        "pyperclip>=1.8.2,<2.0"
],
    include_package_data=True,
)