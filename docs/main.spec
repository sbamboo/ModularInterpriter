=======[CodaSyntax]=======
  Coda is generally split into this context:
  <options><type>:<section><name> <chars_and_expressions>
  Note! The name is optional. But if a name is there it starts with >
  Each options is followed by a space so:
  "ml " not "ml"
  expressions within qoutes are not allowed since the qoutes are recognised as symbols.
  The only non-symbol recognised characters are wildcards the can be recognised by prefixing with \
  Wildcards:
    §  = space
    \§ = §
    \  = 
    \\ = \
  Please note that nothing can be interprited by having nothing after section. This wont get recognised.

=======[EncasedSections]=======
  Encased sections are encloser-syntaxes like parentheses and qoutes, they have two types: Bidirectional and Interchangable.
  Bidirectional encasers have a start expression and an end expression that may not be the same.
  The interpriter can then section out anything inbetween theese symbols.
  > Section: encase
  > Type:    struct
  Examples:
    () {} []
  Json:
  `
    {
      "encase": {
        "struct": [
          {
            "ex": ["(",")"]
          }
        ]
      }
    }
  `
  Coda:
  `
    struct:encase ( )
  `

  Interchangable encasers have one expression which the interpriter sections out content inbetween two instances of.
  > Section: encase
  > Type:    interc
  Examples:
    "" '' ////
  Json:
  `
    {
      "encase": {
        "interc": [
          {
            "ex": '"'
          }
        ]
      }
    }
  `
  Coda:
  `
    interc:encase "
  `

  For an encaser to be recognised beyond line endings they should be prefixed with 'ml ' in Coda or by setting "ml" to True in json.
  `
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
  `
  Coda:
  `
    ml interc:encase "
  `

=======[Keywords.Operands]=======
  Operands are keywords that are excluded from interpriter sections but layed as operations inbetween sections.
  They can be used for tex math, where the interpriter could take <expr> + <expr> as {"operation":"add","elem":["<expr>","<expr>"]}
  > Section: keyword
  > Type:    operand
  Examples:
    +

  They can be listed under an operation like "add":
  Json:
  `
    {
      "keyword": {
        "operand": {
          "add": ["+"]
        }
      }
    }
  `
  Coda:
  `
    operand:keyword>add +
  `

  Or under no operation which in json would lead to "ambi" or ambiguous:
  Json:
  `
    {
      "keyword": {
        "operand": {
          "ambi": ["+"]
        }
      }
    }
  `
  Coda:
  `
    operand:keyword +
  `

=======[Keywords.Literals]=======
  Literals are specific keywords that can be excluded from sectioning and added for context just like operands.
  > Sections: keyword
  > Type:     literal
  Examples:
    not
  Json:
  `
    {
      "keyword": {
        "literal": [
          "not"
        ]
      }
    }
  `
  Coda:
  `
    literal:keyword not
  `

=======[Spacers]=======
  Spacers are expressions used to split sections.
  Examples:
    ' '
  Json:
  `
    {
      "spacer": [
        " "
      ]
    }
  `
  Coda:
  `
    :spacer §
  `

=======[REGEX]=======
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

=======[InterpriterData]=======
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


=======[Rulesets]=======
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