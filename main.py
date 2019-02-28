from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, StickerSet
import logging, re, datetime, random
import datetime_utils as dtutil
import arango_utils as db
from stickermanager_token import TOKEN, PATH
from messages import *


### DEERMAESTER-SPECIFIC
maester_filenames = ["Deerhorn_Medals01_Deer_Thief_Gold", "Deerhorn_Medals02_Deerfender_Gold", "Deerhorn_Medals03_Deer_of_Dice_Gold", "Deerhorn_Medals04_Deer_Arena_Gold", "Deerhorn_Medals05_Rising_Deer_Gold", "Deerhorn_Medals06_Deer_Thief_Silver", "Deerhorn_Medals07_Deerfender_Silver", "Deerhorn_Medals08_Deer_of_Dice_Silver", "Deerhorn_Medals09_Deer_Arena_Silver", "Deerhorn_Medals10_Rising_Deer_Silver", "Deerhorn_Medals11_Deer_Thief_Bronze", "Deerhorn_Medals12_Deerfender_Bronze", "Deerhorn_Medals13_Deer_of_Dice_Bronze", "Deerhorn_Medals14_Deer_Arena_Bronze", "Deerhorn_Medals15_Rising_Deer_Bronze"]
maester_emojis = ["💰", "🛡", "🎲", "⚔️", "💫", "💰", "🛡", "🎲", "⚔️", "💫", "💰", "🛡", "🎲", "⚔️", "💫"]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def open_PNG(bot, user_id, filename):
    """Return File
    """
    try:
        sticker_file = open(PATH + filename + ".png", 'rb')
        return sticker_file
    except OSError as e:
        bot.send_message(user_id, text=CREATE_STICKER_SET_FILE_ERROR.format(filename, filename + ".png"), parse_mode = ParseMode.HTML)
        print(e)
        raise

# UNUSED
def send_stickers_by_set_name(bot, update, args):
    """Send List of all stickers
    """
    name = add_suffix(args[0])
    stickers = bot.get_sticker_set(name)
    text = ''
    for sticker in stickers["stickers"]:
        text += "{} {}\n".format(sticker["file_id"], sticker["emoji"])
    update.message.reply_html(text)

def add_suffix(name):
    if not name.endswith("_by_sticker_manager_bot"):
        name += "_by_sticker_manager_bot"
    return name

def check_user_access_to_set(update, sticker_set, user_id):
    """Return Boolean
    """
    access = True
    if sticker_set["userId"] != user_id:
        update.message.reply_html(ADD_STICKER_NO_PERMISSION)
        access = False
    return access

def check_if_set_exists(update, set_name):
    existent = db.checkDocument("stickers", set_name)
    if not existent:
        update.message.reply_html(ADD_STICKER_UNKNOWN_PACK.format(set_name))
    return existent

def add_sticker(bot, update, args):
    """Send Sticker-URL on success
    """

    user_id = update.message.from_user.id

    # reject if not enough arguments
    if len(args) is not 3:
        update.message.reply_html(ADD_STICKER_MISSING_ARG)
        return

    set_name = add_suffix(args[0])
    filename = args[1]
    sticker_emoji = args[2]

    # reject if wrong set_name
    if not check_if_set_exists(update, set_name):
        return
    sticker_set = db.getStoredDocument("stickers", set_name)

    # reject if user hasn't access to sticker_set
    if not check_user_access_to_set(update, sticker_set, user_id):
        return

    file = open_PNG(bot, user_id, filename)
    stickers = sticker_set["stickers"]

    bot.add_sticker_to_set(user_id, set_name, file, sticker_emoji)

    stickers = update_stickers(bot, set_name, stickers, filename)
    answer = db.updateDocument("stickers", {"stickers": stickers}, set_name)
    if answer:
        update.message.reply_text(ADD_STICKER_SUCCESS.format(sticker_set["stickerURL"]))
    else:
        update.message.reply_text(ERROR_CONSOLE)


def update_stickers(bot, set_name, stickers, filename):
    """Return Sticker-Set
    """
    tg_set = bot.getStickerSet(set_name)
    tg_stickers = tg_set["stickers"]
    for sticker in tg_stickers:
        existent = False
        for k,v in stickers.items():
            if sticker["file_id"] == v:
                existent = True
        if not existent:
            stickers.update({filename: sticker["file_id"]})
    return stickers

def create_sticker_set(bot, update, args):
    user_id = update.message.from_user.id

    # reject if wrong amount of arguments
    if len(args) is not 4:
        update.message.reply_html(CREATE_STICKER_SET_MISSING_ARGUMENT)
        return

    name_suffix = "_by_sticker_manager_bot"
    set_name = args[0]

    # reject if name is too long
    if len(set_name) + len(name_suffix) > 64:
        update.message.reply_html(CREATE_STICKER_SET_NAME_LENGTH.format("name", 64-len(name_suffix)))
        return

    # reject if it contains illegal charactes
    if re.search(r'[^a-zA-Z0-9_]|__', set_name):
        update.message.reply_html(CREATE_STICKER_SET_NAME_INVALID_CHAR)
        return

    set_name += name_suffix

    # reject if title is too long
    title = args[1]
    if len(title) > 64:
        update.message.reply_html(CREATE_STICKER_SET_NAME_LENGTH.format("title", 64))
        return

    filename = args[2]
    sticker_emoji = args[3]
    file = open_PNG(bot, user_id, filename)

    created_at = datetime.datetime.utcnow().isoformat()
    sticker_URL = "t.me/addstickers/{}".format(set_name)
    stickers = {filename: ''}

    bot.create_new_sticker_set(user_id, set_name, title, file, sticker_emoji)

    stickers = update_stickers(bot, set_name, stickers, filename)
    sticker_set = {}
    keys = ["key", "name", "user_id", "title", "sticker_URL", "created_at", "stickers"]
    values = [set_name, set_name, user_id, title, sticker_URL, created_at, stickers]
    for i in range(len(keys)):
        sticker_set[keys[i]] = values[i]

    answer = db.createDocument("stickers", sticker_set)
    if answer:
        update.message.reply_html(CREATE_STICKER_SET_SUCCESS.format(sticker_URL))
    else:
        update.message.reply_html("ERROR in creating the stickerset")

