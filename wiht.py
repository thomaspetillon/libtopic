#Topic wiht module
#Provides automated querying of WhoIsHostingThis.com (WIHT)
import re
import time
import urllib2
import random
import MySQLdb
import socket

def site_exists_in_db(siteUrl):
    # Open connection
    db = MySQLdb.connect(db='poweredby',passwd='qk418633',user='root')
    # Get value
    c = db.cursor()
    sql = "SELECT * FROM WebSite WHERE Url='"+siteUrl+"'"
    c.execute(sql)    
    rowcount = c.rowcount    
    # Close cursor and connection
    c.close()
    db.close()
    # Return result
    if (rowcount==1):
        return 1
    else:
        return 0
    
def get_provider_id(providerUrl):
    # Open connection
    db = MySQLdb.connect(db='poweredby',passwd='qk418633',user='root')
    # Get value
    c = db.cursor()
    c.execute("SELECT ID_HostingProvider FROM HostingProvider WHERE Url='"+providerUrl+"'")    
    if (c.rowcount==1):
        row = c.fetchone()
        providerid = row[0]
    else:
        providerid = -1
    # Close cursor and connection
    c.close()
    db.close()
    return providerid
    
def save_site_urlonly(siteUrl):
    # Open connection
    db = MySQLdb.connect(db='poweredby',passwd='qk418633',user='root')    
    c = db.cursor()
    print 'Registering new url : '+siteUrl
    c.execute("INSERT INTO WebSite(Url) VALUES('"+siteUrl+"')")    
    c.close()    
    db.commit()
    db.close()
    
def execute_query(sql):
    # Open connection
    db = MySQLdb.connect(db='poweredby',passwd='qk418633',user='root')    
    c = db.cursor()
    c.execute(sql)    
    c.close()    
    db.commit()
    db.close()
    
def save(siteUrl,siteName,providerUrl,providerName):
    # Open connection
    db = MySQLdb.connect(db='poweredby',passwd='qk418633',user='root')
    # If provider not referenced yet, create it
    providerid = get_provider_id(providerUrl)
    if (providerid == -1):
        # Insert provider
        c = db.cursor()
        providerName = providerName.replace("'"," ") # Remove simple quotes
        c.execute("INSERT INTO HostingProvider(Url,Name) VALUES('"+providerUrl+"','"+providerName+"')")    
        c.close()    
        # Get inserted provider
        c = db.cursor()
        c.execute("SELECT MAX(ID_HostingProvider) FROM HostingProvider")
        row = c.fetchone()
        providerid=row[0]
        c.close()            
    # Insert web site
    c = db.cursor()
    siteName = siteName.replace("'"," ") # Remove simple quotes
    c.execute("INSERT INTO WebSite(Url,Name,ID_HostingProvider) VALUES('"+siteUrl+"','"+siteName+"',"+str(providerid)+")")    
    c.close()
    # Do final commit and close connection
    db.commit()
    db.close()    

def processWebSiteList(urls):
    for url in urls:
        try:
            processWebSite(url)
        except:
            print 'Error while processing url : '+url
    print '>>Processing completed !'
    
def crawlEntireWebSiteForOutgoingLinks(siteUrl):
    """
    Crawls a web site
    """
    internalLinks = getInternalLinks(siteUrl)    
    for internalLink in internalLinks:
        crawlUrlForOutgoingLinks(internalLink)
        #recursiverly crawl internal link
        crawlEntireWebSiteForOutgoingLinks(internalLink)
        
def crawlUrlForOutgoingLinks(url):
    """
    Crawls the given url for outgoing links
    """    
    try:        
        print 'Crawling external links for url : '+url
        outgoingLinks = getOutgoingLinks(url)
        for link in outgoingLinks:
            print "external link found : "+link
            if (site_exists_in_db(link)==0):        
                save_site_urlonly(link)
            else:
                print "...already registered"
        #Mark input site as 'Crawled'
        db = MySQLdb.connect(db='poweredby',passwd='qk418633',user='root')
        c = db.cursor()
        sql = "UPDATE WebSite SET ExternalLinksCrawled=1 WHERE Url='"+url+"'"
        c.execute(sql)
        c.close()
        db.commit()
        db.close()
    except:
        # Ignore errors
        print 'Failed to explore outgoing links for url : '+url      
        execute_query("UPDATE WebSite SET ExternalLinksCrawlingFailed = 1 WHERE Url='"+url+"'")        
    
