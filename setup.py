from setuptools import setup, find_packages

setup(
    name="utl-framework",
    version="0.1.0",
    description="UTL: Temporal risk detection via EWMA hazard for conversational AI",
    author="Branimir Sabljić",
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt") if line.strip()],
    python_requires=">=3.9",
)
