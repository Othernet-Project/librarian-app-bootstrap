======================
Librarian App Boostrap
======================

Librarian App Boostrap (LAB) is a simple web server that provides a
Librarian-like environment for a single Librarian application.

The main advantage of using LAB is you do not have to package your application
while you are developing it. Main disadvantage is that some of the Librarian
features cannot be tested (such as localization).

Note that LAB is not a replacement for testing with Librarian. It is merely a
convenience option to get started quickly.

Quick usage
===========

To start LAB simply run the ``bootstrap.py`` script::

    bootstrap.py --app /path/to/app --files /path/to/data

The ``--app`` argument is optional and defaults to current directory. This is
where you keep your app files in unpacked form.

The ``--files`` argument is also optional and defaults to ``./data`` directory.
This is where you keep any files that you wish to access using the Librarian
files API. This directory represents the root of the Librarian's files 
directory.

Once the server is started, you can access is at `localhost:8080`_. The home
page simulates the way your application appears in the application list.
Clicking the app, takes you to the app itself.

Differences to Librarian
========================

- There is no way to change the locale.
- The application URL is always ``/app/`` even though Librarian includes the
  ``app ID`` in the URL.

.. _`localhost:8080`: http://localhost:8080/
