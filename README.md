This code produces two dataframes:

1. full_dataset:

-full dataset with "description" and "reason for flag" columns

2. just_flagged_accounts:

-a subset of just flagged accounts

# Task_code
Code to tag potentially suspect accounts based on criteria 1-4:

Step 1: 

1.1 Look for high volume of transactions (by origination customer)
1.2 Check at transaction level for tagged customers

Step 2:   

2.1 Look for high volume of transactions (by merchant name)
2.2 Check at transaction level for tagged merchants

Step 3:  

3.1 Check for transactions just under $10,000 (Currency Transaction Report limit)

Step 4:  

4.1 Check for Largest movements per month >$20,000 p/m
