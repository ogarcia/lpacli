# lpacli

**lpacli** is a tiny CLI helper to get LessPass paswords configuration
directly from a LessPass server.

## Install

1. Install python3 (in Debian `apt-get install python3`).
2. Install virtualenv (in Debian `apt-get install virtualenv`).
3. Configure a Python 3 virtualenv and install _lpacli_ whith `setup.py`.

```bash
virtualenv -p python3 lpaclienv
source lpaclienv/bin/activate
python setup.py install
```

Once the installation ends you must have `lpacli` command.

For enter again in your virtualenv simply run `source` command.

```bash
source lpaclienv/bin/activate
```

## Usage

In first time use you must configure the following evironment variables.

| Variable | Used for |
| --- | --- |
| LESSPASS_HOST | URL of API server (ex. https://lesspass.com) |
| LESSPASS_USER | Username (ex. user@example.com) |
| LESSPASS_PASS | Password |

Now you can run `lpacli ls` to get a list of sites stored in server.

After first run, _lpacli_ stores the login token in your `XDG_CACHE_HOME`
directory, you can run commands with only `LESSPASS_HOST` environment
variable.

For get LessPass configuration of a site run `lpacli SITENAME` being
sitename one of the list given in `lpacli ls` command.

If you set `LESSPASS_MASTERPASS` environment variable with your LessPass
master password, _lpacli_ returns the password of site instead of site
configuration.
