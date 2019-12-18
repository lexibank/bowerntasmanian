from setuptools import setup


setup(
    name='cldfbench_bowerntasmanian',
    py_modules=['cldfbench_bowerntasmanian'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'bowerntasmanian=cldfbench_bowerntasmanian:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
