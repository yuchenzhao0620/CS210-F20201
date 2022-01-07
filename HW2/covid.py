# @author Tianle Chen, tc822; Yuchen Zhao, yz1116
import csv


def age(age_range):
    ls = age_range.split('-')
    average = round((float(ls[1]) - float(ls[0])) / 2 + float(ls[0]))
    return average


def province_city():
    province_city_dict = {}
    city_dict = {}
    stk = {}
    with open('covidTrain.csv') as city:
        reader = csv.reader(city)
        next(reader)
        for row in reader:
            if row[3] == 'NaN':
                continue
            if row[4] not in province_city_dict:
                province_city_dict[row[4]] = {}
                province_city_dict[row[4]][row[3]] = 1
            else:
                if row[3] not in province_city_dict[row[4]]:
                    province_city_dict[row[4]][row[3]] = 1
                else:
                    province_city_dict[row[4]][row[3]] += 1
    for key in province_city_dict.keys():
        stk[key] = {}
        lst = dict(sorted(province_city_dict[key].items(), key=lambda x: x[0], reverse=False))
        stk[key] = lst
    for key, val in stk.items():
        max_val = 0
        for key1 in val.keys():
            if val[key1] > max_val:
                max_val = val[key1]
                word = key1
        city_dict[key] = word
    return city_dict


# print(province_city())


def average_latitude(province):
    total_latitude = 0
    count = 0
    with open('covidTrain.csv') as latitude:
        reader = csv.reader(latitude)
        next(reader)
        for row in reader:
            if row[4] != province or row[6] == "NaN":
                continue
            else:
                total_latitude += float(row[6])
                count += 1
        average = total_latitude / count
    return average


# print(average_latitude('Beijing'))

def average_longitude(province):
    total_longitude = 0
    count = 0
    with open('covidTrain.csv') as longitude:
        reader = csv.reader(longitude)
        next(reader)
        for row in reader:
            if row[4] != province or row[7] == "NaN":
                continue
            else:
                total_longitude += float(row[7])
                count += 1
        average = total_longitude / count
    return average


# print(average_longitude('Hokkaido'))


def date_change(date):
    # date = '15.02.2020'
    ls = date.split('.')
    new_date = ls[1] + '.' + ls[0] + '.' + ls[2]
    return new_date


# print(date_change())

def symptom_dict():
    symptom_province_dict = {}
    stk = {}
    province_dict = {}
    with open('covidTrain.csv') as symptom:
        reader = csv.reader(symptom)
        next(reader)
        for row in reader:
            if row[4] not in symptom_province_dict:
                symptom_province_dict[row[4]] = {}
            if row[11] != 'NaN':
                ls = row[11].split(';')
                for val in ls:
                    if val.strip() not in symptom_province_dict[row[4]]:
                        symptom_province_dict[row[4]][val.strip()] = 1
                    else:
                        symptom_province_dict[row[4]][val.strip()] += 1
    for key in symptom_province_dict.keys():
        stk[key] = {}
        lst = dict(sorted(symptom_province_dict[key].items(), key=lambda x: x[0], reverse=False))
        stk[key] = lst
    for key, val in stk.items():
        max_val = 0
        for key1 in val.keys():
            if val[key1] > max_val:
                max_val = val[key1]
                word = key1
        province_dict[key] = word
    return province_dict


# print(symptom_dict())


def create_covidResult():
    city = province_city()
    symptom = symptom_dict()
    with open('covidResult.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        with open('covidTrain.csv') as readfile:
            reader = csv.reader(readfile)
            row = next(reader)
            writer.writerow(row)
            for row in enumerate(reader):
                out_row = []
                count = 0
                for val in row[1]:
                    if val != 'NaN' and (count == 0 or count == 2 or count == 4 or count == 5):
                        out_row.append(val)
                        count += 1
                    else:
                        if count == 1:
                            try:
                                float(val)
                                out_row.append(val)
                                count += 1
                            except:
                                out_row.append(age(val))
                                count += 1
                        elif count == 3:
                            if val != 'NaN':
                                out_row.append(val)
                                count += 1
                            else:
                                out_row.append(city.get(row[1][4]))
                                count += 1
                        elif count == 6:
                            if val != 'NaN':
                                out_row.append(val)
                                count += 1
                            else:
                                out_row.append(average_latitude(row[1][4]))
                                count += 1
                        elif count == 7:
                            if val != 'NaN':
                                out_row.append(val)
                                count += 1
                            else:
                                out_row.append(average_longitude(row[1][4]))
                                count += 1
                        elif count == 8 or count == 9 or count == 10:
                            out_row.append(date_change(val))
                            count += 1
                        elif count == 11:
                            if val != 'NaN':
                                out_row.append(val)
                            else:
                                out_row.append(symptom.get(row[1][4]))
                writer.writerow(out_row)


create_covidResult()
