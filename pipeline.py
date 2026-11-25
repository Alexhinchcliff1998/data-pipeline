import argparse,json,sqlite3,urllib.request,math
from pathlib import Path
BASE=Path(__file__).parent

def normalize(rows):
    clean=[]; rejected=0
    for row in rows:
        try:
            ident=row['id']; title=row['title'].strip(); category=row['category'].strip().lower(); price=float(row['price'])
            if type(ident) is not int or ident<=0 or not title or not category or not math.isfinite(price) or price<0: raise ValueError()
            clean.append((ident,title,category,round(price,2)))
        except (KeyError,ValueError,TypeError,AttributeError,OverflowError): rejected+=1
    return clean,rejected

def run(live=False, database=None):
    if live:
        with urllib.request.urlopen('https://dummyjson.com/products?limit=100',timeout=15) as response: payload=json.load(response)
    else: payload=json.loads((BASE/'sample.json').read_text())
    rows,rejected=normalize(payload['products'])
    with sqlite3.connect(database or BASE/'products.db') as db:
        db.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,title TEXT,category TEXT,price REAL)')
        db.executemany('INSERT INTO products VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title,category=excluded.category,price=excluded.price',rows)
        count=db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    print(f'Accepted {len(rows)}; rejected {rejected}; stored {count}')
    return len(rows),rejected,count
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');run(parser.parse_args().live)
