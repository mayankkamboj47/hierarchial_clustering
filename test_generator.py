import random
import csv

with open('test_data.csv', mode='w') as test_file:
    test_file.truncate(0)
    test_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    test_writer.writerow(['x', 'y'])
    n = 5000
    while(n > 0):
        n-=1
        x = random.randint(0, 1000000)
        y = random.randint(0, 1000000)
        test_writer.writerow([x, y])
