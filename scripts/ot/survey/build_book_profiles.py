"""Build OT book language profiles for Gen, Exo, Psa, Isa, Dan."""
from bible_grammar.reporting.profiles import save_profile_report

BOOKS = ['Gen', 'Exo', 'Psa', 'Isa', 'Dan']

for book in BOOKS:
    path = save_profile_report(book)
    print(f"Profile: {path}")