def crawlLoop():
    rowcount = 1
    while(rowcount>0):
        rowcount = crawlAllHomePagesForOutgoingLinks()
        
def crawlAllHomePagesForOutgoingLinks():
    """
    Crawls all referenced sites for outgoing links
    """
    # Open connection
    db = MySQLdb.connect(db='poweredby',passwd='qk418633',user='root')
    # Perform query (find all sites that have not already be crawled)
    sql = "SELECT Url FROM WebSite WHERE ExternalLinksCrawled=0 AND ExternalLinksCrawlingFailed=0"
    c = db.cursor()
    c.execute(sql)
    print 'Websites to crawl :'+str(c.rowcount)
    rowcount  = c.rowcount    
    # Process results
    sitesToProcess = []
    while (1):
        # Fetch new url
        row = c.fetchone ()        
        if row == None:
            break
        url = row[0]
        crawlUrlForOutgoingLinks(url)            
    # Close cursor and connection connection    
    c.close()                
    db.close()
    print 'Completed crawling session'
    return rowcount

def processWebSite(siteUrl):
    """
    Find hosting provider information for web site
    """    
    # If already registered, skip it
    if (site_exists_in_db(siteUrl)==1):
        print('website already exits in db : '+siteUrl)
        return    
    # Fetch html result
    print('Starting processing for website : '+siteUrl)
    time.sleep(random.uniform(1,5)) # Perform random sleep before call
    socket.setdefaulttimeout(10)
    sock = urllib2.urlopen("http://www.whoishostingthis.com/"+siteUrl)
    html = sock.read()
    # Extract links
    p = re.compile('<a[^>]*href=\"/linkout[^>]*>[^<]+</a>')
    links = p.findall(html)
    # Define regular expressions
    p1 = re.compile('(?<=href=\"/linkout/\?t=[1-9]{1}&amp;url=)[^\"]+(?=\")')
    p2 = re.compile('(?<=>)[^<]*(?=</a>)')
    # Extract data
    siteUrl  = p1.findall(links[0])[0]
    siteName = p2.findall(links[0])[0]    
    providerUrl  = p1.findall(links[1])[0]
    providerName = p2.findall(links[1])[0]
    print('[SITE] url='+siteUrl+'; name='+siteName)
    print('[HOSTING] url='+providerUrl+'; name='+providerName)
    # Save data
    save(siteUrl,siteName,providerUrl,providerName)
    
def is_absolute_link(link):
    pattern = "http://.*"
    p = re.compile(pattern)
    result = p.findall(link)
    return len(result)        
    
def getInternalLinks(homePageUrl):
    """
    Gets internal links from given page    
    """
    # Find candidate links
    socket.setdefaulttimeout(10)
    sock = urllib2.urlopen("http://"+homePageUrl)
    html = sock.read()
    pattern = "(?<=href=\")[^\"]+(?=\")"    
    p = re.compile(pattern)
    links = p.findall(html)
    # Retain only internal links
    result = []
    for link in links:
        if (is_absolute_link(link)):
            if (link[:len(homePageUrl)+7]=="http://"+homePageUrl):
                result.append(link[7:])
        else:
            prefix = homePageUrl
            if (link[0]!='/'):
                prefix = prefix + '/'                            
            result.append(prefix+link)
    return result

def getOutgoingLinks(pageUrl):
    """
    Gets outgoing links from given page
    Nota : current implementation only retrieve simple .fr links (e.g : www.topic.fr). No subdomains or composed urls (e.g : subdomain.topic.fr ou www.topic.fr/test)
    """
    socket.setdefaulttimeout(10)
    sock = urllib2.urlopen("http://"+pageUrl)
    html = sock.read()
    p = re.compile("(?<=href=\"http://)www.[^.]+.\.fr")
    links = p.findall(html)
    resultlinks = []
    for l in links:
        if l not in resultlinks:
            resultlinks.append(l)
    return resultlinks

    