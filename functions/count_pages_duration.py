def pages_duration(data):
    urls = data['urls']
    total_duration=0
    total_pages=0
    for each in urls:
        total_duration+=each['sec']
        total_pages+=1
    return [total_pages,total_duration]