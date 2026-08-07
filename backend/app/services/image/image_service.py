import os
import secrets

from PIL import Image
from flask import current_app


def save_profile_picture(uploaded_file):

    random_hex = secrets.token_hex(8)

    _, extension = os.path.splitext(uploaded_file.filename)

    filename = random_hex + extension.lower()

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "profile_pictures"
    )

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(
        upload_folder,
        filename
    )

    try:
        image = Image.open(uploaded_file)

        # Convert PNG transparency/RGB issues
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image.thumbnail((300, 300))

        image.save(filepath)

        print("SAVED IMAGE TO:", filepath)

    except Exception as e:
        print("IMAGE UPLOAD ERROR:", e)
        raise e

    return filename