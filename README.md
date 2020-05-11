# DOIHelper

Extracts DOI Links and bibilography from PDF files (**PyPDF3** and **requests** are required).

Usage:`python DOIExtract.py [-h] [-o OUTPUT] [-d] "<PDF file>"`

    -h, --help           show this help message and exit

    -o, --output         save the results to file (rather than print to the console)

    -d, --offline        disable bibliography(offline mode)


This utility is inspired by https://stackoverflow.com/questions/27744210/extract-hyperlinks-from-pdf-in-python
