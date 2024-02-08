## <br>CodaSyntax
Coda is generally split into this context:

`<options><type>:<section><name> <chars_and_expressions>`

Note! The name is optional. But if a name is there it starts with >

Each options is followed by a space so: "ml " not "ml"

Expressions within qoutes are not allowed since the qoutes are recognised as symbols.

The only non-symbol recognised characters are wildcards the can be recognised by prefixing with \\

Wildcards:
>  §  = space
>
>  \\§ = §
>
>  \\  = 
>
>  \\\\ = \\

Please note that nothing can be interprited by having nothing after section. This wont get recognised.

Exception to the general parsing rule is commands like `@pass` or `@opt`

## <br><br>EncasedSections
Encased sections are encloser-syntaxes like parentheses and qoutes, they have two types: **Bidirectional** and **Interchangable**.

### <br><br>Biderectional
Bidirectional encasers have a start expression and an end expression that may not be the same.

The interpriter can then section out anything inbetween theese symbols.
>Section: encase
>
>Type:    struct

Examples:
`() {} []`

**JSON:**
```json
{
  "encase": {
    "struct": [
      {
        "ex": ["(",")"]
      }
    ]
  }
}
```
**CODA:**
```lua
struct:encase ( )
```
### <br><br>Interchangable

Interchangable encasers have one expression which the interpriter sections out content inbetween two instances of.

> Section: encase
>
> Type:    interc

Examples:
`"" '' ////`

**JSON:**
```json
{
  "encase": {
    "interc": [
      {
        "ex": "\""
      }
    ]
  }
}
```
**CODA:**
```lua
interc:encase "
```

For an encaser to be recognised beyond line endings they should be prefixed with `ml ` in c oda or by setting `ml` to `True` in json.
**JSON:**

```json
{
  "encase": {
    "interc": [
      {
        "ex": '"',
        "ml": true
      }
    ]
  }
}
```
**CODA:**
```lua
ml interc:encase "
```

By default encasers are found in *outer-most* matching but the option `fo` can be used to match first-occuerence.

**JSON:**
```json
{
  "encase": {
    "interc": [
      {
        "ex": '"',
        "fo": true
      }
    ]
  }
}
```
**CODA:**
```lua
fo interc:encase "
```

## <br>Keywords.Operands
Operands are keywords that are excluded from interpriter sections but layed as operations inbetween sections.

They can be used for tex math, where the interpriter could take `<expr> + <expr>` as 
`{"operation":"add","elem":["<expr>","<expr>"]}`

> Section: keyword
>
> Type:    operand

Examples:
`+`

They can be listed under an operation like `add`:

**JSON:**
```json
{
  "keyword": {
    "operand": {
      "add": ["+"]
    }
  }
}
```
**CODA:**
```lua
operand:keyword>add +
```

Or under no operation which in json would lead to `ambi` or ambiguous:

**JSON:**
```json
{
  "keyword": {
    "operand": {
      "ambi": ["+"]
    }
  }
}
```
**CODA:**
```lua
operand:keyword +
```

## <br>Keywords.Literals
Literals are specific keywords that can be excluded from sectioning and added for context just like operands.

> Sections: keyword
>
> Type:     literal

Examples:
`not`

**JSON:**
```json
{
  "keyword": {
    "literal": [
      "not"
    ]
  }
}
```
**CODA:**
```lua
literal:keyword not
```

## <br>Spacers
Spacers are expressions used to split sections.
Examples:<span style="margin-left: 10px;">` `<span>

**JSON:**
```json
{
  "spacer": [
    " "
  ]
}
```
**CODA:**
```lua
:spacer §
```

## <br>REGEX
  Regex matches are placed as interpriter sections, they can be cutting or keeping.
  Cutting meaning that the matches get removed from the string before next parse and keeping won't, giving you a wide range of options.
  The matches are bound to a name just like operands and no bound will similarly be bound to "ambi" or ambiguous.
  Types can be shorted to "ke" for keeping and "cu" for cutting.
  > Section: regex
  > Type:    cutting/keeping/cu/ke
  Examples:
    [a-z]
  
  Json:
  `
    {
      "regex": {
        "cutting": {
          "eng_alpha": [
            "[a-z]"
          ]
        }
      }
    }
  `
  Coda:
  `
    cutting:regex>eng_alpha [a-z]
  `

## <br>Rulesets/Passes
Rulesets are files containing the above aswell as a "passes" field, defining the order of parsing aswell as how many times the org-input should be parsed.
The "passes" contain the "calls", calls are the accual instructions in top-down order and the passes are the runs on the org-input, the categories are split by &.
The ruleset reference categories on the above code aswell as their sub-indexes split by commas. Not deffining a index will use ind:0
If you want to you may tell a pass to the use the previous remainder as input by using the @lpass comamnd instead of @pass, theese will however be converted to &-linked @pass statements.
If no spacer was used in the pass it will use al-passes deffined.
Note! You may use * to tell it to run each rule in a pass.

For example if we want to run one pass that parses out literals and operands and a second pass with regex, we first need to setup some coda for the parse-rules.
`
  :spacer §
  literal:keyword not
  operand:keyword>add +
  keeping:regex>eng_alpha [a-z]
`
Aswell as the ruleset in coda:
`
@pass spacer&keyword.literal&keyword.operand
@pass regex.keeping
`
Or:
`
@pass spacer
@lpass keyword.literal
@lpass keyword.operand
@pass regex.keeping
`

