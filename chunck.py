import tiktoken
import os 

from dotenv import load_dotenv
from pathlib import Path

CHUNCK_SIZE = 400
CHUNCK_OVERLAP = 50


def chunck() :
    load_dotenv()
    # Data Folder
    data_folder_path = Path("data")
    encoder = tiktoken.encoding_for_model(os.getenv("MODEL"))

    chuncks = []
    #Iterate over each data file
    for file_path in data_folder_path.iterdir():
        if file_path.is_file() and file_path.suffix == ".txt":

            file_content = file_path.read_text()
            tokens = encoder.encode(file_content)


            for start_index in range(0, len(tokens), CHUNCK_SIZE - CHUNCK_OVERLAP):

                end_index = start_index + CHUNCK_SIZE

                encoded_chuck = tokens[start_index:end_index]
                decoded_chuck = encoder.decode(encoded_chuck)

                chuncks.append({"text" : decoded_chuck, "file_path" : file_path.name})
    return chuncks





