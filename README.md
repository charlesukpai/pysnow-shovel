shovel-pysnow
=============

Simple command line utility for creating new items in ServiceNow using the `pysnow library <http://pysnow.readthedocs.org/>`_.

Values passed to fields with references to other tables are automatically resolved and properly inserted.


Installing
----------
```bash

    $ git clone https://github.com/zetup/shovel-pysnow.git
    $ pip install -r requirements.txt

```

Usage
-----
```bash

  --api_path API_PATH           ServiceNow API path, example: /table/incident
  --payload PAYLOAD             Pass JSON payload string as an argument
  --payload_file PAYLOAD_FILE   Read JSON payload from file
  --config CONFIG_FILE          Config file, defaults to config.json
  --log_file LOG_FILE           Send logs to this file and disable terminal logging

```


Example
-------
```bash

    $ python shovel.py --api_path /table/incident --payload '{"short_description": "snow", "description": "shovel"}'

```

Author
------
Robert Wikman, Zetup
