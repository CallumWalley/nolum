import os
import re
import csv
import json
import urllib.request
import hashlib
from flaskr import model as mdl
from flask import Flask
app = Flask(__name__)

dataPath = "../data"
db_placeholder = [
    {"name": "06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv", "md5sum": "fake", "path": "data"}]

DbSession = mdl.create_session_maker()

def ls(dataPath):
    outlist = []
    for filename in os.listdir(dataPath):
        newpath = os.path.join(dataPath, filename)
        if os.path.isdir(newpath):
            for f in ls(newpath):
                outlist.append(f)
        elif newpath[-4:].lower() == ".csv":
            hd5sum = hashlib.md5(
                open(newpath).read().encode('utf-8')).hexdigest()
            # if file in map(lambda x: x["name"], db_placeholder)
            # If in database, but hex different, add to csv_files_digested_changed.
            # If in database, don't add.
            outlist.append({"path": newpath, "filename": filename, "hd5sum": hd5sum})
    return outlist

@app.route('/bullshit')
def hello():
    return {"bullshit": re.search(r'\n<li>(.*)</li>', urllib.request.urlopen('http://cbsg.sf.net').read().decode('UTF-8')).group(1)}

@app.route('/input-files')
def inputfiles():
    session = DbSession()
    
    # All files in input directory.
    inputFiles = ls("../data")

    # Tag if file with same hash/name exists in db.
    for inputFile in inputFiles:

        filenameMatches = session.query(mdl.InputSource).filter(mdl.InputSource.filename == inputFile["filename"]).all()
        hashMatches = session.query(mdl.InputSource).filter(mdl.InputSource.hd5sum == inputFile["hd5sum"]).all()
        inputFile["filenameindb"] = len(filenameMatches) > 0
        inputFile["hashindb"] = len(hashMatches) > 0           

    return {"input-files":inputFiles}
    # newFiles = foundInputFiles
    # return list(map(lambda x: {'label': x["name"], 'value': x["name"]}, newFiles))

# @app.route('/injested-files')
# def inputfiles():
#     newFiles = filter(lambda x: x['name'] not in map(
#         lambda y: y["name"], db_placeholder), foundInputFiles)

#     return list(map(lambda x: {'label': x["name"], 'value': x["name"]}, newFiles))
# @app.route('/')


def updateInjestedList():
    session = DbSession()
    for entry in session.query(mdl.InputSource).all():
        print("entry")
    # session.close()


def injestDoc(input):
    # 'Input' is an array of id's from the input files list.
    input_files_by_name = find_input_files_by_name()
    # print("My input source is " + str(inputSource))
    # print(list(filter(lambda x: x["name"]==inputSource, foundInputFiles)))
    if inputSource is None:
        return
    session = DbSession()
    for source in inputSource:
        matched_file = input_files_by_name[source]
        filename = os.path.basename(source)
        ingestion_date = date.today()
        hd5sum = matched_file["hd5sum"]
        if len(session.query(mdl.InputSource).filter(mdl.InputSource.path == source).all()) > 0:
            # Skip ingest if already imported
            print(f"Skipping import for {filename} as already in database.")
            continue
        session.add(mdl.InputSource(path=source, filename=filename,
                                    hd5sum=hd5sum, ingest_date=ingestion_date))
    # Save all to the session
    print(f"Committing {len(session.new)} object(s) into database.")
    session.commit()
    session.close()


def updateTagTable(input_files):
    fullList = []

    if input_files:
        for input_file in input_files:
            # try:
            with open(input_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for line in csv_reader:
                    fullList.append(list(line) + [input_file])
    # columns = [
    #     #{"name": "ID", "id": "id"},
    #     {"title": "Import", "field": "include", "sorter": "boolean",
    #         "editor": True, "formatter": "tickCross", "tooltip": "Tooltip!"},
    #     {"title": "Date", "field": "date", "sorter": "date", "sorterParams": {
    #         "format": "YYYY-MM-DD"}, "tooltip": "Tooltip!"},
    #     {"title": "From", "field": "from", 
    #         "sorter": "alphanum", "editor": "autocomplete", "tooltip": "Tooltip!", "editorParams":{
    #             "freetext":True, "showListOnEmpty":True, "values":["person1", "person2", "person3"], "searchFunc":ns_tab("fromFreetext"),
    #         }},
    #     {"title": "To", "field": "to", "editor": True, "tooltip": "Tooltip!"},
    #     {"title": "Amount", "field": "amount", "sorter": "number",
    #         "formatter": "money", "editor": True, "tooltip": "Tooltip!"},
    #     {"title": "Type", "field": "pay_type", "tooltip": "Tooltip!",
    #         "editor": "select", "editorParams": {"values": transaction_types}},
    #     {"title": "Tags", "field": "tags", "tooltip": "Tooltip!"},
    #     {"title": "Details", "field": "details", "tooltip": "Tooltip!"},
    #     {"name": "Source", "id": "source"},
    #     {"name": "Raw String", "id": "raw_string"},
    #     {"title": "Confidence", "field": "confidence"}
    # ]
    
    data = list(map(lambda x: {
        "include": True,
        "date": x[6],
        "amount": x[5],
        "pay_type": x[0],
        "tags": "",
        "details": str([x[1] + x[2] + x[3] + x[4]]),
        "confidence": 0,
        # "source":input_file,
        # "raw_string": str(x)
    }, fullList))
    return data