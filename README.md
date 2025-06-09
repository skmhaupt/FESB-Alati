<a id="readme-top"></a>

# Lab-Generator

<details>
  <summary>Sadrzaj</summary>
  <ol>
    <li><a href="#opis-programa">Opis programa</a></li>
    <li><a href="#instaliranje-programa">Instaliranje programa</a></li>
    <li>
      <a href="#koristenje">Koristenje</a>
      <ul>
        <li><a href="#priprema-ulaznih-podataka">Priprema ulaznih podataka</a></li>
        <li><a href="#program">Program</a>
          <ul>
            <li><a href="#grupe">Grupe</a></li>
            <li><a href="#sudionici">Sudionici</a></li>
            <li><a href="#raspored-studenata">Raspored studenata</a></li>
            <li><a href="#ispuna-grupa">Ispuna grupa</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>

## Opis programa

Cilj programa je olaksati stvaranje rasporeda za nastavu na FESBu.

Za rad programa korisnik mora unijeti zeljeni raspored grupa i listu studenta koju preuzme sa sustava merlin. Zatim program preuzima vec postojece rasporede za svakog studenta kako bi onda popunio sve grupe izbjegavajuci preklapanja.

U planu je nadogradnja programa sa funcijom za pronalazak termina nadoknada i potencijalno pronalazak termina za cijeli predmet.

## Instaliranje programa

1. Preuzeti program za poveznie [Releas](https://github.com/skmhaupt/Lab-Generator)
2. unzip
3. .exe kratica

<!--
<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

## Koristenje

### Priprema ulaznih podataka

Za ispravni rad korisnik mora pripremiti dvije datoteke:

* txt datoteka sa rasporedom grupa

U txt datoteci korisnik mora navesti sve grupe koje zeli ispuniti. Svaka grupa se navodi u novom redu u datoteci. Grupe se navode na sljedeci nacin:

```text
Grupa, dan, termin, dvorana, broj mjesta
Za dan se mora navesti jedna od sljedecih opcija: PON, UTO, SRI, ČET, PET

primjer:
G1, PON, 09:30 - 11:00, B419, 12
G2, PON, 11:00 - 12:30, B419, 12
G3, SRI, 12:30 - 14:00, B419, 12
```

* csv datoteka sa listom svih studenta

U csv datoteci se nalazi lista svih studenta kojima ce se ispuniti zadane grupe. Ona se preuzima sa sustava Merlin. Postupak preuzimanja datoteke je prikazan na sljedecoj slici.

1. U prozoru za sudionike predmeta primjeniti filter za izdvojiti sve studente.
2. Na dnu stranice odabrati sve korisnike.
3. Na dnu stranice po 'S odabranim korisnicima...' odabrati 'Zarezima odvojene vrijednosti (.csv)'
4. Datoteka se sad nalazi u direktoriju preuzimanja pod imenom 'courseid_#_participants.csv'

![alt text](images/cours_participants.png "Preuzimanje liste studenta")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

---

### Program

![alt text](images/program.png "Program")

#### Grupe

Za ucitati grupe prvo je potrebno zadati .txt datoteku. Vise informacija o pripremi datoteke se moze naci u poglavlju ['Priprema ulaznih podataka'](#priprema-ulaznih-podataka).

Datoteka se bira pomocu botuna 'Pretrazi'. Nakon sto se odabere zeljenu datoteku, potrebno ju je ucitati pomocu botuna 'ucitaj datoteku'. Ukoliko je zadana datoteka ispravna, ispod botuna ce biti prikazani zadani podatci te se moze provjeriti ako je sve pravilno ucitano. Ukoliko neka grupa nije pravilno zadana ona nece biti prikazana.

Na slici ispod je prikazan primjer pravilno ucitane datoteke. Sa lijeve strane je .txt datoteka sa podatcima, a sa desne je prikaz sekcije iz programa sa pravilno ucitanim grupama.

![alt text](images/groups.png "Groups")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

### Sudionici

Za ucitati studente prvo je potrebno zadati .csv datoteku. Vise informacija o pripremi datoteke se moze naci u poglavlju ['Priprema ulaznih podataka'](#priprema-ulaznih-podataka).

Datoteka se bira pomocu botuna 'Pretrazi'. Nakon sto se odabere zeljenu datoteku, potrebno ju je ucitati pomocu botuna 'ucitaj datoteku'. Ukoliko je zadana datoteka ispravna, ispod botuna ce biti prikazani zadani podatci te se moze provjeriti ako je sve pravilno ucitano.

Na slici ispod je prikazan primjer pravilno ucitane datoteke. Prvo je prikazana .csv datoteka sa podatcima, te je ispod prikazana sekcije iz programa sa pravilno ucitanim studentima.

![alt text](images/participants.png "Participants")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

### Raspored studenata

Za preuzeti raspored studenata potrebno je zadati raspon datuma unutar kojeg se preuzima raspored i listu studenta. Zadavanje liste studenata je vec opisano u prethodnom poglavlju ['Sudionici'](#sudionici). Pocetni i krajnji datum se zadaju u za to predvidena polja. 

Nakon sto su potrebni podatci zadani, preuzimanje rasporeda se pokrece sa botunom 'Preuzmi raspored'. Preuzimanje rasporeda moze potrajati duze vremena (nekoliko minuta) ovisno o kolicini studenta i o rasponu datuma.

Na slici ispod je vidljiv prikaz preuzimanja rasporeda, prikaz preuzetog rasporeda sa mogucim pogreskama i prikaz sa ispravno preuzetim rasporedom. Slucaj preuzetog rasporeda sa mogucim pogreskama nastupa kad program ne uspije preuzeti raspored za nekog studenta ili/i ako je neki preuzeti raspored prazan. Botunom 'Preuzmi detalje' se moze preuzeti excel datoteka koja sadrzi listu studenata kod kojih je nastupila pogreska.

![alt text](images/scraper.png "Schedule scraper")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

### Ispuna grupa



<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>