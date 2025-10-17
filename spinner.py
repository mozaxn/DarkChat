import sys
import time
import itertools
import threading

def _spinner(stop_event, delay=0.1, message=''):
    for ch in itertools.cycle('|/-\\'):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r{ch} {message}')
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\r')  # move to line start when done

class Spinner:
    def __init__(self, delay=0.1, message=''):
        self._stop = threading.Event()
        self._thread = threading.Thread(target=_spinner, args=(self._stop, delay, message))
        self._thread.daemon = True

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._stop.set()
        self._thread.join()
        # optional: print final status
        if exc:
            pass
            # print('Error')
        else:
            pass
            # print('Done')