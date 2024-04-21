import json
import time
import random
from pynput.keyboard import Key, KeyCode, Controller
from typing import Union


class Worker:
    def __init__(self,
                 profile: str = "profiles/settings.json",
                 commands: str = "commands/example.json"
                 ):
        self.settings = self.load_config(profile)
        self.commands = self.load_config(commands)

        self.start_threads = False

    @staticmethod
    def load_config(file_dir: str) -> dict:
        with open(file_dir, 'r') as f:
            return json.load(f)

    @staticmethod
    def get_key_name(key: Union[Key, KeyCode]) -> str:
        """Return the name of the key pressed."""
        try:
            return key.char  # Type: ignore
        except AttributeError:
            return key.name  # Type: ignore

    def random_wait(self, wait_time: int, random_wait: bool):
        random_time = random.uniform(0, self.settings['random_time']) if random_wait else 0
        time.sleep(random_time + wait_time)

    def start_group(self, group: dict):
        is_peanut_active = True
        while is_peanut_active:
            with open('peanut.json', 'r') as file:
                peanut_data = json.load(file)
                is_peanut_active = peanut_data['active']

            keyboard = Controller()
            if 'command' in group:
                self.random_wait(group['delay'], group['random_wait'])
                keyboard.type(group['command'])
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)

            if 'commands' in group:
                commands = group['commands']
                if 'random_pick' in group:
                    random_pick = group['random_pick']
                else:
                    random_pick = False  # de-nest shit

                if random_pick:
                    self.random_wait(group['delay'], group['random_wait'])
                    command = random.choice(commands)
                    keyboard.type(command)
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)

                else:
                    for command in commands:
                        self.random_wait(group['delay'], group['random_wait'])
                        keyboard.type(command)
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)

    def on_start_press(self, key):
        key_name = self.get_key_name(key)
        # Start when pressing start_key
        if key_name == self.settings['start_key']:
            print('Starting messages!')
            self.start_threads = True
            return False

    def on_stop_press(self, key):
        key_name = self.get_key_name(key)
        # Exit when pressing exit_key
        if key_name == self.settings['exit_key']:
            print('Stopping! Let the last ones get through or just spam Ctrl+D or C')
            # Cursed shit
            with open('peanut.json', 'w') as file:
                json.dump({'active': False}, file, indent=4)
            return False
