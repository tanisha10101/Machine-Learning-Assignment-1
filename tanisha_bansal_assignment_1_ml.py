# -*- coding: utf-8 -*-
"""Tanisha_Bansal_Assignment-1_ML.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12aAd1p70RusCyjQLzoyv8IXz5yQu8a94

**Name - Tanisha Bansal**

**Enrollment No. - 14301172022**

**Assignment - 01**

**Batch: CSE-AI - 2, 2026**
"""

# Importing all the necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Step 1: Load the dataset
print("Loading dataset...")
penguins = sns.load_dataset('penguins')
if penguins is not None:
    print("Dataset loaded successfully.")
    print(penguins.head())
else:
    raise ValueError("Failed to load dataset.")

# Step 2: Data Cleaning
print("\nInitial dataset shape:", penguins.shape)
print("\nColumns with missing values:\n", penguins.isnull().sum())

# Step 3: Normalization of Continuous Features
scaler = StandardScaler()
continuous_features = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
penguins[continuous_features] = scaler.fit_transform(penguins[continuous_features])

# Step 4: Preprocessing Categorical Features
penguins = pd.get_dummies(penguins, columns=['species', 'island', 'sex'], drop_first=True)

# Step 5: Data Transformation
X = penguins.drop(columns=['body_mass_g'])  # Features
y = penguins['body_mass_g']  # Target

from sklearn.impute import SimpleImputer

# Handle missing values
imputer = SimpleImputer(strategy='mean')  # Replace NaN with the mean of the column
X_imputed = imputer.fit_transform(X)

# Polynomial Feature Expansion
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_imputed)

print("Polynomial features generated successfully.")

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)
print("\nTraining and testing datasets created.")

# Step 6: Applying Multiple Regression Models
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=0.1),
    "Decision Tree": DecisionTreeRegressor(max_depth=5, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

print(f"Number of NaN values in target variable y: {y.isnull().sum()}")

non_nan_indices = y.notnull()
X = X[non_nan_indices]  # Keep only rows where y is not NaN
y = y[non_nan_indices]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

results = []

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluation Metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results.append((name, mse, r2))
    print(f"{name} - Mean Squared Error (MSE): {mse:.2f}, R-squared (R²): {r2:.2f}")

# Step 7: Results Comparison
results_df = pd.DataFrame(results, columns=['Model', 'MSE', 'R2'])
print("\nRegression Model Comparison:")
print(results_df)

# Step 8: Visualization
# Bar plot for MSE
plt.figure(figsize=(10, 6))
sns.barplot(data=results_df, x='Model', y='MSE', palette='coolwarm')
plt.title('Mean Squared Error Comparison')
plt.ylabel('MSE')
plt.xlabel('Regression Models')
plt.xticks(rotation=45)
plt.show()

# Bar plot for R-squared
plt.figure(figsize=(10, 6))
sns.barplot(data=results_df, x='Model', y='R2', palette='viridis')
plt.title('R-squared Comparison')
plt.ylabel('R² Score')
plt.xlabel('Regression Models')
plt.xticks(rotation=45)
plt.show()

# Scatter plot for best model predictions
best_model_name = results_df.loc[results_df['R2'].idxmax(), 'Model']
print(f"\nBest performing model: {best_model_name}")
best_model = models[best_model_name]
best_y_pred = best_model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.scatter(y_test, best_y_pred, alpha=0.5, color='green')
plt.title(f'Actual vs Predicted Body Mass ({best_model_name})')
plt.xlabel('Actual Body Mass (Standardized)')
plt.ylabel('Predicted Body Mass (Standardized)')
plt.grid(True)
plt.show()

#Conclusion
print("\nThe program successfully trained multiple regression models, evaluated their performance, and visualized the results.")