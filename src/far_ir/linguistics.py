class Thing:
    def __init__(self, primary_noun, countable=True):
        self.primary_noun = primary_noun
        self.countable = countable

class Container(Thing):
    def __init__(self, primary_noun, countable=True, preposition="on"):
        super().__init__(primary_noun, countable)
        self.preposition = preposition

def there_are_things_here(things):
    result = ["There is"]
    if not things:
        result.append("nothing")
    elif len(things) == 1:
        thing = things[0]
        if thing.primary_noun[0] in "aeiou":
            article = "an"
        else:
            article = "a"
        result.append(f"{article} {thing.primary_noun}")
    else:
        inner = []
        for thing in things[:-1]:
            if thing.countable:
                if thing.primary_noun[0] in "aeiou":
                    article = "an"
                else:
                    article = "a"
            else:
                article = "some"
            inner.append(f"{article} {thing.primary_noun}")

        thing = things[-1]
        if thing.countable:
            article = "a"
        else:
            article = "some"
        result.append(", ".join(inner) + f" and {article} {thing.primary_noun}")
    result.append("here.")
    return " ".join(result)
