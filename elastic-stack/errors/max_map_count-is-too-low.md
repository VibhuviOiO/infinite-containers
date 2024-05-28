## Issues

- max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

## Sol:
add the varibale to /etc/sysctl.conf

vm.max_map_count=262144

OR

sysctl -w vm.max_map_count=262144