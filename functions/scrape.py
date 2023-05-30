import requests
import pandas as pd
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def show(data):
    print('hello user')
    print(data[0]['url'])
    if 'url' in data[0]:
          for i in data:
                print(i['url'])

def scrape_urls(urls):
      urll=urls  
      #print(urll)  
     

     
      keywords = []   
      url = ['chrome://newtab/']
      for i in urll:
            print(i['url'])
            print('line 23')
            r=''
            try:

                  r = requests.get(i['url'])
            except:
                  return
            
            htmlContent = r.content
           
            #print(htmlContent)
            if htmlContent is not None:

                  soup = BeautifulSoup(htmlContent,'html.parser')
                  
                  
                  
                  
                  try: 
                        meta=soup.find("meta", {"name":"keywords"}).attrs['content']
                        
                        removeSpace = meta.replace(" ","")
                        metaList = removeSpace.split(',')
                        for metakeyword in metaList:
                                    keywords.append({'keyword':metakeyword,'sec':i['sec'],'pages':1})
                  except AttributeError:
                        print('attribute error')
                        try:

                              meta=soup.find("meta", {"name":"Keywords"}).attrs['content']
                        
                              removeSpace = meta.replace(" ","")
                              metaList = removeSpace.split(',')
                              for metakeyword in metaList:
                                    keywords.append({'keyword':metakeyword,'sec':i['sec'],'pages':1})
                        except:
                              url=urlparse(i['url']).netloc
                              keywords.append({'keyword':url,'sec':i['sec'],'pages':1})
                        
                        

                  except:
                        pass
                  

    
    
  

 # Python3 code to demonstrate working of
# Each word frequency percentage
# Using count() and split()

# initializing list
    
                        
      # printing original list
      
      return keywords

def words_cloud(keywords_array):
            #print('return keywords 74')
            #print(keywords_array)
            keyword_in_string = ','.join([str(elem) for elem in keywords_array])
            #print(keyword_in_string)
            keywords = list(keyword_in_string.split(","))

            #keywords = ["Gfg is best for geeks","All love Gfg","Gfg is best for CS","For CS geeks Gfg is best"]
      
            #print("The original list is : " + str(keywords))
        
            # concatenating using join
            joined = " ".join(ele for ele in keywords)
            p=joined.split()
            d=dict()
            for i in p:
                    if i not in d.keys():
                        d[i]=(p.count(i)/len(p))*100

            # printing result
            '''
            print("Percentage share of each word : " + str(d))
            chunlen=1
            dislist = list(d.items())
            a=[dict(dislist[i:i + chunlen]) for i in range(0, len(dislist), chunlen)] 
            print(a)
            '''
            new_dict_list = [{'word': word, 'size': str(size*30)}for word, size in d.items()]
            
            return(new_dict_list)


def wcloud (listArr):
      result = pd.DataFrame(listArr).groupby('keyword', as_index=False).sum(numeric_only=False).to_dict(orient='records')
      print('wccloud')
      #print(result)
      try:
             return result
      except:
             pass

def scrape_Video_url(urls):
      urll=urls  
      print(urll)  
     

     
      keywords = []   
      url = ['chrome://newtab/']
      for i in urll:
            print(i['url'])
            r=''
            try:

                  r = requests.get(i['url'])
                  htmlContent = r.content
            except:
                  pass
            
                       
            #print(htmlContent)
            if htmlContent is not None:

                  soup = BeautifulSoup(htmlContent,'html.parser')
                  
                  
                  
                  
                  try: 
                        meta=soup.find("meta", {"name":"keywords"}).attrs['content']
                        
                        removeSpace = meta.replace(" ","")
                        metaList = removeSpace.split(',')
                        vid_url = []
                        vid_url.append(i['url'])
                        for metakeyword in metaList:
                                    keywords.append({'keyword':metakeyword,'sec':i['sec'],'pages':1,'video':1,'video_url':vid_url})
                  except AttributeError:
                        print('attribute error')
                        try:

                              meta=soup.find("meta", {"name":"Keywords"}).attrs['content']
                        
                              removeSpace = meta.replace(" ","")
                              metaList = removeSpace.split(',')
                              vid_url = []
                              vid_url.append(i['url'])
                              for metakeyword in metaList:

                                    keywords.append({'keyword':metakeyword,'sec':i['sec'],'pages':1,'video':1,'video_url':vid_url})
                                    
                        except:
                              pass
                        
                        
                        

                  except:
                        pass
                  

    
    
  

 # Python3 code to demonstrate working of
# Each word frequency percentage
# Using count() and split()

# initializing list
    
                        
      # printing original list
     
      return keywords


#scrape comment url
#08/05/23
def scrape_Comment_url(urls):
      urll=urls  
      print(len(urll))
      print(urll[0]) 
      

     
      keywords = []   
 
      for i in urll:
            # if list of dict is not empty
            if bool(i):
                  #assigning all dict value into comment list using dict
                  comment = []
                  comment.append({'date':i['date'],'title':i['title'],'url':i['form_url'],'comment':i['comment']})
                  
                  r=""
                  try:
                        r=requests.get(i['form_url'])
                  except:
                        print(Exception)
                        return keywords
                  
                  htmlContent = ""
                  if r.content:
                        htmlContent=r.content
                  else:htmlContent=None
            
                  #print(htmlContent)
                  if htmlContent is not None:

                        soup = BeautifulSoup(htmlContent,'html.parser')
                        
                        
                        
                        
                        try: 
                              meta=soup.find("meta", {"name":"keywords"}).attrs['content']
                              
                              removeSpace = meta.replace(" ","")
                              metaList = removeSpace.split(',')
                        
                              for metakeyword in metaList:
                                          keywords.append({'keyword':metakeyword,'pages':1,'sec':10,'comment':comment})
                        except AttributeError:
                              print('attribute error')
                              try:

                                    meta=soup.find("meta", {"name":"Keywords"}).attrs['content']
                              
                                    removeSpace = meta.replace(" ","")
                                    metaList = removeSpace.split(',')
                                    
                                    for metakeyword in metaList:
                                          keywords.append({'keyword':metakeyword,'pages':1,'sec':60,'comment':comment})
                              except:
                                    url=urlparse(i['form_url']).netloc
                                    keywords.append({'keyword':url,'pages':1,'sec':60,'comment':comment})
                        
                        except:
                              pass
                   
      
      return keywords