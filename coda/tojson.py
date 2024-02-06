import json

# Function to simplify index selection and return simple list of only asigned indexes.
# min max are given for the specified indexes to act as default.
def passIndSelectionSimplifier(indexes,min=int,max=int):
    '''min/max are inclusive.'''
    # Handle ranges
    nindexes = []
    int_val_mapp = dict(enumerate(indexes))
    for i,ind in int_val_mapp.items():
        step = 1
        if type(ind) == str:
            if "-" in ind:
                pa = ind.split("-")
                mn = pa[0]
                if len(pa) > 1:
                    if "_" in pa[1]:
                        p = pa[1].split("_")
                        mx = p[0]
                        if len(p) > 1:
                            step = p[1]
                    else:
                        mx = pa[1]
                    nindexes = indexes[:i] + [i2 for i2 in range(int(mn),int(mx)+1,int(step)) if i2 not in indexes] + indexes[i+1:]
                    indexes = [i3 for i3 in nindexes if i3 >= min and i3 <= max]
    # Check if any * should be added due to no inclusive indexes
    has_inclusive = False
    for ind in indexes:
        if not str(ind).startswith("!"):
            has_inclusive = True
    # If no inclusive indexes where found in the previous step, add a * to the start of the indexes
    if has_inclusive == False:
        _pre = ["*"]
        _pre.extend(indexes)
        indexes = _pre
    # If a * is in the index-list add a range of values based on the min-max (inclusive-of-max)
    if "*" in indexes:
        indexes.remove("*")
        for i in range(min,max+1):
            if i not in indexes:
                indexes.append(i)
    # Mark any excluded-index for removal
    toRem = []
    for ind in indexes:
        if str(ind).startswith("!"):
            toRem.append( int(str(ind).replace("!","",1)) )
            toRem.append(str(ind))
    # Remove any excluded index
    for tr in toRem:
        if tr in indexes: indexes.remove(tr)
    # Return
    return [ int(i) for i in indexes ]

# Function to create a category -> length mapping for rulesets.
def createLenghtMapping(ruleset,debug=False):
    mapping = {}
    for key,value in ruleset.items():
        if key != "passes":
            if type(value) == dict:
                for key2,value2 in value.items():
                    mapping[key+"."+key2] = len(value2)
            elif type(value) == list:
                mapping[key] = len(value)
            else:
                mapping[key] = 1
    if debug == True:
        print(f"\033[90mlenghtMapping: \033[33m{mapping}\033[0m\n")
    return mapping

# Function to simply category selection and their related indexes. handling exclusions and all-notation.
def passSelectionSimplifier(inputed_passRules,lengthMapping,fallback=["*"],debug=False):
    # join to one dictionary
    passRules = {}
    debug_keep = {}
    for part in inputed_passRules:
        key = list(part.keys())[0]
        value = list(part.values())[0]
        passRules[key] = value
        if debug: debug_keep[key] = {"old":value,"new":"EXCLUDED"}
    # Check if * is used as fill-in
    toRem = []
    matches = {}
    for key,value in passRules.items():
        if key.endswith(".*"):
            if key.startswith("!"):
                exclusive = True
                key = key.replace("!","",1)
            else:
                exclusive = False
            parent = key[::-1].replace("*.",".",1)[::-1]
            for key2 in lengthMapping.keys():
                if key2.strip().startswith(parent):
                    matches[key2] = value
                    if key not in toRem: toRem.append(key)
    for tr in toRem:
        if tr in passRules.keys(): passRules.pop(tr)
    for m in matches.keys():
        if m not in passRules.keys():
            if debug: debug_keep[m] = {"old":matches[m],"new":"EXCLUDED"}
            passRules[m] = matches[m]
    # check if * should be added (if no inclusive indexes are set)
    has_inclusive = False
    _keys = list(passRules.keys())
    for rule in _keys:
        if not rule.startswith("!"):
            has_inclusive = True
    if has_inclusive == False and inputed_passRules != []:
        passRules["*"] = ["*"]
        _keys.append("*")
    # if * in keys add al non-existing keyss
    if "*" in _keys:
        for key in lengthMapping.keys():
            if key not in _keys:
                passRules[key] = passRules["*"]
                if debug: debug_keep[key] = {"old":passRules["*"],"new":"EXCLUDED"}
        passRules.pop("*")
    # mark to remove any excluded key
    toRem = []
    for key in passRules.keys():
        if key.startswith("!"):
            toRem.append( key.replace("!","",1) )
            toRem.append( key )
    # remove excluded keys
    for tr in toRem:
        if tr in passRules.keys(): passRules.pop(tr)
    # use lengthMapping to simplify the rule's indexes, also make into list of dicts just like inputed from the begining
    toReturn = []
    for key,value in passRules.items():
        if lengthMapping.get(key) != None:
            #get
            nvalue = passIndSelectionSimplifier(value,0,lengthMapping[key]-1)
            # filter
            filtered = []
            for v in nvalue:
                if v >= 0 and v <= lengthMapping[key]-1:
                    filtered.append(v)
            if len(filtered) == 0: filtered = fallback
            # debug
            if debug:
                try: debug_keep[key]["new"] = filtered
                except: pass
            # append
            toReturn.append( {key: filtered} )
    if debug:
        for key,val in debug_keep.items():
            print(f"\033[90mSelectionSimplifier> \033[34m{key}: \033[33m{val['old']} \033[90m=> \033[32m{val['new']}\033[0m")
        print("")
    # return
    return toReturn
    
    
