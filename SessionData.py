import main
class SessionData:
    def __init__(self):
        self.entries = {}
        self.total_duration = 0.0
    def add_entry(self, key, process, title, start_time):
        self.entries[key] = {
            "process": process,
            "title": title,
            "start_time": start_time,
            "end_time": start_time,
            "duration": 0.0
        }
    def update_entry(self, key, end_time):
        entry = self.entries[key]
        entry["duration"] = (end_time - entry["start_time"]).total_seconds()
        entry["end_time"] = end_time
        self.total_duration += entry["duration"]
    def filter_entries(self, min_duration=1):
        return {k: v for k, v in self.entries.items() if v["duration"] >= min_duration and v["process"] not in main.SYSTEM_PROCESSES}
    def get_sorted_entries(self, sort_key="process"):
        filtered = self.filter_entries()
        return sorted(filtered.items(), key=lambda x: x[1][sort_key])