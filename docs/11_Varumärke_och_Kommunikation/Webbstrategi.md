---
title: Webbstrategi
description: Strategi för webbplatsens syfte, målgrupper och funktioner.
owner: Marknadsansvarig
status: published
tags:
  - webb
  - strategi
  - digitalt
---

# Webbstrategi

Vår webbplats är inte en broschyr. Det är en **digital förlängning av bryggeriet**. Besökaren ska känna att de kliver in i produktionen.

## Koncept: "The Digital Taproom"
Webben ska fungera som en dashboard för bryggeriet. Transparens är nyckelfunktionen.

## Målgrupper
1.  **Ölnörden:** Vill veta exakt humleschema, jäststam och OG/FG.
2.  **Hemmbryggaren:** Vill inspireras och kanske klona våra recept.
3.  **Krogen/InkÃ¶paren:** Vill se vad som finns i lager och vad som är på gång.

## Kärnfunktioner

### 1. Batch Tracker (Spårbarhet 2.0)
Detta är vår "killer feature". Varje flaska/burk har ett batchnummer. På webben kan man söka på detta nummer och få upp:
*   **Bryggdatum:** När den gjordes.
*   **Bryggare:** Vem som gjorde den.
*   **Data:** OG, FG, IBU, EBC.
*   **Kurvor:** Jäsningskurva (om vi har dataloggar).
*   **Händelser:** "Dag 4: Torrhumling tillsatt."

### 2. Öppna Recept (Open Source)
Varje öl presenteras med sitt recept.
*   Ingredienser i detalj (Malt, Humle, Jäst, Vattenprofil).
*   Mäsksschema och koktider.
*   **"Clone this beer":** En knapp för att ladda ner receptet som BeerXML eller JSON (för BeerSmith/Brewfather).
*   Länk till GitHub-repot där receptet versionshanteras.

### 3. Live Status
En sektion på startsidan som visar vad som händer *just nu*.
*   "Just nu i tank 1: IPA (Jäsning dag 3, Temp 19.5°C)"
*   "Just nu i bryggverket: Rengöring (CIP)"

### 4. Changelog
Istället för en vanlig "Nyheter"-sida, har vi en "Changelog".
*   "v1.2 av Pale Ale: Justerat vattenprofilen för mjukare munkänsla."
*   "Ny utrustning: Installerat ny plattvärmeväxlare."

## Struktur (Sitemap)

*   **Hem:** Dashboard-känsla. Senaste batcherna, live-status.
*   **Våra Öl:** Lista på produkter. Klick leder till djuplodande teknisk sida + recept.
*   **Bryggeriet:** Om oss, men fokus på utrustning och filosofi.
*   **Labbet (Blogg):** Experiment, misslyckanden och lärdomar.
*   **Ledningssystemet:** Länk hit (till docs). "Läs vår manual".
*   **Kontakt:** Enkel väg att nå oss.

## Tekniska Krav
*   Snabbladdad (ingen onödig bloat).
*   Mobilanpassad (många kollar untappd/webb i mobilen på krogen).
*   Kopplad mot GitHub (för att hämta recept/data automatiskt om möjligt).
