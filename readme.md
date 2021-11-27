# Email Automation
This is a program to automate my email campaigns for marketing my services.  It is based on Google Docs, and Google Email.

## Status
Version 1 Depolyed.

## Motivation
I created this project to maximize my prospecting efforts for my social media marketing agency, Zyst, and refine my skills as a developer. By automating the process, I can send more emails, raise my response rate, and focus on more important matters.

## User Experience

Interface
<br>
<img src="./docs/prospecting.gif" height=200/>

Templates
<br>
<img src="./docs/template.gif" height=340/>

Email
<br>
<img src="./docs/email.png" height=190/>

## Features

- Automatically sends a 5 email sequence
- Does not send on weekends
- Customizable templates
- Editable time delta between emails
- Email personalization
- Tracks sent time
- Collects send recepts
- Creates editable draft in draft folder before sending
- Runs on Google Cloud Platform



## Installation
Do the following steps to get your own email campgain up and running on your own google workspace:

1. Dowload repository

2. Open Google Cloud Platform (GCP) in your browser
    >https://cloud.google.com/

3. Click 'Console'

4. Create new project
    >Name project and click create

5.  Create credentials
    >Using the GCP search bar, open 'Credentials'

    >Click 'CREATE CREDENTIALS'

    >Select 'OAuth client ID'

    >Application type: 'Web application'

    >Name client (eg. 'Email Automation')

    >Download JSON

    >Create '.secrets' folder

    >Put JSON file in folder as 'client_secrets.json'

6.  Copy Google Workspace documents
    >Open Google Sheets template https://docs.google.com/spreadsheets/d/1Mw7FLVJM3l0nSrsFttbrtYMm0BZPt2jti77Iv1WC4Yk/edit?usp=sharing

    >Make a copy
    
    >Open Google Doc template https://docs.google.com/document/d/1HJbk2Altw-W00NATCz9g7OU0Ck0ZiUFEpW-SfLIo94U/edit?usp=sharing

    >Make 5 copies

    >Fill out templates

    >Document IDs are the string of characters in URL (eg. 1HJbk2Altw-W00NATCz9g7OU0Ck0ZiUFEpW-SfLIo94U)

7.  Complete config_example.json
    >Once complete, rename to 'config.json'
  
8.  Compress files into Zip folder

9.  Using the GCP search bar, open 'Cloud Funtions'
    >You will have to enable billing

10. Click 'CREATE FUNCTION'

11. Configure settings
    >Name function (eg. 'email_automation')

    >Select region (eg. 'us-east1')

    >Trigger type: 'HTTP'

    >Authentication: 'Require authentication'

    >Uncheck 'Require HTTPS'

    >If running large numbers through program, change 'Memory allocated' and 'Timeout' accordingly

    >Click 'NEXT'

12. Upload code
    >Select 'Python 3.9' as runtime

    >Entry point: 'gcp_func_entry'

    >Upload Zip and create bucket to store file

    > Click 'DEPLOY'

13. Using the GCP search bar, open 'Cloud Scheduler'

14. Click 'CREATE JOB'

15. Define the schedule
    >Name job (eg. 'email_automation')

    >Write description (eg. 'Runs email automation')

    >Choose frequency (eg. weekdays at 8:15 AM: '15 8 * * 1-5')

    >Choose timezone (eg. 'Eastern Standard Time')

    >Click 'CONTINUE'

16. Configure the execution
    >Target type: 'HTTP'

    >URL: get HTTP trigger from Cloud Funtion

    >Click 'CREATE'

## Dependencies Used
- gspread
- gspread_dataframe
- pandas
- pygsheets
- pydrive

## Author
Cole Goddin
