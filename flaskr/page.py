import os
import re
import csv
import json
import urllib.request
import hashlib
import datetime as dt
from flaskr import model as mdl
from flaskr import train as ai
from flask import Flask
app = Flask(__name__)

dataPath = "../data"
db_placeholder = [
    {"name": "06-0169-0179253-04_Transactions_2019-02-16_2019-12-31.csv", "md5sum": "fake", "path": "data"}]

# Gross global variable.
input_files = []
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
            outlist.append(
                {"path": newpath, "filename": filename, "hd5sum": hd5sum})

    return outlist

# GET to be used in header.
@app.route('/bullshit')
def hello():
    return re.search(r'\n<li>(.*)</li>', urllib.request.urlopen('http://cbsg.sf.net').read().decode('UTF-8')).group(1)

# GET to be displayed as list
@app.route('/input-files')
def inputfiles():
    session = DbSession()

    # All files in input directory.
    input_files = ls("../data")

    # Tag if file with same hash/name exists in db.
    for input_file in input_files:

        filenameMatches = session.query(mdl.InputSource).filter(
            mdl.InputSource.filename == input_file["filename"]).all()
        hashMatches = session.query(mdl.InputSource).filter(
            mdl.InputSource.hd5sum == input_file["hd5sum"]).all()
        input_file["filenameindb"] = len(filenameMatches) > 0
        input_file["hashindb"] = len(hashMatches) > 0
    
    session.close()
    return {"list":input_file}
    # newFiles = foundInputFiles
    # return list(map(lambda x: {'label': x["name"], 'value': x["name"]}, newFiles))

# GET to be displayed as list
@app.route('/injested-files')
def injestedfiles():
    session = DbSession()
    return_list={"list":[injested_file.__dict__ for injested_file in session.query(mdl.InputSource).all()]}
    session.close()
    return return_list

# POST On select input file
# return suggestion table 
@app.route('/tag-table')
def tagTable(input_files):
    fullList = []
    
    if input_files:
        for input_file in input_files:
            with open(input_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row_num=0
                for line in csv_reader:
                    fullList.append(ai.proccessInput(line, row_num, input_file)) #list(line) + [input_file]
                    row_num+=1
    print(fullList)
    return fullList


# POST selected input files, and the modified content of the tagtable
# @app.route('/injest-file')
def injestfile(input_files, tag_table):
    # 'Input' is an array of id's from the input files list.
    # Do input validation here. e.g. get input from file that matches 
    input_files_by_name = find_input_files_by_name()

    if inputSource is None:
        return
    session = DbSession()

    # Save the injested docs to database.
    for source in inputSource:
        matched_file = input_files_by_name[source]
        filename = os.path.basename(source)
        ingestion_date = date.today()
        hd5sum = matched_file["hd5sum"]
        session.add(mdl.InputSource(path=source, filename=filename,
                                    hd5sum=hd5sum, ingest_date=ingestion_date))

    for row in tag_table:
        ai.learn(row)
        session.add(mdl.BankTransaction(
            raw_string="",
            input_source_id="input_source_id",
            to_account_id="id",
            from_account_id="id",
            amount="",
            pay_type="",
            details="",
            date="",
            tags="",
            ml_data=""))
    
    session.commit()
    session.close()

#     # Save all to the session
#     print(f"Committing {len(session.new)} object(s) into database.")



# Add
# DbSession = mdl.create_session_maker()
# session = DbSession()
# session.add(mdl.InputSource(path='source', filename='filename',
#             hd5sum='hd5sum', ingest_date=dt.datetime.now()))
# session.commit()
# session.close()

# # Get
# DbSession = mdl.create_session_maker()
# session = DbSession()
# session.query(mdl.InputSource).all()
# session.commit()
# session.close()

# # Drop
# DbSession = mdl.create_session_maker()
# session = DbSession()
# session.add(mdl.InputSource(path='source', filename='filename',
#             hd5sum='hd5sum', ingest_date=dt.datetime.now()))
# session.commit()
# session.close()