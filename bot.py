

import requests
from pyrogram import Client, filters
from bs4 import BeautifulSoup
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

# Initialize WordPress client
wp_client = WPClient(wp_url + "/xmlrpc.php", wp_username, wp_password)

def scrape_imdb(imdb_url):
    response = requests.get(imdb_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data from IMDb
    title = soup.find("h1").text.strip()
    poster_url = soup.find("div", class_="poster").find("img")["src"]
    rating = soup.find("span", itemprop="ratingValue").text.strip()
    genre = [genre.text.strip() for genre in soup.find_all("span", class_="sc-16ede4f7-2")]

    storyline = soup.find("span", data-testid="plot-xl").text.strip()
    director = soup.find("a", {"href": lambda x: x and x.startswith("/name")}).text.strip()
    writer = [writer.text.strip() for writer in soup.find_all("a", {"href": lambda x: x and x.startswith("/name")})]
    cast = [actor.text.strip() for actor in soup.find_all("a", {"href": lambda x: x and x.startswith("/name")})]

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
    <p><strong>Writer:</strong> {', '.join(imdb_data["writer"])}</p>
    <p><strong>Cast:</strong> {', '.join(imdb_data["cast"])}</p>
    """
    post.thumbnail = poster_id
    post.post_status = "publish"

    # Upload the post
    wp_client.call(posts.NewPost(post))

    await message.reply("Post has been published to WordPress with the movie details!")

app.run()