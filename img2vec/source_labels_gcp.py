# -*- coding: utf-8 -*-
"""img4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G-d9ibV9yoDCQ8VmZDjgOEg9SSYcyyHr
"""

!pip3 install -U pip google-cloud-vision
from google.cloud import vision
import pandas as pd
import os
from multiprocessing import Pool
import itertools

df = pd.read_csv('drive/My Drive/mshr/imgurl.csv', delimiter = ',')
image_uri = df.image_url

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="drive/My Drive/mshr/local-fragment-272823-a0631f5118d9.json"

class create_labels:
  
  def __init__(self, image_uri):
    self.image_uri = image_uri # contains the list of all uri
    self.err = [] # captures broken links and uri that return no labels
    self.result1 = [] # contains result from each parallel process
    self.result_flat = [] # contains final results
  
  def get_labels(self,uri):
    print(uri)
    # using Google Vision API to generate labels
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    label_list = [] # contains the list of labels for the current uri
    if len(response.label_annotations) == 0: # if there are no labels the current uri is marked into err
      print('ERROR')
      return 0
    else:
      for label in response.label_annotations:
            label_list.append(label.description) # otherwise, append label description, ie. the labels to the label_list

    if response.error.message: # if the link is broken or the uri is inaccessible
        print('ERROR')
        return 0
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                  response.error.message))
    return [uri,label_list] # if there are no errors, returnt the label_list
  
  def run_create(self,image_list):
    all_labels = [] # contains the results for each chunk
    for uri in image_list:
      print('finding labels for uri', uri) # only the 1st uri of each chunk gets parsed
      res = self.get_labels(uri)
      if res == 0:
        continue
      else:
        all_labels.append(res)
    return all_labels
  
  def run_mp(self):
    chunks = [self.image_uri[390000:392000],
              self.image_uri[392000:394000],
              self.image_uri[394000:396000],
              self.image_uri[396000:398000],
              self.image_uri[398000:400000]]
   
    pool = Pool(processes = 5) # number of processes = 5, since there are 5 chunks
    self.result1 = pool.map(self.run_create, chunks) # pass these 5 chunks to run_create to parallelly process the chunks
    self.result_flat = list(itertools.chain(*self.result1))
    print(self.result_flat)

  def printlabel(self):
    print('Number of images parsed =', len(self.result_flat))
    f = pd.DataFrame(self.result_flat)
    f.to_csv('drive/My Drive/mshr/label39.csv')
    
obj = create_labels(image_uri)
obj.run_mp()
obj.printlabel()

