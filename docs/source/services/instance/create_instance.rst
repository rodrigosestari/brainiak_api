Create an Instance
==================

This service allows the creation of a new instance, provided its context, class name and JSON.

**Basic usage**

.. code-block:: bash

  $ curl -i -X POST -T "new_york_city.json" http://brainiak.semantica.dev.globoi.com/place/City

  HTTP/1.1 201 Created
  Server: nginx
  Date: Mon, 14 Jul 2014 14:09:27 GMT
  Content-Type: application/json; profile=http://brainiak.semantica.dev.globoi.com/place/City/_schema_list
  Content-Length: 0
  Connection: keep-alive
  X-Brainiak-Resource-Uri: http://semantica.globo.com/place/City/38cea15a-d122-4e53-9214-13c00aec9969
  Location: http://brainiak.semantica.dev.globoi.com/place/City/38cea15a-d122-4e53-9214-13c00aec9969
  Access-Control-Allow-Origin: *

.. warning::

   When using curl, the "-T" param will append the filename to the actual URL, if the URL parameter ends with a "/".
   In order to avoid that, either remove the last "/" or use '-d @new_york_city.json' to expand the file contents.

Sample JSON "new_city.json" for the class City_:

.. _City: http://brainiak.semantica.dev.globoi.com/place/City/_schema

.. include :: examples/create_instance_payload.rst

.. warning::

  Note that prefixes are defined in the "@context" section.
  `Default prefixes  <http://brainiak.semantica.dev.globoi.com/_prefixes>`_ are implicit and don't need to be declared.

Besides using ``POST`` to create new instances, it is also possible to use ``PUT`` (for more information, see :ref:`edit_instance`).
In this case, the ``instance_id`` should be provided, which must be unique in the specified context.
The recommended policy is to use ``POST``, as it will assure uniqueness of the identifiers.

..

Optional query string parameters
--------------------------------

.. include :: ../params/graph_uri.rst
.. include :: ../params/class.rst


Possible responses
------------------


**Status 201**

The instance was created successfully, the response body is empty.
The URI of the new instance is identified by the "Location" header in
the HTTP response.

Note that the URI of a instance is not the same as the URL to retrieve
a instance from the API. For retrieving it, use the retrieve instance primitive <>.

**Status 400**

If there are unknown parameters in the request, the response status code is 400.

The 400 status may also happen when the JSON provided is invalid:

.. include :: examples/create_instance_400.rst

**Status 404**

If the class does not exist, the response status code is 404.

.. code-block:: bash

  $ curl -i -X POST -T "new_york_city.json" http://brainiak.semantica.dev.globoi.com/place/Person


.. code-block:: json

    {
        "errors": [
            "HTTP error: 404\nClass http://semantica.globo.com/place/Person doesn't exist in context http://semantica.globo.com/place/."
        ]
    }

**Status 500**

Internal server error. Please, contact the team <semantica@corp.globo.com>
and provide the URL, JSON and error message.
