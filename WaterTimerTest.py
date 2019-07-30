import datetime

watercounter=datetime.datetime.now()
moisturelevel = 10

print (watercounter)
print (watercounter+datetime.timedelta(hours=24))


if (moisturelevel <= 10 and datetime.datetime.now()>(watercounter-datetime.timedelta(hours=24))):
    print ("running water ")
else:
    print ("not enough time passed ")
