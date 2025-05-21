# AppTracker
## Projekta apraksts

Šī programma darbojas kā aktivitāšu trekeris Windows vidē. Tā reģistrē lietotāja aktīvā loga nosaukumu un saistīto procesu, uzkrāj datus par katras sesijas laiku, veic kopsavilkumu un ģenerē grafisku atskaiti, kā arī saglabā rezultātus **Excel** tabulas formātā.

### <ins>Galvenie uzdevumi:</ins>

Periodiski nosaka aktīvo logu un pievieno jaunas sesijas ierakstus.

Aprēķina katra loga kopējo pavadīto laiku.

Klasificē procesus pēc iepriekš definētām kategorijām (piemēram, `Browser`, `Work`, `Games`, `Messenger`, `Other`).

Saglabā sesijas datus uz laiku un ilgumu **Excel** darbgrāmatā ar krāsu kodiem katrai kategorijai.

Izveido un parāda sektoru diagrammu, kas vizualizē laika sadalījumu pa kategorijām.

### <ins>Izmantotās Python bibliotēkas un to pielietojums</ins>

`pywin32` (`win32gui`, `win32process`): nodrošina Windows API piekļuvi, lai iegūtu aktīvā loga rokturi, procesa PID un loga virsrakstu.

`psutil`: ļauj identificēt un apstrādāt sistēmas procesus, iegūt procesa nosaukumu no PID.

`openpyxl`: veido un modificē **Excel** (.xlsx) failus, pievienojot datus un formatējumu (šūnu krāsas, galvenes).

`matplotlib`: ģenerē sektoru diagrammu, kas vizualizē aktivitāšu laika sadalījumu pa kategorijām.

`datetime`: nodrošina datuma un laika aprēķinus.

## Datu struktūras

Projekta gaitā tiek izmantotas šādas pielāgotas datu struktūras, kas definētas `SessionData.py`:

`SessionData`: satur vairākus `Entry` objektus un ļauj veikt operācijas ar tiem.

Atribūts `_entries`: Vārdnīca, kurā glabājas visi aktivitāšu ieraksti. 

Atribūts `total_duration`: kopējais pavadītais laiks.

## Programmas lietošanas metodes
### <ins>`SessionData.py`</ins>'
Metode `add_entry(key, process, title, start_time)`: Pievieno jaunu ierakstu vārdnīcai.

Metode `update_entry(key, end_time)`: atjaunina atbilstošā ieraksta beigu laiku un kopējo ilgumu.

Metode `get_sorted_entries(sort_key)`: atgriež sakārtotu ierakstu sarakstu.

Metode `filter_entries(min_duration)`: filtrē ierakstus pēc minimālā ilguma (Atgriež jaunu vārdnīcu tikai ar ierakstiem, kur duration >= min_duration.).
### <ins>`Main.py`</ins>'
Metode `get_active_window()`: Iegūst aktīvā loga nosaukumu un procesa informāciju.

Metode `track_activity()`: Galvenais cikls, kas atjaunina datus ik sekundi.

Metode `analyze_session()`: Analizē un vizualizē datus, identificējot:
   - Visilgāk izmantoto logu
   - Laika sadalījumu pa kategorijām
   
Metode `_save_to_excel()`: Saglabā datus struktūrētā Excel failā ar laika zīmogu.

## Sagatavošanās

Instalējiet nepieciešamās bibliotēkas:

`pip install pywin32 psutil openpyxl matplotlib`

## Koda struktūra

`main.py` — galvenais skripts, kas pārlūko aktīvos logus un veic datu apkopošanu.

`SessionData.py` — satur datu struktūru definīcijas un metodes datu apstrādei.

### <ins>Sesijas beigas un rezultātu iegūšana</ins>

Nospiediet `Ctrl+C`, lai pārtrauktu izsekošanu.

**(Atkļūdošanai!)** Tiks izdrukāta īsa kopsavilkuma informācija par katru ierakstu terminālī.

Automātiski tiks izsaukta diagrammas funkcija un parādīta sektoru diagramma.

Dati tiks saglabāti Excel failā `session_data_<YYYY-MM-DD>.xlsx`, kur `<YYYY-MM-DD>` ir datuma zīmogs.

## Papildu pielāgojumi

**Kategorijas:** jūs varat pielāgot `CATEGORIES` vārdnīcu `main.py`, pievienojot vai mainot procesu nosaukumus un krāsu kodus.

**Filtrēšana:** izmantojiet `SessionData.filter_entries()`, lai atlasītu tikai sesijas, kas ilgst vairāk par noteiktu laiku.

**Sistēmas procesu filtrs:** Modificējiet `SYSTEM_PROCESSES`, lai ignorētu papildus sistēmas procesus