#!/usr/bin/env python3

# nederlaands.py - wzzx <wzzx@rmo.so>
# Simple and insecure self-contained website that helps study common irregular
# Dutch verbs

import random
import uuid
from flask import Flask, redirect, request

VERBS = {
    'vergeten': {'imperfectum_p': 'vergaten', 'perfectum': 'vergeten', 'engels': 'forget', 'imperfectum_s': 'vergat', 'hulpwerkwoord': 'zijn'}, \
    'zeggen': {'imperfectum_p': 'zeiden', 'perfectum': 'gezegt', 'engels': 'say', 'imperfectum_s': 'zei', 'hulpwerkwoord': 'hebben'}, \
    'worden': {'imperfectum_p': 'werden', 'perfectum': 'geworden', 'engels': 'become', 'imperfectum_s': 'werd', 'hulpwerkwoord': 'zijn'}, \
    'lezen': {'imperfectum_p': 'lazen', 'perfectum': 'gelezen', 'engels': 'read', 'imperfectum_s': 'las', 'hulpwerkwoord': 'hebben'}, \
    'kiezen': {'imperfectum_p': 'kozen', 'perfectum': 'gekozen', 'engels': 'choose', 'imperfectum_s': 'koos', 'hulpwerkwoord': 'hebben'}, \
    'willen': {'imperfectum_p': 'wilden', 'perfectum': 'wewild', 'engels': 'want', 'imperfectum_s': 'wilde', 'hulpwerkwoord': 'hebben'}, \
    'vinden': {'imperfectum_p': 'vonden', 'perfectum': 'gevonden', 'engels': 'find', 'imperfectum_s': 'vond', 'hulpwerkwoord': 'hebben'}, \
    'drijven': {'imperfectum_p': 'dreven', 'perfectum': 'gedreven', 'engels': 'float', 'imperfectum_s': 'dreef', 'hulpwerkwoord': 'hebben'}, \
    'sluiten': {'imperfectum_p': 'sloten', 'perfectum': 'gesloten', 'engels': 'close', 'imperfectum_s': 'sloot', 'hulpwerkwoord': 'hebben'}, \
    'kijken': {'imperfectum_p': 'keken', 'perfectum': 'gekeken', 'engels': 'look', 'imperfectum_s': 'keek', 'hulpwerkwoord': 'hebben'}, \
    'laten': {'imperfectum_p': 'lieten', 'perfectum': 'gelaten', 'engels': 'let', 'imperfectum_s': 'liet', 'hulpwerkwoord': 'hebben'}, \
    'vragen': {'imperfectum_p': 'vroegen', 'perfectum': 'gevraagd', 'engels': 'ask', 'imperfectum_s': 'vroeg', 'hulpwerkwoord': 'hebben'}, \
    'staan': {'imperfectum_p': 'stonden', 'perfectum': 'gestaan', 'engels': 'stand', 'imperfectum_s': 'stond', 'hulpwerkwoord': 'hebben'}, \
    'weten': {'imperfectum_p': 'wisten', 'perfectum': 'geweten', 'engels': 'know', 'imperfectum_s': 'wist', 'hulpwerkwoord': 'hebben'}, \
    'begrijpen': {'imperfectum_p': 'begrepen', 'perfectum': 'begrepen', 'engels': 'understand', 'imperfectum_s': 'begreep', 'hulpwerkwoord': 'hebben'}, \
    'houden': {'imperfectum_p': 'hielden', 'perfectum': 'gehouden', 'engels': 'hold', 'imperfectum_s': 'hield', 'hulpwerkwoord': 'hebben'}, \
    'lachen': {'imperfectum_p': 'lachten', 'perfectum': 'gelachen', 'engels': 'laugh', 'imperfectum_s': 'lachte', 'hulpwerkwoord': 'hebben'}, \
    'blijven': {'imperfectum_p': 'bleven', 'perfectum': 'gebleven', 'engels': 'stay', 'imperfectum_s': 'bleef', 'hulpwerkwoord': 'zijn'}, \
    'helpen': {'imperfectum_p': 'hielpen', 'perfectum': 'geholpen', 'engels': 'help', 'imperfectum_s': 'hielp', 'hulpwerkwoord': 'hebben'}, \
    'zitten': {'imperfectum_p': 'zaten', 'perfectum': 'gezeten', 'engels': 'sit', 'imperfectum_s': 'zat', 'hulpwerkwoord': 'hebben'}, \
    'nemen': {'imperfectum_p': 'namen', 'perfectum': 'genomen', 'engels': 'take', 'imperfectum_s': 'nam', 'hulpwerkwoord': 'hebben'}, \
    'rijden': {'imperfectum_p': 'reden', 'perfectum': 'gereden', 'engels': 'ride', 'imperfectum_s': 'reed', 'hulpwerkwoord': 'zijn'}, \
    'zien': {'imperfectum_p': 'zagen', 'perfectum': 'gezien', 'engels': 'see', 'imperfectum_s': 'zag', 'hulpwerkwoord': 'hebben'}, \
    'binden': {'imperfectum_p': 'bonden', 'perfectum': 'gebonden', 'engels': 'tie', 'imperfectum_s': 'bond', 'hulpwerkwoord': 'hebben'}, \
    'beginnen': {'imperfectum_p': 'begonnen', 'perfectum': 'begonnen', 'engels': 'begin', 'imperfectum_s': 'begon', 'hulpwerkwoord': 'zijn'}, \
    'komen': {'imperfectum_p': 'kwamen', 'perfectum': 'gekomen', 'engels': 'come', 'imperfectum_s': 'kwam', 'hulpwerkwoord': 'zijn'}, \
    'zoeken': {'imperfectum_p': 'zochten', 'perfectum': 'gezocht', 'engels': 'search', 'imperfectum_s': 'zocht', 'hulpwerkwoord': 'hebben'}, \
    'brengen': {'imperfectum_p': 'brachten', 'perfectum': 'gebracht', 'engels': 'bring', 'imperfectum_s': 'bracht', 'hulpwerkwoord': 'hebben'}, \
    'vechten': {'imperfectum_p': 'vochten', 'perfectum': 'gevochten', 'engels': 'fight', 'imperfectum_s': 'vocht', 'hulpwerkwoord': 'hebben'}, \
    'drinken': {'imperfectum_p': 'dronken', 'perfectum': 'gedronken', 'engels': 'drink', 'imperfectum_s': 'dronk', 'hulpwerkwoord': 'hebben'}, \
    'hebben': {'imperfectum_p': 'hadden', 'perfectum': 'gehad', 'engels': 'have', 'imperfectum_s': 'had', 'hulpwerkwoord': 'hebben'}, \
    'liggen': {'imperfectum_p': 'lagen', 'perfectum': 'gelegen', 'engels': 'lie', 'imperfectum_s': 'lag', 'hulpwerkwoord': 'hebben'}, \
    'dragen': {'imperfectum_p': 'droegen', 'perfectum': 'gedragen', 'engels': 'carry', 'imperfectum_s': 'droeg', 'hulpwerkwoord': 'hebben'}, \
    'mogen': {'imperfectum_p': 'mochten', 'perfectum': 'gemogen', 'engels': 'be allowed to', 'imperfectum_s': 'mocht', 'hulpwerkwoord': 'hebben'}, \
    'moeten': {'imperfectum_p': 'moesten', 'perfectum': 'gemoeten', 'engels': 'must', 'imperfectum_s': 'moest', 'hulpwerkwoord': 'hebben'}, \
    'kunnen': {'imperfectum_p': 'konden', 'perfectum': 'gekund', 'engels': 'be able', 'imperfectum_s': 'kon', 'hulpwerkwoord': 'hebben'}, \
    'treffen': {'imperfectum_p': 'troffen', 'perfectum': 'getroffen', 'engels': 'hit', 'imperfectum_s': 'trof', 'hulpwerkwoord': 'hebben'}, \
    'lopen': {'imperfectum_p': 'liepen', 'perfectum': 'gelopen', 'engels': 'walk', 'imperfectum_s': 'liep', 'hulpwerkwoord': 'hebben'}, \
    'gaan': {'imperfectum_p': 'gingen', 'perfectum': 'gegaan', 'engels': 'go', 'imperfectum_s': 'ging', 'hulpwerkwoord': 'zijn'}, \
    'krijgen': {'imperfectum_p': 'kregen', 'perfectum': 'gekregen', 'engels': 'get', 'imperfectum_s': 'kreeg', 'hulpwerkwoord': 'hebben'}, \
    'denken': {'imperfectum_p': 'dachten', 'perfectum': 'gedacht', 'engels': 'think', 'imperfectum_s': 'dacht', 'hulpwerkwoord': 'hebben'}, \
    'spreken': {'imperfectum_p': 'spraken', 'perfectum': 'gesproken', 'engels': 'speak', 'imperfectum_s': 'sprak', 'hulpwerkwoord': 'hebben'}, \
    'eten': {'imperfectum_p': 'aten', 'perfectum': 'gegeten', 'engels': 'eat', 'imperfectum_s': 'at', 'hulpwerkwoord': 'hebben'}, \
    'liegen': {'imperfectum_p': 'logen', 'perfectum': 'gelogen', 'engels': 'lie', 'imperfectum_s': 'loog', 'hulpwerkwoord': 'hebben'}, \
    'kopen': {'imperfectum_p': 'kochten', 'perfectum': 'gekocht', 'engels': 'buy', 'imperfectum_s': 'kocht', 'hulpwerkwoord': 'hebben'}, \
    'schrijven': {'imperfectum_p': 'schreven', 'perfectum': 'geschreven', 'engels': 'write', 'imperfectum_s': 'schreef', 'hulpwerkwoord': 'hebben'}, \
    'zijn': {'imperfectum_p': 'waren', 'perfectum': 'geweest', 'engels': 'be', 'imperfectum_s': 'was', 'hulpwerkwoord': 'zijn'}, \
    'doen': {'imperfectum_p': 'deden', 'perfectum': 'gedaan', 'engels': 'do', 'imperfectum_s': 'deed', 'hulpwerkwoord': 'hebben'}, \
    'geven': {'imperfectum_p': 'gaven', 'perfectum': 'gegeven', 'engels': 'give', 'imperfectum_s': 'gaf', 'hulpwerkwoord': 'hebben'},
}
VERBS_KW = {'imperfectum_p': 'Imperfectum pl.: ', 'perfectum': 'Perfectum: ', 'engels': 'Engels: ', 'imperfectum_s': 'Imperfectum s.: ', 'hulpwerkwoord': 'Hulpwerkwoord: '}
GAMES = {}
app = Flask(__name__)

