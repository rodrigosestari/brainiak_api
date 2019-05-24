Brainiak
++++++++

Brainiak is a Linked Data RESTful API to provide transparent access to SPARQL endpoints.

This project was created by `Globo.com <http://globo.com/>`_'s engineers to its semantic platform.

We are releasing this as an open-source project in order to give something back to the software community.

Learn more about Brainiak in our recent presentations

- `Linked Data at Globo.com @ WoLE workshop (WWW 2013) <http://www.slideshare.net/icaromedeiros/linked-data-at-globocom>`_.
- `Semantic Day @ Globo.com <http://www.slideshare.net/semantic_team/semantic-day-2013-linked-data-at-globocom>`_.

Documentation
=============

Brainiak full documentation can be found in http://brainiak.readthedocs.org

Motivation
==========

The following topics motivated the development of Brainiak:


* Lower the barrier to use semantic technlogies
* Encapsulate the access to triple stores compatible with RDF/TURTLE and SPARQL (e.g. `OpenLink Virtuoso <http://virtuoso.openlinksw.com/>`_, `Sesame <http://www.aduna-software.com/technology/sesame>`_, `AllegroGraph <http://www.franz.com/agraph/allegrograph/>`_, `Ontotext OWLIM <http://www.ontotext.com/owlim>`_)
* Enhance data management to triple stores
* Provide a unique and coherent interface to other database backends, including non triple stores (e.g.: `ElasticSearch <http://www.elasticsearch.org/>`_).


Running
=======

Brainiak is developed using `Python <http://www.python.org/>`_.

The requirements for currently running Brainiak are:

- Python packages (detailed at requirements.txt)
- Triplestore: `Virtuoso 6 <https://github.com/openlink/virtuoso-opensource>`_
- Search engine: `ElasticSearch 0.90.12 <http://www.elasticsearch.org/>`_
- Event bus: `ActiveMQ 5.8.0 <http://activemq.apache.org/>`_
- *Cache* `Redis <http://redis.io/>`_ (optional)

Currently Brainiak is run in production using CentOS, but the deployment scripts
are of internal use at Globo.com and won't be released open-source.

Fedora
------

There are complete setup instructions and scripts for Fedora 20, at:
https://github.com/globocom/brainiak_api/tree/master/setup/fedora

MacOS
-----

Setup scripts are being added to:

https://github.com/globocom/brainiak_api/tree/master/setup/macosx

General instructions
--------------------

It can be installed using `virtualenvwrapper <http://www.doughellmann.com/projects/virtualenvwrapper/>`_: ::

    # Install virtualenv / virtualenvwraper, in case you didn't yet:
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    source `which virtualenvwrapper.sh`

    # Then, just use it:
    mkvirtualenv brainiak
    workon brainiak
    make install

Or using super-user powers: ::

    sudo make install

After virtualenv is ready (run in development mode): ::

    make run

By default, brainiak will be available at: http://localhost:5100/

Testing
=======

There are two categories of tests in Brainiak:
- Unit (python-only)
- Integration (need other services to be up, e.g Virtuoso)

Run unit tests using: ::

    make unit

Run integration tests using: ::

    make integration

To run all tests, and check how much of the code is covered with tests: ::

    make test

We expect contributions to have related tests, so we can keep up test code
coverage to more than 90%.

DISCLAIMER
==========

The project is released as it is.
This means you might have to tweak it, in order to meet your purpose.
People can contribute to turn this project more adoption-friendly outside its original context of creation and use.

For this purpose, use the forum https://groups.google.com/forum/#!forum/brainiak_api_users to 
discuss ideas and ask questions.

We use the twitter `@brainiak_api <https://twitter.com/brainiak_api>`_'s to broadcast information 
about the project and related subjects.

And we also have a facebook page at https://www.facebook.com/brainiakapi .

The team email semantica@corp.globo.com is also available for contact.


License
=======

Brainiak is GNU GPL 2: ::

    < Brainiak: Linked Data RESTful API >
    Copyright (C) 2013 - Globo.com

    Brainiak is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 2 of the License.

    Brainiak is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Brainiak. If not, see <http://www.gnu.org/licenses/>.

