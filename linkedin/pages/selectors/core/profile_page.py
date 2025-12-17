from .keys.profile_page import ProfilePageKey

PROFILE_PAGE_SELECTORS = {
    # Main Profile Action Bar
    ProfilePageKey.PROFILE_CARD: [
        "(//section[contains(@class,'artdeco-card')])[1]//ul[.//li[contains(normalize-space(.),'connections')]]/following-sibling::*[1]",
    ],
    
    # Buttons (Connect, Message, etc.)
    ProfilePageKey.CONNECT_BUTTON: [
        "//button[.//span[text()='Connect']]",
        "//div[@role='button'][.//span[text()='Connect']]",
    ],
    ProfilePageKey.PENDING_BUTTON: [
        "//button[.//span[text()='Pending']]",
        "//div[@role='button'][.//span[text()='Pending']]",
    ],
    ProfilePageKey.MESSAGE_BUTTON: [
        "//button[.//span[text()='Message']]",
        "//div[@role='button'][.//span[text()='Message']]",
    ],
    ProfilePageKey.FOLLOW_BUTTON: [
        "//button[.//span[text()='Follow']]",
        "//div[@role='button'][.//span[text()='Follow']]",
    ],
    ProfilePageKey.FOLLOWING_BUTTON: [
        "//button[.//span[text()='Following']]",
        "//div[@role='button'][.//span[text()='Following']]",
    ],
    
    # "More" Menu Trigger
    ProfilePageKey.MORE_MENU_BUTTON: [
        "//button[.//span[text()='More']]",
        "//button[@aria-label='More actions']",
    ],
    
    # Menu Items
    ProfilePageKey.UNFOLLOW_BUTTON: [
        "//button[.//span[text()='Unfollow']]",
        "//div[@role='button'][.//span[text()='Unfollow']]",
    ],
    ProfilePageKey.REMOVE_CONNECTION_BUTTON: [
        "//button[.//span[text()='Remove connection']]",
        "//div[@role='button'][.//span[text()='Remove connection']]",
    ],

    # Dialogs
    ProfilePageKey.DIALOG: [

    ],
    
    # Dialog Actions
    ProfilePageKey.ADD_NOTE_BUTTON: [

    ],
    ProfilePageKey.SEND_WITHOUT_NOTE_BUTTON: [

    ],
    ProfilePageKey.SEND_BUTTON: [

    ],
     ProfilePageKey.MESSAGE_INPUT: [

    ]
}
