'''
Script that extracts domain knowledge features from chats

We adopted two strategies:
1) Categorization of chat messages (i.e., wrote by the players)
    Here we defined common words used in different contexts, i.e., laugh, slang, bad and good behaviour, and provocative messages at the end of the game (gg ez).
    We also searched for messages containing only '?' (which is highly provocative for the other team), number of question marks, exclamative marks, capital letters,
    early messages (sent before the game begins, usually sent to make noise or interact with the other team), and messages after a kill (which can be for complaining, provoking, or similar reasons).
    We identified such words by exploring websites (e.g., dota forums, urban dictionary), chats of multiple games, and by our gaming experience.
    Then, we count the occurrences of such words in the chats typed by the player.
2) Categorization of chatweel messages (i.e., pick from pre-defined messages, and automatically translated by the game to the receiver's language)
    Here we categorized chatwheel messages that are pre-defined by the game. These are useful since we do not incur in translation problems.
    We manually analyzed the file chat_wheel.json (containing, in english, all the chatwheel messages) and identified various types of messages, i.e.,
    tactics, good behavior, and caster phrases.
    Moreover, we extracted which of them are reproduced as a sound (audible either in local or global chat), or are sprays left on the ground.
    Then, there is a second chatwheel, customised for each hero. Such messages contains general information, such as if they are laugh or deny messages, which we extracted as feature.

Last, we extracted information such as whether the message was sent locally (same team) or globally (to both teams), and whether the message was an hero message.

All the aforementioned features can be of extreme help for our task.
For instance, the use of slang could be higher for younger players.
Provocative messages can relate to both neurotic and extrovert people.
Agreeableness could be related to the use of good behavior messages.
Conscious people could use more tactics message, and openess could relate to early messages or laugh messages after a kill.
The gender could be affected from several of such typing and hero chatwheel usage.
Last, some hero messages are available only on purchase, which can be an indicator of the occupation and buy_content behavior.
'''


import pandas as pd
import numpy as np
import os
import json
from tqdm import tqdm

f = json.load(open("chat_wheel.json","r"))

#laugh indexes
laugh_index = []
for k,v in f.items():
    if "label" in v and "laugh" in v["label"].lower():
        laugh_index.append(k)

#list_laugh
list_laugh = ["lel", "lol", "lmao", "lmfao", "rofl", "lul", "lulz"]

#index tactics
tactics = [str(x) for x in range(0,61)] + ["65","66","67", "71","72","73"] + [str(x) for x in range(77,86)]

#good behavior indexes
good_behaviour = ["61","62","63","64", "68", "69","70"]

#thank indexes
thank_index = []
for k,v in f.items():
    if "thank" in v["name"]:
        thank_index.append(k)

#deny indexes
deny_index = []
for k,v in f.items():
    if "deny" in v["name"]:
        deny_index.append(k)

#all chat (global) indexes
all_chats = []
for k,v in f.items():
    if "all_chat" in v:
        all_chats.append(k)

#sound (sound_ext = "wav", mp3)
sounds = []
for k,v in f.items():
    if "sound_ext" in v:
        sounds.append(k)

#global chat sound
all_chat_sounds = []
for k,v in f.items():
    if "sound_ext" in v and "all_chat" in v:
        all_chat_sounds.append(k)

#local chat sound
in_chat_sounds = []
for k,v in f.items():
    if "sound_ext" in v and "all_chat" not in v:
        in_chat_sounds.append(k)

#sprays "image": "sprays"
sprays = []
for k,v in f.items():
    if "image" in v:
        sprays.append(k)

#caster phrases both global/local
caster_phrases = [101,112,113,114,115,116,117,118,119,120,121,122,131,152,153,154,155,156,173,174,175,176,177,179,180,181,182,183,190,191,192,193,211,212,213,214]+[x for x in range(215,231)] + [x for x in range(263,281)] + [303,304,305,316,317,318,322,323,324,328,329,330,362]
caster_phrases = [str(x) for x in caster_phrases if str(x) in f.keys()]
caster_global = [str(x) for x in caster_phrases if "all_chat" in f[str(x)]]
caster_local = [str(x) for x in caster_phrases if "all_chat" not in f[str(x)]]


