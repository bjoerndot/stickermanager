CREATE_STICKER_SET_MISSING_ARGUMENT = "You need to send me exactly four arguments: \n1) The name of the sticker set,\n2) the stickersets title,\n3) the filename of your png-file (in a folder with the path ./stickers/),\n4) the emoji for the sticker, e.g. <code>/create_sticker_set name_of_set title_of_set filename emoji</code>"
CREATE_STICKER_SET_NAME_LENGTH = "The {} for your stickerset is too long. It must not be longer than {} digits." #name/title + remaining number of digits
CREATE_STICKER_SET_NAME_INVALID_CHAR = "The name for your stickerset may only contain english letters, digits and underscores, but not two underscore in a row."
CREATE_STICKER_SET_FILE_ERROR = "The filename <code>{}</code> is either incorrect or the file <code>{}</code> doesn't exist." # filename + filename.png
CREATE_STICKER_SET_SUCCESS = "The stickerset has been created. Find it under: {}" # stickerUrl

# add stickers
ADD_STICKER_UNKNOWN_PACK = "This sticker set ({}) does not seem to exist."  # stickerset name
ADD_STICKER_NO_PERMISSION = "You have no permission to add stickers to this set."
ADD_STICKER_MISSING_ARG = "Send me exactly three arguments: \n1) Name of the sticker set\n2) name of the .png-file\n3) the emoji for your sticker.\ne.g. <code>/addsticker name_of_set filename emoji</code>"
ADD_STICKER_SUCCESS = "The sticker was added to your pack. Find it under: {}" # stickerUrl

# deleteStickers
DELETE_STICKERS_MISSING_ARG = "You need to send me exactly one or two arguments: \n- name of the sticker set\n- (optional) -d\ne.g. <code>/deletestickers name_of_set -d</code>"
DELETE_STICKERS_WRONG_NAME = "This stickerset does not exist."
DELETE_STICKERS_SUCCESS = "{} items were deleted from stickerset {}" # num of items + name of stickerset

# deleteSticker
DELETE_STICKER_BY_NAME_SUCCESS = "The sticker '{}' was removed." # filename

#deleteSticker Set
DELETE_STICKER_SET_SUCCESS = "The stickerset {} has been deleted." # packname

# show stickers:
SHOW_STICKER_WRONG_NAME = "This stickerpack does not exist."

ERROR_CONSOLE = "Error. Check console."
