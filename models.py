import pickle
import joblib
import xgboost as xgb
from surprise import SVDpp,SVD,BaselineOnly



bsl = pickle.load(open('./models/baseline_model.sav','rb'))
svd = pickle.load(open('./models/svd_model.sav','rb'))
svdpp = pickle.load(open('./models/svdpp_model.sav','rb'))
# xgb_final = joblib.load('./xgb_model.pkl')
rf = pickle.load(open('./models/random_forest_model.sav','rb'))