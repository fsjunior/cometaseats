import json
from operator import itemgetter




with open("items.json") as items_file:
    items_json = json.load(items_file)

print len(items_json)

occupied_seats = [0 for i in range(46)]

for item in items_json:
    occupied_seats = [x + y for x, y in zip(occupied_seats, item['seats'])]
    

dict_occupied_seats = dict((key + 1, value) for key, value in zip(xrange(46), occupied_seats))

dict_occupied_seats = sorted(dict_occupied_seats.items(), key=itemgetter(1))

print dict_occupied_seats
