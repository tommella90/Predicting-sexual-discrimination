## import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

#%%
"""
df = pd.read_spss('Sexuality_IAT.public.2020.sav')
df = df.sample(frac=.1).reset_index(drop=True)
df.to_csv('sex_temp.csv')
"""

#%%
df = pd.read_csv('sex_temp.csv')
print('d')

#%% DROP IF TOO MANY MISSINGS
## keep if at least 3/4 of the data is not misssing
missing = df.isna().sum()
missing = missing.sort_values(ascending=False)
#fig = missing.plot(kind='bar', figsize=(10, 5))
treshold = len(df)/2.4
missing = missing[missing < treshold]
df = df[missing.index]

## keep only variables of interest
columns = ['weekday', 'birthyear', 'num_002', 'birthSex', 'genderIdentity',
             'sexuality_5', 'ethnicityomb', 'raceomb_002', 'D_biep.Straight_Good_all',
             'Mn_RT_all_3467', 'PCT_error_3467', 'Side_Good_34', 'Side_Straight_34',
             'Tgayleswomen', 'Tgaymen', 'Tstraightmen', 'Tstraightwomen', 'att_7',
             'contactfamily_num', 'contactfriend_num', 'contactfriendly_num',
             'contactmet_num', 'adoptchild', 'marriagerights_3num',
             'relationslegal_3num', 'serverights', 'transgender', 'countrycit_num',
             'edu', 'edu_14', 'politicalid_7', 'occuSelf',
             'religion2014', 'religionid']

df = df[columns]
df.columns = df.columns.str.lower()
## RENAME COLUMNS
df.rename(columns = {"d_biep.straight_good_all": "iat",
                     "birthyear": "y_birth",
                     "att_7": "prefer_straight",
                     "politicalid_7": "liberal",
                     "religionid": "religious",
                     "genderidentity": "gn_id",
                     "side_straight_34": "straight_first",
                     'contactfamily_num': "fam. member",
                     'contactfriend_num': "friend",
                     'contactfriendly_num': "friendly",
                     'contactmet_num': "met gay",
                     'adoptchild': "adoption",
                     'marriagerights_3num': "marriage",
                     'relationslegal_3num': "relation",
                     'serverights': "work"},
          inplace=True)

#%% Keep only those who do the test for the first time
df['num_002'].unique()
df = df.loc[df['num_002'] == str(1)]
df.drop(['num_002'], axis = 1, inplace = True)

#%%
## Transform string to integer
def KeepNumber(col):
    col = col.str.extract('(\d+)')
    return col

num = ['tgayleswomen', 'tgaymen', 'tstraightmen', 'tstraightwomen']
for i in num:
    df[i] = KeepNumber(df[i])

df[num] = df[num].apply(pd.to_numeric)



#%%
correlation = df[num]
correlation = correlation.astype(float).dropna()
correlation = correlation.corr()
sns.heatmap(correlation,cbar=True,square=True,fmt='.1f',annot=True,annot_kws={'size':8},cmap="Blues")


#%%
## Generate row means of variables (might add pca)
def row_mean(subset, sample):
    newcol = subset.sum(axis=1) / sample
    return newcol

## gender feeling: being confortable with gay people
df['gender_feel'] = row_mean(df.loc[:, ['tgayleswomen', 'tgaymen', 'tstraightmen', 'tstraightwomen']], 4)

## gender prejudice: explicit gendere prejudice
#df['gender_preg'] = row_mean(df.loc[:, ['adoptchild', 'marriagerights_3num', 'relationslegal_3num',
#                                    'serverights', 'transgender', 'countrycit_num']], 6)

#df['gender_feel'] = df['gender_feel'].astype(float)


#%%
## Var: Sex assignet at birth
def CleanBirthSex(col):
    col = col.replace({1: "Male", 2: "Female"},
                      inplace = True)
    return col

CleanBirthSex(df['birthsex'])

#%%
## RE-CATEGORIZE VARIABLES VALUES AND CLEAN
## Transform gender identity to dummy: binary/non binary
df['gn_id'].replace({'[1]':'M', '[2]':'F', '[3]': 'Trans_M',
                     '[4]': 'Trans_F', '[5]': 'queer', '[6]': 'other',
                     '1':'M', '2':'F', '3': 'Trans_M',
                     '4': 'Trans_F', '5': 'queer', '6': 'other', "": np.nan },
                    inplace=True)
list(df['gn_id'].unique())
#%%

#%%

df['gn_id'] = df['gn_id'].str.replace('[', '', regex=True)
df['gn_id'] = df['gn_id'].str.replace(']', '', regex=True)
df['gn_id'] = df['gn_id'].str.replace(',', '', regex=True)
df['straight_identity'] = 1 if "1" or "2" in df['gn_id'] else 0
df['transgender'] = 1 if "3" or "4" in df['gn_id'] else 0
df['transgender'] = 1 if "5" in df['gn_id'] else 0

