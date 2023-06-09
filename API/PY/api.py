import logging, requests

from flask                                  import Flask, request
from src.YoworldItems.item_search           import *
from src.YoworldItems.alt_item_search       import *
from discord_webhook                        import DiscordWebhook, DiscordEmbed
from src.utils                              import *

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True


@app.route('/')
def index():
    return 'Welcome To Yoworld.site API v1.0 (Flask Python Version)'

@app.route('/stats')
def statistics():
    s = Statistics()
    gg, hh, jj = s.totalSortedItems()
    return f"{s.totalItems()},{s.totalSearches()},{gg},{hh},{jj}";

"""
    Search Engine
"""
@app.route('/search')
def search():
    search = request.args.get('q');
    ip = request.environ['HTTP_CF_CONNECTING_IP']
    
    eng = YoworldItems();
    n = eng.new_search(search)

    print(f"[ X ] New '/search' Request | IP: {ip} | Query: {search}")
    
    """ Filtering Search Queries """
    if search == "": return '[ X ] Error, You must fill all parameters to continue!';

    if f"{ip}" == "66.45.249.155":
        Logger().NewLog(LogType.Search, AppType.DiscordBot, ip, search);
    else:
        Logger().NewLog(LogType.Search, AppType.Desktop, ip, search);
    
    if search == "niggerbob": return f"{eng.data}";

    """ Filtering Results """
    if len(n) == 0: return f"No items found with '{search}'";
    elif len(n) == 1: return f"[{n[0].name}, {n[0].iid}, {n[0].url}, {n[0].price}, {n[0].last_update}]";
    elif len(n) > 1:
        list_of_items = ""
        c = 0
        for i in n:
            if c == len(n)-1: list_of_items += f"[{n[c].name},{n[c].iid},{n[c].url},{n[c].price},{n[c].last_update}]";
            else: list_of_items += f"[{n[c].name},{n[c].iid},{n[c].url},{n[c].price},{n[c].last_update}]\n";
            c += 1
            
        return f"{list_of_items}";

@app.route("/advance")
def advance_search():
    query = request.args.get('id');
    ip = request.environ['HTTP_CF_CONNECTING_IP'];

    if not query.isdigit():
        return f"[x] Error, Invalid Item ID.....!";

    found = YoworldItems(int(query)).searchByID();
    itm = ItemGrabber().GrabItemFromYoworldDB(query)
    info = itm.item2dict()
    
    # if found.name == "" and itm.name == "": return f"[x] Error, Item was not found";

    return f"{info}";

"""
    Price Change
"""
@app.route("/change")
def change():
    i_id = request.args.get('id')
    n_price = request.args.get('price')
    ip = request.environ['HTTP_CF_CONNECTING_IP']
    
    eng = YoworldItems()
    n = eng.new_search(i_id)
    
    if len(n) == 0: return "No Item found to update...!"
    change_check = YoworldItems.change_price(i_id, n_price)

    if f"{ip}" == "66.45.249.155":
        Logger().NewLog(LogType.Change, AppType.DiscordBot, ip, search);
    else:
        Logger().NewLog(LogType.Change, AppType.Desktop, ip, search);
    
    if change_check: return f"{n[0].name} successfully updated!"
    
    return "Unable to update item!"

"""
    Request Price Change
"""
@app.route("/request")
def request_change():
    item_name = request.args.get('name')
    item_id = request.args.get('id');
    price_req = request.args.get('price');

    hook = DiscordWebhook("https://discord.com/api/webhooks/1101748421217484810/d7Z84YgXbS6IiZt22xK2bBy1OMG5ewKwxV1uGvDNGl3Cf1_fzs3jGa6oCjJ-iY222-fx")

    embed = DiscordEmbed(title='New Price Change Request', description=f'A new user has requested a new price', color='ff0000');
    embed.add_embed_field(name='Item Name', value=f'{item_name}')
    embed.add_embed_field(name='Item ID', value=f'{item_id}')
    embed.add_embed_field(name='Requested Price', value=f'{price_req}')
    embed.set_author(name='Yoworld Price Guide (Desktop Version)', url='https://images-ext-2.discordapp.net/external/ZZDNlMMvNvguEFDRNa_vTxQEzeEPMUo4xr42dpsoRh4/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1088677293997690961/42a2bc5b79a8c76558eb6b017d9be2e9.png', icon_url='https://images-ext-2.discordapp.net/external/ZZDNlMMvNvguEFDRNa_vTxQEzeEPMUo4xr42dpsoRh4/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1088677293997690961/42a2bc5b79a8c76558eb6b017d9be2e9.png')

    hook.add_embed(embed)
    hook.execute()
    return "GG"

@app.route("/app")
def appNews():
    return f"defdfds";

@app.route("/ip")
def get_client_ip():
    ip = request.environ['HTTP_CF_CONNECTING_IP']
    return f"IP: {ip}"
    
if __name__ == '__main__':
    ip = requests.get("https://api.ipify.org").text
    app.run(host="0.0.0.0", port=80)