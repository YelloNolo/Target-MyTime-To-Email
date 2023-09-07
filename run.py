import time, os, re, subprocess, win32gui, platform
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

# Import necessary modules
load_dotenv('.env')
hwnd = win32gui.GetForegroundWindow()

# User Info
url = os.getenv('url')
schedule_file_path = os.getenv('schedule_file_path')
upload_script = os.getenv('upload_script')
username = os.getenv('target_username')
password = os.getenv('target_password')
speed_str = os.getenv('run_speed')
speed = int(speed_str)

# Calculate increase in all wait times (for slow wifi)
def calculate_adjusted_wait_time(wait_time):
    return wait_time + ((wait_time * speed) * 0.5)

# Settings
INITIAL_WAIT_TIME = calculate_adjusted_wait_time(3)
BUTTON_WAIT_TIME = calculate_adjusted_wait_time(1)
LONGER_WAIT_TIME = calculate_adjusted_wait_time(2)
LONGEST_WAIT_TIME = calculate_adjusted_wait_time(4)
VERIFICATION_CODE_LENGTH = 6
PAGES_TO_VIEW = 3

def check_last_edit():
    try:
        # Get the modification date of the file
        modification_date = datetime.fromtimestamp(os.path.getmtime(schedule_file_path)).date()

        # Get the current date
        current_date = datetime.now().date()

        # Calculate the date one week ago
        one_week_ago = current_date - timedelta(days=7)

        # Check if the modification date is within the last week
        if modification_date >= one_week_ago and modification_date <= current_date:
            print("--------------------\nThe file was saved within the last week.")
            while True:
                user_choice = input("Do you want to continue? (y/n): ")
                if user_choice.lower() == 'y':
                    print("--------------------\nContinuing...")
                    break  # Exit the loop and continue with further actions
                elif user_choice.lower() == 'n':
                    print("--------------------\nExiting...")
                    quit()  # Terminate the program
                else:
                    print("--------------------\nInvalid choice. Please try again.")
        else:
            print("--------------------\nThe file was not saved within the last week.")

    except FileNotFoundError:
        print("File not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}.")

def web_driver(url, schedule_file_path, username, password):
    # Set up Chrome driver and options
    chrome_data_dir = os.path.join(os.getcwd(), "chrome-data")
    os.makedirs(chrome_data_dir, exist_ok=True)
    driver_path = r"chromedriver"
    options = Options()
    options.add_argument(f"--user-data-dir={chrome_data_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize Chrome driver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(INITIAL_WAIT_TIME)

    # Check if the password phase is needed
    page_content = driver.find_element(By.TAG_NAME, "body").text
    if "sunday" not in page_content.lower():
        username_input = driver.find_element(By.ID, "loginID")
        username_input.send_keys(Keys.CONTROL, 'a')
        username_input.send_keys(username)
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        time.sleep(BUTTON_WAIT_TIME)
        password_input.send_keys(Keys.ENTER)

        time.sleep(LONGER_WAIT_TIME)
        no_im_good_link = driver.find_element(By.XPATH, '//a[contains(@class, "MuiTypography-colorPrimary") and text()="No, I\'m good"]')
        no_im_good_link.click()

        time.sleep(LONGER_WAIT_TIME)
        sms_option = driver.find_element(By.XPATH, '//button[contains(@class, "MuiButton-root") and .//*[text()="SMS"]]')
        sms_option.click()

        terminal_forward()
        verification_code = input("--------------------\nEnter the verification code received via SMS (6 digits): ")
        while len(verification_code) != VERIFICATION_CODE_LENGTH:
            print("Invalid verification code length. Please enter a 6-digit code.")
            verification_code = input("Enter the verification code received via SMS (6 digits): ")

        print("--------------------\nWait...")

        verification_code_input = driver.find_element(By.XPATH, '//input[contains(@class, "MuiInputBase-input") and @type="password"]')
        verification_code_input.send_keys(verification_code)

        verification_code_input.send_keys(Keys.ENTER)
        time.sleep(LONGER_WAIT_TIME)

        yes_button = driver.find_element(By.XPATH, '//button[contains(@class, "MuiButton-root") and .//span[text()="YES"]]')
        yes_button.click()
        time.sleep(LONGER_WAIT_TIME)
    else:
        print("Skipped Login")

    # Close "New Feature" popup
    while True:
        try:
            New_Feature_Close = driver.find_element(By.XPATH, '//button[contains(@class, "MuiButtonBase-root") and contains(@class, "MuiIconButton-root") and contains(@class, "MuiIconButton-sizeMedium") and contains(@class, "css-1i993nt") and @aria-label="close"]')
            New_Feature_Close.click()
            time.sleep(BUTTON_WAIT_TIME)
        except NoSuchElementException:
            print("'X' not found, skipping...")
            break
    
    for p in range(PAGES_TO_VIEW):
        if (p==0):
            pass
        else:
            next_page_button = driver.find_element(By.XPATH, '//button[contains(@class, "MuiButtonBase-root") and contains(@class, "MuiIconButton-root") and contains(@class, "MuiIconButton-sizeLarge") and contains(@class, "jss91") and contains(@class, "css-1w8s6so") and @aria-label="Go To Next Week"]')
            next_page_button.click()
            time.sleep(BUTTON_WAIT_TIME)

        # Read the entire contents of the page
        page_content = driver.find_element(By.TAG_NAME, "body").text

        # Find the index of the first occurrence of "Sunday" and remove any text before it
        index = page_content.lower().find("sunday")
        if index != -1:
            page_content = page_content[index:].strip()

        # Add a new line after every weekday (first letter capitalized)
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        for weekday in weekdays:
            page_content = page_content.replace(weekday.capitalize(), "\n" + weekday.capitalize())
            
        page_content = re.sub(r"Manage Shift", "\n", page_content, flags=re.IGNORECASE)

        # Page outlines
        schedule = []
        current_page = p + 1
        if (current_page==1):
            schedule.append(f"\n---------- START ----------\n")
        elif (current_page<PAGES_TO_VIEW):
            schedule.append(f"\n---------- Next Week ({current_page}) ----------\n")
        elif (current_page==PAGES_TO_VIEW):
            schedule.append(f"\n---------- Last Week ({current_page}) ----------\n")

        # Group each day with the two following times
        lines = page_content.split('\n')
        for i in range(len(lines) - 2):
            if i % 1 == 0:
                item = lines[i]
                schedule.append((item))

        # Mark END of message
        if (current_page==PAGES_TO_VIEW):
            schedule.append(f"\n---------- END ----------")

        if (p==0):
            # Save the grouped schedule to a file
            with open(schedule_file_path, 'w', encoding='utf-8') as file:
                for item in schedule:
                    file.write(f"{item}\n")
        else:
            # Save the grouped schedule to a file
            with open(schedule_file_path, 'a', encoding='utf-8') as file:
                for item in schedule:
                    file.write(f"{item}\n")

def terminal_forward():
    if os.name == "posix":  # Unix/Linux/MacOS
        subprocess.call(["/usr/bin/osascript", "-e", 'tell app "Terminal" to activate'])
    elif os.name == "nt":  # Windows
        win32gui.SetForegroundWindow(hwnd)
    else:
        return
    
def clear_terminal():
    # Clear the terminal screen based on the operating system
    if os.name == "posix":  # Unix/Linux/MacOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")
    else:
        return
    terminal_forward()

def send_schedule():
    # Choose a script that controls what happens with the text file
    subprocess.call(["python", upload_script])

def done():
    print("DONE :-)")
    quit()

clear_terminal()
check_last_edit()
web_driver(url, schedule_file_path, username, password)
send_schedule()
done()