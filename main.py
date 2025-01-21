"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Copyright (c) 2024, Nick Dilday (https://github.com/awxk)
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

###################### CONFIGURATION ###########################################
email_or_phone = ""  # email or phone number
password = ""        # password
chat_name = ""       # chat name
iterations = 100     # number of times to check for new messages
# (default: 100, set to 0 to run indefinitely)
################################################################################

###################### NOTES ###################################################
# Note: if run indefinitely, the script will stop when the chat is closed
# (use Ctrl+C to stop the script)

# Note: if the chat name contains an emoji or special character, you can find
# the group's aria-label by inspecting the element in the browser
################################################################################

# Set up headless Chrome browser
options = Options()
options.add_argument("--headless")
options.add_experimental_option("prefs", {
  "profile.default_content_setting_values.images": 2,
  "profile.default_content_setting_values.stylesheet": 2
})
driver = webdriver.Chrome(options=options)


# Go to GroupMe login page
driver.get("https://web.groupme.com/signin")

# Wait for the username input field to be present
WebDriverWait(driver, 5).until(
    lambda d: d.find_element(By.ID, "signinUserNameInput"))

# Enter username and password
driver.find_element(By.ID, "signinUserNameInput").send_keys(email_or_phone)
driver.find_element(By.ID, "signinPasswordInput").send_keys(password)

# Submit form
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Enter 2FA code
code = input('Enter 2FA code: ')
WebDriverWait(driver, 5).until(
    lambda d: d.find_element(
        By.CSS_SELECTOR, 'input[ng-model="enteredPIN"]')).send_keys(code)

# Submit form
driver.find_element(By.XPATH, '//button[text()="Verify"]').click()

# Wait for the "Chats" button to be clickable and click it
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable(
        (By.XPATH, '//button[@aria-label="Chats"]'))).click()

# Wait for the chat name to be clickable and click it
WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable(
        (By.XPATH, f'//button[contains(.,"{chat_name}")]'))).click()

# Wait for the chat container to be present and assign it to a variable
chat_container = WebDriverWait(driver, 5).until(
    lambda d: d.find_element(
        By.CSS_SELECTOR, '.chat-content .chat-messages'))

# Assign the list of "like" buttons to a variable
like_buttons = WebDriverWait(driver, 50).until(
    lambda d: chat_container.find_elements(
        By.XPATH, '//button[@role="checkbox" and @title="Like"]'))

# Assign the message input field to a variable
message = driver.find_element(
    By.CSS_SELECTOR, '.message.accessible-focus')

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

                # Click the button
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

    # Scroll to the top of the chat container
    message.send_keys(Keys.CONTROL + Keys.HOME)
    # Find the updated list of "like" buttons
    like_buttons = WebDriverWait(driver, 5).until(
        lambda d: chat_container.find_elements(
            By.XPATH, '//button[@role="checkbox" and @title="Like"]'))


# Print the number of messages that were liked
print("Finished liking the messages!\n\tLiked a total of {} messages."
      .format(len(clicked_buttons)))

# Close the browser
driver.close()
