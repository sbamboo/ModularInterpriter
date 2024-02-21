import zlib,os,json
from coda.norm_rule_file import normRuleFile

def crc32Checksum(filePath):
    crc32Hash = 0
    with open(filePath, "rb") as f:
        for byteBlock in iter(lambda: f.read(4096), b""):
            crc32Hash = zlib.crc32(byteBlock, crc32Hash)
    return crc32Hash & 0xFFFFFFFF

def writeTextAndGetCrc32(text, filePath):
    # Write text to file
    with open(filePath, 'w+') as file:
        file.write(text)
    # Calculate CRC32 checksum
    crc32Hash = 0
    with open(filePath, "rb") as f:
        for byteBlock in iter(lambda: f.read(4096), b""):
            crc32Hash = zlib.crc32(byteBlock, crc32Hash)
    return crc32Hash & 0xFFFFFFFF

class UnsetRuleset(Exception):
    def __init__(self,message="Ruleset was None, have a file been loaded?"):
        self.message = message
        super().__init__(self.message)

class InvalidRulesetTypeOrValue(Exception):
    def __init__(self,message="Invalid ruleset!"):
        self.message = message
        super().__init__(self.message)

class ModularInterpriter():
    '''Main modular interpriter class.'''
    def __init__(self,cache=True,cachePath="./.modintep_cache"):
        self.doCache = cache
        self.cachePath = cachePath
        self.cacheFile = "latest.json"
        self.cacheMem = {
            "hasCached": False,
            "file": None,
            "crc32": None
        }
        self.ruleset = None

    def _cache(self,json):
        '''INTERNAL: Function to cache json.'''
        if self.doCache == True:
            newCacheChecksum = self.cacheMem.get("crc32")
            oldCacheChecksum = None
            if self.cacheMem["hasCached"] == True:
                if os.path.exists(self.chackeMem.get("file")):
                    oldCacheChecksum = crc32Checksum(self.chackeMem.get("file"))
            cacheAgain = True
            if oldCacheChecksum == newCacheChecksum and None not in [newCacheChecksum,oldCacheChecksum]:
                cacheAgain == False
            if cacheAgain == True:
                self.cacheMem["file"] = os.path.join(os.path.abspath(self.cachePath),self.cacheFile)
                self.cacheMem["crc32"] = writeTextAndGetCrc32(json,self.cacheMem.get("file"))
                self.cacheMem["hasCached"] = True
            self.ruleset = self.cacheMem.get("file")
        else:
            self.ruleset = json

    def _getRuleset(self):
        '''INTERNAL: Function to get the asigned ruleset.'''
        if self.ruleset == None:
            raise UnsetRuleset()
        else:
            if self.cache == False:
                if type(self.ruleset) == dict:
                    return self.ruleset
                else:
                    raise InvalidRulesetTypeOrValue(f"Caching is disabled which should deffine ruleset as a dictionary, but it wasnt! (Invalid ruleset type '{type(self.rulesett)}' for cache.mode=Disabled)")
            else:
                if os.path.exists(self.ruleset) == dict:
                    _raw = open(self.ruleset,'r').read()
                    return json.loads(_raw)
                else:
                    raise InvalidRulesetTypeOrValue(f"Caching is enabled which should deffine ruleset as a filepath, but said file does not exist! (Invalid ruleset path '{self.rulesett}' for cache.mode=Enabled)")
    
    def _compile(self):
        '''INTERNAL: Function to compile a ruleset file to an operation-execution-order.'''
        pass
                
    def load(self,filepath,readingtype="byFileExt",debug=False,passIndexFallback=[0],encoding="utf-8"):
        '''Loads a coda or json file and saves it for usage.'''
        json = normRuleFile(
            ruleFile=filepath,
            type=readingtype,
            retDict=False,
            prepDict={},
            debug=debug,
            passIndexFallback=passIndexFallback,
            encoding=encoding
        )
        self._cache(json)

    def parse(self,text):
        '''Parses a string with the currently set ruleset.'''
        pass

test = ModularInterpriter()