HTMLWRAP_HEAD = '<!doctype html>'
HTMLWRAP_HEAD += '<html lang="nl"><head>'
HTMLWRAP_HEAD += '<meta charset=utf-8>'
HTMLWRAP_HEAD += '<meta name="viewport" content="width=device-width, initial-scale=1">'
HTMLWRAP_HEAD += '<title>Onregelmatige werkwoorden</title>'
HTMLWRAP_HEAD += '</head><body><pre>'
HTMLWRAP_FOOT = "</pre></body></html>"

class Game(object):
    def __init__(self, gid):
        self.gid = gid
        self.answers = []
        self.score = 0.0
        self.score_max = 0

    def add_answer(self, answer):
        # convert response to something more mangeable
        sol = VERBS[answer['infinitief']]
        score = 0.0

        answer = answer.to_dict()
        # calculate the score
        for tag in answer.keys():
            if tag != 'infinitief':
                if answer[tag].lower() == sol[tag]:
                    score += 0.2
                    answer[tag] = '<font color="green">{}</font>'.format(answer[tag])
                else: 
                    answer[tag] = '<strike>{}</strike> (<font color="red"><strong>{}</strong></font>)'.format(answer[tag], sol[tag])

        answer['score'] = score
        self.score += score
        self.score_max += 1

        self.answers.append(answer)

    def get_results(self):
        res = ""
        for ans in self.answers:
            res += '<strong>{}</strong> => '.format(ans['infinitief'])
            res += 'Hulpwerkwoord: {} | '.format(ans['hulpwerkwoord'])
            res += 'Imperfectum s.: {} | '.format(ans['imperfectum_s'])
            res += 'Imperfectum pl.: {} | '.format(ans['imperfectum_p'])
            res += 'Perfectum: {} | '.format(ans['perfectum'])
            res += 'Engels: {}'.format(ans['engels'])
            res += '<br />'
        return res

