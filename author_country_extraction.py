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


def return_country_from_string(string):
    for country in pycountry.countries:
        if country.name in string:
            return country.name

# takes a dataframe & a list of names, trimming the dataframe to only include
# entries for the specified viruses
# called by lister
def sub_el_virus_name_binder(df, top_vir_list):
    top_vir_namesIN = {'journal': [],
                       'tax_name': []
                       }
    top_vir_names_df = pd.DataFrame(top_vir_namesIN, columns= ['journal', 'tax_name'])
    for i in range(len(top_vir_list)):
        top_vir = df.loc[df['tax_name'] == top_vir_list[i]]
        top_vir_names_df = top_vir_names_df.append(top_vir)

    return top_vir_names_df  # return df with only the top n virus freqs


# FUNC: takes sub list and calls the binder function on each element, returning sub list with just desired virus data
def sub_el_lister(sub_el_list, top_vir_list):
    new_el_list = []
    year = 1992
    for i in range(len(sub_el_list)):
        new_df = sub_el_virus_name_binder(sub_el_list[i], top_vir_list)
        new_el_list.append(new_df)
        print(str(year), new_df)
        year += 1

    return new_el_list



if __name__ == '__main__':
    top_virus_list = ["Human immunodeficiency virus 1", "Dengue virus 2", "Dengue virus 1",
                      "Dengue virus 3", "West Nile virus", "Hepacivirus C", "Hepatitis C virus subtype 1a",
                      "Hepatitis B virus", "Zika virus", "Hepatitis E virus"]
    top_virus_list_test = ["Human immunodeficiency virus 1", "Dengue virus 2", "Dengue virus 1",
                      "Dengue virus 3", "West Nile virus"]
    sub_els_list = import_sub_els()
    # sub_el_virus_name_binder(sub_els_list[0], top_virus_list_test)
    # pub_els_list = import_pub_els()
    trimmed_sub_el_list = sub_el_lister(sub_els_list, top_virus_list)
    # trimmed_pub_el_list = pub_el_lister(pub_els_list, top_virus_list)

    # print(sub_els_list[0])