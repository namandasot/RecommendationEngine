import requests
from sqlreader import DataCleaner
import csv


def GoogleDistance(origin_coord, destination_coord, mode = 'driving'):
    API_KEY = ""
    url_request = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode={2}&language=fr-FR&key={3}".format(origin_coord, destination_coord, mode, API_KEY)
    rsp = requests.get(url_request)
    return rsp.status_code, rsp.text.encode('utf-8')

if __name__ == '__main__':
    done_pair = {}
    DC = DataCleaner()
    csv_file = csv.writer(open('Google_Distance_Data.csv', 'w'))
    organised_data, project_city_dict = DC.connect_data()
    count = 0
    for i, ele in enumerate(organised_data['Mumbai']['attributes']):
        origin_coord = str(ele[0]) + ',' + str(ele[1])
        for next_ele in organised_data['Mumbai']['attributes'][i+1:]:
            dest_coord = str(next_ele[0]) + ',' + str(next_ele[1])
            if not done_pair.has_key((origin_coord, dest_coord)):
                response_code, response = GoogleDistance(origin_coord, dest_coord)
                count += 1
                print response_code, '<<>>', count
                if str(response_code) == '200':
                    done_pair[(origin_coord, dest_coord)] = 1
                    csv_file.writerow([origin_coord, dest_coord, response])
