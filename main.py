import os
import instaloader
from telegram import InputMediaPhoto, InputMediaVideo
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from keep_alive import keep_alive
keep_alive()

# Your TELEGRAM_BOT_TOKEN here
TELEGRAM_BOT_TOKEN = os.environ.get('token')
L = instaloader.Instaloader()

def send_media_to_telegram(media_urls, chat_id):
    try:
        updater = Updater(TELEGRAM_BOT_TOKEN)

        media = []
        mediaa = []
        mediaaa = []
        mediavariable = []
        i = 0
        z = 0
        for media_url in media_urls:
            i+=1
            if(i<=6):
                if ".mp4" in media_url:
                    media.append(InputMediaVideo(media=media_url))
                else:
                    media.append(InputMediaPhoto(media=media_url))
            elif i<=12 :
                if ".mp4" in media_url:
                    mediaa.append(InputMediaVideo(media=media_url))
                else:
                    mediaa.append(InputMediaPhoto(media=media_url))
            else :
                if ".mp4" in media_url:
                    mediaaa.append(InputMediaVideo(media=media_url))
                else:
                    mediaaa.append(InputMediaPhoto(media=media_url))

        updater.bot.send_media_group(chat_id=chat_id, media=media)
        if mediaa!=[] :
            updater.bot.send_media_group(chat_id=chat_id, media=mediaa)
        if mediaaa !=[] :
            updater.bot.send_media_group(chat_id=chat_id, media=mediaa)

    except Exception as e:
        print("Error sending media:", str(e))

def handle_messages(update, context: CallbackContext) -> None:
    message = update.message
    chat_id = ""

    # Check if the message has a valid Instagram post URL
    if 'instagram.com/p/' in message.text:
        send_messages = message.reply_text("Please wait downlaoding the post...")
        # Extract the Instagram post URL from the message
        post_url = message.text.split()[0]

        # Create an Instaloader instance
        loader = instaloader.Instaloader()

        try:
            # Load the post
            #post = instaloader.Post.from_shortcode(loader.context, post_url.split('/')[-2])
            post = instaloader.Post.from_shortcode(L.context, post_url.split('/')[-2])
            # Get the chat ID to send the media to (replace with the desired chat ID)
            chat_id = message.chat_id

            media_urls = []
            if post.is_video:
                # If the post is a video, add the video URL to media_urls
                media_urls.append(post.url)
            else:
                # If the post is an image, add the image URL to media_urls
                media_urls.append(post.url)

            # For carousel posts, add all image and video URLs to media_urls
            if post.typename == 'GraphSidecar':
                for sidecar_node in post.get_sidecar_nodes():
                    if sidecar_node.is_video:
                        media_urls.append(sidecar_node.video_url)
                    else:
                        media_urls.append(sidecar_node.display_url)

            # Send all media (images and videos) to the specified Telegram chat
            send_media_to_telegram(media_urls, chat_id)

        except Exception as e:
            print("Error processing Instagram post:", str(e))
            message.reply_text("Error processing Instagram post:", str(e))
        context.bot.delete_message(chat_id=chat_id, message_id=send_messages.message_id)
    elif ('instagram.com/reel/' in message.text):
        send_messages = message.reply_text("Please wait downlaoding the post...")
        # Extract the Instagram post URL from the message
        post_url = message.text.split()[0]

        # Create an Instaloader instance
        loader = instaloader.Instaloader()

        try:
            # Load the post
            media_urls = []
            #post = instaloader.Post.from_shortcode(loader.context, post_url.split('/')[-2])
            post = instaloader.Post.from_shortcode(L.context, post_url.split('/')[-2])
            print(post)
            #if post.is_video:
                #  message.reply_text("video...")
            media_urls.append(post.video_url)
            chat_id = message.chat_id
            if post.typename == 'GraphSidecar':
                for sidecar_node in post.get_sidecar_nodes():
                    if sidecar_node.is_video:
                        media_urls.append(sidecar_node.video_url)
                    else:
                        media_urls.append(sidecar_node.display_url)

            # Send all media (images and videos) to the specified Telegram chat
            send_media_to_telegram(media_urls, chat_id)

        except Exception as e:
            print("Error processing Instagram post:", str(e))
            message.reply_text("Error processing Instagram post:", str(e))
        context.bot.delete_message(chat_id=chat_id, message_id=send_messages.message_id)
    else:
        # Reply if the message doesn't contain a valid Instagram post URL
        message.reply_text("Please send a valid Instagram post URL.")
def start(update, context):
    update.message.reply_text("Salut, ce bot peut *télécharger des photos et vidéos* à partir d'une *publication Instagram*. Envoyez simplement le lien d'une publication",parse_mode='Markdown')
def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Handle /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Handle messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
