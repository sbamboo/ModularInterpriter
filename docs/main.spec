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

  Or under no operation which is json would lead to "ambi" or ambiguous:
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