---
title: Receptutveckling
description: Process för att ta fram nya ölrecept och provbryggning.
owner: Bryggmästaren
status: published
tags:
  - produktion
  - utveckling
  - recept
---

# Process: Receptutveckling

**Syfte:** Att skapa nya, högkvalitativa öl som möter marknadens efterfrågan och bryggeriets kvalitetskrav.

**Ansvarig:** Bryggmästare

## 1. Idé och Koncept
*   **Marknadsanalys:** Vad efterfrågas? (Säsong, trender, luckor i sortimentet).
*   **Målbild:** Definiera ölstil, alkoholhalt (ABV), färg (EBC), beska (IBU) och smakprofil.
*   **Kalkyl:** Beräkna råvarukostnad och potentiellt utpris. Är det lönsamt?

## 2. Provbryggning (Pilot)
Innan fullskalig produktion görs ofta en testbryggning (t.ex. 20–50 liter).
*   **Dokumentation:** Alla ingredienser och processteg noteras noga.
*   **Utvärdering:** Blindprovning av resultatet. Justera receptet vid behov.

## 3. Uppskalning
När receptet är godkänt skalas det upp till produktionsvolym (t.ex. 1 000 liter).
*   **Beräkning:** Justera humlegivor (utbytet skiljer sig mellan liten och stor skala).
*   **System:** Lägg in receptet i bryggerisystemet (t.ex. BeerSmith/Brewfather) och affärssystemet.

## 4. Första produktionsbatchen
Den första skarpa batchen övervakas extra noga.
*   **Analys:** Stämmer OG/FG med beräkningen?
*   **Godkännande:** VD/Bryggmästare måste godkänna smaken innan den släpps till försäljning.

## 5. Digital Receptdesign (Beer Designer)
För att snabba på idéfasen använder vi vårt egenutvecklade verktyg **Beer Designer**. Detta verktyg simulerar bryggprocessen baserat på fysiska och kemiska formler för att ge en uppskattning av det färdiga ölet.

### Ingående Parametrar
Verktyget tar hänsyn till följande variabler för att skapa en virtuell batch (standard 20 liter):

*   **Maltbas:**
    *   *Basmalt:* Ger grundläggande sockerarter och enzymaktivitet.
    *   *Karamellmalt:* Bidrar med färg, sötma och kropp.
    *   *Rostad Malt:* Ger mörk färg och rostade smaker (kaffe/choklad).
*   **Humle:**
    *   *Mängd (g):* Total vikt humle.
    *   *Alfa-syra (%):* Humlens styrka/beskpotential.
    *   *Koktid (min):* Påverkar balansen mellan beska (lång tid) och arom (kort tid).
*   **Process:**
    *   *Mäsktemperatur:* Styr jäsbarheten. Lägre temp (62-64°C) ger torrare öl, högre temp (68-72°C) ger fylligare/sötare öl.
    *   *Jästtyp:* Ale (överjäst, fruktig) eller Lager (underjäst, ren).

### Beräkningsmodeller
Verktyget kalkylerar följande nyckeltal i realtid:

1.  **OG (Original Gravity):** Startdensitet baserat på maltmängd och en förväntad effektivitet på 72%.
2.  **FG (Final Gravity):** Slutdensitet, beräknad utifrån mäsktemperatur och maltkomposition (karamellmalt är mindre jäsbar).
3.  **ABV (Alcohol By Volume):** Alkoholhalt beräknad från skillnaden mellan OG och FG.
4.  **IBU (International Bitterness Units):** Beska beräknad enligt **Tinseth-formeln**, som tar hänsyn till koktid och vörtstyrka.
5.  **EBC (European Brewery Convention):** Färgskala beräknad enligt **Morey-formeln**.
6.  **BU:GU (Bitterness Unit to Gravity Unit):** En kvot som indikerar ölets balans (sött vs beskt).

### Stilmatchning
Systemet jämför automatiskt de framräknade värdena mot en databas av definierade ölstilar (t.ex. IPA, Stout, Pilsner) och föreslår vilken stil receptet liknar mest. Detta hjälper oss att hålla oss inom ramarna för klassiska stilar eller medvetet bryta mot dem.
