import os
import re
import requests
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, CallbackQuery
from telegram.helpers import escape_markdown

# Substitua com o seu token
TOKEN = '7528362593:AAGAXrS4soE8OLjFPty6mMYx8a-Qb6EQxGg'

# Caminho para suas imagens
IMAGE_PATH = '/storage/emulated/0/Pictures/100PINT/Pins'

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_name = user.first_name or "Usuário"
    photo_path = os.path.join(IMAGE_PATH, 'start_image.jpg')  # Nome do arquivo da imagem
    caption = f"Olá {escape_markdown(user_name)}, seja bem-vindo ao LexusBot, o que deseja fazer hoje?"

    keyboard = [
        [InlineKeyboardButton("Verificar Logins", callback_data='verify_logins')],
        [InlineKeyboardButton("Buscar Logins", callback_data='search_logins')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(photo=open(photo_path, 'rb'), caption=caption, reply_markup=reply_markup)

async def ajuda(update: Update, context: CallbackContext):
    photo_path = os.path.join(IMAGE_PATH, 'ajuda_image.jpg')  # Nome do arquivo da imagem
    caption = "Tem alguma dúvida? Entre em contato com nosso suporte: @M4rkZuck"

    await update.message.reply_photo(photo=open(photo_path, 'rb'), caption=caption)

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data == 'verify_logins':
        photo_path = os.path.join(IMAGE_PATH, 'verify_logins_image.jpg')  # Nome do arquivo da imagem
        caption = "Certo, agora me envie a URL do site que deseja verificar os logins."
        await query.message.reply_photo(photo=open(photo_path, 'rb'), caption=caption)
        await query.answer()
    elif data == 'search_logins':
        await query.message.reply_text("Você poderá capturar logins e senhas nesse grupo: https://t.me/countryshw")
        await query.answer()

async def handle_document(update: Update, context: CallbackContext):
    user = update.message.from_user
    file = update.message.document.get_file()
    file_path = os.path.join(IMAGE_PATH, 'user_file.txt')  # Salve o arquivo temporariamente

    await file.download_to_drive(file_path)
    await update.message.reply_text("Certo, agora peço que aguarde para que eu possa verificar os logins válidos no site que você me forneceu.")
    
    # Aqui você pode implementar a lógica para ler o arquivo e verificar os logins no site
    # Isso pode ser feito com a biblioteca requests e regex

async def handle_text(update: Update, context: CallbackContext):
    user_text = update.message.text
    if re.match(r'^https?://', user_text):  # Verifica se é uma URL
        await update.message.reply_text("Agora me envie o arquivo .txt com os usuários e senhas.")
    else:
        await update.message.reply_text("Por favor, envie uma URL válida do site.")

async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.Text & ~filters.Command, handle_text))
    application.add_handler(CallbackQueryHandler(button))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())