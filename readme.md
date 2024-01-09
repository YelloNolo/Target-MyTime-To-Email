# Target MyTime To Email

> Share mytime.target.com schedule by email

Note: This script is buggy, and as I no longer work at target, I will not be maintaning it 🥲

## 📃 Prerequisites

-   Python 3.10.11
-   Chrome (Browser must be installed)
-   ChromeDriver (check notes)
-   Conda: https://docs.conda.io/projects/miniconda/en/latest/

## 📒 Notes

-   You may need to update "chromedriver.exe" to a version that matches your chrome install
    -   You can find the current chrome version by: [chrome://settings/help](chrome://settings/help) -> "Version"
-   You can download the latest driver here: https://googlechromelabs.github.io/chrome-for-testing/#stable or https://chromedriver.chromium.org/downloads
-   Make sure to get the 32-bit version of the driver.
-   Replace "chromedriver.exe" in the main directory.

## ⬇️ Installation

1. Clone the repository or download the script.

```
git clone https://github.com/YelloNolo/Target-MyTime-To-Email
```

2. Run `setup.bat` **or** install the script with the following commands:

```batch
conda create --prefix ./conda-env python=3.10.11
conda activate ./conda-env
pip install -r requirements.txt
```

3. Clone `example.env` to `.env`.

4. Edit the `.env` and update the following variables:

    ### Login Credentials for MyTime

    ```
    target_username = "target_user_username"
    target_password = "target_user_password"
    ```

    ### Email Details

    ```
    receiver_emails = "["email_1", "email_2"]"
    subject = "Target Schedule"
    ```

    ### SMTP Mail

    ```
    smtp_username = "enter_email"
    smtp_password = "enter_password"
    ```

## 🪴 Usage

1. Run the script with `run.bat` **or**:

```batch
conda activate ./conda-env
python run.py
```

1. The script will perform the following steps:
    - Check the last modification date of a file.
    - Prompt the user to continue or exit based on the file's modification date.
    - Initialize a Chrome driver and open a specified URL.
    - Perform login and verification steps if necessary.
    - Scrape the web page and save the schedule to a file.
    - Send the saved schedule via email.
2. Follow the prompts in the terminal to proceed or exit.

## 📧 Obtaining Google Email SMTP Server Details

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

## 🪪 License

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/YelloNolo/Target-MyTime-To-Email">Target MyTime To Email</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://www.yello.page">Alec Murphy</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"></a></p>
