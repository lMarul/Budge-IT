from setuptools import setup, find_packages

setup(
    name="budge-it",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8,<3.9",
    install_requires=[
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.0.5",
        "SQLAlchemy==1.4.53",
        "gunicorn==21.2.0",
        "psycopg2-binary==2.9.7",
        "python-dotenv==1.0.0",
        "Flask-Login==0.6.3",
        "Werkzeug==2.3.7"
    ],
) 