start_date = 000000000
start_time = 000000000

Threshold = 0.9

min_temp = int(input("Please enter your minimum temperature: "))
min_humid = int(input("Please enter your minimum humidity: "))
max_temp = int(input("Please enter your maximum temperature: "))
max_humid = int(input("Please enter your maximum humidity: "))

"""
Send a query to the MongoDb to get a Reading_List of readings during a certain
given interval time

"""

ctr=1
while ctr <= 58:
    i=1
    Check_List = []
    while i <= len(Reading_List):
        sensor_name = "sensor"+str(i)
        if i==Reading_List[i][2]:   # to check if the sensor id is the same i
            Check_List.append(Reading_List[i])
        i+=1

    Yes_ctr = 0
    No_ctr = 0
    i=0
    while i<len(Check_List):
        if(Check_List[i][3]>=min_temp and Check_List[i][3]<=max_temp) and (Check_List[i][4]>=min_humid and Check_List[i][4]<=max_humid):
            Yes_ctr+=1
        else:
            No_ctr+=1

        i+=1

    if Yes_ctr == len(Check_list):
        probability = 100
    else:
        probability = Yes_ctr/len(Check_list)

    if probability >= Threshold:
        print("The %s is in danger!" % sensor_name)

    ctr+=1
        
    