## READ SETS
def show_sticker_sets(bot, update):
    """Send list of all sets    print("Listening for updates...")
    """
    all_sticker_sets = db.fetchAllDocuments("stickers")

    list_of_sets = 'STICKER SETS:\n\n'

    for sticker_set in all_sticker_sets:
        sticker_set = db.getStored(sticker_set)
        date = datetime.datetime.fromisoformat(sticker_set["createdAt"])
        date = dtutil.getDateAndTime(date)
        list_of_sets += "Name: <code>{}</code>\nTitle: <code>{}</code>\nNumber of stickers: <code>{}</code>\nCreated at: <code>{}</code>\nURL: {}\n".format(sticker_set["name"], sticker_set["title"], len(sticker_set["stickers"]), date, sticker_set["stickerURL"])
        list_of_sets += "/deletepack_{}\n/showstickers_{}\n\n".format(sticker_set["name"], sticker_set["name"])

    update.message.reply_html(list_of_sets)

def delete_sticker_by_file_id(bot, file_id):
    """Return Boolean
    """
    answer = bot.delete_sticker_from_set(file_id)
    return answer

def delete_sticker_by_filename(bot, set_name, filename):
    """Return Boolean
    """
    sticker_set = db.getStoredDocument("stickers", set_name)
    stickers = sticker_set["stickers"]
    file_id = stickers[filename]
    answer = delete_sticker_by_file_id(bot, file_id)
    if answer:
        del stickers[filename]
        answer = db.updateDocument("stickers", {"stickers": stickers}, set_name)
        return answer

def delete_sticker(bot, update, args):
    """Send success-message
    """
    filename = args[1]
    set_name = add_suffix(args[0])
    answer = delete_sticker_by_filename(bot, set_name, filename)
    if answer:
        update.message.reply_html(DELETE_STICKER_BY_NAME_SUCCESS.format(filename))

def delete_on_answer(bot, update):
    """Send success-message
    """
    sticker = update.message.reply_to_message.sticker
    file_id = sticker.file_id
    answer = delete_sticker_by_file_id(bot, file_id)
    if answer:
        update.message.reply_text("Sticker deleted")

def send_sticker_info(bot, update):
    sticker = update.message.sticker
    set_name = sticker.set_name
    file_id = sticker.file_id
    text = "Set Name: <code>{}</code>\nFile-Id: <code>{}</code>".format(set_name, file_id)
    update.message.reply_html(text)

def manage_deermaester(bot, update):
    set_name = "deer_of_honor_by_sticker_manager_bot"
    user_id = update.message.from_user.id

    sticker_set = db.getStoredDocument("stickers", set_name)
    stickers = sticker_set["stickers"]

    for item in maester_filenames:
        if sticker in stickers:
            sticker_id = stickers[sticker]
            del stickers[sticker]
            bot.delete_sticker_from_set(sticker_id)

    for i in range(len(maester_filenames)):
        file = open_PNG(bot, user_id, maester_filenames[i])
        sticker_emoji = maester_emojis[i]
        bot.add_sticker_to_set(user_id, set_name, file, sticker_emoji)
        stickers = update_stickers(bot, set_name, stickers, maester_filenames[i])
        answer = db.updateDocument("stickers", {"stickers": stickers}, set_name)
        if answer:
            update.message.reply_html("Added {}".format(maester_filenames[i]))
        else:
            update.message.reply_html(ERROR_CONSOLE)

    answer = db.updateDocument("stickers", {"stickers": stickers}, set_name)
    if answer:
        update.message.reply_html("Deer upload completed.")
    else:
        update.message.reply_html(ERROR_CONSOLE)

def fallback(bot, update):
    answers = ["WTF?", "I don't really know, how to answer..., maybe try /help?", "I haven't learned this yet...", "Maybe try /help?"]
    answer_index = random.randint(0, len(answers)-1)
    update.message.reply_html(answers[answer_index])

def error(bot, update, error):
    """Log Errors caused by Updates."""

    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    print("Connection to database...")
    db.connectToDB("deermaester")
    print("Connected.")

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("create_sticker_set", create_sticker_set, pass_args=True))
    dp.add_handler(CommandHandler("show_sets", show_sticker_sets))
    dp.add_handler(CommandHandler("add_sticker", add_sticker, pass_args = True))
    dp.add_handler(CommandHandler("delete_sticker", delete_sticker, pass_args = True))
    dp.add_handler(CommandHandler("deermaester", manage_deermaester))
    dp.add_handler(MessageHandler(Filters.reply & Filters.regex('/delete'), delete_on_answer))
    dp.add_handler(MessageHandler(Filters.sticker, send_sticker_info))
    dp.add_handler(MessageHandler(Filters.all, fallback))

    # log all errors
    dp.add_error_handler(error)

    print("Listening for updates...")
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
