#################################################################
# Python program for extracting NIH data about authors of virus research,
# specifically their nationalities, to map virus research by country
# 1/22/2021
# imports follow in the next block

#################################################################

import pandas as pd
from geotext import GeoText


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


def return_country_from_string(input_string):
    places = GeoText(input_string)
    places = places.countries
    if (places == None) or (places == []):
        return input_string
    return places[0]


# called by lister function!?
# takes one year, parses country from submission column
def parse_country_from_dataframe(df):
    for i in range(len(df["journal"].array)):
        text = return_country_from_string(df["journal"].array[i])
        # print(text)
        df["journal"].array[i] = text

    return df


# takes a dataframe (of 1 year of data) & a list of names, trimming the dataframe to only include
# entries for the specified viruses
# called by lister
def virus_name_binder(df, top_vir_list):
    top_vir_namesIN = {'journal': [],
                       'tax_name': []
                       }
    top_vir_names_df = pd.DataFrame(top_vir_namesIN, columns= ['journal', 'tax_name'])
    for i in range(len(top_vir_list)):
        # looks for 1 virus after another on the whole column of viruses
        top_vir = df.loc[df['tax_name'] == top_vir_list[i]]
        top_vir_names_df = top_vir_names_df.append(top_vir)

    return top_vir_names_df  # return df with only the top n virus freqs


# FUNC: takes sub list and calls the binder function on each element, returning sub list with just desired virus data
# one DF = 1 year
def sub_el_lister(sub_el_list, top_vir_list):
    new_el_list = []
    year = 1992
    for i in range(len(sub_el_list)):
        new_df = virus_name_binder(sub_el_list[i], top_vir_list)
        new_df = parse_country_from_dataframe(new_df)
        # apply country counter function here
        new_el_list.append(new_df)
        print(str(year), new_df)
        year += 1

    return new_el_list


if __name__ == '__main__':
    top_virus_list = ["Human immunodeficiency virus 1", "Dengue virus 2", "Dengue virus 1",
                      "Dengue virus 3", "West Nile virus", "Hepacivirus C", "Hepatitis C virus subtype 1a",
                      "Hepatitis B virus", "Zika virus", "Hepatitis E virus"]
    top_virus_list_TEST = ["Human immunodeficiency virus 1", "Dengue virus 2", "Dengue virus 1",
                      "Dengue virus 3", "West Nile virus"]

    sub_els_list = import_sub_els()
    # pub_els_list = import_pub_els()
    trimmed_sub_el_list = sub_el_lister(sub_els_list, top_virus_list_TEST)
    # trimmed_pub_el_list = pub_el_lister(pub_els_list, top_virus_list)
