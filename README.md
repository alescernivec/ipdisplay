# IPDisplay

Displays countries/cities from my current connections.

## Dependencies

Packages:
 * Python-dev

If you do not have Python-dev package:
```
$ sudo apt-get install python-dev
```

Python dependencies (virtual environment):

```
argparse==1.2.1
ipaddress==1.0.16
psutil==3.3.0
wsgiref==0.1.2
```

You can create virtualenv in order to run the program:

```
virtualenv --no-site-packages virtualenv/
```

and install dependencies 

```
$ . virtualenv/bin/activate
$ pip install -r dependecies.txt
```

Depends on **GeoLite2** database. See bellow.

## Usage

From command line:

```
python ipdisplay.py
```

This will take you some moments since lookup is done using the local database.

Output:

```
Proto Local address                  Remote address                 Status        PID    Program name         Location 1           Location 2          
tcp   127.0.0.1:17603                -                              LISTEN        2988   dropbox              local                local               
tcp   172.16.93.140:58723            52.21.87.43:443                ESTABLISHED   29165  firefox              "United States"      "North America"     
tcp   127.0.0.1:44680                127.0.0.1:2222                 ESTABLISHED   9135   ssh                  local                local               
tcp   127.0.0.1:44088                127.0.0.1:43662                ESTABLISHED   29281  GoogleTalkPlugi      local                local               
tcp6  :::22                          -                              LISTEN        -      ?                    local                local               
udp   0.0.0.0:1196                   -                              NONE          -      ?                    local                local               
tcp   172.16.93.140:45608            74.125.136.189:443             ESTABLISHED   29165  firefox              "United States"      "North America"     
tcp   172.16.93.140:53025            91.217.255.47:443              ESTABLISHED   31424  storagesync          Slovenia             Europe              
tcp   172.16.93.140:36656            148.251.181.44:7615            ESTABLISHED   7720   islpronto            Germany              Europe              
tcp   172.16.93.140:45030            91.217.255.47:443              ESTABLISHED   31433  storagesync          Slovenia             Europe              
...
```

If you do not see all the processes (program names), you can run the command as root.

## Directory structure

Basic directory structure:

```
$ tree -L 2
.
├── database
│   ├── city-locations-en.csv -> GeoLite2-City-CSV_20151201/GeoLite2-City-Locations-en.csv
│   ├── country-blocks-en.csv -> GeoLite2-Country-CSV_20151201/GeoLite2-Country-Blocks-IPv4.csv
│   ├── country-locations-en.csv -> GeoLite2-Country-CSV_20151201/GeoLite2-Country-Locations-en.csv
│   ├── GeoLite2-City-CSV_20151201
│   ├── GeoLite2-City-CSV_20151201.zip
│   ├── GeoLite2-Country-CSV_20151201
│   └── GeoLite2-Country-CSV_20151201.zip
├── README.md
├── src
│   └── ipdisplay.py
└── virtualenv
    ├── bin
    ├── include
    ├── lib
    └── local

```

Under ```database``` directory you need to have links to CSV file of **GeoLite2** database.

```
city-locations-en.csv -> GeoLite2-City-CSV_20151201/GeoLite2-City-Locations-en.csv
country-blocks-en.csv -> GeoLite2-Country-CSV_20151201/GeoLite2-Country-Blocks-IPv4.csv
country-locations-en.csv -> GeoLite2-Country-CSV_20151201/GeoLite2-Country-Locations-en.csv
```

### GeoLite2 Database

You can grab the latest GeoLite2 database from here: 

[ http://dev.maxmind.com/geoip/geoip2/geolite2/ ]:

```
$ cd database
$ wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip
$ wget http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip
$ unzip GeoLite2-City-CSV.zip
$ unzip GeoLite2-Country-CSV.zip
$ cp -s GeoLite2-City-CSV_20151201/GeoLite2-City-Locations-en.csv city-locations-en.csv
$ cp -s GeoLite2-Country-CSV_20151201/GeoLite2-Country-Blocks-IPv4.csv country-blocks-en.csv
$ cp -s GeoLite2-Country-CSV_20151201/GeoLite2-Country-Locations-en.csv country-locations-en.csv
```

Note, comercially you can use **GeoLite2** database for one year for free

Example:

```
lrwxrwxrwx 1 ales ales       57 dec 29 15:14 city-locations-en.csv -> GeoLite2-City-CSV_20151201/GeoLite2-City-Locations-en.csv
lrwxrwxrwx 1 ales ales       62 dec 29 15:15 country-blocks-en.csv -> GeoLite2-Country-CSV_20151201/GeoLite2-Country-Blocks-IPv4.csv
lrwxrwxrwx 1 ales ales       63 dec 29 15:15 country-locations-en.csv -> GeoLite2-Country-CSV_20151201/GeoLite2-Country-Locations-en.csv
drwxrwxr-x 2 ales ales     4096 dec 29 14:28 GeoLite2-City-CSV_20151201/
-rw-rw-r-- 1 ales ales 34001741 dec 29 12:42 GeoLite2-City-CSV_20151201.zip
drwxrwxr-x 2 ales ales     4096 dec 29 12:45 GeoLite2-Country-CSV_20151201/
-rw-rw-r-- 1 ales ales   996915 dec 29 12:42 GeoLite2-Country-CSV_20151201.zip
```

### VirtualEnv

Note, you can use ```virtualenv``` to run the code.