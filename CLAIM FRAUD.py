
# coding: utf-8

# In[1]:


import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly import tools
from datetime import date
import pandas as pd
import numpy as np 
import seaborn as sns
import random 
import gc
import warnings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


gc.get_count()


# In[3]:


gc.collect() # forcefully removing unused memory
gc.get_count()


# In[4]:


import os
os.chdir("C:\\Users\\bunde\\OneDrive\\Desktop\\data scince with python\\Travelers")

train_df= pd.read_csv("uconn_comp_2018_train.csv", parse_dates=["claim_date"])
test_df= pd.read_csv("uconn_comp_2018_test.csv", parse_dates=["claim_date"])


# In[5]:


sns.countplot(x="fraud", data=train_df)


# In[6]:


#dropping row with fraud =-1
train_df = train_df[train_df['fraud']!= -1]


# In[7]:


import pandas_profiling as pp
pp.ProfileReport(train_df)


# In[8]:


# Gender vs Fraud
train_df.groupby(['gender','fraud'])['fraud'].count()
#Visualizing with graph
f,ax=plt.subplots(1,2,figsize=(18,8))
train_df[['gender','fraud']].groupby(['gender']).mean().plot.bar(ax=ax[0])
ax[0].set_title('fraud vs gender',fontsize='15')
sns.countplot('gender',hue='fraud',data=train_df,ax=ax[1])
ax[1].set_title('Sex',fontsize='15')
plt.show()


# In[9]:


#Marital status vs fraud
train_df.groupby(['marital_status','fraud'])['fraud'].count()
f,ax=plt.subplots(1,2,figsize=(18,8))
train_df[['marital_status','fraud']].groupby(['marital_status']).mean().plot.bar(ax=ax[0])
ax[0].set_title('fraud vs marriage',fontsize='15')
sns.countplot('marital_status',hue='fraud',data=train_df,ax=ax[1])
ax[1].set_title('Marriage',fontsize='15')
plt.show()


# In[10]:


f,ax=plt.subplots(1,2,figsize=(18,8))
train_df[['high_education_ind','fraud']].groupby(['high_education_ind']).mean().plot.bar(ax=ax[0])
ax[0].set_title('fraud vs high_education',fontsize='15')
sns.countplot('high_education_ind',hue='fraud',data=train_df,ax=ax[1])
ax[1].set_title('high_education',fontsize='15')
plt.show()


# In[11]:


f,ax=plt.subplots(1,2,figsize=(18,8))
train_df[['address_change_ind','fraud']].groupby(['address_change_ind']).mean().plot.bar(ax=ax[0])
ax[0].set_title('fraud vs address_change',fontsize='15')
sns.countplot('address_change_ind',hue='fraud',data=train_df,ax=ax[1])
ax[1].set_title('address_change',fontsize='15')
plt.show()


# In[12]:


f,ax=plt.subplots(1,2,figsize=(18,8))
train_df[['witness_present_ind','fraud']].groupby(['witness_present_ind']).mean().plot.bar(ax=ax[0])
ax[0].set_title('fraud vs witness_present',fontsize='15')
sns.countplot('witness_present_ind',hue='fraud',data=train_df,ax=ax[1])
ax[1].set_title('witness_present',fontsize='15')
plt.show()


# In[13]:


f,ax=plt.subplots(1,2,figsize=(18,8))
train_df[['past_num_of_claims','fraud']].groupby(['past_num_of_claims']).mean().plot.bar(ax=ax[0])
ax[0].set_title('fraud vs past_num_of_claims')
sns.countplot('past_num_of_claims',hue='fraud',data=train_df,ax=ax[1])
ax[1].set_title('past_num_of_claims')
plt.show()


# In[14]:


test_df['is_test'] = 1 
test_df['is_train'] = 0
train_df['is_test'] = 0
train_df['is_train'] = 1

# target variable
Y = train_df['fraud']
train_X = train_df

# test ID
test_id=test_df['claim_number']
test_X = test_df

# merge train and test datasets for preprocessing
data = pd.concat([train_X, test_X], axis=0)


# In[15]:


#checking percent of missing values  data
total1 = data.isnull().sum().sort_values(ascending = False)
percent1 = (data.isnull().sum()/data.count()*100).sort_values(ascending = False)
missing_data  = pd.concat([total1, percent1], axis=1, keys=['Total','Percent'])
missing_data.head()


