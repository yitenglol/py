import sqlite3
import csv
import argparse
from argparse import RawTextHelpFormatter
import os
import configparser
from collections import OrderedDict
import string
from simplekml import Kml, Style
import re
import shutil
import subprocess
import stat
import json

def gathermacos(database_names):
tempdir()
ignore_dir.append(os.getcwd())
print("...Searching for and copying databases into tmp_apollo...")
for root, dirs, filenames in os.walk(data_dir,followlinks=False):
if not any(ignored in root for ignored in ignore_dir):
for f in filenames:
for db in database_names:
if db == "db":
if re.search(rf'^{db}(-shm|-wal|$)',f):
if not os.path.exists(os.getcwd() + "/tmp_apollo" + root):
os.makedirs(os.getcwd() + "/tmp_apollo" + root)
shutil.copyfile(os.path.join(root,f),os.getcwd() + "/tmp_apollo" + root +"/"+f)
elif re.search(rf'^{db}(-shm|-wal|$)',f):
if not os.path.exists(os.getcwd() + "/tmp_apollo" + root):
os.makedirs(os.getcwd() + "/tmp_apollo" + root)
shutil.copyfile(os.path.join(root,f),os.getcwd() + "/tmp_apollo" + root +"/"+f)
chown_chmod()

def tempdir():
tmpdir = os.getcwd() + "/tmp_apollo"
print("...Creating /tmp_apollo in: " + tmpdir)
if not os.path.exists(tmpdir):
os.makedirs(tmpdir)
os.chown(tmpdir,os.stat(os.getcwd()).st_uid,os.stat(os.getcwd()).st_gid)

def chown_chmod():
print("...chmod/chown all the things...")
for root, dirs, filenames in os.walk(os.getcwd() + "/tmp_apollo"):
for d in dirs:
if os.access(os.path.join(root, d), os.R_OK) == False:
os.chmod(os.path.join(root, d), stat.S_IRWXU)
os.chown(os.path.join(root, d),os.stat(os.getcwd()).st_uid,os.stat(os.getcwd()).st_gid)
for f in filenames:
if os.access(os.path.join(root, f), os.R_OK) == False or os.access(os.path.join(root, f), os.W_OK) == False:
os.chmod(os.path.join(root, f), stat.S_IRWXU)
os.chown(os.path.join(root, f),os.stat(os.getcwd()).st_uid,os.stat(os.getcwd()).st_gid)

def parse_module_definition(mod_info):

print("...Parsing Modules in..." + mod_dir)
database_names = set()
for root, dirs, filenames in os.walk(mod_dir):
for f in filenames: 
if f.endswith(".txt"):
mod_def = os.path.join(root,f) 
fread = open(mod_def,'r')
contents = fread.read()

parser = configparser.ConfigParser()
parser.read(mod_def)

mod_name = mod_def
query_name = parser['Query Metadata']['QUERY_NAME']
activity = parser['Query Metadata']['ACTIVITY']
key_timestamp = parser['Query Metadata']['KEY_TIMESTAMP']
databases = parser['Database Metadata']['DATABASE']
database_name = databases.split(',')

for database in database_name:
database_names.add(database)

for db in database_name:

if subparser == 'extract':
if version == 'yolo':
for section in parser.sections():
if "SQL Query" in section:
sql_query = parser.items(section,'QUERY')
for item in sql_query[0]:
if "SELECT" in item:
query = item
uniquekey = mod_def + "#" + db + "#" + section
mod_info[uniquekey] = [query_name, db, activity, key_timestamp, query]
else:			
for section in parser.sections():
if version in re.split('[ ,]', section):
sql_query = parser.items(section,'QUERY')
for item in sql_query[0]:
query = item
uniquekey = mod_def + "#" + db + "#" + section
mod_info[uniquekey] = [query_name, db, activity, key_timestamp, query]

if subparser =='gather_macos':
gathermacos(database_names)


if __name__ == "__main__":

parser = argparse.ArgumentParser(description="\
Apple Pattern of Life Lazy Outputter (APOLLO)\
\n\nVery lazy parser to extract pattern-of-life data from SQLite databases on iOS/macOS/Android/Windows datasets (though really any SQLite database if you make a configuration file and provide it the proper metadata details.\
\n\nOutputs include SQLite Database (with JSON or '|' Delimited) or Tab Delimited CSV.\
\n\nYolo! Meant to run on anything and everything, like a honey badger - it don't care. Can be used with multiple dumps of devices. It will run all queries in all modules with no regard for versioning. May lead to redundant data since it can run more than one similar query. Be careful with this option.\
\n\tAuthor: Sarah Edwards | @iamevltwin | mac4n6.com"
, prog='apollo.py'
, formatter_class=RawTextHelpFormatter)

subparsers = parser.add_subparsers(help='help for subcommand', dest='subparser')

gather_macos = subparsers.add_parser('gather_macos', help='Gather Files from MacOS System')

parser.add_argument('modules_directory' help="Path to Modules Directory")
parser.add_argument('data_path' help="Path to Data Directory. It can be full file system dump or directory of extracted databases, it is recursive. For gathering files this is the top level directory to search for files.")
parser.add_argument('--ignore', action='append', help='Ignore Path using Gather. Can be used more than once for different paths.')

args = parser.parse_args()

try: 
subparser = args.subparser
print("Action: " + subparser)
except:
pass
try: 
platform = args.p
print("Platform: " + platform)
except:
pass
try:
version = args.v 
print("Version: " + version)
except:
pass
try:
output = args.o 
print("Output: " + output)
except:
pass
try:
data_dir = args.data_path
print("Data Directory: " + data_dir)
except:
pass
try:
ignore_dir = args.ignore
for ignore in ignore_dir:
print("  Ignoring Directory: " + ignore)
except:
pass
try:
mod_dir = args.modules_directory
print("Modules Directory: " + mod_dir)
except:
pass
try:
port = args.port
ip = args.ip
print('Jailbroken Device IP/Domain: ' + ip)
print('Jailbroken Device Port: ' + port)
except:
pass
try:
if args.k:
print("KMZ: TRUE")
except:
pass
print("Current Working Directory: " + os.getcwd())
print("--------------------------------------------------------------------------------------")

if ignore_dir == None:
ignore_dir = []

mod_info = {}

try:
if output == 'csv':

with open('apollo.csv', 'w', newline='') as csvfile:
loccsv = csv.writer(csvfile, dialect='excel',delimiter='\t', quotechar='"')
loccsv.writerow(['Timestamp','Activity', 'Output','Database','Module'])

parse_module_definition(mod_info)

print("\n===> Total number of records: " + str(records))

if args.k:
print("===> Total Number of Location Records: " + str(total_loc_records))

print("\n===> Lazily outputted to CSV file: apollo.csv\n")

elif output == 'sql' or output == 'sql_json':

if os.path.isfile("apollo.db"):
os.remove("apollo.db")
connw = sqlite3.connect('apollo.db')
cw = connw.cursor()
cw.execute("CREATE TABLE APOLLO(Key timestamp, Activity TEXT, Output TEXT, Database TEXT, Module TEXT)")

parse_module_definition(mod_info)

print("\n===> Total Number of Records: " + str(records))

connw.commit()

if args.k:
print("===> Total Number of Location Records: " + str(total_loc_records))

print("\n===> Lazily outputted to SQLite file: apollo.db\n")

except:
pass

if subparser in ['gather_macos','gather_ios']:
parse_module_definition(mod_info)
