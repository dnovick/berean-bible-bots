"""Build NT book language profiles for Mat, Jhn, Rom, Heb, Rev."""
from bible_grammar.reporting.profiles import save_profile_report

BOOKS = ['Mat', 'Jhn', 'Rom', 'Heb', 'Rev']

for book in BOOKS:
    path = save_profile_report(book)
    print(f"Profile: {path}")
