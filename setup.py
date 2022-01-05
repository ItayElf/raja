from setuptools import setup

setup(
    name="raja",
    version="0.1.0",
    packages=["raja"],
    entry_points={
        'console_script': [
            "raja = raja.__main__:main"
        ]
    }
)
