
#api_id = 26847865
#api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"
#bot_token = "6941908449:AAHNGisGgioOKPDWj5dLQGeB6NOFuMtUs_M"
#wp_url = "https://jnmovies.site"
#wp_username = "bot"
#wp_password = "6wQn rEDj lngb XrcK CbsW No2L"
import os
import requests
from pyrogram import Client, filters
from imdb import IMDb
from wordpress_api import WordPressAPI

# Telegram Bot Token
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
ia = IMDb()

# Initialize WordPress API
wp = WordPressAPI(WP_URL, WP_USER, WP_PASSWORD)

# Function to upload image to WordPress media library
def upload_image_to_wordpress(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        file_name = os.path.basename(image_url)
        with open(file_name, "wb") as f:
            f.write(response.content)
        media_response = wp.media().upload(file_name)
        os.remove(file_name)
        return media_response["id"]
    return None

# Function to create WordPress post
def create_wordpress_post(title, content, image_id):
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        "featured_media": image_id,
    }
    wp.posts().create(post_data)

# Function to scrape IMDb data
def scrape_imdb_data(movie_id):
    movie = ia.get_movie(movie_id)
    data = {
        "title": movie.get("title"),
        "rating": movie.get("rating"),
        "genres": ", ".join(movie.get("genres", [])),
        "director": ", ".join([d["name"] for d in movie.get("directors", [])]),
        "writer": ", ".join([w["name"] for w in movie.get("writers", [])]),
        "cast": ", ".join([c["name"] for c in movie.get("cast", [])][:5]),  # Top 5 cast
        "plot": movie.get("plot outline"),
        "poster": movie.get("full-size cover url"),
    }
    return data

# Handle /start command
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Send me an IMDb movie link!")

# Handle IMDb link
@app.on_message(filters.text & ~filters.command)
def handle_imdb_link(client, message):
    try:
        # Extract IMDb ID from the link
        imdb_id = message.text.split("/title/")[1].split("/")[0]
        
        # Scrape IMDb data
        movie_data = scrape_imdb_data(imdb_id)
        
        # Upload poster to WordPress
        poster_id = upload_image_to_wordpress(movie_data["poster"])
        
        # Prepare post content
        post_content = f"""
        <strong>Title:</strong> {movie_data["title"]}<br>
        <strong>Rating:</strong> {movie_data["rating"]}<br>
        <strong>Genres:</strong> {movie_data["genres"]}<br>
        <strong>Director:</strong> {movie_data["director"]}<br>
        <strong>Writer:</strong> {movie_data["writer"]}<br>
        <strong>Cast:</strong> {movie_data["cast"]}<br>
        <strong>Plot:</strong> {movie_data["plot"]}
        """
        
        # Create WordPress post
        create_wordpress_post(movie_data["title"], post_content, poster_id)
        
        # Reply to user
        message.reply_text(f"Post created for {movie_data['title']}!")
    except Exception as e:
        message.reply_text(f"Error: {str(e)}")

# Run the bot
app.run()