#################################################################
# Python program for extracting NIH data about authors of virus research,
# specifically their nationalities, to map virus research by country
# 1/22/2021
# imports follow in the next block

#################################################################

import pandas as pd
from geotext import GeoText
from pubmed_lookup import PubMedLookup
from pubmed_lookup import Publication
import subprocess as sp
import math


def import_sub_els():
    count = 1992
    els_list = []
    for i in range(27):
        data = pd.read_csv(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\sub_els\sub_virus_el_' + str(count) + '.csv')
        df = pd.DataFrame(data, columns=['journal', 'tax_name'])
        els_list.append(df)
        count += 1
    return els_list

# returns df of the Pub els
def import_pub_els():
    data = pd.read_csv(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\pub_top_virus_taxname_redo\NIH_taxid_pubmed_Virus_Pub.csv')
    df = pd.DataFrame(data, columns=['tax_id','tax_name','year','pubmed'])
    return df

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

# takes a list of years (df's), determines top countries over those years for a virus
# pass one virus name from main to get specific viruses
# pass a timeframe (eg 2005 - 2011)
# n is the number of countries printed
def discover_top_countries(years_list, n):
    top_names_out = []
    top_names_dict = {}

    for i in range(len(years_list)):
        for j in range(len(years_list[i]["journal"].array)):
            # if key in dictionary, add its frequency to the existing value
            if ((years_list[i]["journal"].array[j]) in top_names_dict):
                top_names_dict[years_list[i]["journal"].array[j]] += 1
            # else, add key and its existing value to dictionary
            else:
                top_names_dict[years_list[i]["journal"].array[j]] = 1

    top_names_dict = sorted(top_names_dict.items(), key=lambda x: x[1], reverse=True)
    count = 0
    for key, value in top_names_dict:
        print(key + " : " + str(value))
        count += 1
        top_names_out.append(key)
        if count >= n:
            break

    return top_names_out  # of length n - total virus names in sub and pub

# finds author affiliation (country, etc) of each member of the pub net,
# returns top countries (by calling disc_top_c's on the one-long list of pub data
def pubmed_analyzer(df):
    journal_array = []
    # for i in range(len(df["pubmed"].array)):
    for i in range(50):
        pmedIn = math.trunc(df["pubmed"].array[i])
        pmedIn = str(pmedIn)
        url = "http://www.ncbi.nlm.nih.gov/pubmed/" + pmedIn
        lookup = PubMedLookup(url, '')
        # print(lookup)
        publication = Publication(lookup)
        print(publication.cite())
        #journal_array.append(publication.journal)

    print(journal_array)
    return journal_array

# takes a dataframe (of 1 year of data) & a list of names, trimming the dataframe to only include
# entries for the specified viruses
# called by lister
def sub_virus_name_binder(df, top_vir_list):
    top_vir_namesIN = {'journal': [],
                       'tax_name': []
                       }
    top_vir_names_df = pd.DataFrame(top_vir_namesIN, columns= ['journal', 'tax_name'])
    for i in range(len(top_vir_list)):
        # looks for 1 virus after another on the whole column of viruses
        top_vir = df.loc[df['tax_name'] == top_vir_list[i]]
        top_vir_names_df = top_vir_names_df.append(top_vir)

    return top_vir_names_df  # return df with only the top n virus freqs

def pub_virus_name_binder(df, top_vir_list):
    top_vir_namesIN = {'tax_id': [],
                       'tax_name': [],
                       'year': [],
                       'pubmed': []
                       }
    top_vir_names_df = pd.DataFrame(top_vir_namesIN, columns=['tax_id','tax_name','year','pubmed'])
    for i in range(len(top_vir_list)):
        # looks for 1 virus after another on the whole column of viruses
        top_vir = df.loc[df['tax_name'] == top_vir_list[i]]
        top_vir_names_df = top_vir_names_df.append(top_vir)

    # print(top_vir_names_df)
    # top_vir_names_df.to_excel(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\results\author_country_extraction\pub_net\pubmeds.xlsx', index=False, header=True)
    return top_vir_names_df # return df with only the top n virus freqs


# FUNC: takes sub list and calls the binder function on each element, returning sub list with just desired virus data
# one DF = 1 year
def sub_el_lister(sub_el_list, top_vir_list):
    new_el_list = []
    year = 1992
    for i in range(len(sub_el_list)):
        new_df = sub_virus_name_binder(sub_el_list[i], top_vir_list)
        new_df = parse_country_from_dataframe(new_df)
        new_el_list.append(new_df)
        # print(str(year), new_df)
        year += 1

    # desired virus passed from main
    # list markers: 1992 = 0, 2018 = 27
    # 2000 = 9, 2010 = 19
    # print("Top 10 countries working on Zika virus, 2015-2017 worldwide outbreak")
    # discover_top_countries(new_el_list[24:26],10)
    return new_el_list


if __name__ == '__main__':
    top_virus_list = ["Human immunodeficiency virus 1", "Dengue virus 2", "Dengue virus 1",
                      "Dengue virus 3", "West Nile virus", "Zika virus"]
    top_virus_list_TEST = ["Human immunodeficiency virus 1"]

    sub_els_list = import_sub_els()
    pub_els = import_pub_els()
    # pass virus name / names here for specific ones (top virus test)
    trimmed_sub_el_list = sub_el_lister(sub_els_list, top_virus_list)
    trimmed_pub_el_list = pub_virus_name_binder(pub_els, top_virus_list)
    # journal_array = pubmed_analyzer(trimmed_pub_el_list)
    # print(journal_array)
