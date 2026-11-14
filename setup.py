from setuptools import setup, find_packages

setup(
    name="software_vulnerability_data_quality",
    version="1.0.0",
    description="Reproduction & Implementation Suite for Data Quality Assessment in Software Vulnerability Datasets (ICSE 2023)",
    author="Ravikaran Singh",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy",
        "matplotlib"
    ],
    python_requires=">=3.8",
)
