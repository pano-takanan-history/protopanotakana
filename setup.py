from setuptools import setup
import json

with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)

setup(
    name='protopanotakana',
    py_modules=['protopanotakana'],
    include_package_data=True,
    url=metadata.get("url", ""),
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'template=protopanotakana:Dataset',
        ]
    },
    install_requires=[
        "pylexibank>=3.5.0",
        "cldfbench==1.14.0",
        "pycldf==1.41.0",
        "csvw==3.5.1",
        "pyconcepticon==3.1.0",
    ],
    extras_require={
        'test': ['pytest-cldf']
        }
)
