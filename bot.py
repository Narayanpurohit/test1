from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
import os
import ffmpeg


# ---------- Variables Section ----------
API_ID = 15191874
API_HASH = "3037d39233c6fad9b80d83bb8a339a07"
BOT_TOKEN = "7481801715:AAEV22RePMaDqd2tyxH0clxtnqd5hDpRuTw"
SESSION_STRING = "BQDnz0IAY8r1MeaIpWz1oAXpRCe4lzzvNN0MQn45SFksDpFYx0bVIYubTexsw1afXfLKMkKDYsh5byBXrPOpVVZwJ4pOQuUsZtg3_YpM7TfZ2RIz-kGHzd9RtGgIVCTSLVfhjZg3RkIDw_nv91Dx9xEsQL2BrcW2ijz9oZlNhmGM_V9Zosqp3wk3U4YqRxUlQDEGAa73jsb9CeYZJNrG_cgjKQWQxIq2kC-VIQkuu6iEtXRr863OBGE4WLwVCQYP-detekvPe-OrU9Y2ftPPMDMrOS0Mj793qHieU3pE0GT4kXjWZdESx2uWHEfhw9FW4_IbUgaEAAsuOb_3IOzNvc3mqsE-sgAAAAFNo2ggAA"
MONGODB_URI = "mongodb+srv://1by1themes:3snVjsLPmZ9xcbd3@cluster0.uaazt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
QR_IMAGE_LINK = "https://envs.sh/jf1.jpg"
UPI_ID = "example@upi"
LOG_CHANNEL_ID = -1001814601330  # Replace with your log channel ID


# Default Watermark Settings
DEFAULT_WATERMARK = {
    "type": "text",  # Can be "text" or "image"
    "content": "Default Watermark",  # Default text or path to image
    "size": "medium",  # small, medium, large, x-large
    "position": "center"  # center, top-left, top-right, bottom-left, bottom-right
}

# Plans Configuration
PLANS = {
    "Free": {
        "daily_upload_limit": 5 * 1024 * 1024 * 1024,  # 5 GB
        "file_size_limit": 2 * 1024 * 1024 * 1024,  # 2 GB
        "parallel_process": 1,
        "time_gap": 2 * 60,  # 2 minutes
        "auto_watermark": False
    },
    "Basic": {
        "daily_upload_limit": 20 * 1024 * 1024 * 1024,  # 20 GB
        "file_size_limit": 2 * 1024 * 1024 * 1024,  # 2 GB
        "parallel_process": 1,
        "time_gap": 0,
        "auto_watermark": False
    },
    "Standard": {
        "daily_upload_limit": 50 * 1024 * 1024 * 1024,  # 50 GB
        "file_size_limit": 4 * 1024 * 1024 * 1024,  # 4 GB
        "parallel_process": 1,
        "time_gap": 0,
        "auto_watermark": False
    },
    "Premium": {
        "daily_upload_limit": 80 * 1024 * 1024 * 1024,  # 80 GB
        "file_size_limit": 4 * 1024 * 1024 * 1024,  # 4 GB
        "parallel_process": 1,
        "time_gap": 0,
        "auto_watermark": True
    }
}

# Initialize Bot and Database
app = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
client = MongoClient(MONGODB_URI)
db = client["video_bot"]
users = db["users"]

# ---------- Helper Functions ----------
def initialize_user(user_id, name):
    """Initialize new user with default settings."""
    if not users.find_one({"user_id": user_id}):
        users.insert_one({
            "user_id": user_id,
            "name": name,
            "plan": "Free",
            "daily_upload": 0,
            "watermark": DEFAULT_WATERMARK
        })

def get_user_plan(user_id):
    """Fetch user's plan."""
    user = users.find_one({"user_id": user_id})
    return user.get("plan", "Free") if user else "Free"

def get_user_watermark(user_id):
    """Fetch user's watermark settings."""
    user = users.find_one({"user_id": user_id})
    return user.get("watermark", DEFAULT_WATERMARK)

