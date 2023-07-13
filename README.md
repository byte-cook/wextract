# wextract.py

A CLI program to read a html/xml stream from stdin, extracts text and prints it to stdout.

## Requirements
1. Install Python3 and pip as follows in Ubuntu/Debian Linux:
```
sudo apt install python3.6 python3-pip
```

2. Download ZIP of this repository and extract its content.

3. Install dependencies:
```
pip3 install lxml
```
or
```
pip3 install -r requirements.txt
```

## Usage examples

Show help:
```
wextract.py -h
```

Make a simple list from a html table without first header row:
```
cat file.html | wextract.py -l td -s "table tr" td text - ": " "td:nth-child(2)" text 
```

