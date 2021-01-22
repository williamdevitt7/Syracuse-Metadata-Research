####################################################################################
# Python program for extracting virus research information from NIH data
# 1/22/2021
# Returns most common viruses over our time period,
# as well as returns counts of papers on those viruses from any specific year
# with a given list of virus names.
#####################################################################################

# imports and declarations
import pandas as pd
import matplotlib as plt

# sub-virus csv imports
def import_sub_virus():
    count = 1992
    sub_virus_list = []
    for i in range(27):
        data = pd.read_csv(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\sub_top_virus_taxname_redo\sub_top_virus_taxname_redo\sub_top-virus_taxname' + str(count) + '.csv')
        df = pd.DataFrame(data, columns=['Var1','Freq'])
        df.rename(columns={'Freq': 'sub_freq'}, inplace=True)
        sub_virus_list.append(df)
        count += 1
    return sub_virus_list

# pub-virus csv imports
def import_pub_virus():
    count = 1992
    pub_virus_list = []
    for i in range(27):
        data = pd.read_csv(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\pub_top_virus_taxname_redo\pub_top_virus_taxname_redo\pub_top-virus_taxname' + str(count) + '.csv')
        df = pd.DataFrame(data, columns=['Var1','Freq'])
        df.rename(columns={'Freq': 'pub_freq'}, inplace=True)
        pub_virus_list.append(df)
        count += 1
    return pub_virus_list

def import_top_vir_cts():
    data = pd.read_csv('top_virus_cts.csv')
    df = pd.DataFrame(data, columns=['year','virus','sub_count','pub_count','total_count'])
    #print(df)

    return df

########################################################################################

# FUNC: finding top virus names (iterate thru, count occurences of names by year and total)
# operates in O(N) time
# to get sub or pub only, pass an empty list for either sub_vl or pub_vl
# can be edited with simple changes to __main__
def discover_top_names(sub_vl, pub_vl, n):
    top_names_out = []
    top_names_dict = {}  # both

    # sub
    for i in range(len(sub_vl)):
        for j in range(len(sub_vl[i]["Var1"].array)):
            # if key in dictionary, add its frequency to the existing value
            if ((sub_vl[i]["Var1"].array[j]) in top_names_dict):
                top_names_dict[sub_vl[i]["Var1"].array[j]] += sub_vl[i]["sub_freq"].array[j]
            # else, add key and its existing value to dictionary
            else:
                top_names_dict[sub_vl[i]["Var1"].array[j]] = sub_vl[i]["sub_freq"].array[j]

    # pub
    for i in range(len(pub_vl)):
        for j in range(len(pub_vl[i]["Var1"].array)):
            if ((pub_vl[i]["Var1"].array[j]) in top_names_dict):
                top_names_dict[pub_vl[i]["Var1"].array[j]] += pub_vl[i]["pub_freq"].array[j]
            else:
                top_names_dict[pub_vl[i]["Var1"].array[j]] = pub_vl[i]["pub_freq"].array[j]

    top_names_dict = sorted(top_names_dict.items(), key=lambda x: x[1], reverse=True)
    count = 0
    for key, value in top_names_dict:
        #print(key + " : ", end='')
        #print(value)
        count += 1
        top_names_out.append(key)
        if count >= n:
            break

    return top_names_out  # of length n - total virus names in sub and pub

# FUNC: takes a dataframe (for a year) and the list of top_vir_names and returns a dataframe of the frequencies of each virus name, bound to virus names
def sub_top_name_binder(df, top_names_list):
    top_vir_namesIN = {'Var1': [],
                     'sub_freq': []
                     }
    top_vir_names_df = pd.DataFrame(top_vir_namesIN, columns= ['Var1', 'sub_freq'])
    for i in range(len(top_names_list)):
        top_vir = df.loc[df['Var1'] == top_names_list[i]]
        top_vir_names_df = top_vir_names_df.append(top_vir)

    return top_vir_names_df  # return df with only the top n virus names' frequencies

def pub_top_name_binder(df, top_names_list):
    top_vir_namesIN = {'Var1': [],
                     'pub_freq': []
                     }
    top_vir_names_df = pd.DataFrame(top_vir_namesIN, columns= ['Var1', 'pub_freq'])
    for i in range(len(top_names_list)):
        top_vir = df.loc[df['Var1'] == top_names_list[i]]
        top_vir_names_df = top_vir_names_df.append(top_vir)

    return top_vir_names_df  # return df with only the top n virus names' frequencies

# FUNC: takes sub and pub lists and calls the above function on each element, returning sub and pub lists with the same virus names on each
def new_sub_lister(sub_vl, top_names_list):
    new_sub_vl = []
    year = 1992
    for i in range(len(sub_vl)):
        new_df = sub_top_name_binder(sub_vl[i], top_names_list)
        new_sub_vl.append(new_df)
        print(str(year),new_df)
        year += 1

    return new_sub_vl

def new_pub_lister(pub_vl, top_names_list):
    new_pub_vl = []
    year = 1992
    for i in range(len(pub_vl)):
        new_df = pub_top_name_binder(pub_vl[i], top_names_list)
        new_pub_vl.append(new_df)
        print(str(year),new_df)
        year += 1

    return new_pub_vl

#######################################################################################

def plot_and_display(sub_vl, pub_vl, top_cts): # takes final sub and pub of 9 3yr aggs each and plots them
    # import my top virus counts file
    plt.winter()
    #print(top_cts)
    plt.plot('Var1', 'sub_freq', '--ok', lw=0.3, ms=1, aa=True, data=top_cts['sub_count'])  # sub = black line
    plt.plot('Var1', 'pub_freq', '--or', lw=0.3, ms=1, aa=True, data=top_cts['pub_count'])  # pub = magenta line
    plt.xticks(rotation=90)
    #plt.tight_layout()
    #plt.xlim(-0.1, 28)
    #plt.ylim(-80, 3500)
    #plt.xlabel("Virus Name")
    plt.ylabel("Frequency")
    plt.title("Year: 1997")
    plt.legend()

    #plt.show()

#######################################################################################

if __name__ == '__main__': # execute code / main
    sub_virus_list = import_sub_virus() # list of all .csv files for sub_virus
    pub_virus_list = import_pub_virus() # list of all .csv files for pub_virus
    top_vir_cts = import_top_vir_cts()
    #print(top_vir_cts)
    # n is the number of years desired in top virus names list
    top_virus_list = discover_top_names(sub_virus_list, pub_virus_list, 10)
    #pub_top_virus_list = discover_top_names([], pub_virus_list, 10)
    #sub_top_virus_list = discover_top_names(sub_virus_list, [], 10)
    new_sub_vl = new_sub_lister(sub_virus_list, top_virus_list)
    new_pub_vl = new_pub_lister(pub_virus_list, top_virus_list)
    #print(new_sub_vl)
    #print(new_pub_vl)

    #plot_and_display(new_sub_vl, new_pub_vl, top_vir_cts)


