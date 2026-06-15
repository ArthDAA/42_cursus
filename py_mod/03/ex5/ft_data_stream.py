import random
from typing import Generator

players: list[str] = [
    "Alice",
    "Bob",
    "Charlie",
    "Dylan"
]

actions: list[str] = [
    "run",
    "eat",
    "sleep",
    "grab",
    "move",
    "climb",
    "swim",
    "use",
    "release"
]

def gen_event() -> Generator[tuple[str, str], None, None]:
    while (True):
        name: str = random.choice(players)
        action: str = random.choice(actions)
        yield (name, action)


def consume_event(event: list[tuple[str, str]]) -> (Generator[tuple[str, str], None, None]):
    while (len(event) > 0):
        index: int = random.randint(0, len(event) - 1)
        yield event.pop(index)


def main() -> None:
    print("=== Game Data Stream Processor ===")
    stream: Generator[tuple[str, str], None, None] = gen_event()
    for i in range(1000):
        name: str
        action: str
        name, action = next(stream)
        print(f"Event {i}: Player {name} did action {action}")
    events: list[tuple[str, str]] = []
    for _ in range(10):
            events.append(next(stream))
    print(f"Built list of 10 events: {events}")
    for event in consume_event(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()