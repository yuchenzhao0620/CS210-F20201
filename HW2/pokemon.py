# @author Tianle Chen, tc822; Yuchen Zhao, yz1116
import csv


def percentage_pokemon():
    with open('pokemon1.txt', 'w') as outfile:
        with open('pokemonTrain.csv') as pokemon:
            csv_reader = csv.reader(pokemon)
            next(csv_reader)
            count = 0
            length = 0
            for row in csv_reader:
                if row[4] == 'fire':
                    length = length + 1
                    if float(row[2]) >= 40:
                        count = count + 1
            percentage = round(count / length * 100)
            print('Percentage of fire type Pokemons at or above level 40 = ' + str(percentage), file=outfile)


percentage_pokemon()


def fill_type_dict():
    pokemon_type_dict = {}
    pokemon_fill = {}
    stk = {}
    with open('pokemonTrain.csv') as pokemon:
        csv_reader = csv.reader(pokemon)
        next(csv_reader)
        for row in csv_reader:
            if row[4] == "NaN":
                continue
            if row[5] not in pokemon_type_dict:
                pokemon_type_dict[row[5]] = {}
                pokemon_type_dict[row[5]][row[4]] = 1
            else:
                if row[4] not in pokemon_type_dict[row[5]]:
                    pokemon_type_dict[row[5]][row[4]] = 1
                else:
                    pokemon_type_dict[row[5]][row[4]] += 1
        for key in pokemon_type_dict.keys():
            stk[key] = {}
            lst = dict(sorted(pokemon_type_dict[key].items(), key=lambda x: x[0], reverse=False))
            stk[key] = lst
        for key, val in stk.items():
            max_val = 0
            for key1 in val.keys():
                if val[key1] > max_val:
                    max_val = val[key1]
                    word = key1
            pokemon_fill[key] = word
    return pokemon_fill


# print(fill_type_dict())


def average_value(level, item):
    total_atk_40 = 0
    count_atk_40 = 0
    total_def_40 = 0
    count_def_40 = 0
    total_hp_40 = 0
    count_hp_40 = 0
    total_atk = 0
    count_atk = 0
    total_def = 0
    count_def = 0
    total_hp = 0
    count_hp = 0

    with open('pokemonTrain.csv') as pokemon:
        reader = csv.reader(pokemon)
        next(reader)
        for row in reader:
            if float(float(row[0])) > 40:
                if row[6] != 'NaN':
                    total_atk_40 += float(row[6])
                    count_atk_40 += 1
                if row[7] != 'NaN':
                    total_def_40 += float(row[7])
                    count_def_40 += 1
                if row[8] != 'NaN':
                    total_hp_40 += float(row[8])
                    count_hp_40 += 1
            else:
                if row[6] != 'NaN':
                    total_atk += float(row[6])
                    count_atk += 1
                if row[7] != 'NaN':
                    total_def += float(row[7])
                    count_def += 1
                if row[8] != 'NaN':
                    total_hp += float(row[8])
                    count_hp += 1
    if level > 40:
        if item == 'atk':
            return round(total_atk_40 / count_atk_40, 1)
        if item == 'def':
            return round(total_def_40 / count_def_40, 1)
        if item == 'hp':
            return round(total_hp_40 / count_hp_40, 1)
    else:
        if item == 'atk':
            return round(total_atk / count_atk, 1)
        if item == 'def':
            return round(total_def / count_def, 1)
        if item == 'hp':
            return round(total_hp / count_hp, 1)


def create_result():
    type_dict = fill_type_dict()
    with open('pokemonResult.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        with open('pokemonTrain.csv') as poke:
            reader = csv.reader(poke)
            row = next(reader)
            writer.writerow(row)
            for row in enumerate(reader):
                out_row = []
                count = 0
                for val in row[1]:
                    if val != 'NaN':
                        out_row.append(val)
                        count += 1
                    else:
                        if count == 4:
                            out_row.append(type_dict.get(row[1][5]))
                            count += 1
                        elif count == 6:
                            out_row.append(average_value(float(row[1][2]), 'atk'))
                            count += 1
                        elif count == 7:
                            out_row.append(average_value(float(row[1][2]), 'def'))
                            count += 1
                        elif count == 8:
                            out_row.append(average_value(float(row[1][2]), 'hp'))
                            count += 1
                writer.writerow(out_row)


create_result()


def pokemon_type():
    pokemon_personalities_type = {}
    with open('pokemon4.txt', 'w') as outfile:
        print('Pokemon type to personality mapping:\n', file=outfile)
        with open('pokemonResult.csv') as result:
            reader = csv.reader(result)
            next(reader)
            for row in reader:
                if row[4] not in pokemon_personalities_type:
                    pokemon_personalities_type[row[4]] = []
                    if row[3] not in pokemon_personalities_type[row[4]]:
                        pokemon_personalities_type[row[4]].append(row[3])
                else:
                    if row[3] not in pokemon_personalities_type[row[4]]:
                        pokemon_personalities_type[row[4]].append(row[3])
        stk = dict(sorted(pokemon_personalities_type.items(), key=lambda x: x[0], reverse=False))
        for key in stk:
            l1 = sorted(stk.get(key))
            print('\t' + key + ': ' + ", ".join(str(x) for x in l1), file=outfile)


pokemon_type()


def average_hp_3():
    total_hp = 0
    total_pokemon = 0
    with open('pokemon5.txt', 'w') as outfile:
        with open('pokemonResult.csv') as hp:
            reader = csv.reader(hp)
            next(reader)
            for row in reader:
                if float(row[9]) == 3:
                    total_hp += float(row[8])
                    total_pokemon += 1
        print('Average hit point for Pokemons of stage 3.0 = ' + str(round(total_hp / total_pokemon)), file=outfile)


average_hp_3()
