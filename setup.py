from setuptools import setup

setup(
    name="raja",
    version="1.0.0",
    packages=["raja", "raja.actions", "raja.changes_finder", "raja.committer", "raja.file_handler", "raja.utils",
              "raja.changes_finder.changes", "raja.committer.orm"],
    entry_points={
        'console_script': [
            "raja = raja.__main__:main"
        ]
    }
)
