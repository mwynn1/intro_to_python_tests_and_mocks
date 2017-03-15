## Getting started with a virtual environment

The first time you run this tool, you need to setup your environment.
Use these commands:

        virtualenv venv

This will create a directory named 'venv' that the program will use for
installing third-party packages. Now you need to let python know where to look
for required packages. Run this command every time you open a new terminal window.

        source venv/bin/activate
        pip install -r requirements.txt

When finished run:

        deactivate

## Getting started without a virtual environment

The following packages need to be installed (and can all be installed via pip):

    mock (recommended 2.0.0)
    nose (recommended 1.3.7)
    requests (recommended 2.2.1)
    requests-mock  (recommended 1.3.0)

## To run

from within intro_to_python_tests_and_mocks:

    cd chemical_module
    python chemical_property_lookup.py

## To test

from within intro_to_python_tests_and_mocks

    nosetests