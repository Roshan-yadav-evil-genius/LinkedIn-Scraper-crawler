
# Registry for LinkedIn Profile Page Selectors
#
# Strategy:
# - Use a mix of accessibility-based selectors (Role/Label) and structural specific XPaths.
# - The 'defensive' approach means we list the most reliable selector first, followed by fallbacks.

PROFILE_PAGE_SELECTORS = {
    # Main Profile Action Bar
    "action_bar": [
        "(//section[contains(@class,'artdeco-card')])[1]//ul[.//li[contains(normalize-space(.),'connections')]]/following-sibling::*[1]",
        "//main/section[1]//div[contains(@class, 'ph5')]//div[contains(@class, 'mt2')]", # Fallback structural
    ],
    
    # Buttons (Connect, Message, etc.)
    "connect_button": [
        {"role": "button", "name": "Connect"},
        "//button[contains(@aria-label, 'Connect')]",
        "//button[.//span[text()='Connect']]",
    ],
    "pending_button": [
         {"role": "button", "name": "Pending"},
         "//button[contains(@aria-label, 'Pending')]",
    ],
    "message_button": [
        {"role": "button", "name": "Message"},
        "//button[contains(@aria-label, 'Message')]",
    ],
    "follow_button": [
        {"role": "button", "name": "Follow"},
        "//button[contains(@aria-label, 'Follow')]",
    ],
    "following_button": [
        {"role": "button", "name": "Following"},
        "//button[contains(@aria-label, 'Following')]",
    ],
    
    # "More" Menu Trigger
    "more_menu_trigger": [
        "//div[@role='button' or @type='button'][.//span[contains(text(), 'More')]]",
        "//button[contains(@aria-label, 'More')]",
        "//button[.//span[contains(@class, 'artdeco-button__text')][text()='More']]",
    ],
    
    # Menu Items
    "unfollow_button": [
        {"role": "button", "name": "Unfollow"},
        "//div[@role='button'][.//span[text()='Unfollow']]",
    ],
    "remove_connection_button": [
         {"role": "button", "name": "Remove connection"},
    ],

    # Dialogs
    "dialog": [
        "div[role='dialog']",
        "//div[contains(@class, 'artdeco-modal')]",
    ],
    
    # Dialog Actions
    "add_note_button": [
        {"role": "button", "name": "Add a note"},
        "//button[contains(@aria-label, 'Add a note')]",
    ],
    "send_without_note_button": [
        {"role": "button", "name": "Send without a note"},
        "//button[contains(@aria-label, 'Send without a note')]",
    ],
    "send_button": [
         {"role": "button", "name": "Send"},
         "//button[contains(@class, 'artdeco-button--primary')[.//span[text()='Send']]]"
    ],
     "message_input": [
        "textarea[name='message']",
        "//textarea[@id='custom-message']"
    ]
}
