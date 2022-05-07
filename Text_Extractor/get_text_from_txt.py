def get_text_from_txt(FILE_PATH):
    with open(FILE_PATH, 'r') as file:
        data = file.read().rstrip()
    return data