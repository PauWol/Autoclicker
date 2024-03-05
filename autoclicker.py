import sys
from threading import Thread
import threading
from tkinter import messagebox
import pyautogui , keyboard , configparser , time , json
import tkinter as tk
from tkinter import ttk

on:bool = False
root = tk.Tk()

def on_off_hotkey_exe():
    global on
    if on:
        on = False
    else:
        on = True

class Hotkey:
    def __init__(self) -> None:
        self.DEFAULT_HOTKEY = "ö+ä"
        self.hotkey = self.DEFAULT_HOTKEY
        self.rate = 60
        pass

    def load_hotkey_from_config(self):
        try:
            config = configparser.ConfigParser()
            config.read("./config.ini")

            # Check if the section and key exist
            if config.has_option("hotkeys", "hotkey"):
                hotkey = config.get("hotkeys", "hotkey")
                keyboard.add_hotkey(hotkey, on_off_hotkey_exe, suppress=True, trigger_on_release=True)
                print('your Hotkey: {}'.format(hotkey))
                self.hotkey = hotkey
            else:  
                keyboard.add_hotkey(self.DEFAULT_HOTKEY, on_off_hotkey_exe, suppress=True, trigger_on_release=True)  
        except FileNotFoundError:
            keyboard.add_hotkey(self.DEFAULT_HOTKEY, on_off_hotkey_exe, suppress=True, trigger_on_release=True)

    #def save_hotkey_to_config(self,hotkey):
    #    config = {"hotkey": hotkey}
    #    with open("./config.json", "w") as config_file:
   #         json.dump(config, config_file)
    
    def save_hotkey_to_config(self, hotkey):
        # Load existing config (if any)
        config = configparser.ConfigParser()
        config.read("./config.ini")

        # Check if the section exists
        if not config.has_section("hotkeys"):
            config.add_section("hotkeys")

        # Check if the key exists
        #if not config.has_option("hotkeys", "hotkey"):
        config.set("hotkeys", "hotkey", hotkey)
        # Save the updated config
        with open("./config.ini", "w") as config_file:
            config.write(config_file)

    def set_custom_hotkey(self):
        hotkey = None
        try:
            print("Press the keys for your desired hotkey:")
            keys_pressed = []
            while True:
                event = keyboard.read_event(suppress=True)
                if event.event_type == keyboard.KEY_DOWN:
                    keys_pressed.append(event.name)
                elif event.event_type == keyboard.KEY_UP:
                    break
            self.hotkey = "+".join(keys_pressed)
            self.save_hotkey_to_config(self.hotkey)
            print(f"Hotkey '{self.hotkey}' associated with 'Click'.")

            # Register the hotkey
            keyboard.add_hotkey(self.hotkey, on_off_hotkey_exe, suppress=True, trigger_on_release=True)
        except KeyboardInterrupt:
            print("\nHotkey setup interrupted.")


class Clicker:
    def __init__(self) -> None:
        self.rate = 1/60
        self.button_type = 'left'
        self.click_type = 'singel'
        pass

    def set_mouse_button(self,type='left|middel|right'):
        self.button_type = type

    def set_click_rate(self,rate=60):
        self.rate = 1 / rate
        pyautogui.PAUSE = float(self.rate)

    def set_click_type(self,type='singel|doubel|trippel'):
        self.click_type = type
    
    def save_clicker_settings(self):
        config = configparser.ConfigParser()
        config.read("./config.ini")

        if not config.has_section("clicker"):
            config.add_section("clicker")
        options = ['button','rate','type']
        for i in options:

            match i:
                case 'button':
                    value = self.button_type
                case 'rate':
                    value = self.rate
                case 'type':
                    value = self.click_type

            #if not config.has_option("clicker", i):
            config.set("clicker", i, str(value))

            with open("./config.ini", "w") as config_file:
                config.write(config_file)
    def load_clicker_settings(self):
        try:
            config = configparser.ConfigParser()
            config.read("./config.ini")
            options = ['button','rate','type']
            for i in options:
                if config.has_option("clicker", i):
                    val = config.get("clicker", i)
                    match i:
                        case 'button':
                            self.button_type = val
                            print('Button type: {}'.format(val))
                        case 'rate':
                            self.rate = val
                            pyautogui.PAUSE = float(self.rate)
                            print('Rate: {}'.format(val))
                        case 'type':
                            self.click_type = val
                            print('Click type: {}'.format(val))

                else:  
                    print('no settings found!')  
        except FileNotFoundError:
            print('no settingsfile found')

    def click(self):
        match self.button_type:
            case 'left':
                if self.click_type == 'doubel':
                    pyautogui.doubleClick()
                    
                elif self.click_type == 'trippel':
                    pyautogui.tripleClick()
                else:
                    pyautogui.click()
            case 'middel':
                if self.click_type == 'doubel':
                    for i in range(2):
                        pyautogui.middleClick()
                    
                elif self.click_type == 'trippel':
                     for i in range(3):
                        pyautogui.middleClick()
                else:
                    pyautogui.middleClick()
            case 'right':
                if self.click_type == 'doubel':
                    for i in range(2):
                        pyautogui.rightClick()
                    
                elif self.click_type == 'trippel':
                     for i in range(3):
                        pyautogui.rightClick()
                else:
                    pyautogui.rightClick()
