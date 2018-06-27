from collections import defaultdict

from .linguistics import Thing, there_are_things_here

class ParsingException(Exception):
    pass

class Message:
    def __init__(self, verb, sender):
        self.verb = verb
        self.sender = sender

    def __str__(self):
        return self.verb

def child_first_ascent(context):
    processed = set()
    while context is not None:
        for child in context.children:
            if child not in processed:
                yield child
                processed.add(child)
        if context not in processed:
            yield context
            processed.add(context)
        context = context.parent

def find_target(message, context):
    if message == "here":
        return context.parent
    for potential_target in child_first_ascent(context):
        for identifier in [n.primary_noun for n in potential_target.nouns]:
            if identifier == message:
                return potential_target
    raise ParsingException(f"No object accessible from '{context}' matches '{message}'")

def parse(message_text, context):
    if message_text == "look":
        verb = Message("examine", context)
        target = context.parent
    elif message_text.startswith("examine "):
        verb = Message("examine", context)
        target = find_target(message_text[8:], context)
    elif message_text.startswith("go "):
        verb = Message("go", context)
        target = find_target(message_text[3:], context)
    elif message_text.startswith("get "):
        verb = Message("get", context)
        target = find_target(message_text[4:], context)
    elif message_text.startswith("drop "):
        verb = Message("drop", context)
        target = find_target(message_text[5:], context)
    elif message_text == "quit":
        raise Exception("Quiting...")
    else:
        raise ParsingException(f"I don't understand the command")
    return verb, target

class GameObject:
    def __init__(self):
        self.visible = True
        self.grouping = "default"
        self.nouns = []
        self.children = set()
        self.parent = None
        self.message_handlers = {}

    def handle_message(self, message):
        if message.verb in self.message_handlers:
            self.message_handlers[message.verb](message)
        else:
            print("no handler")

def game_loop(player):
    command = "look"
    while True:
        try:
            verb, target = parse(command, player)
            target.handle_message(verb)
        except ParsingException as e:
            print(e)
        command = input()
