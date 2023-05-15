# Automation tests for TESTARENA
The repository contains atumatic tests for [TESTARENA](https://demo.testarena.pl/), which include:   
I. Logging in the demo version   
II. Adding a new task to any project   
III. Performing a login using incorrect data   

## Initializing repository
1. Clone this repo
1. Create virtual environment in local repo - `python -m venv ./`
1. Activate venv - `./Script/activate`
1. Install dependencies `pip install -r requirements.txt`

## Start tests
    pytest tests --browser='chrome'

### Important
You need to have installed 1 out of 4 browser:
- Chrome
- Firefox
- Edge
- Safari


## Author
- [Edwin Pająk](https://github.com/edyp)