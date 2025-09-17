from setuptools import setup, find_packages

# find_packages will find all the packages with __init__.py
print(find_packages())

setup(
    name="taxipred",
    version="0.0.1",
    description="this package contains taxipred app",
    author="Elvira",
    author_email="elvira@mail.se",
    install_requires=["streamlit", "pandas", "fastapi", "uvicorn"],
    package_dir={"": "src"},
    package_data={"taxipred": ["data/*.csv"]},
    packages=find_packages(),
)