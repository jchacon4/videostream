import requests

#http://media.kairos.com/kairos-elizabeth.jpg

def register(img, who, gallery):
    url='https://api.kairos.com/enroll'
    values = """{"image": "%s","subject_id": "%s","gallery_name": "%s"}""" % (img, who, gallery)
    headers = {'Content-Type': 'application/json','app_id': 'd3048a11','app_key': 'df6fd0d96a6ec663d200c8074fa49afe'}
    response = requests.request("POST",url, data=values, headers=headers)
    return(response.json())

def recognize(img, gallery):
    url='https://api.kairos.com/recognize'
    values = """{"image": "%s","gallery_name": "%s"}""" % (img, gallery)
    headers = {'Content-Type': 'application/json','app_id': 'd3048a11','app_key': 'df6fd0d96a6ec663d200c8074fa49afe'}
    response = requests.request("POST",url, data=values, headers=headers)
    return(response.json())

def verify(img, who, gallery):
    url='https://api.kairos.com/verify'
    values = """{"image": "%s","gallery_name": "%s", "subject_id": "%s"}""" % (img, gallery, who)
    headers = {'Content-Type': 'application/json','app_id': 'd3048a11','app_key': 'df6fd0d96a6ec663d200c8074fa49afe'}
    response = requests.request("POST",url, data=values, headers=headers)
    return(response.json())