# In[16]:


#Imputation of values
#Imputing marital_status with mode
from statistics import mode
data['marital_status']=train_df['marital_status'].fillna(mode(data['marital_status']))


# In[17]:


# Imputing claim_est_payout with mean
mean_value=data['claim_est_payout'].mean()
data['claim_est_payout']=data['claim_est_payout'].fillna(mean_value)
# Imputing witness_present_ind with mode
from statistics import mode
data['witness_present_ind']=data['witness_present_ind'].fillna(mode(data['witness_present_ind']))

#Imputing mean_age_value with mean
mean_value_age=data['age_of_vehicle'].median()

data['age_of_vehicle']=data['age_of_vehicle'].fillna(mean_value_age)


# In[18]:


data['zip_code'] = data['zip_code'].astype(str).str[:3]
data['zip_code'] = data['zip_code'].astype('object')


# In[19]:


data['claim_month'] = pd.DatetimeIndex(data['claim_date']).month
data['claim_year'] = pd.DatetimeIndex(data['claim_date']).year
del data['claim_date']


# In[20]:


#Dropping unwanted columns
del data['claim_number']
#fixing datatypes

data['gender'] = data['gender'].astype('object')
data['marital_status'] = data['marital_status'].astype('object')
data['high_education_ind'] = data['high_education_ind'].astype('object')
data['address_change_ind'] = data['address_change_ind'].astype('object')
data['living_status'] = data['living_status'].astype('object')
data['claim_day_of_week'] = data['claim_day_of_week'].astype('object')
data['accident_site'] = data['accident_site'].astype('object')
data['witness_present_ind'] = data['witness_present_ind'].astype('object')
data['channel'] = data['channel'].astype('object')
data['policy_report_filed_ind'] = data['policy_report_filed_ind'].astype('object')
data['vehicle_category'] = data['vehicle_category'].astype('object')
data['vehicle_color'] = data['vehicle_color'].astype('object')


# In[21]:


# adding age of driver buckets, classes based on Standard Deviation and Quartile Ranges
data['age_of_driver_buckets'] = data.age_of_driver
data['age_of_driver_buckets'][data.age_of_driver >= 62] = 'Very High'
data['age_of_driver_buckets'][(data.age_of_driver >= 51) & (data.age_of_driver < 62)] = 'High'
data['age_of_driver_buckets'][(data.age_of_driver >= 43) & (data.age_of_driver < 51)] = 'High Average'
data['age_of_driver_buckets'][(data.age_of_driver >= 35) & (data.age_of_driver < 43)] = 'Low Average'
data['age_of_driver_buckets'][(data.age_of_driver >= 24) & (data.age_of_driver < 35)] = 'Low'
data['age_of_driver_buckets'][data.age_of_driver < 24] = 'Very Low'


# In[22]:


# adding safty rating buckets, classes based on Standard Deviation and Quartile Ranges
data['safty_rating_buckets'] = data.safty_rating
data['safty_rating_buckets'][data.safty_rating >= 105] = 'Very High'
data['safty_rating_buckets'][(data.safty_rating >= 90) & (data.safty_rating < 105)] = 'High'
data['safty_rating_buckets'][(data.safty_rating >= 76) & (data.safty_rating < 90)] = 'High Average'
data['safty_rating_buckets'][(data.safty_rating >= 65) & (data.safty_rating < 76)] = 'Low Average'
data['safty_rating_buckets'][(data.safty_rating >= 50) & (data.safty_rating < 65)] = 'Low'
data['safty_rating_buckets'][data.safty_rating < 50] = 'Very Low'


# In[23]:


# adding income buckets, classes based on Standard Deviation and Quartile Ranges
data['annual_income_buckets'] = data.annual_income
data['annual_income_buckets'][data.annual_income >= 42500] = 'Very High'
data['annual_income_buckets'][(data.annual_income >= 39300) & (data.annual_income < 42500)] = 'High'
data['annual_income_buckets'][(data.annual_income >= 37600) & (data.annual_income < 39300)] = 'High Average'
data['annual_income_buckets'][(data.annual_income >= 35500) & (data.annual_income < 37600)] = 'Low Average'
data['annual_income_buckets'][(data.annual_income >= 32500) & (data.annual_income < 35500)] = 'Low'
data['annual_income_buckets'][data.annual_income < 32500] = 'Very Low'


