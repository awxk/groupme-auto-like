"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Copyright (c) 2023, awxk (https://github.com/awxk)
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

email_or_phone = ""  # phone number
password = ""        # password
chat_name = ""       # chat name

# note: if the chat name contains an emoji, you can find the group's aria-label by inspecting the element in the browser

# Set up headless Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Go to GroupMe login page
driver.get("https://web.groupme.com/signin")

WebDriverWait(driver, 5).until(
    lambda d: d.find_element(By.ID, "signinUserNameInput")
)

# Enter username and password
email_or_phone_input = driver.find_element(By.ID, "signinUserNameInput")
email_or_phone_input.send_keys(email_or_phone)
password_input = driver.find_element(By.ID, "signinPasswordInput")
password_input.send_keys(password)

# Submit form
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Enter 2FA code
code_input_field = WebDriverWait(driver, 5).until(
    lambda driver: driver.find_element(
        By.CSS_SELECTOR, 'input[ng-model="enteredPIN"]')
)
code = input('Enter 2FA code: ')
code_input_field.send_keys(code)

# Submit form
driver.find_element(By.XPATH, '//button[text()="Verify"]').click()

# Wait for the "Chats" button to be clickable and click it
chats_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Chats"]')))
chats_button.click()

# Wait for the chat links to be present
chat_links = WebDriverWait(driver, 5).until(
    lambda driver: driver.find_elements(
        By.XPATH, '//button[starts-with(@aria-label, "Chat")]')
)

# Find the link for the chat we want to like all the messages in and click it
chat_link_xpath = f'//button[@aria-label="Chat {chat_name}"]'
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, chat_link_xpath)))
chat_link = driver.find_element(By.XPATH, chat_link_xpath)
chat_link.click()

# Wait for the chat container element to be present on the page
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.chat-content .chat-messages'))
)

# Assign the chat container element to a variable
chat_container = driver.find_element(
    By.CSS_SELECTOR, '.chat-content .chat-messages')

# Assign the list of "like" buttons to a variable
like_buttons = chat_container.find_elements(
    By.XPATH, '//button[@role="checkbox" and @title="Like"]')

# Keep track of the buttons that have been clicked
clicked_buttons = []

# Set flag to False
printed = False

# Like every message in the chat
while len(like_buttons) > 0:

    # Click on each button that hasn't been clicked yet
    for button in like_buttons:
        if button not in clicked_buttons:
            try:

                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView();", button)

                # Click the button
                button.click()

                # Add the button to the list of clicked buttons
                clicked_buttons.append(button)
            except:

                # If the button is not clickable, move on to the next button
                continue

    # Print the number of messages that have been liked, but only if the message hasn't been printed yet
    if not printed:
        print(f"Liked {len(clicked_buttons)} messages so far...")

        # Set the flag to True
        printed = True

    # Scroll up a full page length in the chat container
    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].offsetHeight", chat_container)

    # Check if the chat is still loading
    spinner_present = True
    while spinner_present:
        try:
            spinner = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.chat-loading-visible')))
        except:

            # If the spinner is not present, the chat has finished loading
            spinner_present = False

    # Scroll up a full page length
    driver.execute_script("window.scrollTo(0, 0);")

    # Find the updated list of "like" buttons
    like_buttons = driver.find_elements(
        By.XPATH, '//button[@role="checkbox" and @title="Like"]')

    # Reset the flag to False
    printed = False


# Print the number of messages that were liked
print(
    f"Finished liking the messages!\n\tLiked a total of {len(clicked_buttons)} messages.")

# Close the browser
driver.close()