# ---------- Bot Handlers ----------
@app.on_message(filters.command("start"))
def start_command(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    initialize_user(user_id, name)
    message.reply_text(
        f"Welcome {name}!\n"
        "I'm your video processing bot.\n\n"
        "Use /help to see the available commands."
    )

@app.on_message(filters.command("help"))
def help_command(client, message):
    message.reply_text(
        "Available Commands:\n"
        "/upgrade - View subscription plans\n"
        "/set_watermark - Configure watermark settings\n"
        "Send a video to apply your watermark."
    )

@app.on_message(filters.command("upgrade"))
def upgrade_command(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌱 Free", callback_data="plan_free")],
        [InlineKeyboardButton("⚡ Basic", callback_data="plan_basic")],
        [InlineKeyboardButton("⭐ Standard", callback_data="plan_standard")],
        [InlineKeyboardButton("🌟 Premium", callback_data="plan_premium")]
    ])
    message.reply_text("Choose a plan to see details:", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"plan_(free|basic|standard|premium)"))
def plan_details(client, callback_query):
    plan = callback_query.data.split("_")[1].capitalize()
    details = PLANS[plan]
    text = (
        f"{plan} Plan Details:\n"
        f"✶ Daily Upload: {details['daily_upload_limit'] // (1024 ** 3)} GB\n"
        f"✶ File Upload Size: {details['file_size_limit'] // (1024 ** 3)} GB\n"
        f"✶ Parallel Processes: {details['parallel_process']}\n"
        f"✶ Time Gap: {'No' if details['time_gap'] == 0 else f'{details['time_gap'] // 60} Minutes'}\n"
        f"✶ Auto Watermark: {'Yes' if details['auto_watermark'] else 'No'}"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Buy Plan", callback_data=f"buy_{plan.lower()}")],
        [InlineKeyboardButton("Back", callback_data="upgrade")]
    ])
    callback_query.message.edit_text(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"buy_(free|basic|standard|premium)"))
def buy_plan(client, callback_query):
    plan = callback_query.data.split("_")[1].capitalize()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Send Screenshot to Owner", url="t.me/OWNER_USERNAME")]
    ])
    callback_query.message.edit_text(
        f"To purchase the {plan} plan, pay using the following details:\n\n"
        f"UPI ID: {UPI_ID}\n\n"
        f"After payment, send a screenshot using the button below.",
        reply_markup=keyboard
    )

@app.on_message(filters.command("set_watermark"))
def set_watermark_command(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Image", callback_data="watermark_image")],
        [InlineKeyboardButton("Text", callback_data="watermark_text")]
    ])
    message.reply_text("Choose watermark type:", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"watermark_(image|text)"))
def watermark_type(client, callback_query):
    watermark_type = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    users.update_one({"user_id": user_id}, {"$set": {"watermark.type": watermark_type}})
    callback_query.message.reply_text(
        f"Send your {watermark_type} watermark content (text or image)."
    )

# More Handlers for Video Upload and Processing Would Go Here


@app.on_message(filters.video | filters.document)
def video_handler(client, message):
    user_id = message.from_user.id
    user_data = users.find_one({"user_id": user_id})
    if not user_data:
        message.reply_text("Please use /start first to initialize your account.")
        return

    # Check for daily upload limit
    plan = user_data["plan"]
    plan_details = PLANS[plan]
    daily_upload = user_data.get("daily_upload", 0)
    if daily_upload >= plan_details["daily_upload_limit"]:
        message.reply_text("You've reached your daily upload limit. Upgrade your plan using /upgrade.")
        return

    # File size check
    file_size = message.video.file_size if message.video else message.document.file_size
    if file_size > plan_details["file_size_limit"]:
        message.reply_text("The file size exceeds your plan's limit. Upgrade your plan to upload larger files.")
        return

    # Auto watermark check
    if not plan_details["auto_watermark"]:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="rename_yes")],
            [InlineKeyboardButton("No", callback_data="rename_no")]
        ])
        message.reply_text("Do you want to rename the file?", reply_markup=keyboard)
        app.set_chat_data(user_id, "video_message", message)
    else:
        process_video(client, message, user_data)


