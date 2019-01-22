from html.parser import HTMLParser
from urllib import parse
from urllib.request import urlopen

d = {}

class DataExtract(HTMLParser):
    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.links = set()
        self.is_span = ""
        self.qid = ""
        self.qa_True = {}
        self.is_span_noans = ""


    def start_span(self,attrs):
        if attrs[1] == 'no answer':
            self.is_span_noans = 1
        else:
            self.is_span = 1


    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for (attribute, value) in attrs:
                if attribute == 'data-id':
                    self.qid = value
                    self.qa_True.update(self.qid,[])

    def handle_data(self,text):
        if self.is_span_noans == 1:
            self.qa_True.update(self.qid,'null')
        if self.is_span ==1:
            self.qa_True.update(self.qid, self.qa_True.get(self.qid).append(text))


    @staticmethod
    def gather_content(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = DataExtract(page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return

str = "https://rajpurkar.github.io/SQuAD-explorer/explore/v2.0/dev/Normans.html"
DataExtract.gather_content(str)
