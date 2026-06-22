#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any
from typing import Protocol


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

    def name(self) -> str:
        return self.__class__.__name__

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

    def ingest(self, data: "int | float | list[int | float]") -> None:
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
        entries: list[dict[str, str]] = (
            data if isinstance(data, list) else [data]
        )
        for entry in entries:
            level: str = entry.get("log_level", "UNKNOWN")
            msg: str = entry.get("log_message", "")
            self._store(f"{level}: {msg}")


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None: ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values: list[str] = [val for _, val in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pairs: list[str] = [f'"item_{rank}": "{val}"' for rank, val in data]
        print("JSON Output:")
        print("{" + ", ".join(pairs) + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled: bool = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - Can't process element in stream: "
                    f"{element}"
                )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            batch: list[tuple[int, str]] = []
            for _ in range(nb):
                if proc.remaining() == 0:
                    break
                batch.append(proc.output())
            if batch:
                plugin.process_output(batch)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            print(
                f"{proc.name()}: total {proc.total_ingested()} items processed, "
                f"remaining {proc.remaining()} on processor"
            )


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")

    ds = DataStream()
    print("Initialize Data Stream...")
    ds.print_processors_stats()
    print()

    print("Registering Processors")
    ds.register_processor(NumericProcessor())
    ds.register_processor(TextProcessor())
    ds.register_processor(LogProcessor())
    print()

    batch1: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch1}\n")
    ds.process_stream(batch1)
    ds.print_processors_stats()
    print()

    print("Send 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, CSVExportPlugin())
    print()
    ds.print_processors_stats()
    print()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"Send another batch of data: {batch2}\n")
    ds.process_stream(batch2)
    ds.print_processors_stats()
    print()

    print("Send 5 processed data from each processor to a JSON plugin:")
    ds.output_pipeline(5, JSONExportPlugin())
    print()
    ds.print_processors_stats()
