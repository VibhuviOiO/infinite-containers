# Delete Index

## Verification

Are you on the production Database ? 

- Make sure you are not DRUNK, be conscious.
- Cross verify the data is not production or client's user data
- If you are on a production database, check with the backup plan
- Once you delete the index you can only recover from backups or nowhere


## Delete the index

```bash
curl -X DELETE "localhost:9200/<INDEX_NAME>?pretty"

# Example
curl -X DELETE "localhost:9200/test?pretty"
```