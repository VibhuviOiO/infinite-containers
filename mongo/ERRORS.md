
# 1. Keyfile issue 

```json
"msg":"Read security file failed","attr":{"error":{"code":30,"codeName":"InvalidPath","errmsg":"Error reading file /opt/keyfile/keyfile: No such file or directory"}}
```

Check with right path name or the file name and update the configuration accordingly.

# 2. Permissions on key file are too open

```json
{"msg":"Read security file failed","attr":{"error":{"code":30,"codeName":"InvalidPath","errmsg":"permissions on /opt/keyfile/mongoKeyFileMac are too open"}}}
```

Recreate the file with mac / linux based permissions. refined in Readme file


# 3. NotYetInitialized 

```json
{
    "ctx":"LogicalSessionCacheRefresh",
    "msg":"Failed to refresh session cache, will try again at the next refresh interval",
    "attr": {
        "error":"NotYetInitialized: Replication has not yet been configured",
        // OR
        "error2": "Cannot use non-local read concern until replica set is finished initializing"
    }
}
```

Initialise the cluster according to README

# 4. MongoServerError: command replSetInitiate requires authentication

Authentication is required while connecting to the `mongosh`

# 5  db.Tab completion error: MongoServerError: node is not in primary or recovering state


