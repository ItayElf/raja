from setuptools import setup
import os

setup(
    name="raja",
    version="1.0.0",
    packages=["raja", "raja.actions", "raja.changes_finder", "raja.committer", "raja.file_handler", "raja.utils",
              "raja.changes_finder.changes", "raja.committer.orm"],
    entry_points={
        'console_script': [
            "raja = raja.__main__:main"
        ]
    },
    package_data={"raja": [os.path.join("changes_finder", "bin", "*.exe")]},
    include_package_data=True
)
