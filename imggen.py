from PIL import Image

DELIMITER = "#####"

# ----------------- Bit Utilities -----------------

def to_bits(text):
    return ''.join(f'{b:08b}' for b in text.encode())

def from_bits(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(int(byte, 2))
    return bytes(chars).decode(errors='ignore')

# ----------------- Encode -----------------

def hide_message(img_path, message, out_path):
    img = Image.open(img_path)
    w, h = img.size
    px = img.load()

    message += DELIMITER
    bits = to_bits(message)
    idx = 0

    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]

            if idx < len(bits):
                r = (r & 254) | int(bits[idx]); idx += 1
            if idx < len(bits):
                g = (g & 254) | int(bits[idx]); idx += 1
            if idx < len(bits):
                b = (b & 254) | int(bits[idx]); idx += 1

            px[x, y] = (r, g, b)

            if idx >= len(bits):
                img.save(out_path)
                return

# ----------------- Decode -----------------

def reveal_message(img_path):
    img = Image.open(img_path)
    w, h = img.size
    px = img.load()

    bits = ""

    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

            if len(bits) >= 8:
                text = from_bits(bits)
                if DELIMITER in text:
                    return text.replace(DELIMITER, "")

    return "No hidden message found"

# ----------------- Main -----------------

input_image = "blank.jpg"
output_image = "hi.png"

secret = "album"

hide_message(input_image, secret, output_image)
print("Message hidden in:", output_image)

decoded = reveal_message(output_image)
print("Decoded message:", decoded)