This would be the same as the JSON:
`
  {
    "spacer": [
      " "
    ],
    "keyword": {
      "literal": [
        "not"
      ]
    },
    "keyword": {
      "operand": {
        "add": [
          "+"
        ]
      }
    },
    "regex": {
      "keeping": {
        "eng_alpha": [
          "[a-z]"
        ]
      }
    },
    "passes": [
      [
        {"spacer": [0] },
        {"keyword.literal": [0] },
        {"keyword.operand": [0] }
      ],
      [
        {"regex.keeping": [0] }
      ]
    ]
  }
`
As you see, "passes" are included as a field at the bottom refferencing rules from the root.

And as you might have noticed the rules are followed by a list of ints, this is due to the index selector defaulting to 0.
But there are other ways to help you note down indexes:
Note! These can be stacked using commas.

First your normal ones where you comma seppareate them:
  `1`   = 1
  `1,2` = 1, 2

But you can also use * to select al, coda then generates a range based on the length of selectable indexes:
An example where we have four selectable indexes would give:
  `*` = [0,1,2,3]

You can also use ! to exclude an index, so if we use our previous example: (combining with the star)
  `*,!2` = [0,1,3]

If only note exclusions it will auto-fill a star so for example: (still using the previous example)
  `!2` => `*,!2` = [0,1,3]

To help with including large amounts of indexes you can use ranges, theese are in the format <min>-<max>
  `0-5` = [0,1,2,3,4,5] # note it being inclusive on both edges.

You can further detail your ranges using step-size, then in the format <min>-<max>_<step>
  `0-10_2` = [0,2,4,6,8,10]


Some of theese can also be used when selecting which rules to run in the pass for example the previous &
  `spacer&keyword.literal` = ["spacer", "keyword.literal"]

But you can also use * here, to select al categories which have rules set,
so for example with rules set for "spacer", "keyword.literal" and "keyword.operand":
  `*` = ["spacer", "keyword.literal", "keyword.operand"]

You can also use exclusions here and the same star-auto-fill rule applies:
  `!spacer` => `*,!spacer` = ["keyword.literal", "keyword.operand"]

Another handy short cut is fill-in, in our previous example it would allow the use of:
  `keyword.*` => `keyword.literal,keyword.operand` = ["keyword.literal", "keyword.operand"]


You can also be more specific in what order and relation the passes should be ran in.
This by specifing "mode", "id" and "link" properties of the pass.
In coda this is done by the syntax:
`<id><mode><link>@<cmd>`
where id is a string (recommended to use short things like numbers) followed by an equal sign,
and link is prefixed by a colon.
The link should be the same as another pass's id.
Example coda:
`
1=org:1@pass regex 0
`
The modes avaliable are:
 - original/org    : Runs the pass on the original input
 - remainder/rem   : Runs the pass on whats left after the previous parse (the non-parsed pieces)
 - result/res      : Runs the pass on the output of the previous parse (the parsed pieces)

Theese ofcourse have a json equivilent: (Note that the mode has been made into it's "longer" form)
`
{
  "passes": [
    {
      "ind": [
        {"regex": [0]}
      ],
      "id": "1",
      "mode": "original",
      "link": "1"
    }
  ]
}
`

If no passes are sent coda will default to `{"*": ["*"]}`, or depending on fallback `{"*": <fallback>}`

## <br>Options
Options are passed to the interpriter and use the '@opt' command followed by the expression.
The expression will be space-split into a list.
Example:
`
@opt arg1 arg2
@opt arg3 arg4
`
Json:
`
{
  "options": [
      ["arg1", "arg2"],
      ["arg3", "arg4"]
  ]
}
`

## <br>Fallback
When parsing @pass commands and their indexes if an index is invalid or out-of-range it is set to a fallback, this is given as an argument to the codaToJson function.
But you can define a overwrite to this using the @fallback command, it's syntax is: `@fallback <fallback>` where <fallback> uses the same syntax as when deffining a pass index.

!NOTE! THE FALLBACK COMMAND CAN BE SET TO INVALID OR OUT-OF-RANGE VALUES WHICH BREAKS THE INTERPRITERS ABILITY TO SELECT PASS-CATEGORIES, SO USE WITH CAUTION ON YOUR OWN RISK!

Examples:
`
@fallback 0
@fallback "*"
@fallback 1,2
@fallback 1-10
`
Due to the way commands are parsed you may also write a list of indexes space seppareated:
`
@fallback 1 2 == @fallback 1,2
`

The fallbacks are set within the coda-parser so the interprited dosen't really have to care about it, thus it has no real meaning to be added into the output JSON,
however to be informative any set fallbacks (not the default ones) will be added as an option:
`
{
  "options": {
    [
      ["fallback",<fallback>]
    ]
  }
}
`

## <br>InterpriterData
# example + of not input
{
  "sections": {
    0: "example",
    1: "of",
    2: "input"
  },
  "context": {
    "operation": [
      {"add":[0,1]}
    ],
    "keywords": [
      {"not":[1,2]}
    ]
  }
}