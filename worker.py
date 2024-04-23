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

    def random_wait(self, group):
        if 'random_time' in group:
            random_time = group['random_time']
        else:
            random_time = self.settings['random_time']

        random_time = random.uniform(0, random_time) if 'random_wait' in group else 0
        wait_time = group['wait_time'] if 'wait_time' in group else 0
        time.sleep(random_time + group['wait_time'])

    def start_group(self, group: dict):
        is_peanut_active = True
        while is_peanut_active:
            with open('peanut.json', 'r') as file:
                peanut_data = json.load(file)
                is_peanut_active = peanut_data['active']

            keyboard = Controller()
            if 'command' in group:
                self.random_wait(group)
                keyboard.type(group['command'])
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)

            if 'commands' in group:
                commands = group['commands']
                if 'random_pick' in group:
                    random_pick = group['random_pick']
                else:
                    random_pick = False

                if random_pick:
                    self.random_wait(group)
                    command = random.choice(commands)
                    keyboard.type(command)
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)

                else:
                    is_stepping = 'chain_step_time' in group
                    if is_stepping:
                        if group['chain_step_time'] < 1:
                            raise ValueError('chain_step_time must be greater than 1')
                        self.random_wait(group)

                    for index, command in enumerate(commands):
                        if not is_stepping:
                            self.random_wait(group)
                        if index > 0 and is_stepping:
                            time.sleep(group['chain_step_time'] + random.random())
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
