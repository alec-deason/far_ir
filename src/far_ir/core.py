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
        for identifier in [potential_target.identifier.primary_noun] + potential_target.secondary_identifiers:
            if identifier in message:
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
    elif message_text == "quit":
        raise Exception("Quiting...")
    else:
        raise ParsingException(f"I don't understand the command")
    return verb, target

class GameObject:
    def __init__(self, identifier, adjectives=None, visible=True, grouping="default"):
        self.identifier = identifier
        self.secondary_identifiers = []
        self.adjectives = adjectives
        self.grouping = grouping
        self.visible = visible
        self.children = set()
        self.parent = None

    def handle_message(self, message):
        raise NotImplementedError

class DescribedObject(GameObject):
    def __init__(self, identifier, description, embeded_description=None, adjectives=None, visible=True, grouping="default"):
        super().__init__(identifier, adjectives=adjectives, visible=visible, grouping=grouping)
        self.description = description
        self.embeded_description = embeded_description

    def handle_message(self, message):
        if message.verb == "examine":
            print(self.description)
            groups = defaultdict(list)
            for c in self.children:
                if c.visible:
                    groups[c.grouping].append(c.identifier)

            for group in groups.values():
                print(there_are_things_here(group))

class Exit(GameObject):
    def __init__(self, identifier, destination, visible=True, grouping="exit"):
        super().__init__(Thing(f"exit to the {identifier}"), visible=visible, grouping=grouping)
        self.secondary_identifiers.append(identifier)
        self.destination = destination

    def handle_message(self, message):
        if message.verb == "go":
            message.sender.parent.children.remove(message.sender)
            self.destination.children.add(message.sender)
            message.sender.parent = self.destination
            self.destination.handle_message(Message("examine", message.sender))



def game_loop(player):
    while True:
        command = input()
        try:
            verb, target = parse(command, player)
            target.handle_message(verb)
        except ParsingException as e:
            print(e)
