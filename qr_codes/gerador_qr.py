import qrcode
import os


website_link = input("Link do casalpage: ")
name_of_qrcode = input("Nome do casalpage: ").lower().replace(" ", "_")

qr = qrcode.make(website_link)
folder = "qr_codes"
os.makedirs(folder, exist_ok=True)

archives = os.path.join(folder, f"qr_{name_of_qrcode}.png")

qr.save(archives)