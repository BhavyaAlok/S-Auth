import qrcode
import random
import string
import hashlib
import subprocess

def generate_key():
  # get random key of 64 bytes
  length = random.randrange(10000)
  characters = string.digits
  text = ''.join(random.choice(characters) for i in range(length))
  key = hashlib.sha512(str(text).encode("utf-8")).hexdigest()
  #print(key)
  #print(len(key))
  return key

def generate_QRCode(key):
  #Creating a QRCode object of the size specified by the user
  qr = qrcode.QRCode(version = 20, box_size = 10, border = 5)
  qr.add_data(key) #Adding the data to be encoded to the QRCode object
  qr.make(fit = True) #Making the entire QR Code space utilized
  img = qr.make_image() #Generating the QR Code
  img.save("static/images/qr.png") #Saving the QR Code
  return img

def get_otp(key):
  otp = subprocess.check_output(f"java generate_HOTP.java {key}", stderr = subprocess.PIPE)
  otp = otp.decode()
  print("OTP: ", otp)
  return otp