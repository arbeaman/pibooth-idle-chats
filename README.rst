=====================
pibooth-idle-chats
=====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-idle-chats`` is a plugin for the `pibooth <https://github.com/pibooth/pibooth>`_
application.

It plays wave files (designed to be speech, but can be anything) when the system is idle.
This can draw attention to the photobooth when it is not in use.

Chats, and time between chats, can be customized (see below).

Install
-------

::

    $ pip3 install pibooth-idle-chats

Configuration
-------------

Here are the new configuration options available in the `pibooth`_ configuration.
**The keys and their default values are automatically added to your configuration
after first** `pibooth`_ **restart.**

.. code-block:: ini

    [IDLECHATS]
    # Path to the chat folder
    # Required by 'pibooth-idle-chats' plugin
    chat_path = ~/.config/pibooth/chats

    # Time between idle chats
    # Required by 'pibooth-idle-chats' plugin
    chat_delay = 90

.. note:: Edit the configuration by running the command ``pibooth --config``.

Customize chats
----------------

Chat files must be ``.wav`` and with a name of photochat#.wav where # starts at 0 and increments.
The chats are played in numerical order.

Custom chats can be added by adding or replacing existing chat files in the chats folder
(by default ``~/.config/pibooth/chats``) with custom ones.

Specific features
^^^^^^^^^^^^^^^^^

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

.. |PypiPackage| image:: https://badge.fury.io/py/pibooth-idle-chats.svg
   :target: https://pypi.org/project/pibooth-idle-chats
   :alt: PyPi package

.. |Downloads| image:: https://img.shields.io/pypi/dm/pibooth-idle-chats?color=purple
   :target: https://pypi.org/project/pibooth-idle-chats
   :alt: PyPi downloads

Attribution
-----------

This plugin is based heavily on the pibooth-sound-effects plugin by werdeil
