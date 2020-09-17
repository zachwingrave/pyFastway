from time import sleep
from sys import stdout

LOADING = False

def animate():
    frames = ["|", "/", "-", "\\"]
    message = "Loading, please wait..."

    print("LOADING in animate():", LOADING)

    while LOADING:
        print("Test")
        sleep(1)
        for frame in frames:
            stdout.write(message, frame)
            stdout.flush()
            sleep(0.1)

    print("Done loading.")

def set_loading(loading):
    LOADING = loading
    return LOADING