@app.on_callback_query(filters.regex(r"rename_(yes|no)"))
def rename_file_callback(client, callback_query):
    user_id = callback_query.from_user.id
    action = callback_query.data.split("_")[1]

    if action == "yes":
        callback_query.message.reply_text("Send me the new file name (without extension).")
        app.set_chat_data(user_id, "rename_file", True)
    else:
        video_message = app.get_chat_data(user_id, "video_message")
        if video_message:
            user_data = users.find_one({"user_id": user_id})
            process_video(client, video_message, user_data)
        else:
            callback_query.message.reply_text("Error: Video not found. Please try again.")


@app.on_message(filters.text)
def rename_file_handler(client, message):
    user_id = message.from_user.id
    rename_file_flag = app.get_chat_data(user_id, "rename_file")

    if rename_file_flag:
        new_file_name = message.text.strip()
        app.set_chat_data(user_id, "new_file_name", new_file_name)
        video_message = app.get_chat_data(user_id, "video_message")
        if video_message:
            user_data = users.find_one({"user_id": user_id})
            process_video(client, video_message, user_data, new_file_name)
        else:
            message.reply_text("Error: Video not found. Please try again.")
        app.set_chat_data(user_id, "rename_file", False)  # Reset rename flag


def process_video(client, message, user_data, new_file_name=None):
    user_id = message.from_user.id
    file_id = message.video.file_id if message.video else message.document.file_id
    file_name = new_file_name or message.video.file_name or message.document.file_name

    # Download video
    download_path = app.download_media(file_id, file_name=file_name)
    watermark_settings = user_data["watermark"]

    # Apply watermark
    processed_path = f"processed_{file_name}"
    try:
        apply_watermark(download_path, processed_path, watermark_settings)
    except Exception as e:
        message.reply_text(f"Failed to process video: {e}")
        os.remove(download_path)
        return

    # Upload to log channel if size exceeds 2 GB
    file_size = os.path.getsize(processed_path)
    if file_size > 2 * 1024 * 1024 * 1024:  # 2 GB
        with Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH) as user_client:
            sent_message = user_client.send_video(
                LOG_CHANNEL_ID, 
                video=processed_path,
                caption=f"Processed video from user {user_id}."
            )
            message.reply_text("Your video is ready! Sending as a copy.")
            client.copy_message(
                chat_id=user_id,
                from_chat_id=LOG_CHANNEL_ID,
                message_id=sent_message.message_id
            )
    else:
        message.reply_video(video=processed_path, caption="Here is your processed video!")

    # Cleanup
    os.remove(download_path)
    os.remove(processed_path)

    # Update daily upload
    users.update_one({"user_id": user_id}, {"$inc": {"daily_upload": file_size}})


def apply_watermark(input_path, output_path, watermark_settings):
    watermark_type = watermark_settings["type"]
    content = watermark_settings["content"]
    position = watermark_settings["position"]
    size = watermark_settings["size"]

    # Watermark position mapping
    position_map = {
        "top-left": "10:10",
        "top-right": "main_w-overlay_w-10:10",
        "bottom-left": "10:main_h-overlay_h-10",
        "bottom-right": "main_w-overlay_w-10:main_h-overlay_h-10",
        "center": "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
    }
    pos = position_map.get(position, "10:10")

    if watermark_type == "text":
        ffmpeg.input(input_path).drawtext(
            text=content,
            fontsize=24 if size == "small" else 36 if size == "medium" else 48,
            x=pos.split(":")[0],
            y=pos.split(":")[1],
            fontcolor="white"
        ).output(output_path).run()
    elif watermark_type == "image":
        ffmpeg.input(input_path).overlay(ffmpeg.input(content), x=pos.split(":")[0], y=pos.split(":")[1]).output(output_path).run()
    else:
        raise ValueError("Invalid watermark type.")
        
        
# ---------- Run Bot ----------
if __name__ == "__main__":
    app.run()