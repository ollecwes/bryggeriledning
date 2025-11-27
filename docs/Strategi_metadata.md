# Strategi för Metadata i Ledningssystemet

## Bakgrund
Vi har diskuterat införandet av metadata (frontmatter) i våra markdown-filer för att öka spårbarhet, ägarskap och struktur. Frågan har också lyfts huruvida vi bör bygga en manuell "kunskapsgraf" genom att definiera relationer (parent/child/relates_to) i metadatan, särskilt med tanke på att AI ska kunna använda systemet effektivt.

## Rekommendation

### 1. Inför Metadata för Attribut
Vi bör absolut införa frontmatter, men begränsa det till **dokumentets egenskaper** som är svåra att utläsa av filnamnet eller innehållet.

**Rekommenderade fält:**
```yaml
---
title: Dravhantering               # För snyggare visning i menyer/sök
description: Kort sammanfattning   # För sökresultat och AI-kontext
owner: Bryggmästaren               # Vem ansvarar för rutinen?
status: published                  # draft / published / archived
tags:                              # För att gruppera tvärs över mappar
  - miljö
  - avfall
---
```

### 2. Undvik Metadata för Relationer
Vi bör **inte** använda metadata för att manuellt bygga en graf (t.ex. `parent:`, `child:`, `relates_to:`).

**Varför?**
*   **Underhållsbörda:** Om en fil flyttas eller döps om måste metadata uppdateras på flera ställen. Det blir snabbt inaktuellt och felaktigt.
*   **Redundans:** Vi har redan en strikt hierarki.
    *   **Mappstrukturen** agerar *Parent/Child*.
    *   **`mkdocs.yml`** agerar *Innehållsförteckning/Karta*.

### 3. Hantering av "Relates To"
Istället för metadata, använd **länkar i löptexten** eller en "Se även"-sektion.
*   *Exempel:* "Se även rutinen för [Rengöring](3_Livsmedelssäkerhet/Rengöringsscheman.md)."
*   Detta ger en starkare koppling än ett nyckelord eftersom det ger **kontext** (varför hänger de ihop?).

## AI-Perspektivet
Är detta tillräckligt för att en AI ska förstå systemet? **Ja.**

En AI navigerar systemet på samma sätt som en utvecklare:
1.  **Sökvägen (Path):** `docs/7_Miljö_och_avfall/Dravhantering.md` berättar omedelbart för AI:n att detta är en underkategori till Miljö och Avfall.
2.  **Strukturen:** `mkdocs.yml` ger AI:n en komplett karta över hur alla delar hänger ihop.
3.  **Länkar:** Hyperlänkar i texten är det mest effektiva sättet för en AI att förstå semantiska kopplingar mellan dokument.

Att lägga till manuella relations-data i frontmatter skulle inte ge AI:n mer värde, utan snarare riskera att förvirra om datan inte hålls 100% synkroniserad med mappstrukturen.

## Slutsats
Håll metadatan fokuserad på **Vem, Vad och Status**. Låt mapparna och länkarna sköta **Var och Hur det hänger ihop**.
