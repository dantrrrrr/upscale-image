import replicate
import urllib.request
import ssl
# client = replicate.Client(api_token='r8_YvOE8zNTBXBgNAv4amksd9J2MGXnGQN2xPWAR')
ssl._create_default_https_context = ssl._create_unverified_context

output = replicate.run(
    "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
    input={
        "image": open("cat-1_spliced/0001_3.jpg", "rb"),
        "scale": 2,
        "face_enhance": False,
    },
)
print(output)
image_url =output
filename = 'output_image.jpg'

urllib.request.urlretrieve(image_url, filename)
print('Image saved successfully.')



# image_url = "https://replicate.delivery/pbxt/WJOGHaYS4nauKlemUn9PKg2Ren1X75fZeRQWgRj6DKkhFyIEB/output.png"
# filename = "output_image.png"

# urllib.request.urlretrieve(image_url, filename)
# print("Image saved successfully.")
