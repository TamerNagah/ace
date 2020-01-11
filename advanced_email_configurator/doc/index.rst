===============================
Odoo Advance Email Configurator
===============================

This module helps to auto-configure the incoming and outgoing mail servers directly from the preferences.

This functionality allows to merge the Incoming mail server and outgoing mail server parameters in one category.

This module allows to fetch new emails (using IMAP) received from the last
time they were downloaded and successfully processed, in addition to 'unseen'
status.

Users with authorization to edit the email server in Odoo can introduce a
new date and time to download from.

In case of errors found during the processing of an email Odoo will
re-attempt to fetch the emails from the last date and time they were
successfully received and processed.

Configuration
=============

To enable this, you have to set a "User" if it is existing or create a new "User".
Go to "settings" --> Users and companies --> Users --> Create --> Save.

For Installation - Go to apps --> Search “odoo advance email configurator” --> Install.

After Installation - Go to settings --> (Username) --> Preferences.

The provider can be directly selected from the preferences.

To enable this, you have to set a 'Last Fetch Date' in the fetchmail.server
After that, emails with an internal date greater than the saved one will be
downloaded.

Usage
=====

* Odoo will attempt to fetch emails starting from the 'Last Fetch Date' defined in the email server. If all mails have been processed successfully,
it will update this date with the latest message received.

Auto Generate
=============

Go to settings --> General settings --> Auto generate ( tick ).

If auto generate is selected, then when the user is created, it will automatically configure Incoming and outgoing mail server.

When the Auto generate is not selected, then user can configure the servers from preferences.

Create Provider
===============

Go to settings --> Technical settings --> Provider -->  Create --> Save.
