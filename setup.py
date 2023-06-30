import setuptools

setuptools.setup(
    name='fridgeGuardian',
    version='0.0.1rc0',
    readme="README.md",
    packages=['fridgeGuardian'],
    install_requires=['requests==2.30.0',
                      'pytest==7.3.1',
                      'mock==5.0.2',
                      'PyYAML~=6.0',
                      'rich~=13.3.5'],
    url='https://github.com/iTom34/fridge-guardian',
    license='',
    author='iTom',
    author_email='',
    description='Monitor weather, and send a notification if the temperature is too low for your fridge',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires="~=3.8",
    entry_points={
        'console_scripts': [
            'fridgeGuardian = fridgeGuardian.user_interface:entry_point'
        ]
    }
)
