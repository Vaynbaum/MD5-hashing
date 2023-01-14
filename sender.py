from tkinter import *

from common.const import *
from common.work_file import *
from common.alg_merkle_hellman import AlgMerkleHellman
from common.md5 import MD5


def encrypt_message():
    key = read_json_file(DIR_KEY)
    text = editor.get("1.0", "end")
    text = text[:len(text)-1]
    hash = hasher.Process(text)
    signature = sender.Encrypt(hash, key)
    message = {"text": text, "signature": signature}
    write_json_file(DIR_MSG_TXT, message)


root = Tk()
root.title("Отправитель")
root.geometry("300x250")
sender = AlgMerkleHellman()
hasher = MD5()

Button(root, text="Отправить сообщение", command=encrypt_message).pack(
    side=BOTTOM, pady=5
)
editor = Text(root)
editor.pack(anchor=N, fill=X, pady=5)
