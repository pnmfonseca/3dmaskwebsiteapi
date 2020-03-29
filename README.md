## Up and running
> Personal-notes style...not a comprehensive tutorial

> Note: development under python 3.8.0
 * Install Python 3.x
 * Clone this project from Git
 * Install dependencies from *requirements.txt*
 * Run

### Recipe


* Install pyenv
* * (mac) brew install pyenv-virtualenv
* * (ubuntu) curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
* Install essentials if not there already
* * apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev
* Install Python 3.8.0
* * pyenv install 3.8.0
* Confirm
* * pyenv versions
* Create a virtual env for this purpose
* * pyenv virtualenv 3.8.0 venv380
* Clone this project
* * git clone git@github.com:pnmfonseca/3dmaskwebsiteapi.git
* Set the code folder's respective Python version
* * cd 3dmaskwebsiteapi
* * ~/3dmaskwebsiteapi# pyenv local venv380
* * /3dmaskwebsiteapi# python -V -> Python 3.8.0
* Install requirements
* * pip install -r requirements.txt

## Running the project
### Environment variables
The following environment variables should be set:

 Name | Affects
|---|---
|MASK_LANDSCAPE| log file name, some config settings
|MASK_PASSWORD| The database credentials (username:password)

If not set, the app behaviour is set to *sandbox*

### Starting

From the project's folder:
```
# python application.py
```
The application bootstraps:
```
(...)
03/29/2020 03:05:43 AM||WARNING||config.py||66||setupLogger()||Logging under darwin
03/29/2020 03:05:43 AM||WARNING||config.py||67||setupLogger()||Log file is [./3dmaskapi-sandbox.log]


03/29/2020 03:05:43 AM||WARNING||application.py||72||<module>()||=== Launching 3DMask Web API (sandbox) ===
```