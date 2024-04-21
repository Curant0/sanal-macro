import json
from sys import argv
from worker import Worker
from pynput.keyboard import Listener
import threading


def main(**kwargs):
    worker = Worker(**kwargs)
    threads = []
    with Listener(on_press=worker.on_start_press) as start_listener:
        start_listener.join()

    with open('peanut.json', 'w') as file:
        json.dump({'active': True}, file, indent=4)

    if worker.start_threads:
        for group in worker.commands.values():
            thread = threading.Thread(target=worker.start_group, args=(group,))
            threads.append(thread)
            thread.start()

        with Listener(on_press=worker.on_stop_press) as stop_listener:
            stop_listener.join()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    if len(argv) == 2:
        main(commands=f'commands/{argv[1]}.json')
    if len(argv) == 3:
        main(commands=f'commands/{argv[1]}.json', profile=f'profiles/{argv[2]}.json')
    else:
        main()

else:
    print('amogus')
