from .keys.profile_page import ProfilePageKey

PROFILE_PAGE_SELECTORS = {
    # Main Profile Action Bar
    ProfilePageKey.ACTION_BAR: [
        "(//section[contains(@class,'artdeco-card')])[1]//ul[.//li[contains(normalize-space(.),'connections')]]/following-sibling::*[1]",
        "//main/section[1]//div[contains(@class, 'ph5')]//div[contains(@class, 'mt2')]", # Fallback structural
    ],
    
    # Buttons (Connect, Message, etc.)
    ProfilePageKey.CONNECT_BUTTON: [
        "//button[contains(@aria-label, 'Connect')]",
        "//button[.//span[text()='Connect']]",
        "//button[text()='Connect']", 
    ],
    ProfilePageKey.PENDING_BUTTON: [
         "//button[contains(@aria-label, 'Pending')]",
         "//button[text()='Pending']",
    ],
    ProfilePageKey.MESSAGE_BUTTON: [
        "//button[contains(@aria-label, 'Message')]",
        "//button[text()='Message']",
    ],
    ProfilePageKey.FOLLOW_BUTTON: [
        "//button[contains(@aria-label, 'Follow')]",
        "//button[text()='Follow']",
    ],
    ProfilePageKey.FOLLOWING_BUTTON: [
        "//button[contains(@aria-label, 'Following')]",
        "//button[text()='Following']",
    ],
    
    # "More" Menu Trigger
    ProfilePageKey.MORE_MENU_TRIGGER: [
        "//div[@role='button' or @type='button'][.//span[contains(text(), 'More')]]",
        "//button[contains(@aria-label, 'More')]",
        "//button[.//span[contains(@class, 'artdeco-button__text')][text()='More']]",
    ],
    
    # Menu Items
    ProfilePageKey.UNFOLLOW_BUTTON: [
        "//div[@role='button'][.//span[text()='Unfollow']]",
        "//div[contains(@class, 'artdeco-dropdown__item')][.//span[text()='Unfollow']]",
    ],
    ProfilePageKey.REMOVE_CONNECTION_BUTTON: [
         "//div[@role='button'][.//span[text()='Remove connection']]",
         "//div[contains(@class, 'artdeco-dropdown__item')][.//span[text()='Remove connection']]",
    ],

    # Dialogs
    ProfilePageKey.DIALOG: [
        "//div[@role='dialog']",
        "//div[contains(@class, 'artdeco-modal')]",
    ],
    
    # Dialog Actions
    ProfilePageKey.ADD_NOTE_BUTTON: [
        "//button[contains(@aria-label, 'Add a note')]",
        "//button[text()='Add a note']",
    ],
    ProfilePageKey.SEND_WITHOUT_NOTE_BUTTON: [
        "//button[contains(@aria-label, 'Send without a note')]",
        "//button[text()='Send without a note']",
    ],
    ProfilePageKey.SEND_BUTTON: [
         "//button[contains(@class, 'artdeco-button--primary')[.//span[text()='Send']]]",
         "//button[text()='Send']",
    ],
     ProfilePageKey.MESSAGE_INPUT: [
        "//textarea[@name='message']",
        "//textarea[@id='custom-message']"
    ]
}
