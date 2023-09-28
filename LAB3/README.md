# LAB3

## Class Task

Change `start_url` and `max_page_num` in `main` to a predifined number you want to set.

```py
start_url = "https://999.md/ro/list/transport/cars"
scrape_links(start_url, max_page_num=10)
```

Run `python3 in_class.py` and open `in_class.txt` file for viewing all filetered urls.

Example of `in_class.txt`:

```
https://999.md/ro/84237763
https://999.md/ro/84237763
https://999.md/ro/84237763
https://999.md/ro/83823218
https://999.md/ro/83823218
https://999.md/ro/83823218
https://999.md/ro/83849383
https://999.md/ro/83849383
https://999.md/ro/83849383
https://999.md/ro/84129441
https://999.md/ro/84129441
https://999.md/ro/84129441
https://999.md/ro/83908834
https://999.md/ro/83908834
https://999.md/ro/83908834
https://999.md/ro/83251086
https://999.md/ro/83251086
https://999.md/ro/83251086
https://999.md/ro/84336684
https://999.md/ro/84336684
https://999.md/ro/84336684
...
```

## Homework

Modify `base_url` field with url of your choice in `main` section and run `python3 homework.py` in order to view scrapped content in `homework.json`. This implementation is based for ads from `https://999.md/ro/list/transport/cars`.

```py
base_url = "https://999.md/ro/83927441"
```

Example of `homework.json`:

```json
{
    "product_name": "Nissan Qashqai",
    "content_description": "Masina a fost procurata si deservita la Daac Hermes.\nNu necesita investitii, totul functioneaza perfect. \nAutomat, 4x4.\nAnul 2019",
    "seller_id": "msi2004",
    "price": {
        "amount": "13900",
        "currency": "\u20ac"
    },
    "region": {
        "country": "Moldova",
        "locality": "Chisinau mun."
    },
    "tel": "+37369135206",
    "general": {
        "tip oferta": "Vand",
        "marca": "Nissan",
        "modelul": "Qashqai",
        "inmatriculare": "Republica Moldova",
        "stare": "Cu rulaj",
        "disponibilitate": "Disponibil"
    },
    "safety": [
        "sistem de antiblocare a franelor (abs)",
        "airbaguri perdea",
        "sistem antiderapare (tcs, asr, trc)",
        "airbaguri laterale",
        "parktronic",
        ...
    ],
    "feature": {
        "autorul anuntului": "Persoana fizica",
        "anul fabricatiei": "2019",
        "volan": "Stanga",
        "numarul de locuri": "5",
        ...
    },
    "comfort": [
        "clima automata",
        "servodirectie",
        "volan reglabil pe inaltime",
        "volan reglabil pe lungime",
        "trapa",
        ...
    ]
}
```
