reached the limit of incoming shard recoveries [2], cluster setting [cluster.routing.allocation.node_concurrent_incoming_recoveries=2] (can also be set via [cluster.routing.allocation.node_concurrent_recoveries])

"there are too many copies of the shard allocated to nodes with attribute [aws_availability_zone], there are [2] total configured shard copies for this shard id and [3] total attribute values, expected the allocated shard count per attribute [2] to be less than or equal to the upper bound of the required number of shards per attribute [1]


 "the shard cannot be allocated to the same node on which a copy of the shard already exists [[notification][4], node[<NODEONE_ID>], [P], s[STARTED], a[id=<ID>]]"

  "there are too many copies of the shard allocated to nodes with attribute [aws_availability_zone], there are [2] total configured shard copies for this shard id and [3] total attribute values, expected the allocated shard count per attribute [2] to be less than or equal to the upper bound of the required number of shards per attribute [1]"

  