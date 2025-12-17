from enum import Enum

class ProfilePageKey(Enum):
    # Main Sections
    PROFILE_CARD = "action_bar"
    
    # Buttons
    CONNECT_BUTTON = "connect_button"
    PENDING_BUTTON = "pending_button"
    MESSAGE_BUTTON = "message_button"
    FOLLOW_BUTTON = "follow_button"
    FOLLOWING_BUTTON = "following_button"
    UNFOLLOW_BUTTON = "unfollow_button"
    REMOVE_CONNECTION_BUTTON = "remove_connection_button"
    
    # Menus
    MORE_MENU_BUTTON = "more_menu_trigger"
    
    # Dialogs
    DIALOG = "dialog"
    ADD_NOTE_BUTTON = "add_note_button"
    SEND_WITHOUT_NOTE_BUTTON = "send_without_note_button"
    SEND_BUTTON = "send_button"
    MESSAGE_INPUT = "message_input"
