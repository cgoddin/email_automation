# Email Automation
This is a program to automate my email campaigns for marketing my services.  It is based on Google Docs, and Google Email.

## Getting Started
Do the following things to get your own email campgain up and running on your own google domain.

1. Open a command prompt window and navigate to your local source folder `c:\src`
2. Clone this repository from Github to your local drive `git clone https://github.com/cgoddin/email_automation.git`
3. Make a virtual environment `python -m venv .env`
4. Activate the virtual environment `.env/Scripts/activate.bat`
5. Load your virtual environment `pip install -r requirements.txt`
6. Copy in your secrets files: `.secrets\client_secrets.json`
   1. To generate your secret file, see #create_secret
7. Copy and edit your config file: `.config\config.json`
8. Run the program: `python email_automation.py`
   1. The first time you run the file, you will need to approve your application for use!
 

### TODO List
- [ ] Create Secret Directory and move all tokens & creds to that folder.
    Add this folder to .gitignore
- [ ] Fill in readme.md with instructions to another developer
    on how to use and customize this program for themselves.
    Things like: What do you setup in Google?  What do you need
    to configure here?
- [ ] Move your DOC_IDs into a configuration file (config.json)
- [ ] Move your FROM_ADDRESS into a configuration file (config.json)
- [ ] Move your SERVICE_ACCOUNT_CREDS_FILE into a configuration file (config.json)
- [ ] Your client_secrets.json filename should not be hardcoded, move to configuration file variable.
- [ ] Your token.pickle file should not be hardcoded name.