# Function to join @pass and following @lpass command-args to one @pass command
def join_lpasses(lines,debug=False):
    seenPass = False
    markedForRem = []
    for i,line in enumerate(lines):
        sline = line.strip().lower()
        _parts = sline.split(" ")
        checkLine = _parts[0]
        prefix = ""
        if "@" in checkLine:
            prefix = checkLine.split("@")[0]
            command = "@"+checkLine.split("@")[1]
            sline = sline.replace(prefix,"",1)
        if debug: print(f"\033[90mlPassJoiner>\033[33m {seenPass}\033[90m,\033[34m {sline}\033[90m,\033[31m{prefix}\033[0m")
        if sline.startswith("@pass"):
            seenPass = i
        elif sline.startswith("@lpass"):
            if type(seenPass) == bool and seenPass == False:
                lines[i] = line.lower().replace("@lpass","@pass")
                seenPass = i
            else:
                parts = line.split(" ")
                if len(parts) > 1:
                    if i != 0:
                        prevLines = lines[seenPass].rstrip(" ")
                        if prevLines.endswith("&"):
                            lines[seenPass] = prevLines + ' '.join(parts[1:])
                        else:
                            lines[seenPass] = prevLines + "&" + ' '.join(parts[1:])
                        markedForRem.append(i)
    for ind in sorted(markedForRem)[::-1]:
        lines.pop(ind)
    return lines


