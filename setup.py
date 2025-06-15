from setuptools import setup, find_packages

setup(
    name="budge-it",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8,<3.9",
    install_requires=[
        "Flask==2.0.3",
        "Flask-SQLAlchemy==2.5.1",
        "SQLAlchemy==1.4.53",
        "gunicorn==20.1.0",
        "psycopg2-binary==2.9.5",
        "python-dotenv==0.19.2",
        "Flask-Login==0.5.0",
        "Werkzeug==2.0.3",
        "click==7.1.2",
        "blinker==1.4"
    ],
) 