def save_settings():
    global cl
    print('Speichern...')
    cl.set_click_rate(int(clickrate_var.get()))
    print(clickrate_var.get())
    cl.set_click_type(str(click_type_var.get()))
    print(click_type_var.get())
    cl.set_mouse_button(str(hotkey_var.get()))
    print(hotkey_var.get())
    cl.save_clicker_settings()

def tkinter(): 
    
    def set_hotkey_combi():
        key.set_custom_hotkey()
        display_value.set(key.hotkey)

    def trigger_hotkey():
        thread = Thread(target=set_hotkey_combi)
        thread.daemon = True
        thread.start()
        #thread.join()


    root.title("Autoclicker")
    # Load the image file from disk.
    icon = tk.PhotoImage(file="cursor.png")

    # Set it as the window icon.
    root.iconphoto(True, icon)
    #root.iconphoto(False, icon)
    style = ttk.Style()
    style.theme_use("clam")

    global clickrate_var , hotkey_var , click_type_var
    clickrate_var = tk.IntVar(value=round(1/float(cl.rate)))
    hotkey_var = tk.StringVar(value=cl.button_type)
    click_type_var = tk.StringVar(value=cl.click_type)
    keys = ["left", "middle", "right"]
    click_types = ["single", "double", "triple"]

    clickrate_label = ttk.Label(root, text="Clickrate:")
    clickrate_label.grid(row=0, column=0, padx=10, pady=10)
    clickrate_input = ttk.Entry(root, width=5, textvariable=clickrate_var, validate="key", validatecommand=(root.register(lambda key: key.isdigit()), '%S'))
    clickrate_input.grid(row=0, column=1, padx=10, pady=10)

    button_label = ttk.Label(root, text="Button:")
    button_label.grid(row=1, column=0, padx=10, pady=10)
    hotkey_frame = ttk.Frame(root)
    hotkey_frame.grid(row=1, column=1, padx=10, pady=10)
    hotkey_buttons = []
    for i, hotkey in enumerate(keys):
        button = ttk.Radiobutton(hotkey_frame, text=hotkey, variable=hotkey_var, value=hotkey)#, command=save_settings
        button.grid(row=i//3, column=i%3, padx=5, pady=5)
        hotkey_buttons.append(button)

    click_type_label = ttk.Label(root, text="Click type:")
    click_type_label.grid(row=2, column=0, padx=10, pady=10)
    click_type_menu = ttk.Combobox(root, textvariable=click_type_var, state="readonly", values=click_types)
    click_type_menu.grid(row=2, column=1, padx=10, pady=10)
    click_type_menu.current(0)

    display_label = ttk.Label(root, text="Hotkey:")
    display_label.grid(row=3, column=0, padx=10, pady=10)
    display_value = tk.StringVar(value=key.hotkey)
    display_field = ttk.Entry(root, width=15, textvariable=display_value, state="readonly")
    display_field.grid(row=3, column=1, padx=10, pady=10)

    hotkey_trigger_button = ttk.Button(root, text="Trigger hotkey", command=trigger_hotkey)
    hotkey_trigger_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    save_button = ttk.Button(root, text="Save", command=save_settings)
    save_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    root.resizable(False, False)
    messagebox.showinfo("Greeting", "Usage:\nHotkeys are set by pressing the requestet combination on your Keyboard.\nAs son as you lift up (up press) a key the ones that were pressed are set as a Hotkey!")
    root.mainloop()

def init():
    global cl , on , key
    cl = Clicker()
    #cl.set_click_rate(10)
    #cl.set_click_type('singel')
    #cl.set_mouse_button('left')
    cl.save_clicker_settings()
    cl.load_clicker_settings()
    key = Hotkey()
    key.load_hotkey_from_config()
    key.save_hotkey_to_config(key.hotkey)
    #key.set_custom_hotkey()
def click_check():
    while True:
        if on:
            cl.click()

def main():  
    init()
    try:
        thread_click_check = Thread(target=click_check)
        thread_click_check.daemon = True
        thread_click_check.start()
        tkinter()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
