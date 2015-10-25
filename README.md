# healthhack2015_genome_browser

##About
FileUM (the application) is a front end interface for automating the upload of genome file types for visualisation in a [Genome Browser](http://gb.pearg.com).  Generally the features  of a genome browser are:
- a web browser that visualises genome data
- a central database that references a database per genome 
- each genome also references file blobs on the filesystem to further express data 

This will be of benefit to genetics researchers (without any bioinfomatics skill set) to contribute data and knowledge to a common database. Thereby, increasing accessibility to the wider scientific community and further research efforts in these domains. 
This project was created as part of [Healthhack 2015 Melbourne] (http://healthhack.com.au)

## Techstack
Created as an open source tool with a high level of extensibility, FileUM uses the following: 

##Dependencies
* nodejs
* bower

## Setup Instructions
```shell
bower update
python -m SimpleHTTPServer &
```
