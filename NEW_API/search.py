import sys

from src.yoguide.yoguide import *
from src.yoguide.item_searches import *
args = sys.argv;

if len(args) < 2:
    print(f"[ X ] Error, Invalid argument provided\nUsage: {args[0]} <query>");
    exit(0);

query = f"{args}".replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(f"{args[0]} ", "").replace(f"{args[0]}", "");

eng = YoworldEngine()
n = eng.Search(query);
print(f"{n}")
if n == Response.NONE:
    print("[ X ] Unable to find item.....!");
    exit(0);

elif n == Response.EXACT:

    r = eng.getResults();
    gg = ItemSearch.ywdbSearch(r[0]);
    print(f"Item: {r[0].name} | {r[0].id} | {r[0].price} | {r[0].update} | {gg.in_store}");
    exit(0);

elif n == Response.EXTRA:
    r = eng.getResults();
    c = 0;
    for itm in r:
        print(f"Item: {r[c].name} | {r[c].id} | {r[c].price} | {r[c].update}");
        c += 1