# Kotlin Timetable Fetcher

Ovaj projekt dohvaća rasporede studenata i računa periode kada su svi slobodni.

## Najlakše je pokrenuti koristeći IDE poput Android studio ili Intellij IDEA

## Zahtjevi

Prije pokretanja projekta, osiguraj da imaš instalirane sljedeće alate:
- [JDK 11+](https://adoptopenjdk.net/)


## Instalacija i pokretanje bez IDE-a

1. Kloniraj repozitorij:
   ```sh
   git clone <URL_REPOZITORIJA>
   cd <NAZIV_PROJEKTA>
   ```

2. Dodaj korisnička imena u `data/usernames.txt` (jedno po liniji):
   ```
   abbbbb00
   user123
   testuser
   ```

3. Dodaj početni i krajnji datum u `data/dates.txt` (jedan datum po liniji, u formatu `DD-MM-YYYY`):
   ```
   02-24-2024
   06-06-2024
   ```
4. Dodaj početno i krajnje vrijeme u `data/times.txt` (jedno vrijeme po liniji, u formatu `HH:MM`):
   ```
   08:00
   20:00
   ```

4. Pokreni aplikaciju:
   ```sh
   ./gradlew run
   ```

## Struktura projekta

- `Main.kt` - Ulazna točka aplikacije, dohvaća raspored za zadane korisnike i sprema podatke u CSV.
- `TimetableService.kt` - Klasa koja upravlja HTTP pozivima za dohvaćanje rasporeda.
- `TimeTableRepository.kt` - Repozitorij koji koristi `TimetableService` za dohvaćanje podataka.
- `data/usernames.txt` - Datoteka s popisom korisničkih imena.
- `data/dates.txt` - Datoteka s početnim i krajnjim datumom.
- `data/timetables/` - Direktorij u koji se spremaju CSV datoteke.
- `build.gradle.kts` - Konfiguracija projekta i ovisnosti.

## Konfiguracija

- Korisnički podaci se čitaju iz `data/usernames.txt`.
- Početni i krajnji datum se čitaju iz `data/dates.txt`.
- Za svakog korisnika generira se CSV datoteka u `data/timetables/` u obliku `<username>_<startDate>_to_<endDate>.csv`.

## Format CSV datoteke

Svaka generirana CSV datoteka sadrži sljedeće stupce:
```
id, name, shortName, colorId, professor, eventType, groups, classroom, start, end, description, recurring, recurringType, recurringUntil, studyCode
532053,Kriptografija i mrežna sigurnost,KIMS,0,Čagalj Mario,PREDAVANJE,,C501,2024-02-26T10:15,2024-02-26T12:00,ponedjeljak 26.2.2024. 10:15 - 12:00 (2 sata),true,WEEKLY,do 9.6.2024.,250
532137,Podržano strojno učenje,PSU,0,Vasilj Josip,PREDAVANJE,,A243,2024-02-27T08:15,2024-02-27T10:00,utorak 27.2.2024. 8:15 - 10:00 (2 sata),true,WEEKLY,do 9.6.2024.,250
532077,Metode optimizacije,MO,0,Marasović Jadranka,PREDAVANJE,,C502,2024-02-27T10:15,2024-02-27T12:00,utorak 27.2.2024. 10:15 - 12:00 (2 sata),true,WEEKLY,do 9.6.2024.,250

```

Primjer occupiedTimes.csv i freeTimes.csv datoteka:
```
DayOfWeek,StartTime,EndTime
MONDAY,08:00,09:15
MONDAY,12:00,12:15
MONDAY,14:00,14:15
MONDAY,16:00,18:15
TUESDAY,08:00,08:15
TUESDAY,14:00,14:15
TUESDAY,16:00,18:30
WEDNESDAY,08:00,08:15
WEDNESDAY,14:45,15:15
WEDNESDAY,17:00,18:00
WEDNESDAY,19:30,20:00
THURSDAY,08:00,08:15
THURSDAY,13:00,13:30
THURSDAY,15:00,19:30
FRIDAY,09:30,10:15
FRIDAY,17:00,20:00
SATURDAY,09:30,20:00

```

## Dodatne informacije

- OkHttp se koristi za slanje HTTP zahtjeva.
- Ako `data/timetables/` ne postoji, aplikacija će ga automatski kreirati.
- Ako `data/usernames.txt` ili `data/dates.txt` nisu pravilno konfigurirani, aplikacija će baciti grešku.

Ako imaš bilo kakvih problema, provjeri ovisnosti i verzije alata koje koristiš.

## Napomene

- Što je veći vremenski raspon, dulje traje dohvaćanje podataka.
- Ako program naiđe na grešku pri dohvaćanju rasporeda za nekog korisnika, taj korisnik će biti preskočen.

