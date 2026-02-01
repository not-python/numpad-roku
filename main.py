from roku import Roku
import keyboard

print("Connecting to your Roku...")
try:
    roku = Roku.discover(timeout=10)[0]
    print(f"Connected to {roku.device_info.user_device_name}.")
except:
    print("Failed to find Roku device.\nThis could just require another try or you may need to enable 'Control by mobile apps' in the Roku settings.")
    exit(1)

currently_pressed = set()
numpad_map = {
    71: "back",
    72: "up",
    73: "home",
    75: "left",
    76: "select",
    77: "right",
    79: "volume_down",
    80: "down",
    81: "volume_up"
}


def on_key_event(e):
    if e.scan_code in numpad_map and e.is_keypad:
        if e.event_type == "down":
            action = numpad_map.get(e.scan_code)
            if not action:
                return

            if e.scan_code not in currently_pressed:
                currently_pressed.add(e.scan_code)
                getattr(roku, action)()
                
        elif e.event_type == "up":
            for action in list(currently_pressed):
                if action in numpad_map:
                    currently_pressed.discard(e.scan_code)


keyboard.hook(on_key_event)
keyboard.wait()
