from setuptools import setup, find_packages

setup(
    name="budget-tracker",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8,<3.12",
    install_requires=[
        "Flask==2.3.3",
        "SQLAlchemy==1.4.53",
        "Flask-SQLAlchemy==3.0.5",
        "psycopg2-binary==2.9.9",
        "python-dotenv==1.0.0",
        "gunicorn==21.2.0",
    ],
) 