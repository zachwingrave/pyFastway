import itertools, threading, time, sys

LOADING = False

def set_loading(loading):
    LOADING = loading
    return LOADING



def animate_cycles(cycles):
    frames = ["[|]", "[/]", "[-]", "[\\]"]
    counter = 0
    while counter < cycles:
        for frame in frames:
            stdout.write(frame)
            sleep(0.1)
    print("Done!")

def test_animate_cycles(cycles=200):
    return animate_cycles(cycles)



def animate_thread():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

def test_animate_thread():
    t = threading.Thread(target=animate, daemon=True)
    t.start()
    #long process here
    time.sleep(5)
    done = True
    return done



def animate_while():
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

def test_animate_while():
    return animate_while()



def test():
    print('start test')
    test_animate_cycles()
    # test_animate_thread()
    # test_animate_while()
    print('stop test')