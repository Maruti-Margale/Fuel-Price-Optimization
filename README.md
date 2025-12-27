# Fuel-Price-Optimization

Live Demo : https://fuel-price-optimization-bymaruti.streamlit.app/

## Overview
This project recommends the optimal daily fuel price to maximize profit using a Random Forest regression model. It considers historical data, competitor prices, and business constraints.

## Features
- Predict daily fuel demand using Random Forest
- Compute rolling and lag features
- Simulate candidate prices and calculate expected profit
- Recommend the optimal price
- Streamlit interface for interactive input

## Installation
1. Clone the repository:
```bash
git clone https://github.com/Maruti-Margale/Fuel-Price-Optimization/tree/Maruti
cd fuel-price-optimization
```

```mermaid
graph TD
    A[User opens Streamlit app] --> B[App loads UI components]
    B --> C[User enters today's prices and cost in sidebar]
    C --> D[App loads historical data and trains Random Forest model]
    D --> E[App creates derived features: lags, rolling averages, competitor comparisons]
    E --> F[App simulates candidate prices within business constraints]
    F --> G[Predict demand and compute profit for each candidate price]
    G --> H[Select price with maximum expected profit]
    H --> I[Update UI with recommended price, expected volume, and expected profit]
    I --> J[User sees optimized price recommendation on screen]
```
