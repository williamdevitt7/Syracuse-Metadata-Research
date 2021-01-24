#################################################################
# Python program for extracting NIH data about authors of virus research,
# specifically their nationalities, to map virus research by country
# 1/22/2021
# imports follow in the next block
#################################################################

import pandas as pd
import pycountry


def import_sub_els():
    count = 1992
    els_list = []
    for i in range(27):
        data = pd.read_csv(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\sub_els\sub_virus_el_' + str(count) + '.csv')
        df = pd.DataFrame(data, columns=['journal', 'tax_name'])
        els_list.append(df)
        count += 1
    return els_list

#################################################################


def return_country_from_string(text):
    for country in pycountry.countries:
        if country.name in text:
            return country.name


if __name__ == '__main__':
    sub_els_list = import_sub_els()
    # print(sub_els_list[0])