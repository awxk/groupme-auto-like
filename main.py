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

###################### CONFIGURATION ###########################################
email_or_phone = ""  # email or phone number
password = ""        # password
chat_name = ""       # chat name
iterations = 1000    # number of times to check for new messages
# (default: 1000, set to 0 to run indefinitely)
################################################################################

###################### NOTES ###################################################
# Note: if run indefinitely, the script will stop when the chat is closed
# (use Ctrl+C to stop the script)

# Note: if the chat name contains an emoji or special character, you can find
# the group's aria-label by inspecting the element in the browser
################################################################################

# Set up headless Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Go to GroupMe login page
driver.get("https://web.groupme.com/signin")

# Wait for the username input field to be present
WebDriverWait(driver, 5).until(
    lambda d: d.find_element(By.ID, "signinUserNameInput"))

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
        By.CSS_SELECTOR, 'input[ng-model="enteredPIN"]'))
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
        By.XPATH, '//button[starts-with(@aria-label, "Chat")]'))

# Find the link for the chat we want to like all the messages in and click it
chat_link_xpath = f'//button[@aria-label="Chat {chat_name}"]'
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, chat_link_xpath)))
chat_link = driver.find_element(By.XPATH, chat_link_xpath)
chat_link.click()

# Wait for the chat container element to be present on the page
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.chat-content .chat-messages')))

# Assign the chat container element to a variable
chat_container = driver.find_element(
    By.CSS_SELECTOR, '.chat-content .chat-messages')

# Assign the list of "like" buttons to a variable
like_buttons = WebDriverWait(driver, 5).until(
    lambda d: chat_container.find_elements(
        By.XPATH, '//button[@role="checkbox" and @title="Like"]'))

# Keep track of the buttons that have been clicked
clicked_buttons = []
liked_messages = len(clicked_buttons)

# Like every message in the chat
iteration_count = 0
while len(like_buttons) > 0:

    # Click on each button that hasn't been clicked yet
    for button in like_buttons:
        if button not in clicked_buttons:
            try:

                # Scroll to the button and click it
                driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()

                # Add the button to the list of clicked buttons
                clicked_buttons.append(button)
            except:

                # If the button is not clickable, move on to the next button
                continue

    # Check if the number of liked messages has increased
    if liked_messages < len(clicked_buttons):

        # Print the message and update the stored value
        print(f"Liked {len(clicked_buttons)} messages so far...")
        liked_messages = len(clicked_buttons)

        # Reset the iteration count
        iteration_count = 0
    else:
        # If the number of liked messages has not increased, increment the
        # iteration count
        iteration_count += 1

    # If the number of liked messages has not increased in the set number of
    # iterations, break out of the loop, set iterations to 0 to run indefinitely
    if iteration_count >= iterations and iterations != 0:
        break

    # Scroll up a full page length in the chat container
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - "
                          "arguments[0].offsetHeight", chat_container)

    # Find the updated list of "like" buttons
    like_buttons = WebDriverWait(driver, 5).until(
        lambda d: chat_container.find_elements(
            By.XPATH, '//button[@role="checkbox" and @title="Like"]'))


# Print the number of messages that were liked
print("Finished liking the messages!\n\tLiked a total of {} messages."
      .format(len(clicked_buttons)))

# Close the browser
driver.close()