# In[24]:


# adding vehcile weigh buckets, classes based on Standard Deviation and Quartile Ranges
data['vehicle_weight_buckets'] = data.vehicle_weight
data['vehicle_weight_buckets'][data.vehicle_weight >= 41500] = 'Very High'
data['vehicle_weight_buckets'][(data.vehicle_weight >= 29500) & (data.vehicle_weight < 41500)] = 'High'
data['vehicle_weight_buckets'][(data.vehicle_weight >= 21000) & (data.vehicle_weight < 29500)] = 'Average High'
data['vehicle_weight_buckets'][(data.vehicle_weight >= 14250) & (data.vehicle_weight < 21000)] = 'Average Low'
data['vehicle_weight_buckets'][(data.vehicle_weight >= 5000) & (data.vehicle_weight < 14250)] = 'Low'
data['vehicle_weight_buckets'][data.vehicle_weight < 5000] = 'Very Low'


# In[25]:


## adding Vehicle price buckets, classes based on Standard Deviation and Quartile Ranges
data['vehicle_price_buckets'] = data.vehicle_price
data['vehicle_price_buckets'][data.vehicle_price >= 41500] = 'Very High'
data['vehicle_price_buckets'][(data.vehicle_price >= 29500) & (data.vehicle_price < 41500)] = 'High'
data['vehicle_price_buckets'][(data.vehicle_price >= 21000) & (data.vehicle_price < 29500)] = 'Average High'
data['vehicle_price_buckets'][(data.vehicle_price >= 14250) & (data.vehicle_price < 21000)] = 'Average Low'
data['vehicle_price_buckets'][(data.vehicle_price >= 5000) & (data.vehicle_price < 14250)] = 'Low'
data['vehicle_price_buckets'][data.vehicle_price < 5000] = 'Very Low'


# In[26]:


# adding age of vehcile buckets, classes based on Standard Deviation and Quartile Ranges
data['age_of_vehicle_buckets'] = data.age_of_vehicle
data['age_of_vehicle_buckets'][data.age_of_vehicle >= 6] = 'Very High'
data['age_of_vehicle_buckets'][(data.age_of_vehicle >= 5) & (data.age_of_vehicle < 6)] = 'High'
data['age_of_vehicle_buckets'][(data.age_of_vehicle >= 3) & (data.age_of_vehicle < 5)] = 'Low'
data['age_of_vehicle_buckets'][data.age_of_vehicle < 3] = 'Very Low'


# In[27]:


data.drop(['age_of_driver','safty_rating','annual_income','vehicle_weight','vehicle_price','age_of_vehicle'],axis=1,inplace=True)


# In[28]:


data['claim_month'] = data['claim_month'].astype('object')
data['claim_year'] = data['claim_year'].astype('object')


# In[29]:


#### prepare final Train X and Test X dataframes 
ignore_features = ['is_train', 'is_test']
relevant_features = [col for col in data.columns if col not in ignore_features]
trainX = data[data['is_train'] == 1][relevant_features]
testX = data[data['is_test'] == 1][relevant_features]


# In[30]:


#outlier treatment
trainX = trainX[np.abs(trainX.past_num_of_claims-trainX.past_num_of_claims.mean()) <= (3*trainX.past_num_of_claims.std())]
trainX = trainX[np.abs(trainX.liab_prct-trainX.liab_prct.mean()) <= (3*trainX.liab_prct.std())]
trainX = trainX[np.abs(trainX.claim_est_payout-trainX.claim_est_payout.mean()) <= (3*trainX.claim_est_payout.std())]


# In[31]:


#Correlation in the dataset
corr = train_df.corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
sns.set(style="white")

f, ax = plt.subplots(figsize=(10, 8))
cmap = sns.diverging_palette(30, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.1, cbar_kws={"shrink": .5});


# In[32]:


# function to obtain Categorical Features
def _get_categorical_features(df):
    feats = [col for col in list(df.columns) if df[col].dtype == 'object']
    return feats

# function to factorize categorical features
def _factorize_categoricals(df, cats):
    for col in cats:
        df[col], _ = pd.factorize(df[col])
    return df 

