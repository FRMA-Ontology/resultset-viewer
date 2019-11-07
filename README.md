# Result-Set Viewer
## Introduction
Machine learning allows computers to learn a model for a given task, such as face recognition, with a high degree of accuracy, using data. However, after these models are generated, they are often treated as black boxes by developers and the limitations of a model are often unknown to end-users. To address these issues this paper introduces the Face Recognition Model Analyzer (FRMA) ontology and a semantically enabled Result-Set Viewer. Together these resources describe image features relevant to face recognition and allow users to explore how well a face recognition model does at classifying images that contain an image feature.

## Installing for Linux
### Requirements
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


### Download Code and Data

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


### Configure Enviornment

   `cd project_folder/`
   
   `pip2 install -r requirements.txt`


### Start blazegraph:

   `cd project_folder/lib/blazegraph`
   
   `java -server -Xmx4g -Dbigdata.propertyFile=RWStore.properties -jar blazegraph.jar`


### Start GUI

   `cd project_folder/`
   
   `python main.py`
   
   
## Usage
### Ontology Load
On first startup the triplestore needs to be intialized by running clicking:

   `File -> Clear Datasets -> Yes`
   
This will load the ontologies and lfw labels into blazegraph and clear the previous datasets.

### Loading Dataset
After that datasets can be loaded in by clicking:

   `File -> New Dataset`

Fill out this dialog box with the ResultSetName, Algorithm, and a ResultSetFile path then click done. Two ResultSet files are included with the viewer `project_folder/data/dlib_result.txt` and `project_folder/data/facenet_result.txt`. ResultSet files are tab separated files where each row is one model comparison and is of the following form:

```
PersonNameImage1  ImageNumber1   PersonNameImage2  ImageNumber2   ClassifiedCorrectly
```

This dialog box will generate an RDF representation of the results and load it into blazegraph.

### Select Dataset
After loading a dataset it can be selected in the viewer by clicking:

   `File -> Select ResultSet -> Choose ResultSet from drop down -> select done`
   
This will load the ResultSet into the viewer so a user can begin to explore the model. This process can take some time to load in for large dataset, but once loaded performance will improve.

