# Functions to normalise rule files, so takes both rule.coda, ruleset.coda, rule.json, ruleset.json
# Note the difference between ruleset and rule, a rule-sheet contain only the parsing config not the "passes" field.
#

import json,os
from tojson import codaToJson

# Main function
def normRuleFile(ruleFile,type="byFileExt",retDict=False,prepDict={},debug=False,passIndexFallback=[0],encoding="utf-8"):
    '''Function to take in either a codafile or jsonfile and retun '''
    _raw = None
    if os.path.exists(ruleFile):
        _raw = open(ruleFile,'r',encoding=encoding).read()
    else:
        raise FileNotFoundError(f"File not found! {ruleFile}")
    if _raw != None:
        if type.lower() == "byfileext":
            _, file_extension = os.path.splitext(ruleFile)
            if file_extension.lower() == ".coda":
                type = "coda"
            elif file_extension.lower() == ".json":
                type = "json"
            else:
                raise Exception(f"Readingtype set to 'byFileExt' but type for file-extension '{file_extension}' could not be determined!")
        if type.lower() == "coda":
            parts = []
            for p in _raw.split("\n"):
                parts.extend(p.split(";"))
            _dict = codaToJson(
                codaString='\n'.join(parts),
                retDict=True,
                prepDict=prepDict,
                passIndexFallback=passIndexFallback,
                debug=debug
            )
            if retDict == True: return            _dict
            else:               return json.dumps(_dict)
        elif type.lower() == "json":
            _dict = json.loads(_raw)
            if prepDict != None and prepDict != {}:
                _dict = prepDict.update(_dict)
            _dictU = codaToJson(
                codaString="",
                retDict=True,
                prepDict=_dict,
                passIndexFallback=passIndexFallback,
                debug=debug
            )
            if retDict == True: return            _dictU
            else:               return json.dumps(_dictU)
        else:
            raise Exception(f"Can't determine readingtype, set 'type' to either 'coda'/'json' or 'byFileExt' (type: {type})")
    else:
        raise Exception("Can't load file, content was None!")
    
res = normRuleFile("C:\\Users\\simonkalmi.claesson\\Documents\\GitHub\\ModularInterpriter\\docs\\example2.json",retDict=True)
print(res)