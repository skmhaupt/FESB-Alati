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

Cilj programa je olakšati stvaranje rasporeda za nastavu na FESB-u.

Za rad programa korisnik mora unijeti željeni raspored grupa i listu studenta koju preuzme sa sustava merlin. Zatim program preuzima već postojeće rasporede za svakog studenta kako bi onda popunio sve grupe izbjegavajući preklapanja.

U planu je nadogradnja programa s funkcijom za pronalazak termina nadoknada i potencijalno pronalazak termina za cijeli predmet.

## Instaliranje programa

1. Preuzeti program za poveznie [Releas](https://github.com/skmhaupt/Lab-Generator)
2. unzip
3. .exe kratica

<!--
<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->

## Upozorenja

> [!WARNING]
> Pri pokretanju raznih sekcija istovremeno moze nastupiti pogreska. Npr. ako se pokrene ucitavanje grupa dok se vec radi preuzimanje studentskih rasporeda nastane nepovratna greska. - Trenutno se radi na ispravljanju greske. - 

## Korištenje

### Priprema ulaznih podataka

Za ispravni rad korisnik mora pripremiti dvije datoteke:

* txt datoteka s rasporedom grupa

U txt datoteci korisnik mora navesti sve grupe koje želi ispuniti. Svaka grupa se navodi u novom redu u datoteci. Grupe se navode na sljedeći način:

```text
Grupa, dan, termin, dvorana, broj mjesta
Za dan se mora navesti jedna od sljedećih opcija: PON, UTO, SRI, ČET, PET

primjer:
G1, PON, 09:30 - 11:00, B419, 12
G2, PON, 11:00 - 12:30, B419, 12
G3, SRI, 12:30 - 14:00, B419, 12
```

* csv datoteka s listom svih studenta

U csv datoteci se nalazi lista svih studenta kojima će se ispuniti zadane grupe. Ona se preuzima sa sustava Merlin. Postupak preuzimanja datoteke je prikazan na sljedećoj slici.

1. U prozoru za sudionike predmeta primijeniti filter za izdvojiti sve studente.
2. Na dnu stranice odabrati sve korisnike.
3. Na dnu stranice po 'S odabranim korisnicima...' odabrati 'Zarezima odvojene vrijednosti (.csv)'
4. Datoteka se sad nalazi u direktoriju preuzimanja pod imenom 'courseid_#_participants.csv'

![alt text](images/cours_participants.png "Preuzimanje liste studenta")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

---

### Program

![alt text](images/program.png "Program")

#### Grupe

Za učitati grupe prvo je potrebno zadati .txt datoteku. Vise informacija o pripremi datoteke se može naći u poglavlju ['Priprema ulaznih podataka'](#priprema-ulaznih-podataka).

Datoteka se bira preko botuna 'Pretrazi'. Nakon što se odabere željenu datoteku, potrebno ju je učitati pomoću botuna 'učitaj datoteku'. Ako je zadana datoteka ispravna, ispod botuna će biti prikazani zadani podatci te se može provjeriti ako je sve pravilno učitano. Ako neka grupa nije pravilno zadana ona neće biti prikazana.

Na slici ispod je prikazan primjer pravilno učitane datoteke. S lijeve strane je .txt datoteka s podatcima, a s desne je prikaz sekcije iz programa s pravilno učitanim grupama.

![alt text](images/groups.png "Groups")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

### Sudionici

Za učitati studente prvo je potrebno zadati .csv datoteku. Vise informacija o pripremi datoteke se može naći u poglavlju ['Priprema ulaznih podataka'](#priprema-ulaznih-podataka).

Datoteka se bira pomoću botuna 'Pretrazi'. Nakon što se odabere željenu datoteku, potrebno ju je učitati pomoću botuna 'ucitaj datoteku'. Ako je zadana datoteka ispravna, ispod botuna će biti prikazani zadani podatci te se može provjeriti ako je sve pravilno učitano.

Na slici ispod je prikazan primjer pravilno učitane datoteke. Prvo je prikazana .csv datoteka s podatcima, te je ispod prikazana sekcije iz programa s pravilno učitanim studentima.

![alt text](images/participants.png "Participants")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

### Raspored studenata

Za preuzeti raspored studenata potrebno je zadati raspon datuma unutar kojeg se preuzima raspored i listu studenata. Zadavanje liste studenata je već opisano u prethodnom poglavlju ['Sudionici'](#sudionici). Početni i krajnji datum se zadaju u za to predviđena polja.

Nakon što su potrebni podatci zadani, preuzimanje rasporeda se pokreće s botunom 'Preuzmi raspored'. Preuzimanje rasporeda može potrajati duže vremena (nekoliko minuta) ovisno o količini studenta i o rasponu datuma.

Na slici ispod je vidljiv prikaz preuzimanja rasporeda, prikaz preuzetog rasporeda s mogućim pogreškama i prikaz s ispravno preuzetim rasporedom. Slučaj preuzetog rasporeda s mogućim pogreškama nastupa kad program ne uspije preuzeti raspored za nekog studenta ili/i ako je neki preuzeti raspored prazan. Botunom 'Preuzmi detalje' se može preuzeti excel datoteka koja sadrži listu studenata kod kojih je nastupila pogreška.

![alt text](images/scraper.png "Schedule scraper")

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>

### Ispuna grupa

Ispuniti grupe nije moguce sve dok nisu spremni svi potrebni podatci (grupe, studenti, rasporedi studenata). Ispunjavanje grupa se pokreće botunom 'pokreni'. Ako je zadani ukupni broj dostupnih mjesta po grupama manji od broja zadanih studenata pri pokretanju ce program izbaciti upozorenje i pitati ako korisnik zeli nastaviti.

__abecedni prioritet:__
Prije pokretanja ispune moze se zadati razina abecednom prioritetu. Abecedni prioritet definira koji studenti imaju prioritet pri popunjavanju grupa. Ako se zada vrijednost od '100' onda se studenti biraju po striktno abecednom redosljedu prezimena. Ako se zada vrijednost od '0' onda se studenti biraju striktno po kriteriju kolicine odgovarajucih grupa (dostupnih mjesta). Npr. ako student A moze samo u grupu 4 koja ima 12 slobodnih mjesta, a student B moze u grupe 1,2,3 sa ukupno 10 slobodnih mjesta, student B ima prioritet i biti ce razvrstan prije studenta A.

Ako su svi studenti uspjesno razvrstani po grupama korisnik moze preuzeti excel datoteku sa popunjenim grupama. Ako nisu svi studenti uspjesno razvrstani po grupama korisnik moze, pored standarndne datoteke sa rezultatom, preuzeti i excel datoteku sa dodatnim informacijama o pogreskama.

<p align="right">(<a href="#readme-top">povratak na vrh</a>)</p>