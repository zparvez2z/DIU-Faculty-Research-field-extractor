from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
from bs4 import BeautifulSoup as bs


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    extracted_data_file = ''
    queue = set()
    crawled = set()
    extracted_data = set()
    NameSet = set()
    NameFile = ''


    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.extracted_data_file = Spider.project_name + '/extracted_data_file.txt'
        Spider.NameFile = Spider.project_name+'/NameFile.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.extracted_data = DataFile_to_set(Spider.extracted_data_file)
        Spider.NameSet = file_to_set(Spider.NameFile)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8','ignore')
                Spider.Extract_data(html_string)
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)

        except Exception as e:
            print(str(e))
            print('Name Set : ' + str(len(Spider.NameSet)))
            set_to_file(Spider.NameSet, Spider.NameFile)
            print('Data Set : ' + str(len(Spider.extracted_data)))
            set_to_file(Spider.extracted_data, Spider.extracted_data_file)
            return set()
        return finder.page_links()


    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        print('Name Set : ' + str(len(Spider.NameSet)))
        set_to_file(Spider.NameSet,Spider.NameFile)
        print('Data Set : ' + str(len(Spider.extracted_data)))
        set_to_file(Spider.extracted_data,Spider.extracted_data_file)


    @staticmethod
    def Extract_data(html_string):
        name = ""
        research = ""
        soup = bs(html_string, 'html.parser')
        div = soup.find_all("div", {"class": "profile-header"})
        for x in div:
            name = str(x.span.text)

        #if name in Spider.NameSet:
            #print("Repeated Name : " +name)
        if name not in Spider.NameSet:
            print('New Name found : '+name)
            Spider.NameSet.add(name)
        div2 = soup.find_all("div", {"id": "Research"})
        for x in div2:
            research = str(x.text)
        teacher = str("Name : " + name + " | Research :" + research + "$")
        if teacher not in Spider.extracted_data:
            Spider.extracted_data.add(teacher)
            








