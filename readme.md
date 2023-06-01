# Script Description

This script performs a specific task using Selenium and sends the result via email.

## Prerequisites

- Python 3.x
- Chrome browser installed
- ChromeDriver

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
3. Rename the `example.env` file to `.env`.
4. Edit the `.env` file and update the following variables with your own values:

   ### User Info - Change username
   target_username = "target_user_username"
   target_password = "target_user_password"

   ### Email Details
   receiver_emails = "["email_1@gmail.com", "email_2@example.com"]"
   subject = "Target Schedule"

## Usage

1. Run the script `run.py`.
2. The script will perform the following steps:
   - Check the last modification date of a file.
   - Prompt the user to continue or exit based on the file's modification date.
   - Initialize a Chrome driver and open a specified URL.
   - Perform login and verification steps if necessary.
   - Scrape the web page and save the schedule to a file.
   - Send the saved schedule via email.
3. Follow the prompts in the terminal to proceed or exit.

### Obtaining Google Email SMTP Server Details

To obtain the SMTP server details for Google email, follow these steps:

1. Go to your Google Account settings.
2. Navigate to the "Security" tab.
3. Scroll down and enable "Less secure app access".
4. Go back to the main settings page and click on "Account info".
5. Scroll down to the "Sign-in & security" section and click on "App passwords".
6. Select the app you want to generate an app password for (e.g., "Mail" or "Other (Custom name)").
7. Follow the instructions to generate an app password.
8. Use your personal email as the `smtp_user` in the `.env` file
9. Use the generated app password as the `smtp_password` in the `.env` file.
10. Obtain the SMTP Server Port Number:
    - The SMTP server port number is specific to your email service provider. Here are some common port numbers:
        - Gmail: Port 587 or 465 (TLS/SSL)
        - Outlook.com/Hotmail.com: Port 587 or 25
        - Yahoo Mail: Port 587 or 465 (SSL)
        - AOL Mail: Port 587 or 465 (SSL)
        - Office 365: Port 587 or 25
    - To find the SMTP server port number for your email provider, you can refer to their documentation or support resources.
    - Once you have the port number, update the `smtp_port` variable in the `.env` file, replacing `###` with the appropriate port number.


## License

This script is licensed under the [MIT License](LICENSE).