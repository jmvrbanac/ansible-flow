Using ansible-flow
==================

Project virtual environment for ansible-flow
-----------------------------------------------

``ansible-flow`` will execute all of its actions under a virtual environment.
This allows for you to pin specific versions ansible and any other dependencies.
``ansible-flow`` can maintain the virtual environment for you using the venv
sub-command.

.. note::

    The packages installed into the virtual environment are defined in the
    requirements section of your ``project.yml``

Working with ansible-flow's venv sub-command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Create a fresh virtual environment
    ansible-flow venv create

    # Recreates the virtual environment (commonly used when you change dependencies)
    ansible-flow venv recreate

    # Completely deletes the virtual environment
    ansible-flow venv delete

Running ansible-flow
--------------------

Assuming you've written your ``project.yml`` configuration, you can execute a
target against a given environment using the following command:

.. code-block:: bash

    ansible-flow run ping --env dev
