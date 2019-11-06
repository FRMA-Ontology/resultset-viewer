# Installing for Linux

## Requirements
1. java

   `sudo apt update`
   
   `sudo apt install openjdk-8-jdk`

2. python 2

   `sudo apt install python2.7`

3. pip2

   `sudo apt install python-pip`

4. python Tkinter

   `sudo apt install python-tk`

5. git

   `sudo apt install git`

6. curl

   `sudo apt install curl`

7. wget

   `sudo apt install wget`


## Download Code and Data

1. Download Result-Viewer

   `git clone https://github.com/FRMA-Ontology/resultset-viewer.git project_folder`

2. Download Blazegraph

   `curl -L http://sourceforge.net/projects/bigdata/files/bigdata/2.1.4/blazegraph.jar/ > project_folder/lib/blazegraph/blazegraph.jar`

3. Download LFW Images

   `curl -L http://vis-www.cs.umass.edu/lfw/lfw-deepfunneled.tgz > project_folder/lib/lfw-deepfunneled.tgz`
   
   `tar zxvf project_folder/lib/lfw-deepfunneled.tgz --one-top-level=lfw --strip-components 1 -C project_folder/lib`

4. Download LFW Features

   `wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1QLpFBM6N4CNZnyeDsDAjOmK2fpcEKCqN' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1QLpFBM6N4CNZnyeDsDAjOmK2fpcEKCqN" -O lfw_tags.rdf && rm -rf /tmp/cookies.txt`

   `mv lfw_tags.rdf project_folder/lib/ontologies/lfw_tags.rdf`


## Configure Enviornment

   `cd project_folder/`
   
   `pip2 install -r requirements.txt`


## Start blazegraph:

   `cd project_folder/lib/blazegraph`
   
   `java -server -Xmx4g -Dbigdata.propertyFile=RWStore.properties -jar blazegraph.jar`


## Start GUI

   `cd project_folder/`
   
   `python main.py`
