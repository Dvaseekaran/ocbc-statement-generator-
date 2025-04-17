# VALIDATIONS.md

## Input Validation Rules

### 1. Card Number / Card ID
- **Accepted:** 
  - Alphanumeric strings (e.g., `CARD45678`)
  - Must not be empty
  - No special characters except hyphens (if used)
- **Rejected:** 
  - Empty values
  - Strings with spaces or unsupported special characters

### 2. ZIP/Postal Code (if used)
- **Accepted:** 
  - 5 or 6 digit numbers (e.g., `12345`, `123456`)
  - Alphanumeric postal codes (for international addresses, e.g., `560123`, `S123456`)
- **Rejected:** 
  - Empty values
  - Strings with special characters (except space or hyphen if required by country format)

### 3. Date Format
- **Accepted:** 
  - `YYYY-MM-DD` (e.g., `2024-06-01`)
  - Dates must be valid calendar dates
- **Rejected:** 
  - Invalid dates (e.g., `2024-02-30`)
  - Incorrect formats (e.g., `06/01/2024`, `2024/06/01`)

### 4. Currency Amounts
- **Accepted:** 
  - Positive numbers with up to two decimal places (e.g., `1234.56`)
  - Zero is accepted where appropriate
- **Rejected:** 
  - Negative values (unless specifically for refunds/credits)
  - Non-numeric values

### 5. Language Selection
- **Accepted:** 
  - Only the following codes: `en`, `zh`, `ta`, `ms`
- **Rejected:** 
  - Any code not in the above list

### 6. Required Fields
- All required fields must be present and non-empty.

---

## General Notes
- All inputs are validated server-side.
- Invalid or missing inputs will result in a validation error and the statement will not be generated.
- For any questions, refer to the project documentation or contact the developer.