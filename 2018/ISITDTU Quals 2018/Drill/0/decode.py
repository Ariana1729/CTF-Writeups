mclist={'...--': '3', '--..--': ',', '....-': '4', '.....': '5', '-...': 'B', '-..-': 'X', '.-.': 'R', '--.-': 'Q', '--..': 'Z', '.': 'E', '.----.': "'", '..---': '2', '.--': 'W', '.-': 'A', '..': 'I', '-.-.': 'C', '---...': ':', '---': 'O', '-.--': 'Y', '-': 'T', '-..-.': '/', '.--.-.': '@', '.-..': 'L', '...': 'S', '..-': 'U', '..--..': '?', '.----': '1', '-----': '0', '-.-': 'K', '-..': 'D', '----.': '9', '-....': '6', '-...-': '=', '.---': 'J', '.--.': 'P', '.-.-.-': '.', '--': 'M', '-.': 'N', '....': 'H', '---..': '8', '...-': 'V', '--...': '7', '--.': 'G', '..-.': 'F', '-....-': '-'}
from PIL import Image
img=Image.open("key.png","r")
pixels=list(img.getdata())
mcode="".join([chr(i[0]) for i in pixels])
mcode=mcode[:mcode.find("\x00")].split(" ")[:-1]
print mcode
pw="".join([mclist[i] for i in mcode])
print pw
print pw.lower()