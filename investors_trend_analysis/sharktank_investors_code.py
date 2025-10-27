import pandas as pd
import numpy as np

# --- Configuration & Setup ---
FILE_NAME = "ShartankIndiaAllPitches.csv"
SHARK_COLS = ['anupam', 'ashneer', 'namita', 'aman', 'peyush', 'vineeta', 'ghazal']

# --- 1. Data Cleaning and Organization ---
print("--- Phase 1: Data Cleaning ---")

# Load the dataset
df = pd.read_csv(FILE_NAME)

# Standardize column names (lowercase, replace spaces with underscores)
df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False).str.replace(r'[^\w_]', '', regex=True)

# Correctly identify the cleaned column names (based on file structure)
investment_col = [col for col in df.columns if 'investment_amount' in col][0]
equity_col = 'equity'

# 1.1 Convert Equity to Numeric
# Remove '%' and convert to float
df[equity_col] = df[equity_col].astype(str).str.replace('%', '', regex=False)
df[equity_col] = pd.to_numeric(df[equity_col], errors='coerce')

# 1.2 Create 'Deal Status' Column
df['deal_status'] = np.where(df[investment_col] > 0, 'Deal', 'No Deal')

# 1.3 Create a 'Domain/Industry' Categorization Function
def categorize_domain(idea):
    idea = str(idea).lower()
    
    # Define broad domain keywords
    if any(keyword in idea for keyword in ['food', 'momo', 'chip', 'coffee', 'juice', 'chaat', 'tea', 'snacks', 'chocolate', 'dessert', 'beverage']):
        return 'Food & Beverage (F&B)'
    elif any(keyword in idea for keyword in ['sleeve', 'footwear', 'clothing', 'jutt', 'apparel', 'garment', 'lingerie', 'jewelry', 'mask', 't-shirt', 'fashion']):
        return 'Fashion & Apparel'
    elif any(keyword in idea for keyword in ['app', 'tech', 'software', 'platform', 'saas', 'robot', 'automation', 'gaming', 'ai', 'website', 'e-commerce', 'data']):
        return 'Tech, App & E-commerce'
    elif any(keyword in idea for keyword in ['health', 'skincare', 'beauty', 'dermato', 'grooming', 'ayurveda', 'organic', 'wellness', 'brain', 'pharma', 'medical']):
        return 'Health, Wellness & Beauty'
    elif any(keyword in idea for keyword in ['home', 'decor', 'bike', 'auto', 'vehicle', 'car', 'lifestyle', 'mobility', 'rental']):
        return 'Home & Lifestyle'
    else:
        return 'Miscellaneous'

df['domain'] = df['idea'].apply(categorize_domain)

# Filter for successful deals for all subsequent analyses
successful_deals = df[df['deal_status'] == 'Deal'].copy()

# Save the cleaned data for potential Excel/Tableau use (Phase 3 Preparation)
cleaned_file_name = "Shark_Tank_Cleaned.csv"
df.to_csv(cleaned_file_name, index=False)
print(f"Cleaned data successfully saved to: {cleaned_file_name}")

# --- 2. Core Analysis & Metrics ---
print("\n--- Phase 2: Core Analysis (KPIs) ---")

# 2.1 Domain Success Rate
domain_success = df.groupby('domain')['deal_status'].value_counts(normalize=True).mul(100).unstack(fill_value=0)['Deal'].sort_values(ascending=False).reset_index(name='Success Rate (%)')

print("\n2.1 Funding Stage Success Rate by Domain:")


print(domain_success.to_string(index=False, float_format="%.2f"))


# 2.2 Average Investment and Equity (Successful Deals Only)
avg_investment = successful_deals[investment_col].mean()
avg_equity = successful_deals[equity_col].mean()

print("\n2.2 Average Deal Metrics:")
print(f"Average Investment Amount in Successful Deals: {avg_investment:.2f} Lakhs INR")
print(f"Average Equity Given Up in Successful Deals: {avg_equity:.2f}%")


# 2.3 Investor Activity and Preferences
# Total Deals Made by Each Shark
investor_deals = successful_deals[SHARK_COLS].apply(lambda x: (x == 'Y').sum()).sort_values(ascending=False).reset_index(name='Total Deals Made')
investor_deals.rename(columns={'index': 'Shark'}, inplace=True)

print("\n2.3 Total Deals Made by Each Shark:")

print(investor_deals.to_string(index=False))


# 2.4 Shark-Domain Preference (Pivot Table)
shark_domain_pivot = successful_deals.groupby('domain')[SHARK_COLS].apply(lambda x: (x == 'Y').sum()).T
shark_domain_pivot.columns.name = None # Clean up column name

print("\n2.4 Shark-Domain Investment Pivot Table (Deals Count):")
print(shark_domain_pivot.to_string())
print("-" * 40)
