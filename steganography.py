from PIL import Image

# Constants
END_OF_MESSAGE_DELIMITER = '1111111111111110'  # 16-bit delimiter to mark the end of the message

def _message_to_binary(message):
    """Convert a message string to a binary string."""
    return ''.join(format(ord(char), '08b') for char in message)

def _binary_to_message(binary_str):
    """Convert a binary string to a message string."""
    message = ''
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        message += chr(int(byte, 2))
    return message

def _validate_image_capacity(image, binary_message):
    """Check if the image has enough capacity to store the binary message."""
    required_pixels = len(binary_message) // 3 + (1 if len(binary_message) % 3 != 0 else 0)
    available_pixels = image.width * image.height
    if required_pixels > available_pixels:
        raise ValueError(f"Message is too long to be encoded in the image. Required pixels: {required_pixels}, Available pixels: {available_pixels}")

def encode_message(image_path, message, output_path):
    """
    Encode a message into an image using LSB steganography.

    :param image_path: Path to the input image.
    :param message: The secret message to encode.
    :param output_path: Path to save the encoded image.
    """
    try:
        # Open the image
        img = Image.open(image_path)
        if img.mode not in ['RGB', 'RGBA']:
            raise ValueError("Image must be in RGB or RGBA mode.")

        # Convert the message to binary and add the delimiter
        binary_message = _message_to_binary(message) + END_OF_MESSAGE_DELIMITER

        # Validate if the image can store the message
        _validate_image_capacity(img, binary_message)

        # Get pixel data
        pixels = list(img.getdata())
        binary_index = 0

        # Encode the message into the image
        new_pixels = []
        for pixel in pixels:
            new_pixel = list(pixel)
            for i in range(3):  # Modify only the RGB channels
                if binary_index < len(binary_message):
                    new_pixel[i] = new_pixel[i] & ~1 | int(binary_message[binary_index])
                    binary_index += 1
            new_pixels.append(tuple(new_pixel))

        # Create and save the encoded image
        encoded_img = Image.new(img.mode, img.size)
        encoded_img.putdata(new_pixels)
        encoded_img.save(output_path)
        print(f"Message encoded successfully and saved to {output_path}")

    except Exception as e:
        raise ValueError(f"Error during encoding: {e}")

def decode_message(image_path):
    """
    Decode a message from an image using LSB steganography.

    :param image_path: Path to the encoded image.
    :return: The decoded message.
    """
    try:
        # Open the image
        img = Image.open(image_path)
        if img.mode not in ['RGB', 'RGBA']:
            raise ValueError("Image must be in RGB or RGBA mode.")

        # Extract binary message from the image
        binary_message = ''
        for pixel in img.getdata():
            for value in pixel[:3]:  # Read only the RGB channels
                binary_message += str(value & 1)

        # Find the end-of-message delimiter
        delimiter_index = binary_message.find(END_OF_MESSAGE_DELIMITER)
        if delimiter_index == -1:
            raise ValueError("No valid message found in the image.")

        # Extract and convert the binary message to text
        binary_message = binary_message[:delimiter_index]
        message = _binary_to_message(binary_message)
        return message

    except Exception as e:
        raise ValueError(f"Error during decoding: {e}")