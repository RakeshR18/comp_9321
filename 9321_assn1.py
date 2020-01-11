# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:32:39 2019

@author: HP
"""

import pandas as pd
import matplotlib.pyplot as plt


def question_1():
    dataset_1 = pd.read_csv('Olympics_dataset1.csv')
    dataset_2 = pd.read_csv('Olympics_dataset2.csv')
    
    dataset_1 = dataset_1.drop(dataset_1.index[0])
    dataset_2 = dataset_2.drop(dataset_2.index[0])
    
    df = pd.merge(dataset_1,dataset_2, on ='Team',how = 'inner')
    
    columns_to_use = ['Country', 'summer_rubbish', 'summer_participation', 'summer_gold',
                      'summer_silver', 'summer_bronze', 'summer_total', 'winter_participation',
                      'winter_gold', 'winter_silver', 'winter_bronze', 'winter_total']
    
    new_df = df[df.columns[0:len(columns_to_use)]]
    new_df.columns = columns_to_use
    
    final_df = new_df[new_df.Country != 'Totals']
    print(final_df.head(5).to_string)
    return final_df


def question_2(final_df):
    
    final_df['Country'] = final_df['Country'].str.replace(r"[\(\[].*?[\)\]]","").str.strip()
    final_df.index = final_df['Country']
    
    drop_columns = ['summer_rubbish', 'summer_total' , 'winter_total']
    final_df.drop(drop_columns, inplace=True, axis=1)
    
    print(final_df.head(5).to_string())
    return final_df


def question_3(question_3_df):
    
    question_3_df = question_3_df.dropna()
    print(question_3_df.tail(10).to_string())
    return question_3_df

def question_4(question_4_df):
    
    summer_gold = question_4_df['summer_gold'].tolist()
    
    summer_gold = list(map(lambda x: x.replace(',',''), summer_gold))
    question_4_df['summer_gold'] = summer_gold
    
    question_4_df = question_4_df.astype({"summer_gold": int, "winter_gold": int,"summer_silver":int,
                                "summer_bronze":int,"winter_silver":int,"winter_bronze":int,
                               "summer_participation":int,"winter_participation":int})
    
    most_summer_gold = question_4_df.index[question_4_df['summer_gold'] == question_4_df['summer_gold'].max()].tolist()
    
    print("\n".join([str(x) for x in most_summer_gold]))
    return question_4_df

def question_5(question_4_df):
    summer_minus_winter = question_4_df.copy()

    summer_minus_winter['summer_winter'] = abs(summer_minus_winter['summer_gold'] - summer_minus_winter['winter_gold'])
    
    summer_minus_winter['(Country,difference)'] = summer_minus_winter[['Country','summer_winter']].apply(tuple, axis=1)
    
    most_difference = summer_minus_winter['(Country,difference)'][summer_minus_winter.summer_winter == summer_minus_winter.summer_winter.max()].tolist()
    
    print("\n".join([str(x) for x in most_difference]))


def question_6(question_4_df):
    Total_medals = question_4_df.copy()

    Total_medals['winter_medals'] = Total_medals['winter_silver'] + Total_medals['winter_bronze'] + Total_medals['winter_gold']
    Total_medals['summer_medals'] = Total_medals['summer_gold'] + Total_medals['summer_silver'] + Total_medals['summer_bronze']
    
    Total_medals['Total_medals'] = Total_medals['summer_medals'] + Total_medals['winter_medals']
    
    descending_df = Total_medals.sort_values(['Total_medals'],ascending = [False])
    
    print(descending_df.head(5).to_string())
    return descending_df



def question_7(descending_df):
    
    top_10_countries = descending_df['Country'].head(10).tolist()
    winter_medals = descending_df['winter_medals'].head(10).tolist()
    summer_medals = descending_df['summer_medals'].head(10).tolist()
    
    
    top_10_countries = list(map(lambda x: x.strip() , top_10_countries))
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.barh(top_10_countries, summer_medals, align='center', height=.75, color='b',label='summer_medals')
    ax.barh(top_10_countries, winter_medals, align='center', height=.75, left=summer_medals, color='g',label='winter_medals')
    ax.set_yticks(top_10_countries)
    
    ax.set_title('Medals for winter and summer games')
    ax.xaxis.grid(True)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), ncol=2)
    plt.tight_layout()
    
    plt.show()


def question_8(question_4_df):
    
    subset_df = question_4_df[question_4_df['Country'].isin (['United States','Australia','Great Britain', 'Japan', 'New Zealand'])]

    countries = subset_df['Country'].tolist()
    winter_gold = subset_df['winter_gold'].tolist()
    winter_silver = subset_df['winter_silver'].tolist()
    winter_bronze = subset_df['winter_bronze'].tolist()
    
    bar_width = 0.3
    
    r1 = [x for x in range(len(winter_gold))]
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    
    plt.bar(r1, winter_gold, color='b', width=bar_width, edgecolor='white', label='Gold')
    plt.bar(r2, winter_silver, color='g', width=bar_width, edgecolor='white', label='Silver')
    plt.bar(r3, winter_bronze, color='c', width=bar_width, edgecolor='white', label='Bronze')
    
    
    plt.xticks([r + bar_width for r in range(len(winter_gold))], countries)
    
    plt.title('Winter Games')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07), ncol=3)
    
    plt.show

def summer_ranking_scheme(row):
    if row['summer_participation'] == 0:
        return 0
    else:
        scheme = (row['summer_gold'] *5 + row['summer_silver'] *3 + row['summer_bronze'] *1)/(row['summer_participation'])
        return scheme

def question_9(question_4_df):
    

    question_9_df = question_4_df.copy()
    
    question_9_df['Ranking_scheme_summer'] = question_9_df.apply(summer_ranking_scheme,axis = 1)
    
    question_9_df = question_9_df.sort_values(['Ranking_scheme_summer'], ascending = [False])
    
    print(question_9_df.head(5).to_string())
    return question_9_df

def winter_ranking_scheme(row):
    if row['winter_participation'] == 0:
        return 0
    else:
        scheme = (row['winter_gold'] *5 + row['winter_silver'] *3 + row['winter_bronze'] *1)/(row['winter_participation'])
        return scheme

def question_10(question_9_df):
    q_10 = question_9_df.copy()
    
    q_10['Ranking_scheme_winter'] = q_10.apply(winter_ranking_scheme,axis = 1)
    continent_df = pd.read_csv('Countries-Continents.csv')
    q_10.reset_index(drop=True,inplace=True)
    new_df = pd.merge(continent_df,q_10,on='Country',how='right')
    
    new_df['Continent'] = new_df['Continent'].fillna('None')
    
    df_Asia = new_df.query('Continent == "Asia"')
    df_Africa = new_df.query('Continent == "Africa"')
    df_northAm = new_df.query('Continent == "North America"')
    df_southAm = new_df.query('Continent == "South America"')
    df_europe = new_df.query('Continent == "Europe"')
    df_oceania = new_df.query('Continent == "Oceania"')
    df_None = new_df.query('Continent == "None"')
    
    
    ax = df_Asia.plot.scatter(x='Ranking_scheme_summer', y='Ranking_scheme_winter', label='Asia',color = 'green')
    ax = df_Africa.plot.scatter(x='Ranking_scheme_summer', y='Ranking_scheme_winter', label='Africa',color = 'red',ax=ax)
    ax = df_northAm.plot.scatter(x='Ranking_scheme_summer', y='Ranking_scheme_winter', label='North America',color = 'blue',ax=ax)
    ax = df_southAm.plot.scatter(x='Ranking_scheme_summer', y='Ranking_scheme_winter', label='South America',color = 'cyan',ax=ax)
    ax = df_europe.plot.scatter(x='Ranking_scheme_summer', y='Ranking_scheme_winter', label='Europe',color = 'yellow',ax=ax)
    ax = df_oceania.plot.scatter(x='Ranking_scheme_summer', y='Ranking_scheme_winter', label='Oceania',color = 'black',ax=ax)
    ax = df_None.plot.scatter(x='Ranking_scheme_summer', y='Ranking_scheme_winter', label='None',color = 'grey',ax=ax)
    plt.show()  
    
    


if __name__ == "__main__":
    question_1_df = question_1()
    question_2_df = question_2(question_1_df)
    question_3_df = question_3(question_2_df)
    question_4_df = question_4(question_3_df)
    question_5(question_4_df)
    question_6_df = question_6(question_4_df)
    question_7(question_6_df)
    question_8(question_4_df)
    question_9_df = question_9(question_4_df)
    question_10(question_9_df)