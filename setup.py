from setuptools import setup

setup(
    name="dabot",
    version="1.0.0",
    description="Discord Bot for RazorDevs' server.",
    py_modules=["dabot"],
    entry_points={
        "console_scripts": ["dabot=dabot:main"],
    },
)