#%%
## Var: sexuality to dummy: Straight/non Straight
df.sexuality_5.unique()
def Sexuality(col):
    col.replace({'Heterosexual or Straight': 'Yes',
                 'Bisexual':'No',
                 'Other': 'No',
                 'Lesbian or Gay': 'No'},
                inplace=True)
    return col

df['sexuality_5'] = Sexuality(df['sexuality_5'])
df.rename(columns={'sexuality_5': 'straight'}, inplace=True)

#%%
## Var: Attitude towards gay people at work (Against or not)
df.work.unique()
def CleanWork(col):
    col.replace({'Should not be legal': 'Against',
                 'Should be legal':'Pro/neutral',
                 'No opinion': 'Pro/neutral'},
                inplace=True)
    return col
df['work'] = CleanWork(df['work'])

#%%
## Var: Trans people should use bathroom rooms of sex assigner at birth: against or not
df.transgender.unique()

def CleanTransgender(col):
    col.replace({'Transgender people should use the bathroom/locker rooms of the sex they were assigned '
                 'at birth': 'Against',
                 'Transgender people should use the bathrooms/locker rooms of their preferred gender identity':'Pro'},
                inplace=True)
    return col
df['transgender'] = CleanTransgender(df['transgender'])


#%%
## Var: Marriage between gay people: Against or not
df.marriage.unique()
def CleanMarriage(col):
    col.replace({'Should not be valid': 'Against',
                 'Should be valid': 'Pro/neutral',
                 'No opinion': 'Pro/neutral'},
                inplace=True)
    return col
df['marriage'] = CleanMarriage(df['marriage'])

#%%
## Var: Adoption for gay people: Against or not
def CleanAdoption(col):
    col.replace({'Should not be legal': 'Against',
                 'Should be legal': 'Pro/neutral',
                 'No opinion': 'Pro/neutral'},
                inplace=True)
    return col
df['adoption'] = CleanAdoption(df['adoption'])

#%%
## Var: Relation between gay people: Against or not
def CleanRelation(col):
    col.replace({'Should not be legal': 'Against',
                 'Should be legal': 'Pro/neutral',
                 'No opinion': 'Pro/neutral'},
                inplace=True)
    return col
df['relation'] = CleanRelation(df['relation'])

#%%
def CleanRace(col):
    col = col.replace({'American Indian/Alaska Native': 'Other or unknown',
                       'Native Hawaiian or other Pacific Islander':'Other or unknown'})
    return col
df['raceomb_002'] = CleanRace(df['raceomb_002'])
df.rename(columns={'raceomb_002': 'race'}, inplace=True)


#%%
## Var: Prefer gay or straight people (numerical)
def CleanPrefStraight(col):
    col = col.replace({'I strongly prefer Straight People to Gay People.': 7,
                       'I moderately prefer Straight People to Gay People.': 6,
                       'I slightly prefer Straight People to Gay People.': 5,
                       'I like Straight People and Gay People equally.': 4,
                       'I slightly prefer Gay People to Straight People.': 3,
                       'I moderately prefer Gay People to Straight People.': 2,
                       'I strongly prefer Gay People to Straight People.': 1}
                      )
    return col
df['prefer_straight'] = CleanPrefStraight(df['prefer_straight'])

#%%
## Var: Political orientation: Liberal vs Conservative (numerical)
def CleanPolitics(col):
    col = col.replace({'strongly liberal': 7,
                       'moderately liberal': 6,
                       'slightly liberal': 5,
                       'neutral': 4,
                       'slightly conservative': 3,
                       'moderately conservative': 2,
                       'strongly conservative': 1}
                      )
    return col
df['liberal'] = CleanPolitics(df['liberal'])
df['liberal'] = df['liberal'].astype('float32')

#%%
## Var: Religious (numerical)
def CleanReligion(col):
    col = col.replace({'strongly religious': 4,
                       'moderately religious': 3,
                       'slightly religious': 2,
                       'not at all religious': 1}
                      )
    return col
df['religious'] = CleanReligion(df['religious'])
df['religious'] = df['religious'].astype('float32')

#%%
## Choose final columns
final_columns = ['y_birth', 'birthsex', 'gn_id', 'straight', 'race', 'iat', 'straight_first',
                 'prefer_straight', 'fam. member', 'friend', 'friendly',
                 'met gay', 'edu', 'liberal', 'religious', 'gender_feel',
                 "adoption", "marriage", "relation", "work", "transgender", 'straight_identity']

df = df[final_columns]
df = df.loc[df['iat'].isnull() == False]

#
#%%
numerical = ['y_birth', 'iat', 'edu', 'liberal',
             'religious', 'gender_feel', 'prefer_straight']
df_numerical = df[numerical]

categorical = ['race', 'fam. member', 'friend', 'straight_first', 'straight',
               'birthsex', 'friendly', 'met gay',
               'adoption', 'marriage', 'relation', 'work', 'transgender']
df_categorical = df[categorical]


#%%
categories = pd.get_dummies(df_categorical, drop_first=True)
df = pd.concat([df_numerical, categories], axis=1)

#%%
df.to_excel("cleaned_data.xlsx")
print('done')

#%%
df.columns
#%%
