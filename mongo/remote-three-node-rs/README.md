#

When dealing with the three servers for production level configuration 

- Create the keyfile on one server and copy the same file into number of servers required 
- Chnage the permision within the server according to the server configuration it works else it fails with 
            1. file permision is too open 
            2. bad file 
- Here is the steps 

Step 1: 
    
    ssh into node 1
    create the file 
            Choose the path for storing the file

            `openssl rand -base64 756 > mongoKeyFileLinux`

            `chmod 600 mongoKeyFileLinux`

            `sudo chown 999 mongoKeyFileLinux`

            `sudo chgrp 999 mongoKeyFileLinux`
    
Step 2 
    ssh into node 2
    Copy the file and chnage permissions
            Choose the path for storing the file

            `scp -r user@node-one-ip/path/mongoKeyFileLinux <path/copy>`

            `sudo chown 999 mongoKeyFileLinux`

            `sudo chgrp 999 mongoKeyFileLinux`

Step 3
    ssh into node 3
    Copy the file and chnage permissions
            Choose the path for storing the file

            `scp -r user@node-one-ip/path/mongoKeyFileLinux <path/copy>`

            `sudo chown 999 mongoKeyFileLinux`

            `sudo chgrp 999 mongoKeyFileLinux`