# Takes Coda and returns JSON
def codaToJson(codaString,retDict=False,prepDict=None,passIndexFallback=[0],debug=False):
    lines = codaString.split("\n")
    lines = join_lpasses(lines,debug)
    if prepDict != None:
        jsonDict = prepDict
    else:
        jsonDict = {}
    hasshdebt = False
    for line in lines:
        line = line.strip()
        if line.startswith("!"):
            line = line.replace("!", "", 1)
        # check for commands (prefixed by @)
        checkLine = line.split(" ")[0]
        if "@" in checkLine:
            # remove @
            _parts = checkLine.split("@")
            section = _parts[1].lower()
            # get command by splitting by space and rest as args
            parts = line.replace(checkLine,"",1).strip().split(" ")
            if type(parts) == str: parts = [parts]
            if len(parts) >= 1:
                expression = [i.lower() for i in parts]
            else:
                expression = []
            _type = "syntx_command"
            operand = _parts[0]
        # otherwise parse as rulew
        else:
            # find type:section part
            ind = line.find(":")
            # find section part
            post_colon_part = line[ind:].split(" ")
            section = (post_colon_part[0]).lstrip(":")
            expression = post_colon_part[1:]
            # find type part
            post_colon_part = line[:ind].split(" ")
            _type = post_colon_part[-1].lower()
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
            section = section.lower()
            _type = _type.lower()

        # commands
        if _type == "syntx_command":
            lastPassInd = -1
            if section == "pass":
                if jsonDict.get("passes") == None: jsonDict["passes"] = []
                pieces = ' '.join(expression)
                pieces = pieces.split("&")
                # get indexes for piece
                hpieces = []
                for p in pieces:
                    parts = p.split(" ")
                    key = parts[0]
                    if len(parts) > 1:
                        vls = ','.join(parts[1:])
                        vls = vls.replace(",,",",")
                        value = vls.split(",")
                    else:
                        # not-exclusions should have value of [] not [0]
                        if key.startswith("!"):
                            value = []
                        # for all-notations (*) the default should be *
                        elif key == "*":
                            value = ["*"]
                        # normal is default to 0 (set by: passIndexFallback)
                        else:
                            value = passIndexFallback
                    if key != "" and key != None:
                        exi = False
                        for i,_exi in enumerate(hpieces):
                            if list(_exi.keys())[0] == key:
                                exi = [i,key]
                        if exi == False:
                            hpieces.append({key:value})
                        else:
                            for v in value:
                                if v not in hpieces[exi[0]][exi[1]]:
                                    hpieces[exi[0]][exi[1]].append(v)
                _id = ""
                _mode = ""
                _link = ""
                if "=" in operand:
                    _id = operand.split("=")[0]
                    _mode = operand.split("=")[1]
                else:
                    _mode = operand
                if ":" in _mode:
                    _mode = _mode.split(":")[0]
                    _link = operand.split(":")[1]
                if _mode == "org": _mode = "original"
                if _mode == "rem": _mode = "remainder"
                if _mode == "res": _mode = "result"
                jsonDict["passes"].append({"ind":hpieces,"id":_id,"mode":_mode,"link":_link})
                lastPassInd += 1
            elif section == "opt":
                if jsonDict.get("options") == None: jsonDict["options"] = []
                jsonDict["options"].append(expression)

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

        # regex
        elif section == "regex":
            if jsonDict.get("regex") == None: jsonDict["regex"] = {}
            # cutting
            if _type == "cu": _type = "cutting"
            if _type == "cutting":
                if jsonDict["regex"].get("cutting") == None: jsonDict["regex"]["cutting"] = {}
                if jsonDict["regex"]["cutting"].get(operand) == None: jsonDict["regex"]["cutting"][operand] = []
                for p in expression:
                    if p not in jsonDict["regex"]["cutting"][operand]:
                        jsonDict["regex"]["cutting"][operand].append(p)
            # keeping
            if _type == "ke": _type = "keeping"
            if _type == "keeping":
                if jsonDict["regex"].get("keeping") == None: jsonDict["regex"]["keeping"] = {}
                if jsonDict["regex"]["keeping"].get(operand) == None: jsonDict["regex"]["keeping"][operand] = []
                for p in expression:
                    if p not in jsonDict["regex"]["keeping"][operand]:
                        jsonDict["regex"]["keeping"][operand].append(p)

        if debug:
            if hasshdebt == False:
                print("\033[90mCodaToJson >")
                hasshdebt = True
            print(
f"""
    \033[90mline:       \033[32m{line}\033[90m,
    \033[90msection:    \033[32m{section}\033[90m,
    \033[90m_type:      \033[32m{_type}\033[90m,
    \033[90moperand:    \033[32m{operand}\033[90m,
    \033[90mexpression: \033[32m{expression}\033[0m
"""
        )

    # Simplify passes
    exklNms = [key for key in list(jsonDict.keys()) if key not in ["passes","options"]]
    if exklNms != []:
        if jsonDict.get("passes") == None or jsonDict.get("passes") == []:
                jsonDict["passes"] = [ {"ind":[{"*":["*"]}],"id":"","mode":"","link":""} ]
        lengthMapping = createLenghtMapping(jsonDict,debug) # get length-mapping
        toRem = []
        for i,codapass in enumerate(jsonDict["passes"]):
            nv = passSelectionSimplifier(codapass["ind"],lengthMapping,passIndexFallback,debug)
            if nv != []:
                jsonDict["passes"][i]["ind"] = nv
            else:
                toRem.append(i)
        for i in toRem[::-1]:
            jsonDict["passes"].pop(i)

    # return as json
    if retDict == True:
        return jsonDict
    else:
        return json.dumps(jsonDict)