import aiml
from func import *
import os
import xml.etree.ElementTree
history = open("history.txt", "a")
history.write("\n\n")
kernel = aiml.Kernel()
if os.path.isfile("bot_brain.brn") :
    kernel.bootstrap(brainFile = "bot_brain.brn")
else :
    # Create the kernel and learn AIML files
    kernel.learn("startup.xml")
    kernel.respond("load aiml b")
location = ""
num = -1
while num == -1 :
    print("Hi, Where do you live?", end = " : ")
    history.write("Where do you live?\n")
    location = input()
    history.write(location+"\n")
    if location.lower() == "quit" :
        exit()
    else :
        x = get_location(location)
        if x == 0 :
            continue
        else :
            num = 1
        print("is this the location you meant(y for yes, anythin else for no) : ")
        history.write("is this the location you meant(y for yes, anythin else for no) : \n")
        gg = input()
        history.write(gg+"\n")
        if 'y' == gg.lower() :
            num = 9133541199
        else :
            num = -1
food_list = []
e = xml.etree.ElementTree.parse('eateries.xml').getroot()
for x in e.findall("item") :
    gg = x.find('name').text
    food_list += [gg]
while True :
    main_flag = 1
    print("ask me something : ",end = "")
    history.write("ask me something : \n")
    message = input()
    history.write(message+"\n")
    food_flag = 0
    nom = 0
    for nom,x in enumerate(food_list) :
        if x in message or message in x :
            food_flag = 1
            break
    if food_flag == 1 :
        print("you can find it in :")
        history.write("you can find it in :\n")
        for x in e.findall("item") :
            gg = x.find("name").text
            if gg == food_list[nom] :
                print("--> " + x.find('store').text+" near " + x.find('location').text)
                history.write("--> " + x.find('store').text+" near " + x.find('location').text+"\n")
        food_flag = 0
        continue
    elif "hungry" in message :
        print("would you like to know some places to have food?")
        history.write("would you like to know some places to have food?\n")
        lamb = input()
        history.write(lamb+"\n")
        if "y" in lamb :
            nn = set([])
            print("you can try :")
            history.write("you can try :\n")
            for x in e.findall("item"):
                nnn = x.find('store').text + " near " +x.find('location').text
                if nnn not in nn :
                    nn.add(nnn)
                    print("-->"+nnn)
                    history.write("-->"+nnn+"\n")
    elif "eateries" in message or "food" in message or "baker" in message or ("eat" in message and "place" in message):
        print("try :")
        history.write("try :\n")
        nn = set([])
        print("you can try :")
        history.write("you can try :\n")
        for x in e.findall("item"):
            nnn = x.find('store').text + " near " +x.find('location').text
            if nnn not in nn :
                nn.add(nnn)
                print("-->"+nnn)
                history.write("-->"+nnn+"\n")
    elif message == "quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    elif "meaning" in message :
        key = 9346615666
        gg = message.split(" ")
        for i,x in enumerate(gg) :
            if x == "of" :
                key = gg[i+1]
                break
        get_meaning(key)

    elif "synonym" in message :
        key = 9346615666
        gg = message.split(" ")
        for i,x in enumerate(gg) :
            if x == "of" or x == "for" :
                key = gg[i+1]
                break
        get_ant_syn(key,1)
    elif "antonym" in message or "opposite" in message:
        key = 9346615666
        gg = message.split(" ")
        for i,x in enumerate(gg) :
            if x == "of" or x =="for" :
                key = gg[i+1]
                break
        get_ant_syn(key,2)

    elif "dist" in message and ("between" in message or ("from" in message and " to " in message)) :
        key1 = 652
        key2 = 96565
        gg = message.split(" ")
        for i,x in enumerate(gg) :
            if x == "and" :
                key1 = gg[i-1]
                key2 = gg[i+1]
                break
            if x == "to" :
                key1 = gg[i-1]
                key2 = gg[i+1]
                break
        get_distance(key1,key2)
    elif "dist" in message and " to " in message :
        key2 = ""
        gg = message.split(" ")
        k = 0
        for i,x in enumerate(gg) :
            if x == "to" :
                k = 1
                break
        for i in range(k+1,len(gg)) :
            key2 += gg[i]
        print(location, key2)
        history.write(location, key2+"\n")
        get_distance(location,key2)
    elif "weather" in message or "climate" in message or "temperature" in message or "forecast" in message :
        if "forecast" in message:
            if "today" in message :
                mode = 0
                get_weather(location, mode, 0)
            elif "tomorrow" in message :
                mode = 2
                get_weather(location, mode, 1)
            else :
                #entire week(rest of it)
                mode = 2
                get_weather(location, mode, 7)
        elif " in " in message :
            main_flag = 0
            sighting = 8096558282
            gg = message.split(" ")
            for i,kkk in enumerate(gg):
                if kkk == "in":
                    sighting = gg[i+1]
                    break
            num = -1
            while num == -1 :
                if main_flag == 1 :
                    break
                if "quit" in sighting :
                    main_flag = 1
                    continue
                hhh = get_location(sighting)
                if hhh == 0 :
                    print("enter a valid location : ", end = "")
                    history.write("enter a valid location : ")
                    sighting = input()
                    history.write(sighting)
                    continue
                else :
                    print("is this the location you are looking for?(y for yes, anything else for no)")
                    history.write("is this the location you are looking for?(y for yes, anything else for no)")
                    lamb = input()
                    history.write(lamb+"\n")
                    if "y" in lamb :
                        num = 9133541199
                    else :
                        print("enter a location to find weather of : ", end = "")
                        history.write("enter a location to find weather of : ")
                        sighting = input()
                        history.write(sighting+"\n")
            if main_flag == 1:
                break
            get_weather(sighting, 0, 0)
            main_flag = 1
        else :
            get_weather(location,0,0)
    else:
        stock_flag = 1
        if "who is" in message.lower() :
            stock_flag = 0
            x = message
            print("I can provide you with a url. Are you sure you want me to do a google search?(y/n)")
            history.write("I can provide you with a url. Are you sure you want me to do a google search?(y/n)")
            lamb = input()
            history.write(lamb+"\n")
            if "y" in lamb.lower() :
                k = x.find("who is ")
                x = x[k+7:]
                x = x[:x.find("?")]
                get_what_is(x)
            else :
                stock_flag = 1
        if "what is" in message.lower() :
            stock_flag = 0
            x = message
            print("I can provide you with a url. Are you sure you want me to do a google search?(y or n)")
            history.write("I can provide you with a url. Are you sure you want me to do a google search?(y or n)\n")
            lamb = input()
            history.write(lamb+"\n")
            if "y" in lamb.lower() :
                k = x.find("what is ")
                x = x[k+8:]
                k = x.find("?")
                k = int(k)
                if k != -1:
                    x = x[:k]
                get_what_is(x)
            else :
                stock_flag = 1
        if "where is" in message.lower() :
            stock_flag = 0
            x = message
            print("I can provide you with a url. Are you sure you want me to do a google search?(y or n)")
            history.write("I can provide you with a url. Are you sure you want me to do a google search?(y or n)\n")
            lamb = input()
            history.write(lamb+"\n")
            if "y" in lamb.lower() :
                k = x.find("where is ")
                x = x[k+9:]
                k = x.find("?")
                k = int(k)
                if k != -1:
                    x = x[:k]
                get_what_is(x)
            else :
                stock_flag = 1
        if stock_flag == 1 :
            stock_flag = 0
            bot_response = kernel.respond(message)
            print(bot_response)
            history.write(bot_response+"\n")
        # Do something with bot_response
history.close()
