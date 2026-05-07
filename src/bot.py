from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN

from parser import fetch_data, parse_data
from ranking import build_ranking
from messages import format_ranking_message


async def top_pm25(update: Update, context: ContextTypes.DEFAULT_TYPE):

    raw = fetch_data()

    stations = parse_data(raw)

    ranking = build_ranking(stations, "PM25")

    msg = format_ranking_message(
        ranking,
        pollutant="PM25",
        top=5
    )

    await update.message.reply_text(msg)


async def top_pm10(update: Update, context: ContextTypes.DEFAULT_TYPE):

    raw = fetch_data()

    stations = parse_data(raw)

    ranking = build_ranking(stations, "PM10")

    msg = format_ranking_message(
        ranking,
        pollutant="PM10",
        top=5
    )

    await update.message.reply_text(msg)


def main():

    app = ApplicationBuilder().token(
        TELEGRAM_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("top_pm25", top_pm25)
    )

    app.add_handler(
        CommandHandler("top_pm10", top_pm10)
    )

    print("🤖 Bot iniciado")

    app.run_polling()


if __name__ == "__main__":
    main()
