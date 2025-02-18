

import requests
from pyrogram import Client, filters
from imdb import IMDb
from wordpress_xmlrpc import Client as WPClient
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client

# Define your bot API credentials and WordPress API credentials
api_id = 26847865
api_hash = "0ef9fdd3e5f1ed49d4eb918a07b8e5d6"
bot_token = "6941908449:AAHNGisGgioOKPDWj5dLQGeB6NOFuMtUs_M"
wp_url = "https://jnmovies.site"
wp_username = "bot"
wp_password = "6wQn rEDj lngb XrcK CbsW No2L"

# Initialize the bot
app = Client("imdb_scraper_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize IMDbPY
ia = IMDb()

# Initialize WordPress client
wp_client = WPClient(wp_url + "/xmlrpc.php", wp_username, wp_password)

def scrape_imdb(imdb_url):
    # Get IMDb movie ID from the URL
    imdb_id = imdb_url.split("/")[-2]
    
    # Fetch movie details using IMDbPY
    movie = ia.get_movie(imdb_id)
    
    # Extract required data
    title = movie["title"]
    poster_url = movie["full-size cover url"]
    rating = movie.get("rating", "N/A")
    genre = movie.get("genres", [])
    storyline = movie.get("plot", ["N/A"])[0]
    director = ", ".join([director["name"] for director in movie.get("directors", [])])
    writer = ", ".join([writer["name"] for writer in movie.get("writers", [])])
    cast = ", ".join([actor["name"] for actor in movie.get("cast", [])])
    
    return {
        "title": title,
        "poster_url": poster_url,
        "rating": rating,
        "genre": genre,
        "storyline": storyline,
        "director": director,
        "writer": writer,
        "cast": cast
    }

def upload_image_to_wp(image_url):
    # Download the image
    img_data = requests.get(image_url).content
    file_name = image_url.split("/")[-1]

    # Prepare the image for WordPress media upload
    data = {
        "name": file_name,
        "type": "image/jpeg",
        "bits": xmlrpc_client.Binary(img_data)
    }

    # Upload image to WordPress
    response = wp_client.call(media.UploadFile(data))
    return response["id"], response["url"]

@app.on_message(filters.photo)
async def handle_image(client, message):
    # Send a message to ask for the IMDb URL
    await message.reply("Please provide the IMDb link for the movie:")

    # Wait for the user's response
    response = await client.listen(message.chat.id)
    imdb_url = response.text.strip()

    # Scrape IMDb details
    imdb_data = scrape_imdb(imdb_url)

    # Upload movie poster to WordPress
    poster_id, poster_url = upload_image_to_wp(imdb_data["poster_url"])

    # Create a new post in WordPress
    post = posts.NewPost()
    post.title = imdb_data["title"]
    post.content = f"""
    <h2>{imdb_data["title"]}</h2>
    <p><strong>Rating:</strong> {imdb_data["rating"]}</p>
    <p><strong>Genre:</strong> {', '.join(imdb_data["genre"])}</p>
    <p><strong>Storyline:</strong> {imdb_data["storyline"]}</p>
    <p><strong>Director:</strong> {imdb_data["director"]}</p>
    <p><strong>Writer:</strong> {imdb_data["writer"]}</p>
    <p><strong>Cast:</strong> {imdb_data["cast"]}</p>
    """
    post.thumbnail = poster_id
    post.post_status = "publish"

    # Upload the post
    wp_client.call(posts.NewPost(post))

    await message.reply("Post has been published to WordPress with the movie details!")

app.run()