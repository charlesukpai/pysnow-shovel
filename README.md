snag
====

Simple command line utility to create an incident in ServiceNow by passing a delimited string


Installing
----------
```bash
$ git clone https://github.com/zetup/snag.git
$ pip install -r requirements.txt
```

Usage
-----
```bash
$ python push.py "SERVER_NAME::description::short_description"
```

Example
-------
```bash
$ python push.py "SERVER01::Server reboot::The server was rebooted"
```

Flow
----
1) Parse STDIN
3) Resolve CI
4) Create incident

Logging
-------
Logs ends up in **snag.log**

Config
------
Config is set in **config.py**
