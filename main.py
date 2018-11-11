start_date = 000000000
start_time = 000000000

Threshold = 0.5

min_temp = float(input("Please enter your minimum temperature: "))
min_humid = float(input("Please enter your minimum humidity: "))
max_temp = float(input("Please enter your maximum temperature: "))
max_humid = float(input("Please enter your maximum humidity: "))

"""
Send a query to the MongoDb to get a Reading_List of readings during a certain
given interval time

"""

Reading_List = [
                [02.28,"00:59:16.02785",1,19.9884,37.0933],   
                [02.28,"01:03:16.33393",1,19.3024,38.4629],   
                [02.28,"01:06:16.013453",1,19.1652,38.8039],   
                [02.28,"01:06:46.778088",1,19.175,38.8379],   
                [02.28,"01:08:45.992524",1,19.1456,38.9401]
                ]
print("Length of Reading_List:", len(Reading_List))
ctr=1
Check_List = []
while ctr <= 1:
    i=0
    j = 1
    while i < len(Reading_List):
        sensor_name = "sensor1"
        if j==Reading_List[i][2]:   # to check if the sensor id is the same i
            Check_List.append(Reading_List[i])
        i+=1

    print("Length of Check_List:", len(Check_List))
    Yes_ctr = 0
    No_ctr = 0
    i=0
    while i<len(Check_List):
        if(Check_List[i][3]>=min_temp and Check_List[i][3]<=max_temp) and (Check_List[i][4]>=min_humid and Check_List[i][4]<=max_humid):
            Yes_ctr+=1
        else:
            No_ctr+=1

        i+=1

    if Yes_ctr == len(Check_List):
        probability = 100
    else:
        probability = No_ctr/len(Check_List)

    if probability >= Threshold:
        print("The %s is in danger!" % sensor_name)
    else:
        print("The probability was calculated is:", Yes_ctr/len(Check_List))
    
    ctr+=1
        
    