lista_slang = [":)","xd","^^",":D",":(","r","ty","idk","thx","u","ur","def","lp","pos","afk","bb","ez","aoe","bot","bots","buff","nerf","feed","feeding","throw","throwing","gank","lag","op","ragequit","rq","smurf","booster","wtf","gigalel","omegalul","4head","pog","pogchamp","lol","lul","lel","lmao","rofl","omg", "omfg", "tbh","btw","brb","bff","w/e","w/o","imo","imho","dc","gtfo","irl","ftw","nvm","ff","gl","hf","rat"]

lista_bad={"fuck","bad","noob","shit","bitch","stupid","fucking","buyer","boosted","smurf","booster","fuckin","report","retard","cyka","blyat","penopt","kill","die","idiot","moron","nigger","nigga","trash","bad","dumb","pussy","clown","end","ff","reported","cancer","dick","suck", "asshole","bastard","dog","subhuman","cunt"}

ls_gb=["ggwp","gg","wp","GG","GGWP","WP", "gg wp", "gege", "gege wp"]

lista_ggez = ["ggez","gg ez", "g", "easy", "ez", "ez pz", "izi", "close game"]


df_new_features = pd.DataFrame(columns = [
        "counterTattic", #number of tactic messages (e.g., push top, go back)
        "counterGB", #number of good behavior messages (e.g., thanks, well played!)
        "counterLaugh", #number of laugh words (e.g., ahah, lol )
        "counterThank", #number of thanks messages
        "counterDeny", #number of deny messages
        "counterAllChat", #number of messages sent in all chat
        "counterSounds", #number of sound messages
        "counterSoundsAllChat", #number of sound messages sent in all chat (global)
        "counterSoundsInChat", #number of sound messages sent in local chat
        "counterSprays", #number of sprays (imgs) drawn on the ground
        "counterCaster", #number of messages (sound) that are from casters (e.g, very famous and often hilarious)
        "counterCasterIn", #number of caster messages in local chat
        "counterCasterAll", #number of caster messages in all chat
        "ggez_counter", #number of provocative/mock messages sent at the end of the game
        "bad_counter", #number of bad messages (e.g., insults, swear words0)
        "slang_counter", #number of messages using slang
        "question_mark_counter", #counter of messages containing only ? (very provocative in Dota 2)
        "counter_capital",#counter of capital letters
        "counter_question", #counter of ? in a message (e.g., "WHAT???????" can be messages coming from low agreableness people)
        "counter_exclamation", #counter of exclamation marks (!)
        "earlySpeak", #number of messages sent within the first two minutes of the game
        "spam_kill", #number of messages sent after a kill
        "hero_msg"]) #number of messages coming from hero chatwheel 

