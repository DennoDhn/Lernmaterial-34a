"""
Karten-Verwaltungssystem für §34a Lernkarten

Dieses Skript ermöglicht es:
1. Neue Karten hinzuzufügen
2. Duplikate zu prüfen
3. Kategorien zu verwalten
4. Statistiken anzuzeigen
"""

import json
import sys
from pathlib import Path

def load_cards():
    """Lädt die konsolidierten Karten."""
    with open('lernkarten_consolidated.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_cards(cards):
    """Speichert die Karten."""
    with open('lernkarten_consolidated.json', 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def normalize(text):
    """Normalisiert Text für Vergleich."""
    return ' '.join(text.lower().strip().split())

def is_duplicate(question, cards):
    """Prüft ob eine Frage bereits existiert."""
    normalized_q = normalize(question)
    for category_cards in cards.values():
        for card in category_cards:
            if normalize(card['question']) == normalized_q:
                return True
    return False

def add_card(category, question, answer, cards):
    """Fügt eine neue Karte hinzu."""
    
    if not question or not answer:
        print("Fehler: Frage und Antwort dürfen nicht leer sein!")
        return False
    
    if is_duplicate(question, cards):
        print("Fehler: Diese Frage existiert bereits!")
        return False
    
    if category not in cards:
        print(f"Warnung: Kategorie '{category}' existiert nicht. Erstelle neue Kategorie.")
        cards[category] = []
    
    new_card = {
        'question': question,
        'answer': answer,
        'page': 0  # Neue Karten haben keine Seitenzahl
    }
    
    cards[category].append(new_card)
    print(f"OK: Karte zu '{category}' hinzugefügt!")
    return True

def show_stats(cards):
    """Zeigt Statistiken."""
    total = sum(len(cs) for cs in cards.values())
    print(f"\n=== Statistik ===")
    print(f"Gesamt: {total} Kartenpaare")
    print(f"\nKategorien:")
    for cat, card_list in sorted(cards.items()):
        print(f"  {cat}: {len(card_list)}")
    print()

def list_categories(cards):
    """Listet alle Kategorien."""
    print("\nVerfügbare Kategorien:")
    for i, cat in enumerate(sorted(cards.keys()), 1):
        count = len(cards[cat])
        print(f"  {i}. {cat} ({count} Karten)")

def interactive_add():
    """Interaktive Karten-Hinzufügung."""
    cards = load_cards()
    
    print("\n=== Neue Karte hinzufügen ===\n")
    show_stats(cards)
    list_categories(cards)
    
    print("\nGib die Daten ein (oder 'abbrechen' zum Beenden):")
    
    category = input("\nKategorie: ").strip()
    if category == 'abbrechen':
        return
    
    question = input("Frage: ").strip()
    if question == 'abbrechen':
        return
    
    answer = input("Antwort: ").strip()
    if answer == 'abbrechen':
        return
    
    if add_card(category, question, answer, cards):
        save_cards(cards)
        show_stats(cards)
        print("\nKarte erfolgreich gespeichert!")

def batch_import(filepath):
    """Importiert Karten aus einer Textdatei."""
    cards = load_cards()
    
    print(f"\nImportiere aus: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Einfache Markdown-Parsing
    import re
    pattern = r'F:\s*(.*?)\s*A:\s*(.*?)(?=F:|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    category = input("Kategorie für alle Karten: ").strip()
    
    added = 0
    skipped = 0
    
    for question, answer in matches:
        question = question.strip()
        answer = answer.strip()
        
        if add_card(category, question, answer, cards):
            added += 1
        else:
            skipped += 1
    
    save_cards(cards)
    print(f"\nImport abgeschlossen:")
    print(f"  Hinzugefügt: {added}")
    print(f"  Übersprungen (Duplikate): {skipped}")

def main():
    """Hauptfunktion."""
    if len(sys.argv) < 2:
        print("Verwendung:")
        print("  python manage_cards.py stats          - Zeige Statistiken")
        print("  python manage_cards.py categories     - Liste Kategorien")
        print("  python manage_cards.py add            - Füge Karte hinzu")
        print("  python manage_cards.py import <file>  - Importiere aus Datei")
        return
    
    command = sys.argv[1]
    
    if command == 'stats':
        cards = load_cards()
        show_stats(cards)
    
    elif command == 'categories':
        cards = load_cards()
        list_categories(cards)
    
    elif command == 'add':
        interactive_add()
    
    elif command == 'import':
        if len(sys.argv) < 3:
            print("Fehler: Dateiname fehlt!")
            print("Verwendung: python manage_cards.py import <datei>")
            return
        batch_import(sys.argv[2])
    
    else:
        print(f"Unbekanntes Kommando: {command}")

if __name__ == "__main__":
    main()

