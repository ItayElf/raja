from setuptools import setup

setup(
    name="raja",
    version="0.1.0",
    packages=["raja", "raja.actions", "raja.changes_finder", "raja.committer", "raja.file_handler", "raja.utils"],
    entry_points={
        'console_script': [
            "raja = raja.__main__:main"
        ]
    }
)
