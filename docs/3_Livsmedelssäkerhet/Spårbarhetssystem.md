# Rutin: Spårbarhetssystem

**Syfte:** Att kunna spåra en produkt bakåt till råvaran (vid kvalitetsfel) och framåt till kund (vid återkallande).
**Lagkrav:** "Ett steg bakåt, ett steg framåt."

## 1. Batchnummer
Varje bryggning tilldelas ett unikt batchnummer.
*   **Format:** `B[ÅÅ][NR]` (t.ex. B2501 för första batchen 2025).
*   Detta nummer följer ölet genom hela processen: Bryggning -> Jäsning -> Lagring -> Tappning.

## 2. Spårbarhet BAKÅT (Råvaror)
I `Bryggprotokollet` för varje batch noteras:
*   **Malt:** Leverantör, maltsort, batchnummer/bäst-före-datum.
*   **Humle:** Leverantör, sort, skördeår/batchnummer.
*   **Jäst:** Leverantör, stam, batchnummer/generation.
*   **Vatten:** Datum (kommunalt vatten spåras via datum).

*Test:* Vi ska kunna svara på frågan: "Vilka öl innehåller malt från Weyermann batch X?"

## 3. Spårbarhet FRAMÅT (Försäljning)
När ölet tappas märks varje flaska/fat/kartong med:
*   **Bäst-före-datum**
*   **Batchnummer** (ofta stämplat på etikett eller flaskhals).

Vid försäljning till återförsäljare (Systembolaget, Grossist, Restaurang) registreras i affärssystemet/fakturan:
*   Vilken produkt (Artikelnummer).
*   Vilket batchnummer (om möjligt, annars datumintervall).
*   Vem som köpte (Kundnummer, Namn).

*Test:* Vi ska kunna svara på frågan: "Vilka kunder har fått flaskor från batch B2501?"

## 4. Spårbarhetstest
Ett spårbarhetstest genomförs **en gång per år**.
1.  Välj en slumpmässig batch från förra månaden.
2.  Ta fram alla råvaror som användes.
3.  Ta fram alla kunder som köpt batchen.
4.  Kontrollera att mängden stämmer (Producerat = Sålt + Lager + Spill).
5.  Dokumentera resultatet.
