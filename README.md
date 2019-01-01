# Statusboard Ctrl

This is a python app to controle a ThePiHut Status board.


## Usage

### Scripts

Best you put your executable scripts in the `scripts` subfolder and then
symlink to `1` to `5` and `1.btn` to `5.btn` in the scripts directory.

The script will be called every `UPDATE` amount of time (default 30 seconds).
Depending on the return code, the leds light up:

* 0 - Green ON, Red OFF
* 1 - Green OFF, Red OFF
* 2 - Green OFF, Red ON
* other - Green OFF, Red ON

If you only use two bits to represent the return code, it basically means
that the last bit stands for NOT Green, while the second to last bit stands
for Red. I'm still thinking about supporting blink mode for the leds but how
do you encode this in a sensible manner in the return code?

The `.btn` script will be called when you press the button. I'm still thinking
about a good interface to support different lengths of button press but for now
this is enough for me.

### Starting as a Service

It's best to install a systemd unit file to manage the service. Here's an example
that works fine:

```
[Unit]
Description=Statusboard Control
After=network.target
[Service]
Type=simple
User=root
ExecStart=/root/statusboard-ctrl/ctrl.py --leds 3 --interval 60
Restart=always
RestartSec=30
[Install]
WantedBy=multi-user.target
```

## Dependencies

* GPIO Zero (v1.4 or above) (like https://github.com/ThePiHut/statusboard)
* RPi.GPIO or other GPIO-lib

```
apt install python3-gpiozero python3-pip
pip3 install RPi.GPIO
```

## TODO

* System calls are currently synchronous, so if your check scripts run in sum longer
than your interval, your mileage will vary
* No blinking
* No double-press, hold, etc. for buttons
