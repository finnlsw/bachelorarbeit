# -*- coding: utf-8 -*-
import subprocess

def unzip(date):  # Replace this with your actual date e.g. "2023-08-11"
    zip_file_path = f"/home/fmahnken/PycharmProjects/data/{date}.zip"
    destination_path = "/home/fmahnken/PycharmProjects/data"
    command = ["unzip", zip_file_path, "-d", destination_path]
    subprocess.run(command, check=True)
    print(f"file '{zip_file_path}' unziped.")
    subprocess.run(["rm", zip_file_path])
    print(f"file '{zip_file_path}' removed.")

#test:
#unzip("2023-08-11" )

