import datetime as dt
from typing import List, Tuple, Dict

class Entry: # vienas aktivitātes ierakstīšana

    def __init__(self, process: str, title: str, start_time: dt.datetime):
        self.process = process
        self.title = title
        self.start = start_time
        self.end = start_time
        self.duration = 0.0

    def update(self, end_time: dt.datetime): # atjauno aktivitātes beigu laiku
        self.end = end_time
        self.duration = (self.end - self.start).total_seconds()


class SessionData: # vārdnīca vairāku ierakstu apvienošanai
    def __init__(self):
        self._entries: List[Entry] = []
        self.total_duration = 0.0

    def add_entry(self, key: str, process: str, title: str, start_time: dt.datetime): # jaunā ieraksta pievienošana
        self._entries.append(Entry(process, title, start_time))

    def update_entry(self, key: str, end_time: dt.datetime): # ieraksta atjaunošana
        process, title = key.split(" - ", 1)
        for entry in self._entries:
            if entry.process == process and entry.title == title:
                entry.update(end_time)
                self.total_duration += entry.duration
                break

    def get_sorted_entries(self, sort_key="process") -> List[Tuple[str, Dict]]: # ierakstu sakārtošana
        return [
            (
                f"{entry.process} - {entry.title}",
                {
                    "process": entry.process,
                    "title": entry.title,
                    "start": entry.start,
                    "end": entry.end,
                    "duration": entry.duration
                }
            )
            for entry in sorted(self._entries, key=lambda x: getattr(x, sort_key))
        ]

    def filter_entries(self, min_duration=1): # ierakstu filtrēšana
        return {
            f"{e.process} - {e.title}": {
                "process": e.process,
                "title": e.title,
                "duration": e.duration
            }
            for e in self._entries
            if e.duration >= min_duration
        }
