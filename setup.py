import pathlib
from setuptools import setup



HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="Color_Palette_ARaveMistake",
    version="1.0.0",
    description="A tool for artists that allows to create and save color palettes using text and images.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/A-Rave-Mistake/Color_Palette",
    author="A-Rave-Mistake",
    author_email="adrian.urbaniak1336@gmail.com",
    license="GNU GPLv3",
    classifiers=[
                "Topic :: Software Development",
                "Programming Language :: Python :: 3.10",
                "License :: OSI Approved :: GNU GPLv3 License",
                "Operating System :: Windows 10",
],
    packages=['src'],
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