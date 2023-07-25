# Wextract.py

A CLI program to read a html/xml stream from stdin, extracts text and prints it to stdout.

## Requirements
1. Install Python3 and pip as follows in Ubuntu/Debian Linux:
```
sudo apt install python3.6 python3-pip
```

2. Install dependencies:
```
pip3 install lxml
```
or
```
pip3 install -r requirements.txt
```

3. Download Wextract.py and set execute permissions:
```
curl -LJO https://github.com/byte-cook/wextract/raw/main/wextract.py
chmod +x wextract.py
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
Explanation:  
```-l td``` : skip line if text is empty  
```-s "table tr"``` : select tr tag of table as root element (all sub elements are run through)  
```td text``` : print text of td tag  
```- ": "``` : print ": " as separator  
```"td:nth-child(2)" text``` : print text of the second td tag  

    
