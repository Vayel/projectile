import os
import json
from urllib.parse import quote
from slugify import slugify
import webbrowser

import requests
from six.moves import BaseHTTPServer
from six.moves import http_client
from six.moves import urllib

__all__ = ('TrelloRequestError', 'Trello',)


# Exceptions
class TrelloRequestError(IOError): pass


class ClientRedirectServer(BaseHTTPServer.HTTPServer):
    token = ""
    run = True


class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(http_client.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        query = urllib.parse.urlparse(self.path).query

        if query:
            self.wfile.write(
                b'<html><head><title>Authentification terminee</title></head><body>')

            try:
                self.server.token = urllib.parse.parse_qs(query)["token"][0]
            except KeyError:
                self.wfile.write(b"<p>Echec lors de l'authentification. Vous pouvez fermer cet onglet.</p>")
            else:
                self.wfile.write(b'<p>Vous pouvez fermer cet onglet.</p>')

            self.wfile.write(b'</body></html>')
            self.server.run = False
            return

        self.wfile.write(
            b'<html><head><title>Authentication Status</title></head>')
        self.wfile.write(
            b'<body><script>window.location = window.location.href.replace("#", "?");</script>')
        self.wfile.write(b'</body></html>')


def request(method=requests.get):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            params = dict(key=self.api_key, token=self.get_token())
            gen = func(self, *args, **kwargs)
            url, data = next(gen)

            resp = method(url, params=params, data=dict(value=data))
                    
            if resp.status_code != 200:
                raise TrelloRequestError(resp.text)

            return gen.send(resp.json())

        return wrapper
    return decorator


def card_reader(func):
    """Allow to read a card from either a JSON object or an url."""
    def wrapper(self, *args, url='', card=None, **kwargs):
        if not card:
            card = self.get_card_from_url(url=url)
        
        return func(self, *args, card, **kwargs)

    return wrapper


class Trello:
    def __init__(self, api_key, api_secret_path, app_name):
        self.api_key = api_key
        self.api_secret_path = api_secret_path
        self.app_name = app_name


    def get_token(self):
        try:
            with open(self.api_secret_path, "r") as f:
                data = f.read().strip()
                if data:
                    return data
        except FileNotFoundError:
            pass

        # Create file
        with open(self.api_secret_path, "w") as f:
            host = "localhost"
            port = 8080
            url = ("https://trello.com/1/authorize?key={}&name={}&"
                   "expiration=never&response_type=token&"
                   "callback_method=fragment&scope=read,write&"
                   "return_url=http://{}:{}/").format(self.api_key, quote(self.app_name),
                                                      host, port)

            httpd = ClientRedirectServer((host, port), ClientRedirectHandler)
            webbrowser.open(url)

            while httpd.run:
                httpd.handle_request()

            f.write(httpd.token)

            return httpd.token
   

    @request()
    def get_card_from_url(self, url):
        """Return the JSON content of the card with the url `url`."""
        data = yield "{}.json".format(url), None
        yield data


    @card_reader
    def get_card_members(self, card):
        return card["idMembers"]


    @request()
    def get_member(self, id):
        data = yield "https://trello.com/1/members/{}".format(id), None
        yield data


    def get_mail_from_id(self, id):
        fullname = get_member(id=id)["fullName"]
        return ".".join(slugify(el.lower()) for el in fullname.split(" ")) + "@nsigma.fr"


    @request()
    def get_list_cards(self, list_id):
        """Return the cards in the list `list_id`."""
        data = yield "https://trello.com/1/lists/{}/cards".format(list_id), None
        yield data


    def get_card_insertion_pos(self, list_id):
        """Return the position to insert a card at. A card must be inserted next
        to the ones of the same project manager.
        """
        cards = self.get_list_cards(list_id)
        member_id = self.get_member("me")["id"]

        for i in range(len(cards)):
            card = cards[i]

            if member_id in card["idMembers"]:
                previous_pos = card["pos"]
                try:
                    next_pos = cards[i+1]["pos"]
                except IndexError: # The card is the last one
                    return card["pos"]

                break

        return (next_pos - previous_pos)/2.0


    @request(requests.put)
    @card_reader
    def add_members_to_card(self, ids, card):
        members = list(set(card["idMembers"]) | set(ids))

        data = yield "https://trello.com/1/cards/{}/idMembers".format(card["id"]), members
        yield


    @request(requests.put)
    @card_reader
    def set_card_pos(self, pos, card):
        data = yield "https://trello.com/1/cards/{}/pos".format(card["id"]), pos
        yield


    @request(requests.put)
    @card_reader
    def set_card_list(self, list_id, card):
        data = yield "https://trello.com/1/cards/{}/idList".format(card["id"]), list_id
        yield


    @card_reader
    def insert_card_in_list(self, list_id, card):
        """Insert the card `card` in the list `list_id` at the right position."""
        self.set_card_list(list_id, card=card)
        self.set_card_pos(self.get_card_insertion_pos(list_id), card=card)
