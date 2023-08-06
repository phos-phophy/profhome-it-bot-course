from argparse import ArgumentParser

from telebot import TeleBot

from src import setup_bot


if __name__ == '__main__':
    parser = ArgumentParser(description='Bot CLI arguments')

    DEFAULT_CONFIG_PATH = './config.yaml'

    parser.add_argument('-c', '--config', help='Path to the configuration file', type=str, required=False, default=DEFAULT_CONFIG_PATH)
    parser.add_argument('-t', '--token', help='Bot HTTP API access token', type=str, required=False, default=None)
    args = parser.parse_args()

    bot: TeleBot = setup_bot(args)

    bot.infinity_polling()
