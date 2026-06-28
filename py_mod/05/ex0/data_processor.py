#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._rank_counter: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool: ...

    @abstractmethod
    def ingest(self, data: Any) -> None: ...

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data to output")
        return self._storage.pop(0)

    def total_ingested(self) -> int:
        return self._rank_counter

    def remaining(self) -> int:
        return len(self._storage)

    def _store(self, value: str) -> None:
        self._storage.append((self._rank_counter, value))
        self._rank_counter += 1


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(
        self, data: "int | float | list[int | float]"
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._store(str(item))
        else:
            self._store(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: "str | list[str]") -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        if isinstance(data, list):
            return all(
                isinstance(d, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in d.items()
                )
                for d in data
            )
        return False

    def ingest(self, data: "dict[str, str] | list[dict[str, str]]") -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        entries: list[dict[str, str]]
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
        for entry in entries:
            level: str = entry.get("log_level", "UNKNOWN")
            msg: str = entry.get("log_message", "")
            self._store(f"{level}: {msg}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    np = NumericProcessor()
    print(f"Trying to validate input '42': {np.validate(42)}")
    print(f"Trying to validate input 'Hello': {np.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        np.ingest("foo")
    except TypeError as e:
        print(f"Got exception: {e}")
    np.ingest([1, 2, 3, 4, 5])
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = np.output()
        print(f"Numeric value {rank}: {val}")
    print()

    print("Testing Text Processor...")
    tp = TextProcessor()
    print(f"Trying to validate input '42': {tp.validate(42)}")
    tp.ingest(["Hello", "Nexus", "World"])
    print("Extracting 1 value...")
    rank2, val2 = tp.output()
    print(f"Text value {rank2}: {val2}")
    print()

    print("Testing Log Processor...")
    lp = LogProcessor()
    print(f"Trying to validate input 'Hello': {lp.validate('Hello')}")
    logs: list[dict[str, str]] = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    lp.ingest(logs)
    print("Extracting 2 values...")
    for _ in range(2):
        rank3, val3 = lp.output()
        print(f"Log entry {rank3}: {val3}")
