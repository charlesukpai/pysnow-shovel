snag
====

Usage
-----
```bash
$ python push.py <payload>
```

Example
-------
```bash
$ python push.py "SETHNLS089::Server reboot::The server was rebooted"
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
