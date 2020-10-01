# pyFastway API Client
A client for the RESTful myFastway API service. Official API documentation can be found [here](https://github.com/mindfulsoftware/myFastway.ApiClient/wiki).

## Installation and Setup
1. Install [project dependencies](#installing-python-and-dependencies).
2. Place `fastway/labels.csv` in `pyFastway/fastway/tracking/`.
3. Run program with `python pyFastway/fastway/fastway_client.py`.
4. Enter `client_id` and `client_secret` from [your myFastway account](https://myfastway.com.au/#/admin/api-keys/list) on first run.

## Running the Program
1. Run program with `python pyFastway/fastway/fastway_client.py` and arguments `write` (default) or `print`.
2. Find results in `pyFastway/fastway/results/fastway_results.csv` when the program is finished (`write` only).
3. View logging information in `pyFastway/fastway/results/fastway_log.json` if required.

### Arguments

| Argument          | Description                             |
| ----------------- | --------------------------------------- |
| `write` (default) | Writes output to `fastway_results.csv`. |
| `print`           | Prints output to the console only.      |

Examples:

```
python pyFastway/fastway/fastway_client.py print
```
```
python pyFastway/fastway/fastway_client.py write
```

### Installing Python and Dependencies
Python 3 must be installed. For information on downloading and installing Python, visit the [official downloads page](https://www.python.org/downloads/).

The following packages must also be installed with Pip:

* [requests](https://pypi.org/project/requests/)
* [pandas](https://pypi.org/project/pandas/)

For information on installing Pip and Python packages, read [this tutorial on w3schools](https://www.w3schools.com/python/python_pip.asp).

### Support
Contact [zach@zachwingrave.com](mailto:zach@zachwingrave.com) for support. API documentation can be found [here](https://github.com/mindfulsoftware/myFastway.ApiClient/wiki).

### License
This software is licensed under the [GNU General Public License v3](LICENSE.md).

### Attributions
[Code Programming Python](https://pixabay.com/photos/code-programming-python-1084923/) by [Johnson Martin](https://pixabay.com/users/JohnsonMartin-724525/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1084923) from [Pixabay](https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1084923).
