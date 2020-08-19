# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 23:36:07 2020

@author: dat18
"""
#%%
import os

#%% Train Catboost model
from catboost import CatBoostRegressor, Pool
from utils import display_Results, save_Model, grid_search, save_best_params

def fit_model(inputs):
    
    X_train_random_split = inputs.X_train_random_split
    y_train_random_split = inputs.y_train_random_split
    X_test_random_split = inputs.X_test_random_split
    y_test_random_split = inputs.y_test_random_split
    X_train_hist_split = inputs.X_train_hist_split
    y_train_hist_split = inputs.y_train_hist_split
    X_test_hist_split = inputs.X_test_hist_split
    y_test_hist_split = inputs.y_test_hist_split
    
    params = {        
        'loss_function': 'RMSE',
        'n_estimators': 1000,
        'eval_metric': 'RMSE',
        'random_seed': 24,
        'verbose': 0,
    }
    
    param_space = {
                    'learning_rate': [0.03, 0.1, 0.005],
                    'depth': [4, 6, 10],
                    'l2_leaf_reg': [1, 3, 5, 7, 9]
                  }
    
    model_name = "Catboost Regression"
    
    model_save_path = inputs.model_save_path
    results_save_path = inputs.results_save_path
    
    print(model_name)
    ###################### Random Split Training ###########################
    random_split_model = CatBoostRegressor(**params)
    random_split_model_best = grid_search(random_split_model, param_space)
    # train_pool = Pool(X_train_random_split, y_train_random_split.pm25)
    # val_pool = Pool(X_validation, y_validation)
    # test_pool = Pool(X_test_random_split, y_test_random_split.pm25)
    print("Fitting model using Random Split Data...")
    
    #%%
    random_split_model_best.fit(X_train_random_split, y_train_random_split.pm25)
    
    # print('Model validation accuracy: {:.4}'.format(
    #     mean_absolute_error(y_validation, model.predict(X_validation))
    # ))
    
    #%% Evaluate model
    print("Evaluating with Test set")
    preds_random_split = random_split_model_best.predict(X_test_random_split)
    print("Done!")
    
    #%% Random Split Results
    save_path = os.path.join(results_save_path, "Random Split")
    os.makedirs(save_path, exist_ok=True)
    filePath = os.path.join(save_path, model_name + " Results.txt")
    bestparamPath = os.path.join(save_path, model_name + " Best params.txt")
    print("Saving best params...")
    save_best_params(random_split_model_best, bestparamPath)
    print("Done!")
    print("Showing result for Random Split")
    display_Results(y_test_random_split, preds_random_split, writeFile = True, fPath = filePath, modelName = model_name)
    
    #%% Save model
    model_save_name = model_name + " Random Split Model.pickle"
    save_Model(random_split_model_best, model_save_name, model_save_path)
    
    #%%#######################################################################
    ###################### Historical Split Training #########################
    hist_split_model = CatBoostRegressor(**params)
    hist_split_model_best = grid_search(hist_split_model, param_space)
    # Single variable
    # train_pool = Pool(X_train_hist_split, y_train_hist_split.pm25)
    # test_pool = Pool(X_test_hist_split, y_test_hist_split.pm25)
    print("Fitting model using Historical Split Data...")
    hist_split_model_best.fit(X_train_hist_split, y_train_hist_split.pm25)
    # Multi-variable
    # model.fit(X_train, y_train.drop(columns=['aqi', 'aqi_rank']))
    print("Done!")
    
    #%% Evaluate model
    print("Evaluating with Test set")
    preds_hist_split = hist_split_model_best.predict(X_test_hist_split)
    print("Done!")
    
    #%% Historical Split Results
    save_path = os.path.join(results_save_path, "Historical Split")
    os.makedirs(save_path, exist_ok=True)
    filePath = os.path.join(save_path, model_name + " Results.txt")
    bestparamPath = os.path.join(save_path, model_name + " Best params.txt")    
    print("Saving best params...")
    save_best_params(hist_split_model_best, bestparamPath)
    print("Done!")
    print("Showing result for Historical Split")
    display_Results(y_test_hist_split, preds_hist_split, writeFile = True, fPath = filePath, modelName = model_name)
    
    #%% Save model
    model_save_name = model_name + " Historical Split Model.pickle"
    save_Model(hist_split_model_best, model_save_name, model_save_path)
