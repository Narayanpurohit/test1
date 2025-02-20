import os
import re
import requests
import logging
from pyrogram import Client, filters
from imdb import Cinemagoer

# Logging setup
logging.basicConfig(level=logging.INFO)

# Telegram Bot Credentials
API_ID = 26847865
API_HASH = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"
BOT_TOKEN = "6941908449:AAHNGisGgioOKPDWj5dLQGeB6NOFuMtUs_M"

# WordPress API Credentials
WP_URL = "https://jnmovies.site/wp-json/wp/v2"
WP_USER = "bot"
WP_PASSWORD = "6wQn rEDj lngb XrcK CbsW No2L"

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize IMDbPY
ia = Cinemagoer()

# Function to upload image to WordPress media library
def upload_image_to_wordpress(image_url):
    # Download the image
    response = requests.get(image_url)
    if response.status_code == 200:
        file_name = os.path.basename(image_url)
        with open(file_name, "wb") as f:
            f.write(response.content)
        
        # Upload to WordPress
        with open(file_name, "rb") as f:
            upload_response = requests.post(
                f"{WP_URL}/media",
                headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
                auth=(WP_USER, WP_PASSWORD),
                files={"file": f},
            )
        
        os.remove(file_name)
        if upload_response.status_code == 201:
            return upload_response.json()["id"]
    return None

# Function to create WordPress post
def create_wordpress_post(title, content, image_id):
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        "featured_media": image_id,
    }
    response = requests.post(
        f"{WP_URL}/posts",
        json=post_data,
        auth=(WP_USER, WP_PASSWORD),
    )
    return response.status_code == 201

# Function to scrape IMDb data
def scrape_imdb_data(movie_id):
    movie = ia.get_movie(movie_id)
    data = {
        "title": movie.get("title"),
        "rating": movie.get("rating"),
        "genres": ", ".join(movie.get("genres", [])),
        "director": ", ".join([str(director) for director in movie.get('director', [])[:3]]) or "N/A",
        "writer": ", ".join([str(writer) for writer in movie.get('writer', [])[:3]]) or "N/A",
        "cast": ", ".join([str(cast) for cast in movie.get('cast', [])[:5]]) or "N/A",  # Top 5 cast
        "plot": movie.get("plot outline"),
        "poster": movie.get("full-size cover url"),
    }
    return data

# Handle /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send me an IMDb movie link!")

# Handle IMDb link
@app.on_message(filters.text)
async def handle_imdb_link(client, message):
    try:
        imdb_url = message.text
        imdb_id_match = re.search(r'imdb\.com/title/tt(\d+)', imdb_url)
        imdb_id = imdb_id_match.group(1) if imdb_id_match else None
        
        if not imdb_id:
            await message.reply_text("⚠️ Invalid IMDb link!")
            return
        
        # Scrape IMDb data
        movie_data = scrape_imdb_data(imdb_id)
        
        # Upload poster to WordPress
        poster_id = upload_image_to_wordpress(movie_data["poster"])
        
        if poster_id:
            # Ask for audio language
            await message.reply_text("🎙️ What is the audio language of the movie?")
            audio_language = (await client.listen(message.chat.id)).text.strip()
            
            # Ask for screenshot links
            await message.reply_text("📸 Now send me the screenshot links (each on a new line):")
            screenshots_response = (await client.listen(message.chat.id)).text.strip()
            screenshots = screenshots_response.split("\n")
            
            if len(screenshots) < 2:
                await message.reply_text("⚠️ Please send at least two screenshot links.")
                return
            
            # Generate HTML for screenshots
            screenshots_html=""
            #screenshots_html = '<div class="neoimgs"><div class="screenshots"><ul class="neoscr">\n'
            for link in screenshots:
                screenshots_html += f'<li class="neoss"><img src="{link}" /></li>\n'
            #screenshots_html += '</ul></div></div>'
            
            # Ask for download links
            await message.reply_text("📥 Send me the download links in the format:\n`Resolution | Download Link`")
            download_response = (await client.listen(message.chat.id)).text.strip()
            download_links = download_response.split("\n")
            
            # Prepare download links HTML
            download_html = "<br><strong>Download Links:</strong><br>"
            for line in download_links:
                parts = line.split("|")
                if len(parts) == 2:
                    resolution, dl_link = map(str.strip, parts)
                    download_html += (
                        f'<p style="text-align: center;">'
                        f'<a href="{dl_link}" target="_blank"><button>{resolution}</button></a></p>\n'
                    )
            
            # Prepare post content
            post_content = f"""
             <br><img src="{movie_data["poster"]}" alt="{movie_data["title"]} Poster">
            <strong>Title:</strong> {movie_data["title"]}<br>
            <strong>Rating:</strong> {movie_data["rating"]}<br>
            <strong>Genres:</strong> {movie_data["genres"]}<br>
            <strong>Director:</strong> {movie_data["director"]}<br>
            <strong>Writer:</strong> {movie_data["writer"]}<br>
            <strong>Cast:</strong> {movie_data["cast"]}<br>
            <strong>Plot:</strong> {movie_data["plot"]}<br>
            <strong>Audio Language:</strong> {audio_language}<br>
            {screenshots_html}
            {download_html}
           
            """
            
            # Create WordPress post
            if create_wordpress_post(movie_data["title"], post_content, poster_id):
                await message.reply_text(f"✅ Post created for {movie_data['title']}!")
            else:
                await message.reply_text("❌ Failed to create WordPress post.")
        else:
            await message.reply_text("❌ Failed to upload the poster to WordPress.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {str(e)}")

# Run the bot
app.run()