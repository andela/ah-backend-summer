import tempfile
from PIL import Image

image = Image.new("RGB", (50, 100), (255, 255, 255))
image_file = tempfile.NamedTemporaryFile(suffix=".jpg")
image.save(image_file)
image = open(image_file.name, "rb")

valid_partial_profile_data = {
    "bio": "okay"
}

no_username_data = {
    "username": ""
}

no_image_data = {
    "image": ""
}

no_username_image_data = {
    "username": "",
    "image": ""
}

valid_profile_data = {
    "username": "nice",
    "first_name": "first",
    "last_name": "last",
    "bio": "okay",
    "image": image
}

another_user_register_data = {
    "email": "admin123@email.com",
    "username": "admin123",
    "password": "pass1234"
}

another_user_login_data = {
    "email": "admin123@email.com",
    "password": "pass1234"
}

initial_profile_data = {
    "username": "abc123",
    "image": "/media/author.jpg"
}

non_profile_fields_data = {
    "okay": "ksbajk"
}

no_image_error = "The submitted data was not a file. \
Check the encoding type on the form."

no_username_error = "This field may not be blank."