def parse_match(game, player_slot):
    root = "parsed-matches/parsed/"
    with open(root+game+'.json',encoding="utf8") as f:
        data = json.load(f)

        #counters
        counterTattic = 0
        counterGB = 0
        counterLaugh = 0
        counterThank = 0
        counterDeny = 0
        counterAllChat = 0
        counterSounds = 0
        counterSoundsAllChat = 0
        counterSoundsInChat = 0
        counterSprays = 0
        counterCaster = 0
        counterCasterIn = 0
        counterCasterAll = 0
        ggez_counter = 0
        bad_counter = 0
        slang_counter = 0
        question_mark_counter = 0
        counter_capital=0
        counter_question=0
        counter_exclamation=0
        earlySpeak = 0
        spam_kill = 0
        hero_msg = 0


        lista_tempi=[]
        #for to cycle over the players, find the target players, and save the times when kills involving him happened
        for player in data['players']:
            try:
                if player['player_slot'] == player_slot:
                    for kill in player['kills_log']:
                        lista_tempi.append(kill['time'])
            except:
                print("error first for")


        #chatwheel features
        for chat in data['chat']:
            try:

                if(chat['player_slot']==player_slot):

                    #type is "tattic"
                    if chat['key'] in tactics:
                        counterTattic += 1

                    #type is laugh:
                    if chat['key'] in laugh_index or chat['key'].lower() in list_laugh or sorted(list(set(chat['key']))) in ["ah","aj","ax","lo","eh","hi","ho","hu"]:
                        counterLaugh += 1

                    #type is good behavior
                    if chat['key'].lower() in ls_gb or chat['key'].lower() in good_behaviour:
                        counterGB += 1

                    #type is thank
                    if chat['key'] in thank_index:
                        counterThank += 1

                    #type is deny
                    if chat['key'] in deny_index:
                        counterDeny += 1

                    #type is all chat
                    if chat['key'] in all_chats:
                        counterAllChat += 1

                    #type is sounds
                    if chat['key'] in sounds:
                        counterSounds += 1

                    #type is sounds all chat
                    if chat['key'] in all_chat_sounds:
                        counterSoundsAllChat += 1

                    #type is sounds in chat
                    if chat['key'] in in_chat_sounds:
                        counterSoundsInChat += 1

                    #type is sprays
                    if chat['key'] in sprays:
                        counterSprays += 1


                    if chat['key'] in caster_phrases:
                        counterCaster += 1

                    if chat['key'] in caster_local:
                        counterCasterIn += 1

                    if chat['key'] in caster_global:
                        counterCasterAll += 1

                    if chat['key'].lower() in lista_ggez or "ez" in chat['key'].lower():
                        ggez_counter+=1

                    #take all words separately
                    token = chat['key'].split()

                    bad_counter += sum(1 for t in token if (t.lower() in lista_bad))
                    slang_counter += sum(1 for t in token if (t.lower() in lista_slang))

                    if chat['key'] == "?":
                        question_mark_counter += 1

                    if chat['type'] == "chat": #if its a custom chat (handwritten, no chatwheel)
                        counter_capital += sum(1 for c in chat['key'] if c.isupper()) #Capital chars
                        counter_question += sum(1 for c in chat['key'] if c == "?")
                        counter_exclamation += sum(1 for c in chat['key'] if c == "!")

                    #if a chat happened in first 120 sec
                    if chat['time'] < 120:
                        earlySpeak += 1

                    #if a chat happened within 40 seconds after a kill
                    for i in range(len(lista_tempi)):
                        if (int(chat['time']) <= int(lista_tempi[i]) + 40 and chat['time'] >= int(lista_tempi[i])):
                            spam_kill+=1

                    #if a chat is a 'hero' radial message, i.e., pre-defined for each hero
                    if chat['key'].isnumeric() and int(chat['key']) >= 1000:
                        hero_msg += 1


            except Exception as e:
                print("An exception occurred", e)
                print(chat)
                break

        df_new_features.loc[len(df_new_features)] = [counterTattic,
                counterGB,
                counterLaugh,
                counterThank,
                counterDeny,
                counterAllChat,
                counterSounds,
                counterSoundsAllChat,
                counterSoundsInChat,
                counterSprays,
                counterCaster,
                counterCasterIn,
                counterCasterAll,
                ggez_counter,
                bad_counter,
                slang_counter,
                question_mark_counter,
                counter_capital,
                counter_question,
                counter_exclamation,
                earlySpeak,
                spam_kill,
                hero_msg]


df = pd.read_csv("new_dataset_heroes.csv")

for i,r in tqdm(df.iterrows()):
    parse_match(str(r["match_id"]),r["player_slot"])


print(df_new_features.shape)
final_df = pd.concat([df,df_new_features], axis = 1)

df_new_features.to_csv("df_new_features.csv",index=False)

final_df.to_csv("final_df.csv",index=False)
#print(df.head())
