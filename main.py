"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Copyright (c) 2023, awxk (https://github.com/awxk)
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Wait for page to load
time.sleep(5)

# Enter username and password
email_or_phone_input = driver.find_element(By.ID, "signinUserNameInput")
email_or_phone_input.send_keys(email_or_phone)
password_input = driver.find_element(By.ID, "signinPasswordInput")
password_input.send_keys(password)

# Submit form
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Wait for 2FA code prompt
time.sleep(5)

# Enter 2FA code
code_input = driver.find_element(
    By.CSS_SELECTOR, 'input[ng-model="enteredPIN"]')
code = input('Enter 2FA code: ')
code_input.send_keys(code)

# Submit form
driver.find_element(By.XPATH, '//button[text()="Verify"]').click()

# Wait for GroupMe to load
time.sleep(5)

# Click on "Chats" button
chats_button = driver.find_element(By.XPATH, '//button[@aria-label="Chats"]')
chats_button.click()

# Wait for chats to load
time.sleep(5)

# Find chat with the title
chat_link = driver.find_element(
    By.XPATH, f'//button[@aria-label="Chat {chat_name}"]')

# Click on chat to open it
chat_link.click()

# Wait for chat to load
time.sleep(5)

# Find chat container element
chat_container = driver.find_element(
    By.CSS_SELECTOR, '.chat-content .chat-messages')

# Find "like" buttons within the chat container
like_buttons = chat_container.find_elements(
    By.XPATH, '//button[@role="checkbox" and @title="Like"]')

# Keep track of the buttons that have been clicked
clicked_buttons = []

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

    # Print the number of messages that have been liked
    print(f"Liked {len(clicked_buttons)} messages so far...")

    # Scroll up a full page length in the chat container
    driver.execute_script(
        "arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].offsetHeight", chat_container)

    # Check if the chat is still loading
    spinner_present = True
    while spinner_present:
        try:

            # Wait for the spinner to disappear
            spinner = driver.find_element(
                By.CSS_SELECTOR, '.chat-loading-visible')
            time.sleep(1)
        except:

            # If the spinner is not present, the chat has finished loading
            spinner_present = False

    # Scroll up a full page length
    driver.execute_script("window.scrollTo(0, 0);")

    # Find the updated list of "like" buttons
    like_buttons = driver.find_elements(
        By.XPATH, '//button[@role="checkbox" and @title="Like"]')


# Print the number of messages that were liked
print(
    f"Finished liking the messages!\n\tLiked a total of {len(clicked_buttons)} messages.")

# Close the browser
driver.close()
