# Wextract.py

A CLI program to read a html/xml stream from stdin, extracts text and prints it to stdout.

## Install

1. Install Python3 and pip as follows in Ubuntu/Debian Linux:
```
sudo apt install python3 python3-pip
```

2. Install dependencies:
```
pip3 install lxml bs4
```

3. Download Wextract.py and set execute permissions:
```
curl -LJO https://raw.githubusercontent.com/byte-cook/wextract/main/wextract.py
chmod +x wextract.py
```

3. (Optional) Use [opt.py](https://github.com/byte-cook/opt) to install it to the /opt directory:
```
sudo opt.py install wextract wextract.py
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

    
