
def ceaser_cipher_encode(message,shift):
    result = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result += chr(base+shifted)
        else:
            result+=char
    return result

def ceaser_cipher_decode(message,shift):
    return ceaser_cipher_encode(message,-shift)

message = input("Enter the message: ")
shift = 5

encoded_msg = ceaser_cipher_encode(message,shift)
print(f"Encoded message: {encoded_msg}")
decoded_msg = ceaser_cipher_decode(encoded_msg,shift)
print(f"Decoded message: {decoded_msg}")