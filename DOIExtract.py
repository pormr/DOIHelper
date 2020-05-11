import PyPDF3, sys, requests

try:
    PDFsource = sys.argv[1]
except:
    print('Incorrect/invalid argument(s) supplied.')
    sys.exit(1)

PDFFile = open(PDFsource,'rb')

PDF = PyPDF3.PdfFileReader(PDFFile)
pages = PDF.getNumPages()
key = '/Annots'
uri = '/URI'
anc = '/A'
bib = []
headers = {
    "Accept": "text/x-bibliography"
}

for page in range(pages):

    pageSliced = PDF.getPage(page)
    pageObject = pageSliced.getObject()

    if key in pageObject:
        ann = pageObject[key]
        for a in ann:
            u = a.getObject()
            if uri in u[anc] and "doi" in u[anc][uri]:
                bib.append(u[anc][uri])


for bib_url in bib:
    print(bib_url)
    print(requests.post(bib_url, headers=headers).text)
