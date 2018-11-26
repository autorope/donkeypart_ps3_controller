The code for this part was copied from [Tawn Kramer's](https://github.com/tawnkramer/donkey) fork of donkeycar.

# PS3 Joystick Controller

The default web controller may be replaced with a one line change to use a physical joystick part for input. This uses 
the OS device /dev/input/js0 by default. In theory, any joystick device that the OS mounts like this can be used. In 
practice, the behavior will change depending on the model of joystick ( Sony, or knockoff ), or XBox controller 
and the Bluetooth driver used to support it. The default code has been written and tested with
 a [Sony brand PS3 Sixaxis controller](https://www.amazon.com/Dualshock-Wireless-Controller-Charcoal-playstation-3). 
 Other controllers may work, but will require alternative Bluetooth installs, and tweaks to the software for correct 
 axis and buttons.

These can be used plugged in with a USB cable - but the default code and os driver has a bug polling this configuration. 
It's been much more stable, and convenient, to setup Bluetooth for a wireless, responsive control.

## Install

1. Connect your bluetooth controller to the raspberry pi. See the Bluetooth section below.

2. Install the parts python package.
    ```bash
    pip install git+https://github.com/autorope/donkeypart_ps3_controller.git
    ```

3. Import the part at the top of your manage.py script.
    ```python
    from donkeypart_ps3_controller import PS3Joystick
    ```   
    
4. Replace the controller part of your manage.py to use the JoysticController part.
    ```python
    ctr = PS3JoystickController(
       max_throttle=cfg.JOYSTICK_MAX_THROTTLE,
       steering_scale=cfg.JOYSTICK_STEERING_SCALE,
       throttle_axis=cfg.JOYSTICK_THROTTLE_AXIS,
       auto_record_on_throttle=cfg.AUTO_RECORD_ON_THROTTLE
    )

     V.add(ctr,
          inputs=['cam/image_array'],
          outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
          threaded=True)
    ```

5. Add the required config paramters to your config.py file. It should look something like this.
    ```python
    #JOYSTICK
    JOYSTICK_MAX_THROTTLE = 0.25
    JOYSTICK_STEERING_SCALE = 1.0
    JOYSTICK_THROTTLE_AXIS = 'rz'
    AUTO_RECORD_ON_THROTTLE = True
    ```
6. Now you're ready to run the `python manage.py drive` command to start your car. 

### Bluetooth Setup

Follow [this guide](https://pythonhosted.org/triangula/sixaxis.html). You can ignore steps past the 'Accessing 
the SixAxis from Python' section. I will include steps here in case the link becomes stale.

``` bash
sudo apt-get install bluetooth libbluetooth3 libusb-dev
sudo systemctl enable bluetooth.service
sudo usermod -G bluetooth -a pi
```

Reboot after changing the user group.

Plug in the PS3 with USB cable. Hit center PS logo button. Get and build the command line pairing tool. Run it:

```bash
wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair sixpair.c -lusb
sudo ./sixpair
```

Use bluetoothctl to pair
```bash
bluetoothctl
agent on
devices
trust <MAC ADDRESS>
default-agent
quit
```

Unplug USB cable. Hit center PS logo button.

To test that the Bluetooth PS3 remote is working, verify that /dev/input/js0 exists.

```bash
ls /dev/input/js0
```

### Charging PS3 Sixaxis Joystick

For some reason, this joystick doesn't like to charge in a powered USB port that doesn't have an active Bluetooth 
control and OS driver. This means a phone type USB charger will not work, and charging from a Windows machine doesn't 
work either.

You can always charge from the Raspberry Pi, though.  Just plug the joystick into the Pi and power the Pi using a 
charger or your PC, and you are good to go.

### New Battery for PS3 Sixaxis Joystick

Sometimes these controllers can be quite old. Here's a link to a [new battery](http://a.co/5k1lbns). Be careful when 
taking off the cover. Remove 5 screws. There's a tab on the top half between the hand grips. You'll want to split/open
 it from the front and try pulling the bottom forward as you do, or you'll break the tab off as I did.


### Joystick Controls

* Left analog stick - Left and right to adjust steering
* Right analog stick - Forward to increase forward throttle
* Pull back twice on right analog to reverse

> Whenever the throttle is not zero, driving data will be recorded - as long as you are in User mode!

* Select button switches modes - "User, Local Angle, Local(angle and throttle)"
* Triangle - Increase max throttle
* X  - Decrease max throttle
* Circle - Toggle recording (disabled by default. auto record on throttle is enabled by default)
* dpad up - Increase throttle scale
* dpad down - Decrease throttle scale
* dpad left - Increase steering scale
* dpad right - Decrease steering scale
* Start - Toggle constant throttle. Sets to max throttle (modified by X and Triangle).

### Driving tips
Hit the Select button to toggle between three modes - User, Local Angle, and Local Throttle & Angle.

* User - User controls both steering and throttle with joystick
* Local Angle - Ai controls steering, user controls throttle
* Local Throttle & Angle - Ai controls both steering and throttle

When the car is in Local Angle mode, the NN will steer. You must provide throttle.