def offer_game():
        res = HTMLWRAP_HEAD
        res +=  "This game doesn't exist!!!"
        res += '<br /><br />'
        res += '<a href="/"><strong>But you can start a new one...!</strong></a>'
        res += HTMLWRAP_FOOT
        return res

def gen_question(gid):
    q = random.choice(list(VERBS.keys()))
    dynfrm = {} # to keep the presentation a little bit standardised
    for tag in VERBS[q]:
        if tag == 'hulpwerkwoord':
            dynfrm['aux'] = '<label for="{}">Hebben</label><input type="radio" name="{}" value="hebben" checked="checked" /> '.format(tag, tag)
            dynfrm['aux'] += '<label for="{}">Zijn</label><input type="radio" name="{}" value="zijn" /><br />'.format(tag, tag)
        else:
            dynfrm[tag] = '<label for="{}">{}</label>'.format(tag, VERBS_KW[tag])
            dynfrm[tag] += '<input type="text" autocomplete="off" name="{}" id="{}" value="" />'.format(tag, tag)
            dynfrm[tag] += '<br />'


    frm = HTMLWRAP_HEAD
    frm += '<form action="/{}/" method="post">'.format(gid)
    frm += '<input type="hidden" name="infinitief" value="{}" />'.format(q)
    frm += '<label for="infinitief"><strong>{}</strong></label><br />'.format(q)
    frm += dynfrm['aux']
    frm += dynfrm['imperfectum_s']
    frm += dynfrm['imperfectum_p']
    frm += dynfrm['perfectum']
    frm += dynfrm['engels']
    frm += '<input type="submit" value="Submit" />'
    frm += '<input type="submit" value="Stop" formaction="stop/" />'.format(gid)
    frm += '</form>'
    frm += '<br />Please note that the STOP button will not count the current results'
    frm += HTMLWRAP_FOOT
    return frm

@app.route("/<gid>/stop/", methods=['GET', 'POST'])
def stop(gid=None):
    if gid not in GAMES.keys():
        return offer_game()

    g = GAMES.pop(gid)
    results = []

    score = HTMLWRAP_HEAD
    score += "Total score: {} / {}!".format(round(g.score, 2), g.score_max)
    score += '<br /><br />'
    score += g.get_results()
    score += '<br /><br />'
    score += '<a href="/"><strong>New game</strong></a>'
    score += HTMLWRAP_FOOT

    return score

@app.route("/<gid>/", methods=['GET', 'POST'])
def question(gid=None):
    global GAMES
    if gid not in GAMES.keys():
        return offer_game()

    g = GAMES[gid]

    # we are dealing with answers here
    if request.method == 'POST':
        g.add_answer(request.form)
        return gen_question(g.gid)
    else: # this is a brand new question
        return gen_question(g.gid)

@app.errorhandler(404)
def page_not_found(e):
    return offer_game()

@app.route("/")
def index():
    # generate game ID and redirect
    g = Game(str(uuid.uuid4()))
    GAMES[g.gid] = g

    return redirect("/{}".format(g.gid))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
