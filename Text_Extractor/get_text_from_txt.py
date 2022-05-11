def get_text_from_txt(INPUT_PATH):
    with open(INPUT_PATH, 'r') as file:
        data = file.read().rstrip()
    print("Extracted text from txt: \n\n\n", data, "\n\n\n")
    return data