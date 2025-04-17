# Test Cases for OCBC Statement Generator

This document lists test cases for validating the input and output behavior of the OCBC Statement Generator.  
Each test case includes: inputs, expected outputs, actual results, and a PASS/FAIL status.

---

## Test Case 1: Valid Card ID, Valid Dates, English
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  PDF generated in English with correct data.
- **Actual Result:**  
  PDF generated in English with correct data.
- **Status:** PASS

---

## Test Case 2: Valid Card ID, Valid Dates, 中文
- **Inputs:**  
  Card ID: CARD45678  
  Language: zh  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  PDF generated in Chinese with correct data.
- **Actual Result:**  
  PDF generated in Chinese with correct data.
- **Status:** PASS

---

## Test Case 3: Valid Card ID, Valid Dates, தமிழ்
- **Inputs:**  
  Card ID: CARD45678  
  Language: ta  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  PDF generated in Tamil with correct data.
- **Actual Result:**  
  PDF generated in Tamil with correct data.
- **Status:** PASS

---

## Test Case 4: Valid Card ID, Valid Dates, Bahasa Melayu
- **Inputs:**  
  Card ID: CARD45678  
  Language: ms  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  PDF generated in Bahasa Melayu with correct data.
- **Actual Result:**  
  PDF generated in Bahasa Melayu with correct data.
- **Status:** PASS

---

## Test Case 5: Invalid Card ID (empty)
- **Inputs:**  
  Card ID: (empty)  
  Language: en  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 6: Invalid Card ID (special characters)
- **Inputs:**  
  Card ID: CARD#123!  
  Language: en  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 7: Invalid Date Format
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: 06/01/2024  
  End Date: 06/30/2024  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 8: Invalid Date (nonexistent date)
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: 2024-02-30  
  End Date: 2024-03-01  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 9: Start Date After End Date
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: 2024-07-01  
  End Date: 2024-06-01  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 10: Invalid Language Code
- **Inputs:**  
  Card ID: CARD45678  
  Language: fr  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 11: Missing Required Field (Start Date)
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: (empty)  
  End Date: 2024-06-30  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 12: Card ID with spaces
- **Inputs:**  
  Card ID: CARD 45678  
  Language: en  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
- **Expected Output:**  
  Validation error, statement not generated.
- **Actual Result:**  
  Validation error shown.
- **Status:** PASS

---

## Test Case 13: Valid Card ID, No Transactions in Date Range
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: 2023-01-01  
  End Date: 2023-01-31  
- **Expected Output:**  
  PDF generated with zero transactions.
- **Actual Result:**  
  PDF generated with zero transactions.
- **Status:** PASS

---

## Test Case 14: Valid Card ID, Zero Amount Transaction
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
  (Ensure at least one transaction with amount 0.00 exists)
- **Expected Output:**  
  PDF generated, zero amount transaction displayed.
- **Actual Result:**  
  PDF generated, zero amount transaction displayed.
- **Status:** PASS

---

## Test Case 15: Valid Card ID, Refund Transaction (Negative Amount)
- **Inputs:**  
  Card ID: CARD45678  
  Language: en  
  Start Date: 2024-06-01  
  End Date: 2024-06-30  
  (Ensure at least one transaction with negative amount exists)
- **Expected Output:**  
  PDF generated, negative amount transaction displayed as refund/credit.
- **Actual Result:**  
  PDF generated, negative amount transaction displayed as refund/credit.
- **Status:** PASS

---