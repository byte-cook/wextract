#!/usr/bin/env python

import os
import sys
import logging
import argparse
import textwrap
from bs4 import BeautifulSoup

# https://lxml.de/installation.html
# pip install lxml

HELP_APP = '''\
            Reads a html/xml stream from stdin, extracts text and prints it to stdout.
            
            To print a multiline output, use the option -s to select multiple elements. 
            For each element, a line is created based on the output definition.
            
            Use CSS selectors to select the relavant elements: .class, #id, element, element[attr]
            See for more information: https://www.w3schools.com/cssref/css_selectors.php
            
            Examples:
                cat file.html | wextract.py -s html "" text
                    Print all texts of a html file.
                
                cat file.html | wextract.py -s "table tr:not(:first-child)" td text - ": " "td:nth-child(2)" text 
                cat file.html | wextract.py -l td -s "table tr" td text - ": " "td:nth-child(2)" text 
                    Make a simple list from a html table without first header row.
                
                cat file.html | wextract.py -B "[" -A "]" -L "," -s "table tr" - "{ \"name\": \"" td text - "\" }" 
                    Create a JSON text from a html table.
            '''
HELP_OUTPUTDEF = '''\
            Defines the output format. 
            If the option -s is used, the CSS selector is applied for each element. 
            Otherwise, the complete stream is used resulting in a single-line output.
            
            Format: 
                SELECTOR USAGE [SELECTOR USAGE]*
                SELECTOR: <CSS-selector>|-
                    Selects a single element only, can be "-" for constant strings
                USAGE: text|<attribute name>|<string>
                    Prints the text of an element, the attribute of an element or a constant string
                
            Examples:
                "div a" text     Print the text of an anchor element inside a div element. 
                a href           Print the target url of an anchor element.
                - INFO           Print the string "INFO".
            '''

EMPTY_SELECTOR = '-'


def _create_output(rootTag, selector, usage, replace):
    tag = None
    if selector == EMPTY_SELECTOR:
        pass
    elif selector == '':
        tag = rootTag
    else:
        tag = rootTag.select_one(selector)
    
    match usage:
        case 'text':
            if tag:
                # return tag's text
                output = tag.text
                if replace:
                    output = output.replace(replace[0], replace[1])
                return output
            else:
                logging.debug('The CSS selector "{}" returns no result for: \n{}'.format(selector, rootTag))
                return None
        case _:
            if selector == EMPTY_SELECTOR:
                # return constant string
                return usage
            else:
                if not tag:
                    logging.debug('The CSS selector "{}" returns no result for: \n{}'.format(selector, rootTag))
                    return None
                # return tag's attribute
                output = tag.get(usage)
                if replace:
                    output = output.replace(replace[0], replace[1])
                return output

# curl https://free-proxy-list.net/
# cat proxies.html | ./wparse.py --debug -r ".table-striped tbody tr" "http://" const td text : const "td:nth-child(2)" text

if __name__ == '__main__':
    try: 
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent(HELP_APP))
        parser.add_argument("--debug", help="debugging output", action="store_true")
        parser.add_argument('--parser', choices=['html.parser', 'lxml', 'lxml-xml', 'xml', 'html5lib'], default='html.parser', help='the parser type: https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)')
        parser.add_argument("-B", "--before", help='text to be printed before the output')
        parser.add_argument("-A", "--after", help='text to be printed after the output')
        parser.add_argument("-L", "--line-sep", dest='lineSep', help='text to be printed after each output line except the last one')
        parser.add_argument("-r", "--replace", nargs=2, metavar=('original', 'new'), help='Replaces original by new of all extracted texts')
        parser.add_argument("-s", "--select", help='CSS selector for multiple elements to produce a multiline output')
        parser.add_argument("-l", "--skip-line", dest='skipLine', help='skip line if CSS selector returns empty result')
        parser.add_argument('outputdefinition', nargs='+', help=textwrap.dedent(HELP_OUTPUTDEF))
        args = parser.parse_args()
        
        # init logging
        level = logging.DEBUG if args.debug else logging.WARNING
        logging.basicConfig(format='%(levelname)s: %(message)s', level=level, force=True)
        
        # chech number of arguments
        if len(args.outputdefinition) % 2 != 0:
            print('Error: Illegel number of arguments: {}. Use an even number of arguments.'.format(len(args.outputdefinition)))
            exit()
        
        # read from stdin
        soup = BeautifulSoup(sys.stdin.read(), args.parser)
        
        # select root tags
        selection = soup
        if args.select:
            selection = soup.select(args.select)
        logging.debug('Selected tag(s):\n' + str(selection) + '\n')
        
        if args.before:
            print(args.before)
        
        tokens = args.outputdefinition
        for tag in selection:
            logging.debug('Tag: \n' + str(tag))
            
            if args.skipLine:
                result = tag.select_one(args.skipLine)
                if result is None:
                    continue
            
            outputLine = ''
            selector = None
            for token in tokens:
                if selector is None:
                    selector = token
                else:
                    output = _create_output(tag, selector, token, args.replace)
                    if output is not None:
                        outputLine += output
                    selector = None
            
            if args.lineSep and tag != selection[-1]:
                # do not print lineSep for the last line
                outputLine += args.lineSep
                
            if outputLine != '':
                print(outputLine)
        
        if args.after:
            print(args.after)
            
    except Exception as e:
        print(e)