# function to create dummy variables of categorical features
def _get_dummies(df, cats):
    for col in cats:
        df = pd.concat([df, pd.get_dummies(df[col], prefix=col)], axis=1)
    return df 


# In[33]:


# get categorical features
train_df_cats = _get_categorical_features(trainX)


# In[34]:


# factorize the categorical features from train and test data
train_df = _factorize_categoricals( trainX, train_df_cats)


# In[35]:


train_df = _get_dummies( trainX, train_df_cats)


# In[36]:


train_df.drop(['claim_month','claim_year','age_of_driver_buckets','safty_rating_buckets','vehicle_weight_buckets','annual_income_buckets','gender','living_status','claim_day_of_week','accident_site','channel','vehicle_category','vehicle_color','marital_status','high_education_ind','address_change_ind','witness_present_ind','zip_code','policy_report_filed_ind','vehicle_price_buckets','age_of_vehicle_buckets'],axis=1,inplace=True)


# In[37]:


# get categorical features
test_df_cats = _get_categorical_features(testX)
test_df_cats
# factorize the categorical features from train and test data
test_df = _factorize_categoricals( testX, test_df_cats)
test_df = _get_dummies( testX, test_df_cats)


# In[38]:


test_df.drop(['vehicle_price_buckets','age_of_vehicle_buckets','claim_month','claim_year','age_of_driver_buckets','safty_rating_buckets','vehicle_weight_buckets','annual_income_buckets','gender','living_status','claim_day_of_week','accident_site','channel','vehicle_category','vehicle_color','marital_status','high_education_ind','address_change_ind','witness_present_ind','zip_code','policy_report_filed_ind'],axis=1,inplace=True)


# In[39]:


#for checking predictions
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# to divide train and test set
from sklearn.model_selection import train_test_split
X_train = train_df.drop('fraud',axis=1)
Y_train = train_df['fraud']
X_train, X_test, Y_train, Y_test = train_test_split(X_train,Y_train,test_size=0.02,random_state=0)
X_train.shape, X_test.shape

X_train_columns = X_train.columns


# In[40]:


#checking the distribution of fraud in train and test sets

print(Y_test.value_counts(normalize=True))
print(Y_train.value_counts(normalize=True))


# In[41]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Fit on training set only.
scaler.fit(X_train)
# Apply transform to both the training set and the test set.
scaled_X_train = scaler.transform(X_train)
scaled_X_test = scaler.transform(X_test)


# In[43]:


from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score 
from sklearn.metrics import confusion_matrix, precision_recall_curve, roc_curve, auc, log_loss

# check classification scores of logistic regression
logreg = LogisticRegression()
logreg.fit(scaled_X_train, Y_train)
y_pred = logreg.predict(scaled_X_test)
y_pred_proba = logreg.predict_proba(scaled_X_test)[:, 1]
[fpr, tpr, thr] = roc_curve(Y_test, y_pred_proba)
print('Train/Test split results:')
print(logreg.__class__.__name__+" accuracy is %2.3f" % accuracy_score(Y_test, y_pred))
print(logreg.__class__.__name__+" log_loss is %2.3f" % log_loss(Y_test, y_pred_proba))
print(logreg.__class__.__name__+" auc is %2.3f" % auc(fpr, tpr))

idx = np.min(np.where(tpr > 0.95)) # index of the first threshold for which the sensibility > 0.95

plt.figure()
plt.plot(fpr, tpr, color='coral', label='ROC curve (area = %0.3f)' % auc(fpr, tpr))
plt.plot([0, 1], [0, 1], 'k--')
plt.plot([0,fpr[idx]], [tpr[idx],tpr[idx]], 'k--', color='blue')
plt.plot([fpr[idx],fpr[idx]], [0,tpr[idx]], 'k--', color='blue')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (1 - specificity)', fontsize=14)
plt.ylabel('True Positive Rate (recall)', fontsize=14)
plt.title('Receiver operating characteristic (ROC) curve')
plt.legend(loc="lower right")
plt.show()

print("Using a threshold of %.3f " % thr[idx] + "guarantees a sensitivity of %.3f " % tpr[idx] +  
      "and a specificity of %.3f" % (1-fpr[idx]) + 
      ", i.e. a false positive rate of %.2f%%." % (np.array(fpr[idx])*100))


