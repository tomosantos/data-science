# Olist Freight Regression

Regression project to predict the freight value (`freight_value`) for orders from the Brazilian e-commerce Olist, using Machine Learning techniques.

## Objective

Predict the freight value (`freight_value`) of orders based on variables from the public Olist dataset, applying and comparing different regression models.

## Project Structure

- `EDA.ipynb`: Exploratory data analysis, feature engineering, and preparation of the final dataset (`df_final.csv`).
- `Model.ipynb`: Training, evaluation, and comparison of regression models.
- `Train.py`: Script for model training and analysis.
- `data/`: Contains original data files and the processed final dataset.

## Main Models Used

- XGBoost Regressor
- LightGBM Regressor
- CatBoost Regressor
- Decision Tree Regressor

## Main Steps

1. Data loading and preparation
2. Feature engineering (volume, density, distance, dates, promotional periods)
3. Categorical variable encoding
4. Model training and evaluation
5. Feature importance analysis
6. Cross-validation and fine-tuning
7. Experiment tracking with MLflow

## How to Run

1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Make sure the file `df_final.csv` is in the `data/` folder (it can be generated from `EDA.ipynb`).
3. Run the main script:
   ```
   python Train.py
   ```

## Experiment Tracking

- The project uses [MLflow](https://mlflow.org/) for experiment tracking.
- The tracking server should be running at `http://localhost:5000/`.

## Data

- Source: [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download)

---