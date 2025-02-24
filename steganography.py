from PIL import Image

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # End of message delimiter

    if len(binary_message) > img.width * img.height * 3:
        raise ValueError("Message is too long to be encoded in the image.")

    pixels = list(img.getdata())
    index = 0

    for i in range(len(pixels)):
        pixel = list(pixels[i])
        for j in range(3):  # RGB
            if index < len(binary_message):
                pixel[j] = pixel[j] & ~1 | int(binary_message[index])
                index += 1
        pixels[i] = tuple(pixel)

    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(pixels)
    encoded_img.save(output_path)

def decode_message(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary_message = ''

    for pixel in pixels:
        for value in pixel[:3]:  # RGB
            binary_message += str(value & 1)

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '11111110':  # End of message delimiter
            break
        message += chr(int(byte, 2))

    return message