Requirements-
java
python 2, 3 might work?

Setup-
Download LFW images:
http://vis-www.cs.umass.edu/lfw/lfw-deepfunneled.tgz
unzip
put folder in project_folder/lib/

Download blazegraph:
https://www.blazegraph.com/download/
put jar in project_folder/lib/blazegraph

Install virtualenv:
cd project_folder
pip install -r requirements.txt


Run(this will get better)-
Start blazegraph:
cd project_folder/lib/blazegraph
java -server -Xmx4g -Dbigdata.propertyFile=RWStore.properties -jar blazegraph.jar

Run gui:
source env/bin/activate
cd project_folder
python main.py
