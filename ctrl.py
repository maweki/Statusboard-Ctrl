#!/usr/bin/python3

# apt install python3-gpiozero python3-pip
# pip3 install RPi.GPIO

import time
timefunc = time.monotonic

def call(path):
    import os
    from subprocess import run
    sdir = os.path.dirname(os.path.realpath(__file__))
    e = os.path.join(sdir, path)
    if os.path.exists(e):
        # print("calling", e)
        return run([e])
    else:
        # print("no script", e)
        pass

class statusline(object):
    __next_sched = 0
    red = None
    green = None

    def __init__(self, prefix):
        self.__prefix = prefix

    @property
    def next_sched(self):
        return self.__next_sched

    @property
    def prefix(self):
        return self.__prefix

    def press(self):
        print(self.prefix, "pressed")
        call(self.prefix + ".btn")

    def check(self, interval):
        # call check script
        ret = call(self.prefix)

        if ret:
            # Set Leds
            if ret.returncode == 0:
                self.green.on()
                self.red.off()
            elif ret.returncode == 1:
                self.green.off()
                self.red.off()
            elif ret.returncode == 2:
                self.green.on()
                self.red.on()
            else:
                self.green.off()
                self.red.on()

        # set interval
        self.__next_sched = timefunc() + interval

def idx_to_identifier(idx):
    return 'l' + str(idx)

def main(args):
    global timefunc
    if args.system:
        timefunc = time.time

    line_it = tuple(map(str, range(1,4) if args.zero else range(1,6)))
    lines = list(map(statusline, line_it))
    identifiers = list(map(idx_to_identifier, line_it))

    # print("init with", identifiers)
    if args.zero:
        # print("zero")
        from gpiozero import StatusZero
        sb = StatusZero(*identifiers)
    else:
        # print("board")
        from gpiozero import StatusBoard
        sb = StatusBoard(*identifiers)
    print(sb)

    # attach leds
    # print("leds")
    for l in lines:
        l.green = sb.__getattr__(idx_to_identifier(l.prefix)).lights.green
        l.red = sb.__getattr__(idx_to_identifier(l.prefix)).lights.red
        l.red.on()
        l.green.on()
        time.sleep(0.2)
        l.red.off()
        l.green.off()

    print("callbacks")
    # attach buttons
    if not args.zero:
        for l in lines:
            sb.__getattr__(idx_to_identifier(l.prefix)).button.when_pressed = l.press

    # loop
    while True:
        lines[0].check(args.interval)
        lines.sort(key=lambda x: x.next_sched)
        time.sleep(max(0, lines[0].next_sched - timefunc()))



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Status Board Control")
    parser.add_argument("-i", "--interval", type=int, default=30)
    parser.add_argument("--zero", action='store_const', const=True, default=False, help="Status Board is a Zero, without button support")
    parser.add_argument("--system", action='store_const', const=True, default=False, help="Use system time instead of monotonic time")
    main(parser.parse_args())
