from collections import defaultdict

from .core import GameObject, Message, game_loop
from .linguistics import Thing, there_are_things_here

def exit(direction, destination, key=None):
    if key is None:
        locked = False
    else:
        locked = True
    def exit_handler(message):
        nonlocal locked
        if not locked or key in message.sender.children:
            if locked:
                print(f"You use the {key.nouns[0].primary_noun} to unlock the exit")
                locked = False
            print(f"You go {direction}")
            message.sender.parent.children.remove(message.sender)
            destination.children.add(message.sender)
            message.sender.parent = destination
            destination.handle_message(Message("examine", message.sender))
        else:
            print("It's locked")
    def print_description(message):
        print(f"An exit to the {direction}")

    go = GameObject()
    go.grouping = "exit"
    go.message_handlers["go"] = exit_handler
    go.message_handlers["examine"] = print_description
    go.nouns = [Thing(f"exit to the {direction}"), Thing(direction)]
    return go

class GOProxy:
    def __init__(self, name):
        self.name = name
        self._handlers = {}
        self._nouns = []
        self._visible = True
        self._pickable = False
        self._contents = set()
        self.go = GameObject()

    def description(self, text):
        def print_description(m):
            print(text)
            groups = defaultdict(list)
            for c in self.go.children:
                if c.visible:
                    groups[c.grouping].append(c.nouns[0])
            for group in groups.values():
                print(there_are_things_here(group))


        self._handlers["examine"] = print_description
        return self

    def noun(self, noun):
        self._nouns.append(noun)
        return self

    def visible(self, is_visible):
        self._visible = is_visible
        return self

    def contains(self, *others):
        self._contents.update(others)
        return self

    def can_pickup(self, is_pickable):
        self._pickable = is_pickable
        return self

    def realize(self, objects):
        go = self.go
        go.visible = self._visible
        if self._nouns:
            go.nouns = [Thing(n) for n in self._nouns]
        else:
            go.nouns = [Thing(self.name)]
        go.message_handlers = dict(self._handlers)
        if self._pickable:
            def drop(message):
                go.parent = message.sender.parent
                message.sender.children.remove(go)
                message.sender.parent.children.add(go)
                del go.message_handlers["drop"]
                go.message_handlers["get"] = pickup
            def pickup(message):
                go.parent.children.remove(go)
                go.parent = message.sender
                message.sender.children.add(go)
                del go.message_handlers["get"]
                go.message_handlers["drop"] = drop

            go.message_handlers["get"] = pickup
        for child in {objects[v].go if isinstance(v, str) else v.go for v in self._contents}:
            go.children.add(child)
            child.parent = go
        return go

class RoomProxy(GOProxy):
    def __init__(self, name):
        super().__init__(name)
        self._exits = {}

    def exit(self, name, target, key=None):
        self._exits[name] = (target, key)
        return self

    def realize(self, objects):
        go = super().realize(objects)
        for k, (v, l) in self._exits.items():
            if isinstance(v, str):
                v = objects[v].go
            else:
                v = v.go
            if l is not None:
                if isinstance(l, str):
                    l = objects[l].go
                else:
                    l = l.go
            go.children.add(exit(k, v, l))
        return go

class Game:
    def __init__(self):
        self._objects = {"player": GOProxy("player")}
        self._objects["player"].visible(False)

    @property
    def p(self):
        return self._objects["player"]

    def o(self, name):
        if name not in self._objects:
            self._objects[name] = GOProxy(name)
        return self._objects[name]

    def r(self, name):
        if name not in self._objects:
            self._objects[name] = RoomProxy(name)
        return self._objects[name]

    def compile(self):
        realized = {k:v.realize(self._objects) for k,v in self._objects.items()}
        return realized["player"]

    def run(self):
        player = self.compile()
        game_loop(player)
