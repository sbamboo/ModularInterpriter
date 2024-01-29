import json

# Takes Coda and returns JSON
def codaToJson(codaString,retDict=False,prepDict=None):
    lines = codaString.split("\n")
    if prepDict != None:
        jsonDict = prepDict
    else:
        jsonDict = {}
    for line in lines:
        if line.startswith("!"):
            line = line.replace("!", "", 1)
        # find type:section part
        ind = line.find(":")
        # find section part
        post_colon_part = line[ind:].split(" ")
        section = (post_colon_part[0]).lstrip(":")
        expression = post_colon_part[1:]
        # find type part
        post_colon_part = line[:ind].split(" ")
        _type = post_colon_part[-1]
        options = post_colon_part[:-1]
        # handle options
        _options = {}
        for opt in options:
            if opt.strip() != "":
                _options[opt] = True
        options = _options
        # check/find operand
        operand = "ambi"
        if ">" in section:
            _section = section.split(">")
            section = _section[0]
            operand = _section[1]
        # handle expressions
        _expression = []
        for exp in expression:
            if exp.strip() != "":
                exp = exp.replace("\\§","%1")
                exp = exp.replace("§"," ")
                exp = exp.replace("%1","§")
                exp = exp.replace("\\\\","%2")
                exp = exp.replace("\\","")
                exp = exp.replace("%2","\\")
                _expression.extend( [exp] )
        expression = _expression

        # encase
        if section == "encase":
            if jsonDict.get("encase") == None: jsonDict["encase"] = {}
            if jsonDict["encase"].get(_type) == None: jsonDict["encase"][_type] = []
            # struct
            if _type == "struct":
                data = {"ex":expression}
                data.update(options)
                jsonDict["encase"]["struct"].append(data)
            # interc
            elif _type == "interc":
                data = {"ex":expression[0]}
                data.update(options)
                jsonDict["encase"]["interc"].append(data)
        
        # keyword
        elif section == "keyword":
            if jsonDict.get("keyword") == None: jsonDict["keyword"] = {}
            # operand
            if _type == "operand":
                if jsonDict["keyword"].get("operand") == None: jsonDict["keyword"]["operand"] = {}
                if jsonDict["keyword"]["operand"].get(operand) == None: jsonDict["keyword"]["operand"][operand] = []
                for p in expression:
                    if p not in jsonDict["keyword"]["operand"][operand]:
                        jsonDict["keyword"]["operand"][operand].append(p)
            # literal
            elif _type == "literal":
                if jsonDict["keyword"].get("literal") == None: jsonDict["keyword"]["literal"] = []
                for p in expression:
                    if p not in jsonDict["keyword"]["literal"]:
                        jsonDict["keyword"]["literal"].append(p)

        # spacers
        elif section == "spacer":
            if jsonDict.get("spacer") == None: jsonDict["spacer"] = []
            for p in expression:
                if p not in jsonDict["spacer"]:
                    jsonDict["spacer"].append(p)

    # return as json
    if retDict == True:
        return jsonDict
    else:
        return json.dumps(jsonDict)