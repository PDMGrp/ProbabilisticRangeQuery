import MongoDB
import matplotlib
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import random

Threshold=0.95
print("Confidence Threshold: ",Threshold)

min_temp = float(input("Please enter your minimum temperature: "))
min_humid = float(input("Please enter your minimum humidity: "))
max_temp = float(input("Please enter your maximum temperature: "))
max_humid = float(input("Please enter your maximum humidity: "))

sw_range = int(input("Please enter the Sliding Window size: "))
start_time = input("Please enter your start time of query (YYYY-M-D-H): ")

counter = 0
coord = []

while True:
  Reading_List = MongoDB.main(sw_range, start_time, counter)
  print("Length of Reading_List:", len(Reading_List))

  ctr=1 
  Check_List = []
  Num_Of_Sensors = 58
  
  while ctr <= Num_Of_Sensors:
    i=0
    while i < len(Reading_List):
      sensor_name = "sensor"+str(ctr)
      if ctr==Reading_List[i][1]:   # to check if the sensor id is the same ctr's value
        Check_List.append(Reading_List[i])
      i+=1
      
    Yes_ctr = 0     #to count number of readings fall in the user-given range query
    No_ctr = 0      #to count number of readings fall out of the user-given range query

    if len(Check_List) > 0:
      s_min_temp = Check_List[0][2]
      s_min_hum = Check_List[0][3]
    else:
      s_min_temp = 0
      s_min_hum = 0
      
    s_max_hum = 0
    s_max_temp = 0

    i=0
    while i<len(Check_List):

      if(Check_List[i][2] < s_min_temp):
        s_min_temp = Check_List[i][2]

      if(Check_List[i][2] > s_max_temp):
        s_max_temp = Check_List[i][2]

      if(Check_List[i][3] < s_min_hum):
        s_min_hum = Check_List[i][3]

      if(Check_List[i][3] > s_max_hum):
        s_max_hum = Check_List[i][3]

      if(Check_List[i][2]>=min_temp and Check_List[i][2]<=max_temp) and (Check_List[i][3]>=min_humid and Check_List[i][3]<=max_humid):
        Yes_ctr+=1
      else:
        No_ctr+=1

      i+=1

    if No_ctr == len(Check_List):
      probability = 100
    else:
      probability = No_ctr/len(Check_List)

    if len(Check_List) == 0:
      print("No readings returned for the %s during the given range!" % sensor_name)
    elif probability >= Threshold:
      print("Warning: the %s is in danger with confidence %f!" % (sensor_name,probability))
    else:
      print("No action is required: %s %f" % (sensor_name, probability))
      
    coord.append([s_min_temp,s_min_hum,s_max_temp,s_max_hum])

    Check_List.clear()    
    ctr+=1

  plt.axes()
  rectangle = plt.Rectangle((min_temp, min_humid), max_temp - min_temp, max_humid - min_humid, fc='y', linestyle='dashed')
  plt.gca().add_patch(rectangle)

  Color_List = list(colors._colors_full_map.values())

  i=0
  while i<len(coord):
      MBR = plt.Rectangle((coord[i][0], coord[i][1]), coord[i][2] - coord[i][0], coord[i][3] - coord[i][1], fc=random.choice(Color_List))
      plt.gca().add_patch(MBR)
      i+=1
    

  plt.axis('scaled')
  plt.show()

  counter+= 1
  
  Key = input("Enter Y to check the sensor situations, N to stop checking: ")
  if Key=='N' or Key=='n':
    break
        




    

