from tkinter import *

from common.alg_merkle_hellman import AlgMerkleHellman
from common.const import *
from common.md5 import MD5
from common.work_file import *


def create_keys():
    key = recipient.CreateKeys()
    write_json_file(DIR_KEY, key)


def get_message():
    message = read_json_file(DIR_MSG_TXT)
    text = message["text"]
    signature = message["signature"]
    set_text(text)
    signature = recipient.Decrypt(signature)
    hash_msg = hasher.Process(text)
    result_check.set(
        "Сообщение не изменено" if hash_msg == signature else "Сообщение изменено"
    )


def set_text(text):
    entry.delete("1.0", END)
    entry.insert("1.0", text)


recipient = AlgMerkleHellman()
hasher = MD5()
root = Tk()
root.title("Получатель")
root.geometry("300x250")

Button(root, text="Генерация ключей", command=create_keys, width=40).grid(
    row=0, column=0, padx=5, pady=5, columnspan=2
)
Button(root, text="Получить сообщение", command=get_message).grid(row=2, column=0)
result_check = StringVar()
result_check_label = Label(root, textvariable=result_check)
result_check_label.grid(row=2, column=1)
entry = Text(root, width=35, height=10)
entry.grid(row=1, column=0, columnspan=2, pady=5)
