# IMPLICIT SEXUAL DISCRIMINATION
## DESCRIPTION
I use the Harvard test IAT to explore potential predictors of implicit sexual discrimination. The IAT association test is a cognitive test used to measure implicit discrimination through associatons (e.g.: associate good/bad inputs with gay/straight inputs) as time reactions. For a deeper explanation, click here
RESEARCH QUESTION
Which individual characteristics predict implicit sexual discrimination? The IAT tests asks the respondents to fill some information about their believes, politics orientations, explicit discrimination and so on. I use these information to predict the measure of implicit discrimination (time reaction to the association test).
(Unfortunatly, the target variables is already standardized, so it's not possible to see how much it really consists of in terms of milliseconds).

## HOW:
I will use:
2021 DATASET AS TRAINING DATA
2020 DATASET AS TEST SET Data found at this link

### FILES: 
- data_prep: data cleaning and data preparation
- data_modeling: EDA and ML modeling
- Sexuality_IAT.public.2020.sav and Sexuality_IAT.public.2021.sav: row data
- df_ready: data cleaned (ready for modeling)
- docs_files contains information on the variables
- img: contains the images of the results

## Results
First exploratory analysis shows the potential predictors of implicit sexual discrimination. 

[<img src="https://github.com/tommella90/Predicting-sexual-discrimination/blob/main/img/ols_coeff.png" width="500" height="400">](https://github.com/tommella90/Tommy_Portfolio) [<img src="https://github.com/tommella90/Predicting-sexual-discrimination/blob/main/img/ols_coeff_ci.png" width="500" height="400">](https://github.com/tommella90/Tommy_Portfolio)
Variables that significantly predict implicit sexual discrimination are:

:heavy_plus_sign: Preference for straight people (surprisingly :P), being religious

:heavy_minus_sign: Age, education, liberal political view (vs conservative)

In terms of prediction, the maximum R2 reached is .35. Considering the volatily of the variables considered, it's not so bad. 

[<img src="https://github.com/tommella90/Predicting-sexual-discrimination/blob/main/img/r2.png" width="500" height="400">](https://github.com/tommella90/Tommy_Portfolio) [<img src="https://github.com/tommella90/Predicting-sexual-discrimination/blob/main/img/prediction.png" width="500" height="400">](https://github.com/tommella90/Tommy_Portfolio)

