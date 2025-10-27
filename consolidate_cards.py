import json
import re
from collections import defaultdict

def normalize_text(text):
    """Normalisiert Text für Duplikatsprüfung."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text.lower().strip())
    text = text.rstrip('.,!?;:')
    return text

def find_duplicates(cards):
    """Findet Duplikate basierend auf Frage-Text."""
    seen_questions = {}
    duplicates = []
    
    for card in cards:
        normalized_q = normalize_text(card.get('question', ''))
        if normalized_q in seen_questions:
            duplicates.append({
                'original': seen_questions[normalized_q],
                'duplicate': card
            })
        else:
            seen_questions[normalized_q] = card
    
    return duplicates, seen_questions

def consolidate_all_sources():
    """Konsolidiert alle Quellen und entfernt Duplikate."""
    
    print("=== Konsolidierung der Lernkarten ===\n")
    
    with open('lernkarten.json', 'r', encoding='utf-8') as f:
        final3_cards = json.load(f)
    
    print(f"Original: {sum(len(cards) for cards in final3_cards.values())} Karten")
    
    all_cards = []
    for category, cards in final3_cards.items():
        for card in cards:
            all_cards.append({
                **card,
                'category': category,
                'source': 'Final3.2'
            })
    
    duplicates, unique_questions = find_duplicates(all_cards)
    
    print(f"\nGefundene Kategorien:")
    category_count = defaultdict(int)
    for card in all_cards:
        category_count[card['category']] += 1
    
    for cat, count in sorted(category_count.items()):
        print(f"  {cat}: {count}")
    
    print(f"\nDuplikate: {len(duplicates)}")
    
    consolidated = defaultdict(list)
    used_questions = set()
    
    for card in all_cards:
        normalized_q = normalize_text(card['question'])
        if normalized_q not in used_questions and card['question'] and card['answer']:
            used_questions.add(normalized_q)
            consolidated[card['category']].append({
                'question': card['question'],
                'answer': card['answer'],
                'page': card.get('page', 0)
            })
    
    consolidated_dict = dict(consolidated)
    
    print(f"\nNach Konsolidierung:")
    for cat, cards in sorted(consolidated_dict.items()):
        print(f"  {cat}: {len(cards)}")
    
    total = sum(len(cards) for cards in consolidated_dict.values())
    print(f"\nGesamt: {total} einzigartige Karten")
    
    with open('lernkarten_consolidated.json', 'w', encoding='utf-8') as f:
        json.dump(consolidated_dict, f, ensure_ascii=False, indent=2)
    
    print("\nOK: Datei gespeichert: lernkarten_consolidated.json")
    
    stats = {
        'total_categories': len(consolidated_dict),
        'total_cards': total,
        'categories': {cat: len(cards) for cat, cards in consolidated_dict.items()},
        'duplicates_found': len(duplicates)
    }
    
    with open('card_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    return consolidated_dict, stats

if __name__ == "__main__":
    consolidated, stats = consolidate_all_sources()
    print(f"\nZusammenfassung: {stats['total_cards']} Karten in {stats['total_categories']} Kategorien")

