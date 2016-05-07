import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_PATH = os.path.join("IP = ", BASE_DIR, 'Just_game', 'Pictures')

print(IMAGE_PATH)
if __name__ == "__main__":
    print(BASE_DIR)