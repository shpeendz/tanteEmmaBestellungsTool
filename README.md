# Projekt Tante Emma - Webanwendung

Dieses Repository enthält den Tech-Stack für die Erstellung einer vollwertigen Webanwendung für einen Tante-Emma-Shop.

Die Anwendung besteht aus einem logischen Backend, einer Benutzeroberfläche und einer persistenten Datenbank auf Basis von MariaDB.

## Ziel der Anwendung

Die Webanwendung soll Kunden ermöglichen, Produkte online zu bestellen, Bestellungen nachzuverfolgen und ein eigenes Benutzerkonto zu verwalten.  
Zusätzlich erhält der Betrieb eine Verwaltungsansicht, um Bestellungen, Lieferungen und Lagerbestände zu organisieren.

## Geplanter Tech-Stack

- Frontend: Weboberfläche für Kunden und Betrieb
- Backend: Logik für Bestellungen, Benutzer, Lager und Lieferungen
- Datenbank: MariaDB zur persistenten Speicherung der Daten

## Use Cases

### Kundenansicht

Kunden können folgende Funktionen nutzen:

- Artikel durchsuchen
- Bestellung erstellen
- Bestellpositionen erfassen
- Lieferintervall festlegen
- Liefertermin auswählen
- Bestellstatus einsehen
- Benutzerkonto erstellen
- Bestellung bezahlen

### Betriebsansicht / Admin

Mitarbeiter und Geschäftsleitung können folgende Funktionen nutzen:

- Bestellungen verwalten
- Lieferungen planen
- Lieferungen durchführen
- Lieferstatus pflegen
- Lagerbestand kontrollieren
- Artikelbestand aktualisieren
- Lagerbestände und Mindestbestände auswerten
- Verkaufs- und Umsatzstatistiken anzeigen

### Lieferantenansicht

Lieferanten können folgende Funktionen nutzen:

- Ware anliefern
- Lieferung bestätigen
- Lieferartikel anbieten

## Use-Case-Diagramm

```mermaid
flowchart LR
    %% Akteure
    Kunde((Kunde))
    Mitarbeiter((Mitarbeiter))
    Lieferant((Lieferant))
    Leitung((Geschäftsleitung))

    %% Systemgrenze
    subgraph System["Tante Emma Shop - Bestell- und Liefersystem"]

        %% Kundenfunktionen
        UC1[Artikel durchsuchen]
        UC2[Bestellung erstellen]
        UC3[Bestellposition erfassen]
        UC4[Lieferintervall festlegen]
        UC5[Liefertermin auswählen]
        UC6[Bestellstatus einsehen]
        UC23[Benutzerkonto erstellen]
        UC24[Bestellung bezahlen]

        %% Mitarbeiterfunktionen
        UC7[Bestellung bearbeiten]
        UC8[Lieferung planen]
        UC9[Lieferung durchführen]
        UC10[Lieferstatus pflegen]
        UC11[Lagerbestand kontrollieren]
        UC12[Artikelbestand aktualisieren]

        %% Lieferantenfunktionen
        UC13[Ware anliefern]
        UC14[Lieferung bestätigen]
        UC15[Lieferartikel anbieten]

        %% Geschäftsleitung / Auswertungen
        UC16[Personalstatistik auswerten]
        UC17[Bestellungen pro Zeitraum auswerten]
        UC18[Umsatz pro Kunde auswerten]
        UC19[Lieferpünktlichkeit auswerten]
        UC20[Offene Lieferungen auswerten]
        UC21[Artikelverkauf auswerten]
        UC22[Lagerbestand und Mindestbestand auswerten]
    end

    %% Kunde
    Kunde --- UC1
    Kunde --- UC2
    Kunde --- UC6
    Kunde --- UC23
    Kunde --- UC24

    %% Mitarbeiter
    Mitarbeiter --- UC7
    Mitarbeiter --- UC8
    Mitarbeiter --- UC9
    Mitarbeiter --- UC10
    Mitarbeiter --- UC11
    Mitarbeiter --- UC12

    %% Lieferant
    Lieferant --- UC13
    Lieferant --- UC14
    Lieferant --- UC15

    %% Geschäftsleitung
    Leitung --- UC16
    Leitung --- UC17
    Leitung --- UC18
    Leitung --- UC19
    Leitung --- UC20
    Leitung --- UC21
    Leitung --- UC22

    %% Include-Beziehungen
    UC2 -. "include" .- UC3
    UC2 -. "include" .- UC4
    UC2 -. "include" .- UC5
    UC2 -. "include" .- UC24

    UC8 -. "include" .- UC11
    UC9 -. "include" .- UC10
    UC13 -. "include" .- UC12
