Issue:


```json
{
  "error" : {
    "root_cause" : [
      {
        "type" : "mapper_parsing_exception",
        "reason" : "analyzer [autocomplete_analyzer] not found for field [autocomplete]"
      }
    ],
    "type" : "mapper_parsing_exception",
    "reason" : "Failed to parse mapping [workspace]: analyzer [autocomplete_analyzer] not found for field [autocomplete]",
    "caused_by" : {
      "type" : "mapper_parsing_exception",
      "reason" : "analyzer [autocomplete_analyzer] not found for field [autocomplete]"
    }
  },
  "status" : 400
}
```

Solution: Update setting with analysis

```json
"settings" : {
      "index" : {
        "analysis" : {
          "filter" : {
            "autocomplete_filter" : {
              "type" : "edge_ngram",
              "min_gram" : "1",
              "max_gram" : "20"
            }
          },
          "analyzer" : {
            "case_insensitive_analyzer" : {
              "filter" : [
                "lowercase"
              ],
              "tokenizer" : "keyword"
            },
            "autocomplete_analyzer" : {
              "filter" : [
                "lowercase",
                "autocomplete_filter"
              ],
              "tokenizer" : "standard"
            }
          }
        },
      }
    }
```