# groupme-auto-like
1. Opens a headless Chrome browser and navigates to the GroupMe login page.
2. Enters the username and password, and submits the form to log in.
3. Prompts the user to enter their 2FA code and then submits the form to verify the code.
4. Navigates to the chats page and clicks on the desired chat.
5. Waits for the chat to load, and finds the chat container element.
6. Finds all of the "like" buttons within the chat container.
7. Enters a loop that will continue until there are no more "like" buttons to be found:
- The script will scroll to each button that hasn't been clicked yet and click on it.
- It will then scroll up by the height of the chat container to load more messages.
- It will wait for the chat to finish loading, and then find the updated list of "like" buttons.
8. When the loop ends, it will print a message to let the user know that all buttons have been clicked.
9. The script will then close the browser.

The user must input their login information and desired GroupMe chat manually.
