import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import imp
import Models
from sklearn.cross_validation import train_test_split

def convertCategoricalVaribalesToNumEncoding(data,columns):
    for column in columns:        
        data[column] = data[column].astype("category").cat.codes
    
    return data
    
def convertCategoricalVaribalesToOneHotEncoding(data,columns):
    for column in columns:        
        dummyCol = column.replace(" ","_") + "_"                
        cat_list = pd.get_dummies(data[column], prefix=dummyCol)
        data=pd.concat([data,cat_list], axis = 1)
    
    data.drop(columns,axis = 1,inplace = True)
    return data

data = pd.read_csv("./data/data.csv")
data.drop(["Id"],inplace = True, axis = 1)
data = convertCategoricalVaribalesToNumEncoding(data,["Churn","Area code","International plan","Voice mail plan"])
data = convertCategoricalVaribalesToOneHotEncoding(data,["State"])

#---------Split dataset into train and test
train_x, test_x, train_y, test_y = train_test_split(data.loc[:,data.columns !="Churn"]
                    ,data.loc[:,data.columns =="Churn"]
                    ,test_size=0.30
                    , random_state=42)


from sklearn.tree import DecisionTreeClassifier
from sklearn. model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import xgboost as xgb

"""
params = {
        'n_estimators' : [x for x in range(100,501,100)]
        ,'max_depth' : [6,7,8,9,10]
        }
"""
    
"""
model = xgb.XGBClassifier(
              objective = 'binary:logistic'
              ,early_stopping_rounds  = 5
              ,booster = 'gbtree'
              ,learning_rate = 0.1
              ,max_depth = 8
              ,colsample_bytree = .9
              ,n_estimators = 100
              ,subsample = 0.8
              )
"""
model = DecisionTreeClassifier(class_weight = "balanced"
                               ,max_depth = 6
                               ,min_samples_split = 8
                               ,random_state = 6)

model.fit(train_x,train_y)
result = model.predict(test_x)

accuracy_score(test_y,result)
print(classification_report(test_y,result))

"""
clf = GridSearchCV(model, params
                   , scoring = "recall"
                   , cv = 5
                   ,n_jobs = 5)
clf.fit(train_x,train_y)

clf.grid_scores_, clf.best_params_, clf.best_score_
"""
 
FeatureImpDF = pd.DataFrame({"Name":data.columns[0:69],"Score":model.feature_importances_ })
sns.barplot(y = 'Name', x = 'Score' , data = FeatureImpDF.loc[FeatureImpDF['Score'] >0,:].sort_values('Score'))


#---------------Models


