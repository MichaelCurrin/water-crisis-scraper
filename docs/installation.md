# Installation


## Install OS-level dependencies

```bash
$ sudo apt-get update
$ sudo apt-get update
$ sudo apt-get install python3.5
$ sudo apt-get install virtualenv
```

## Install python packages in a virtual environment

```bash
$ cd path/to/repo
$ virtualenv venv --python python3.5
$ source venv/bin/activate
(venv) $ pip install pip --upgrade
(venv) $ pip install -r requirements.txt
```

Now you can continue to usage instructions for:

- the [properties module](docs/usage_properties.md)
