# iteso-o2022-bda-mongodb

A place to share mongodb app code

### Setup a python virtual env with python cassandra installed
```
# If pip is not present in you system
sudo apt update
sudo apt install python3-pip

# Install and activate virtual env
python3 -m pip install virtualenv
virtualenv -p python3 ./venv
source ./venv/bin/activate

# Install project python requirements
python3 -m pip install -r requirements.txt
```

### To run the API service
```
python3 -m uvicorn main:app --reload
```

### To load data
Ensure you have a running mongodb instance
i.e.:
```
docker run --name mongodb -d -p 27017:27017 mongo
```
Once your API service is running (see step above), run the populate script
```
cd data/
python3 populate.py
```