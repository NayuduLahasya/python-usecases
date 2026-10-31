import pandas as pd

# Load CSV files
cust_df = pd.read_csv("customers.csv")
prod_df = pd.read_csv("products.csv")
ord_df = pd.read_csv("orders.csv")

# Remove duplicate customers
cust_df = cust_df.drop_duplicates(subset=["customer_id"])

# Find orders with invalid customers
invalid_orders = ord_df.loc[
    ~ord_df["customer_id"].isin(cust_df["customer_id"])
]

print("Orders with Invalid Customer IDs:")
print(invalid_orders)

# Keep only valid orders
valid_orders = ord_df.loc[
    ord_df["customer_id"].isin(cust_df["customer_id"])
]

# Merge with customer details
order_customer = valid_orders.merge(
    cust_df,
    how="left",
    on="customer_id"
)

# Merge with product details
final_data = order_customer.merge(
    prod_df,
    how="left",
    on="product_id"
)

# Calculate order value
final_data["total_amount"] = final_data.eval(
    "quantity * price"
)

# Select required columns
result = final_data[
    [
        "order_id",
        "customer_name",
        "city",
        "product_name",
        "quantity",
        "price",
        "status",
        "total_amount"
    ]
]

# Write output file
result.to_csv("final_orders.csv", index=False)

print("\nProcessed Orders:")
print(result)
