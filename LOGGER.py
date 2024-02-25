from db_interaction import add_log
import util


def log(data):
    print(f"{util.get_date()} LOG: {data}")
    add_log(util.get_date(), "LOG", "BOT", data)


def log_error(data):
    print(f"{util.get_date()} ERROR: {data}")
    add_log(util.get_date(), "ERROR", "BOT", data)


def msg_log(msg, channel_name, author_name):
    print(f"{util.get_date()} MSG: [{channel_name}]: {author_name}: {msg}")
    add_log(util.get_date(), channel_name, author_name, msg)
