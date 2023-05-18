# Automated tests for TESTARENA
The repository contains atumatic tests for [TESTARENA](https://demo.testarena.pl/), which include:   
I. Logging in the demo version   
II. Adding a new task to any project   
III. Performing a login using incorrect data   

## Local environment setup
1. Clone this repo
1. Create virtual environment in local repo - `python -m venv ./`
1. Activate venv - `./Script/activate`
1. Install dependencies `pip install -r requirements.txt`

## Start tests
    pytest tests --browser='chrome'

### Important
You need to have at least 1 out of 3 browser installed locally:
- Chrome
- Firefox
- Safari (alpha - not tested)


## Author
- [Edwin Pająk](https://github.com/edyp)