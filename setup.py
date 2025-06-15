from setuptools import setup, find_packages

setup(
    name="budge-it",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.12,<3.13",
    install_requires=[
        "Flask==2.2.5",
        "Flask-SQLAlchemy==3.0.2",
        "SQLAlchemy==1.4.53",
        "gunicorn==20.1.4",
        "psycopg2-binary==2.9.5",
        "python-dotenv==1.0.0",
        "Flask-Login==0.6.2",
        "Werkzeug==2.2.3",
        "click==8.1.3",
        "blinker==1.6.2"
    ],
) 