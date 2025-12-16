from .keys.profile_page import ProfilePageKey

PROFILE_PAGE_SELECTORS = {
    # Main Profile Action Bar
    ProfilePageKey.ACTION_BAR: [
        "(//section[contains(@class,'artdeco-card')])[1]//ul[.//li[contains(normalize-space(.),'connections')]]/following-sibling::*[1]",
        "//main/section[1]//div[contains(@class, 'ph5')]//div[contains(@class, 'mt2')]", # Fallback structural
    ],
    
    # Buttons (Connect, Message, etc.)
    ProfilePageKey.CONNECT_BUTTON: [
        {"role": "button", "name": "Connect"},
        "//button[contains(@aria-label, 'Connect')]",
        "//button[.//span[text()='Connect']]",
    ],
    ProfilePageKey.PENDING_BUTTON: [
         {"role": "button", "name": "Pending"},
         "//button[contains(@aria-label, 'Pending')]",
    ],
    ProfilePageKey.MESSAGE_BUTTON: [
        {"role": "button", "name": "Message"},
        "//button[contains(@aria-label, 'Message')]",
    ],
    ProfilePageKey.FOLLOW_BUTTON: [
        {"role": "button", "name": "Follow"},
        "//button[contains(@aria-label, 'Follow')]",
    ],
    ProfilePageKey.FOLLOWING_BUTTON: [
        {"role": "button", "name": "Following"},
        "//button[contains(@aria-label, 'Following')]",
    ],
    
    # "More" Menu Trigger
    ProfilePageKey.MORE_MENU_TRIGGER: [
        "//div[@role='button' or @type='button'][.//span[contains(text(), 'More')]]",
        "//button[contains(@aria-label, 'More')]",
        "//button[.//span[contains(@class, 'artdeco-button__text')][text()='More']]",
    ],
    
    # Menu Items
    ProfilePageKey.UNFOLLOW_BUTTON: [
        {"role": "button", "name": "Unfollow"},
        "//div[@role='button'][.//span[text()='Unfollow']]",
    ],
    ProfilePageKey.REMOVE_CONNECTION_BUTTON: [
         {"role": "button", "name": "Remove connection"},
    ],

    # Dialogs
    ProfilePageKey.DIALOG: [
        "div[role='dialog']",
        "//div[contains(@class, 'artdeco-modal')]",
    ],
    
    # Dialog Actions
    ProfilePageKey.ADD_NOTE_BUTTON: [
        {"role": "button", "name": "Add a note"},
        "//button[contains(@aria-label, 'Add a note')]",
    ],
    ProfilePageKey.SEND_WITHOUT_NOTE_BUTTON: [
        {"role": "button", "name": "Send without a note"},
        "//button[contains(@aria-label, 'Send without a note')]",
    ],
    ProfilePageKey.SEND_BUTTON: [
         {"role": "button", "name": "Send"},
         "//button[contains(@class, 'artdeco-button--primary')[.//span[text()='Send']]]"
    ],
     ProfilePageKey.MESSAGE_INPUT: [
        "textarea[name='message']",
        "//textarea[@id='custom-message']"
    ]
}
