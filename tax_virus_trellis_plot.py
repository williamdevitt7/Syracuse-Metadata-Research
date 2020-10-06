####################################################################################
# Python program
# for plotting virus data via Trellis plot
# Sep 18, 2020
# two lines: orange / blue = sub_virus / pub_virus
# todo: so: function that finds the top virus names
# todo: scale out aggregator to handle every year, not just 2016-2018 subset I made manually, from 92-18
# todo: handle years that have no
#####################################################################################

# imports and declarations
import pandas as pd
from matplotlib import pyplot as plt

# sub-virus csv imports
def import_sub_virus():
    count = 1992
    sub_virus_list = []
    for i in range(26):
        data = pd.read_csv(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\sub_virus\top_virus_name\sub_top-virus_taxname' + str(count) + '.csv')
        df = pd.DataFrame(data, columns=['Var1','Freq'])
        df.rename(columns={'Freq': 'sub_freq'}, inplace=True)
        sub_virus_list.append(df)
        count += 1
    return sub_virus_list

# pub-virus csv imports
def import_pub_virus():
    count = 1992
    pub_virus_list = []
    for i in range(26):
        data = pd.read_csv(r'C:\Users\Will\OneDrive\Documents\CollabNet_Research\Taxonomy_Virus_Data\Taxonomy_Network_Analysis\pub_virus\top_virus_name\pub_top-virus_taxname' + str(count) + '.csv')
        df = pd.DataFrame(data, columns=['Var1','Freq'])
        df.rename(columns={'Freq': 'pub_freq'}, inplace=True)
        pub_virus_list.append(df)
        count += 1
    return pub_virus_list

########################################################################################

# FUNC: finding top virus names (iterate thru, count occurences of names by year and total)
# maybe call this explicitly on certain years (pass n parameter that determines either specific year or # of times run)
# operates in O(N) time
def discover_top_names(sub_vl, pub_vl, n):
    sub_dict = {}
    pub_dict = {}
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
        print(key + " : ", end='')
        print(value)
        count += 1
        top_names_out.append(key)
        if count > n:
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

    return top_vir_names_df  # return df with only the top 10 virus names' frequencies

def pub_top_name_binder(df, top_names_list):
    top_vir_namesIN = {'Var1': [],
                     'pub_freq': []
                     }
    top_vir_names_df = pd.DataFrame(top_vir_namesIN, columns= ['Var1', 'pub_freq'])
    for i in range(len(top_names_list)):
        top_vir = df.loc[df['Var1'] == top_names_list[i]]
        top_vir_names_df = top_vir_names_df.append(top_vir)

    return top_vir_names_df  # return df with only the top 10 virus names' frequencies

# FUNC: takes sub and pub lists and calls the above function on each element, returning sub and pub lists with the same virus names on each
def new_sub_lister(sub_vl, top_names_list):
    new_sub_vl = []
    for i in range(26):
        new_df = sub_top_name_binder(sub_vl[i], top_names_list)
        new_sub_vl.append(new_df)

    return new_sub_vl

def new_pub_lister(pub_vl, top_names_list):
    new_pub_vl = []
    for i in range(26):
        new_df = pub_top_name_binder(pub_vl[i], top_names_list)
        new_pub_vl.append(new_df)

    return new_pub_vl

# FUNC: takes any 3 dataframes (with the same virus names, of length 10) and returns one dataframe with the frequencies averaged
def sub_triple_df_agg(df, df1, df2):
    # problem: when virus names arent found!
    # expand to handle list of 10 rather than 3
    df.reset_index(inplace=True, drop=True)
    df1.reset_index(inplace=True, drop=True)
    df2.reset_index(inplace=True, drop=True)
    a = df['sub_freq']
    col1 = df['Var1']
    b = df1['sub_freq']
    c = df2['sub_freq']
    a_v_a = []  # array of the average values
    for i in range(4):  # expand to 10, this averages each freq per name across rows
        a_v_a.append((a[i] + b[i] + c[i]) / 3)

    out_d = {'Var1':[col1[0], col1[1], col1[2], col1[3]], 'sub_freq':[a_v_a[0], a_v_a[1], a_v_a[2], a_v_a[3]]}  # add ava and var1 vals till 10
    out_df = pd.DataFrame(out_d)
    #print(out_df)

    return out_df  # return avg df

def pub_triple_df_agg(df, df1, df2):
    # problem: when virus names arent found!
    # expand to handle list of 10 rather than 3
    df.reset_index(inplace=True, drop=True)
    df1.reset_index(inplace=True, drop=True)
    df2.reset_index(inplace=True, drop=True)
    a = df['pub_freq']
    col1 = df['Var1']
    b = df1['pub_freq']
    c = df2['pub_freq']
    a_v_a = []  # array of the average values (each index holds a
    for i in range(4):  # expand to 10
        a_v_a.append((a[i] + b[i] + c[i]) / 3)

    out_d = {'Var1': [col1[0], col1[1], col1[2], col1[3]], 'pub_freq': [a_v_a[0], a_v_a[1], a_v_a[2], a_v_a[3]]}  # expand up to 10
    out_df = pd.DataFrame(out_d)
    #print(out_df)

    return out_df  # return avg df

# FUNC: calls triple_df, runs thru new sub and pub list, passes 3 dataframes, aggregates and returns sub and pub lists of 9 dataframes covering 3 year spans each
def new_subvl_final(new_sub_vl):
    # if you don't call triple df, all you need is the new sub and pub lists!
    sub_vl_final = []  # list of 9 df's aggd and averaged
    count = 0
    sub_vl_final.append(sub_triple_df_agg(new_sub_vl[23], new_sub_vl[24], new_sub_vl[25]))
    #for i in range(9):
     #   sub_vl_final.append(sub_triple_df_agg(new_sub_vl[count], new_sub_vl[count+1], new_sub_vl[count+2]))

    return sub_vl_final

def new_pubvl_final(new_pub_vl):
    pub_vl_final = []  # list of 9 df's aggd and averaged
    count = 0
    pub_vl_final.append(pub_triple_df_agg(new_pub_vl[23], new_pub_vl[24], new_pub_vl[25]))

    #for i in range(9):
     #   pub_triple_df_agg(new_pub_vl[23], new_pub_vl[24], new_pub_vl[25])

    return pub_vl_final

#######################################################################################

def plot_and_display(sub_vl, pub_vl): # takes final sub and pub of 9 3yr aggs each and plots them
    # take sub_vl and pub_vl from new_subvl_final, new_pubvl_final (size 9 each)
    # 3x3 subplots, 92-94, 95-97, 98-00, 01-03, 04-06, 07-09, 10-12, 13-15, 16-18
    #fig, ax = plt.subplots(3, 3, sharex='col', sharey='row') #what to do for trellis
    #plt.show()
    plt.winter()
    plt.plot('Var1', 'sub_freq', '--ok', lw=0.3, ms=1, aa=True, data=sub_vl[6])  # sub = black line
    plt.plot('Var1', 'pub_freq', '--or', lw=0.3, ms=1, aa=True, data=pub_vl[6])  # pub = magenta line
    #plt.xticks(rotation=90)
    #plt.tight_layout()
    #plt.xlim(-0.1, 28)
    #plt.ylim(-80, 3500)
    #plt.xlabel("Virus Name")
    plt.ylabel("Frequency")
    plt.title("Year: 1997")
    plt.legend()

    plt.show()

#######################################################################################

if __name__ == '__main__': # execute code / main
    sub_virus_list = import_sub_virus() # list of all .csv files for sub_virus
    pub_virus_list = import_pub_virus() # list of all .csv files for pub_virus
    top_virus_list = discover_top_names(sub_virus_list, pub_virus_list, 4)
    new_sub_vl = new_sub_lister(sub_virus_list, top_virus_list)
    new_pub_vl = new_pub_lister(pub_virus_list, top_virus_list)
    #sub_vl_TOGRAPH = new_subvl_final(new_sub_vl)  # pass these to plot_n_d
    #pub_vl_TOGRAPH = new_pubvl_final(new_pub_vl)

    #plot_and_display(new_sub_vl, new_pub_vl)
    #plot_and_display(sub_vl_TOGRAPH, pub_vl_TOGRAPH)



