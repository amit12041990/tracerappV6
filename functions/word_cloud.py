def words_cloud(keywords_array):
            print(keywords_array)
            keywords = ["Gfg is best for geeks",
                        "All love Gfg",
                        "Gfg is best for CS",
                        "For CS geeks Gfg is best"]
      
            print("The original list is : " + str(keywords))
        
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
            new_dict_list = [{'word': word, 'size': str(size*3)}for word, size in d.items()]
            
            return(new_dict_list)
