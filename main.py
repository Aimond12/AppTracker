import win32gui as win
import win32process as proc
import os
import time
import datetime as dt
import psutil 
import SessionData
from openpyxl import Workbook
from openpyxl.styles import PatternFill

SYSTEM_PROCESSES = {'Explorer', 'Svchost', 'Taskmgr'}
CATEGORIES = {
    "Browser": {
        "processes": ["Chrome", "Firefox", "msedge", "opera"],
        "color": "FFB8F0B4"  
    },
    "Work": {
        "processes": ["Code", "Pycharm", "Devenv", "Excel", "Winword"],
        "color": "FFF0E68C"
    },
    "Games": {
        "processes": ["Steam", "Dota2", "Cs2", "Game"],
        "color": "FFFFC0CB"
    },
    "Messenger": {
        "processes": ["Telegram", "Discord", "Whatsapp"],
        "color": "FFADD8E6"
    },
}
DEFAULT_CATEGORY = {
    "name": "Other",
    "color": "FFFFFFFF"
}

def get_active_window(): # iegūstam aktīvo logu (nosaukumu un procesu)
    try:
        window = win.GetForegroundWindow()
        pid = proc.GetWindowThreadProcessId(window)[1]
        exetubale = psutil.Process(pid).name().capitalize().removesuffix(".exe")
        title = win.GetWindowText(window)
        return {"process": exetubale, "title": title.strip()}
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None
def track_activity():
    today = dt.datetime.now().strftime("%Y-%m-%d")
    filename = f"session_data_{today}.xlsx"
    session = SessionData.SessionData() # izveidojam sesiju
    if os.path.exists(filename):
        session.load_from_excel(filename)
    current_window = None

    try:
        while True:
            new_window = get_active_window()
            if not new_window:
                continue
            new_key = f"{new_window['process']} - {new_window['title']}" # izveidojam atslēgu no procesa un loga nosaukuma
            if new_key != current_window:
                if current_window in session.entries:
                    session.update_entry(current_window, dt.datetime.now())
                if new_key not in session.entries:
                    session.add_entry(key = new_key, process=new_window['process'], title=new_window['title'], start_time=dt.datetime.now())
                current_window = new_key
            else:
                session.update_entry(current_window, dt.datetime.now())
            time.sleep(1) # gaidām 1 sekundi pirms nākamās pārbaudes
    except KeyboardInterrupt:
        if current_window:
            session.update_entry(current_window, dt.datetime.now())
        print("Session ended.")
        print(session.entries)

        _save_to_excel(session) # saglabājam datus Excel failā

def _save_to_excel(data):
        today = dt.datetime.now().strftime("%Y-%m-%d")
        filename = f"session_data_{today}.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "Session Report"
        ws.append(["Window Title", "Process", "Duration (HH:MM)", "Start Time", "End Time", "Activity type"])

        styles = {cat: PatternFill(start_color=data["color"], fill_type="solid")  # pievienojam krāsu katrai kategorijai
                  for cat, data in CATEGORIES.items()}
        default_style = PatternFill(start_color=DEFAULT_CATEGORY["color"], fill_type="solid") # noklusējuma krāsa

        for key, entry in data.get_sorted_entries(sort_key="process"):
            category = get_category(entry["process"])
            duration = seconds_to_hhmm(entry["duration"])
            ws.append([
                entry["title"],
                entry["process"],
                duration,
                entry["start"].strftime("%Y-%m-%d %H:%M:%S"),
                entry["end"].strftime("%Y-%m-%d %H:%M:%S"),
                category["name"]
            ])
            ws.cell(row=ws.max_row, column=4).fill = styles.get(category["name"], default_style)

        wb.save(filename)
        print(f"Dati saglabāti: {filename}")

def seconds_to_hhmm(seconds):
    hours = seconds // 3600 # 3600 sekundes = 1 stunda (saglabam tikati veselu skaitli)
    minutes = (seconds % 3600) // 60 # 60 sekundes = 1 minūte
    return f"{int(hours):02}:{int(minutes):02}"

def get_category(process_name): # piešķiram kategoriju katram procesam
    for category, data in CATEGORIES.items():
        if any(process_name in p for p in data["processes"]):
            return {
                "name": category,
                "color": data["color"]
            }
    return DEFAULT_CATEGORY

if __name__ == "__main__":
    track_activity()