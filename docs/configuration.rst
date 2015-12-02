Configuration
=============

ansible-flow looks for a ``project.yml`` file within the executing directory.

Each ``project.yml`` file contains three different sections:

* requirements
* environments
* targets

Requirements
------------

The requirements section is where you define any python requirements (in a list)
that you will need to execute your ansible playbooks. For simple use-cases you
should only need to define ``ansible`` or ``ansible==1.9.4``.

Example:

.. code-block:: yaml

    requirements:
        - ansible==1.9.4

Environments
------------

The environments section is where you define specific for custom variable files,
vault keys, and ansible configuration files on a per environment basis.

If you have a number of common values that you'd like to share across environments,
then you can specify a ``default`` environment. If a ``default`` environment is
specified then all other environments will just layer their settings on-top of
the ``default``.

Per Environment Options
^^^^^^^^^^^^^^^^^^^^^^^

* ``vault-key``: Path to your vault password file
* ``custom-var-files``: A list of YAML files to load when executing your playbooks
* ``directory``: A base directory for your ``custom-var-files``
* ``ansible-config``: Path to a ansible configuration file

Example
^^^^^^^

A environments section containing two different environments each with a file
encrypted with two different vault keys.

**Directory Structure**

.. code-block:: text

    envs/dev/
        - general.yml
        - auth.vault.yml
    envs/test/
        - general.yml
        - auth.vault.yml
    dev-vault-key
    test-vault-key
    project.yml

**Environments section of** ``project.yml``

.. code-block:: yaml

    environments:
        default:
            custom-var-files:
                - general.yml
                - auth.vault.yml
        dev:
            directory: ./envs/dev
            vault-key: ./dev-vault-key
        test:
            directory: ./envs/test
            vault-key: ./test-vault-key

Targets
-------
The targets section allows for you to define a set of playbooks to be executed.

Per Target Options
^^^^^^^^^^^^^^^^^^

* ``playbooks``: A list of playbooks to be executed in sequential order.
* ``inventory``: The inventory script or ini file you wish to use.
* ``tags``: Tags you wish to pass to ansible
* ``ansible-options``: Custom cli arguments for ansible-playbook

Example
^^^^^^^

.. code-block:: yaml

    targets:
        ping:
            playbooks:
                - ping.yml
            inventory: ./inventory.ini
        bootstrap:
            playbooks:
                - bootstrap.yml
                - 2fa.yml
            inventory: ./inventory.ini

Example Configuration
---------------------

.. code-block:: yaml

    ---
    requirements:
        - ansible==1.9.4

    environments:
        default:
            custom-var-files:
                - general.yml
                - auth.vault.yml
        dev:
            directory: ./envs/dev
            vault-key: ./dev-vault-key
        test:
            directory: ./envs/test
            vault-key: ./test-vault-key

    targets:
        ping:
            playbooks:
                - ping.yml
            inventory: ./inventory.ini
        bootstrap:
            playbooks:
                - bootstrap.yml
                - 2fa.yml
            inventory: ./inventory.ini
