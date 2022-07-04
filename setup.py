from setuptools import setup, find_packages

setup(
    name='nearly-solid',
    version='0.0.5',
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'Jinja2==3.1.2',
        'SQLAlchemy==1.4.36',
        'pydantic==1.9.0',
        'PyJWT==2.4.0',
        'inject==4.3.1',
        'flask==2.1.2',
    ],
    packages=find_packages(),
)