# In[44]:


#fit a decision tree classifier
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier().fit(X_train, Y_train)
print('Accuracy of Decision Tree classifier on training set: {:.2f}'
     .format(clf.score(X_train, Y_train)))
print('Accuracy of Decision Tree classifier on test set: {:.2f}'
     .format(clf.score(X_test, Y_test)))

pred_clf = clf.predict(X_test)
print(confusion_matrix(Y_test, pred_clf))
print(classification_report(Y_test, pred_clf))


# In[45]:


#fit a knn classifier
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(scaled_X_train, Y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'
     .format(knn.score(scaled_X_train, Y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'
     .format(knn.score(scaled_X_test, Y_test)))

pred_knn = knn.predict(scaled_X_test)
print(confusion_matrix(Y_test, pred_knn))
print(classification_report(Y_test, pred_knn))


# In[46]:


#fit a lda
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis()
lda.fit(scaled_X_train, Y_train)
print('Accuracy of LDA classifier on training set: {:.2f}'
     .format(lda.score(scaled_X_train, Y_train)))
print('Accuracy of LDA classifier on test set: {:.2f}'
     .format(lda.score(scaled_X_test, Y_test)))

pred_lda = lda.predict(scaled_X_test)
print(confusion_matrix(Y_test, pred_lda))
print(classification_report(Y_test, pred_lda))


# In[47]:


#fit a naive bayes model
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(scaled_X_train, Y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'
     .format(gnb.score(scaled_X_train, Y_train)))
print('Accuracy of GNB classifier on test set: {:.2f}'
     .format(gnb.score(scaled_X_test, Y_test)))

pred_gnb = gnb.predict(scaled_X_test)
print(confusion_matrix(Y_test, pred_gnb))
print(classification_report(Y_test, pred_gnb))


# In[48]:


#fit a svm classifier
from sklearn.svm import SVC
svm = SVC()
svm.fit(scaled_X_train, Y_train)
print('Accuracy of SVM classifier on training set: {:.2f}'
     .format(svm.score(scaled_X_train, Y_train)))
print('Accuracy of SVM classifier on test set: {:.2f}'
     .format(svm.score(scaled_X_test, Y_test)))

pred_svm = svm.predict(scaled_X_test)
print(confusion_matrix(Y_test, pred_svm))
print(classification_report(Y_test, pred_svm))


# In[49]:


#fit a random forest classifier
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()
rfc.fit(X_train, Y_train)
print('Accuracy of Random Forest Classifier on training set: {:.2f}'
     .format(rfc.score(X_train, Y_train)))
print('Accuracy of Random Forest Classifier on test set: {:.2f}'
     .format(rfc.score(X_test, Y_test)))

pred_rfc = rfc.predict(X_test)
print(confusion_matrix(Y_test, pred_rfc))
print(classification_report(Y_test, pred_rfc))


# In[50]:


# Random Forest feature importance
importance = pd.Series(rfc.feature_importances_)
importance.index = X_train_columns
importance.sort_values(inplace=True, ascending=False)
importance.plot.bar(figsize=(50,10))


# In[51]:


#fit a xgboost classifier
import xgboost as xgb
from xgboost import plot_importance
xgb_model = xgb.XGBClassifier()

eval_set = [(X_test,Y_test)]
xgb_model.fit(X_train,Y_train, eval_set=eval_set, verbose=False)
print('Accuracy of XGboost on training set: {:.2f}'
     .format(xgb_model.score(X_train, Y_train)))
print('Accuracy of XGboost on test set: {:.2f}'
     .format(xgb_model.score(X_test, Y_test)))

pred_xgb = xgb_model.predict(X_test)
print(confusion_matrix(Y_test, pred_xgb))
print(classification_report(Y_test, pred_xgb))
ax = plot_importance(xgb_model)
fig = ax.figure
fig.set_size_inches(10, 10)


# In[53]:


import lightgbm as lgb
from sklearn.model_selection import train_test_split, GridSearchCV
train_data=lgb.Dataset(X_train, label=Y_train)

#Select Hyper-Parameters
params = {'boosting_type': 'gbdt',
          'max_depth' : -1,
          'objective': 'binary',
          'nthread': 5,
          'num_leaves': 64,
          'learning_rate': 0.07,
          'max_bin': 512,
          'subsample_for_bin': 200,
          'subsample': 1,
          'subsample_freq': 1,
          'colsample_bytree': 0.8,
          'reg_alpha': 1.2,
          'reg_lambda': 1.2,
          'min_split_gain': 0.5,
          'min_child_weight': 1,
          'min_child_samples': 5,
          'scale_pos_weight': 1,
          'num_class' : 1,
          'metric' : 'binary_error'
          }

# Create parameters to search
gridParams = {
    'learning_rate': [0.07],
    'n_estimators': [8,16],
    'num_leaves': [20, 24, 27],
    'boosting_type' : ['gbdt'],
    'objective' : ['binary'],
    'random_state' : [501], 
    'colsample_bytree' : [0.64, 0.65],
    'subsample' : [0.7,0.75],
    #'reg_alpha' : [1, 1.2],
    #'reg_lambda' : [ 1.2, 1.4],
    }

# Create classifier to use
mdl = lgb.LGBMClassifier(boosting_type= 'gbdt',
          objective = 'binary',
          n_jobs = 5, 
          silent = True,
          max_depth = params['max_depth'],
          max_bin = params['max_bin'],
          subsample_for_bin = params['subsample_for_bin'],
          subsample = params['subsample'],
          subsample_freq = params['subsample_freq'],
          min_split_gain = params['min_split_gain'],
          min_child_weight = params['min_child_weight'],
          min_child_samples = params['min_child_samples'],
          scale_pos_weight = params['scale_pos_weight'])

# View the default model params:
mdl.get_params().keys()

# Create the grid
grid = GridSearchCV(mdl, gridParams, verbose=2, cv=4, n_jobs=-1)

# Run the grid
grid.fit(X_train,Y_train)

# Print the best parameters found
print(grid.best_params_)
print(grid.best_score_)

# Using parameters already set above, replace in the best from the grid search
params['colsample_bytree'] = grid.best_params_['colsample_bytree']
params['learning_rate'] = grid.best_params_['learning_rate']
# params['max_bin'] = grid.best_params_['max_bin']
params['num_leaves'] = grid.best_params_['num_leaves']
#params['reg_alpha'] = grid.best_params_['reg_alpha']
#params['reg_lambda'] = grid.best_params_['reg_lambda']
params['subsample'] = grid.best_params_['subsample']
# params['subsample_for_bin'] = grid.best_params_['subsample_for_bin']

print('Fitting with params: ')
print(params)

#Train model on selected parameters and number of iterations
lgbm = lgb.train(params,
                 train_data,
                 280,
                 #early_stopping_rounds= 40,
                 verbose_eval= 4
                 )

#Predict on test set
predictions_lgbm_prob = lgbm.predict(X_test)
predictions_lgbm_01 = np.where(predictions_lgbm_prob > 0.5, 1, 0) #Turn probability to 0-1 binary output

#--------------------------Print accuracy measures and variable importances----------------------
#Plot Variable Importances
lgb.plot_importance(lgbm, max_num_features=21, importance_type='split')

#Print accuracy
acc_lgbm = accuracy_score(Y_test,predictions_lgbm_01)
print('Overall accuracy of Light GBM model:', acc_lgbm)

#Print Area Under Curve
plt.figure()
false_positive_rate, recall, thresholds = roc_curve(Y_test, predictions_lgbm_prob)
roc_auc = auc(false_positive_rate, recall)
plt.title('Receiver Operating Characteristic (ROC)')
plt.plot(false_positive_rate, recall, 'b', label = 'AUC = %0.3f' %roc_auc)
plt.legend(loc='lower right')
plt.plot([0,1], [0,1], 'r--')
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.0])
plt.ylabel('Recall')
plt.xlabel('Fall-out (1-Specificity)')
plt.show()

print('AUC score:', roc_auc)

#Print Confusion Matrix
plt.figure()
cm = confusion_matrix(Y_test, predictions_lgbm_01)
labels = ['No Default', 'Default']
plt.figure(figsize=(8,6))
sns.heatmap(cm, xticklabels = labels, yticklabels = labels, annot = True, fmt='d', cmap="Blues", vmin = 0.2);
plt.title('Confusion Matrix')
plt.ylabel('True Class')
plt.xlabel('Predicted Class')
plt.show()

