import setuptools

INSTALL_REQUIRES = [
   'loguru'
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bmio",
    version="0.1.9",
    author="coyote963",
    author_email="coyoteandbird@gmail.com",
    description="Boring Man Rcon Scripting Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coyote963/bmio/",
    project_urls={
        "Bug Tracker": "https://github.com/coyote963/bmio/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.6",
)
