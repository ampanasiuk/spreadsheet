from __future__ import annotations

import weakref


class Listener:
    def onevent(self, *args, **kwargs):
        pass


class Listenable:
    def __init__(self):
        self.listeners = weakref.WeakSet()

    def add_listener(self, listener: Listener):
        self.listeners.add(listener)

    def notify(self, *args, **kwargs):
        for listener in set(self.listeners):
            listener.onevent(*args, **kwargs)
