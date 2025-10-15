# Contributing

Hvala na interesu za doprinos UTL Frameworku!

## Kako doprinositi
1. Otvorite **issue** s jasnim opisom problema ili prijedloga.
2. Forkajte repozitorij i kreirajte branch: `feat/ime-funkcionalnosti` ili `fix/kratki-opis`.
3. Dodajte testove za svoj kod (`tests/`).  
4. Pokrenite lokalno provjere:
   ```bash
   pip install -r requirements.txt
   pip install pytest ruff black
   pytest -q
   ruff check .
   black --check .
   ```
5. Pošaljite **pull request** i referencirajte povezani issue.

## Smjernice kodiranja
- Python 3.11+
- **black** i **ruff** prolazak obavezan
- Minimalni docstring za svaku javnu funkciju/klasu

## Etičke smjernice
Ovaj projekt je namijenjen prevenciji štete u konverzacijskim sustavima. Korištenje u svrhe nadzora bez pristanka, diskriminacije ili manipulacije je zabranjeno (vidi LICENSE).

Hvala!