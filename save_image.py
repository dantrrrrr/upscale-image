import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

image_url = "https://replicate.delivery/pbxt/WJOGHaYS4nauKlemUn9PKg2Ren1X75fZeRQWgRj6DKkhFyIEB/output.png"
filename = "output_image.png"

urllib.request.urlretrieve(image_url, filename)
print("Image saved successfully.")
