# 📝 FIELD INPUT GUIDE - WHAT YOU CAN ENTER

## 📅 Updated: March 27, 2026 - 6:57 AM

---

## 🎯 **PURCHASE FORM FIELDS**

### **1. Supplier Name**
- ✅ **Type**: Any text (free typing)
- ✅ **Length**: Any length (no minimum/maximum)
- ✅ **Characters**: Letters, numbers, spaces, special characters
- ✅ **Examples**: 
  - "A" (single character)
  - "John Supplier"
  - "ABC Textiles Ltd."
  - "Supplier #123"
  - "Very Long Supplier Name Inc."

### **2. Invoice Number**
- ✅ **Type**: Uppercase letters, numbers, hyphens only
- ✅ **Format**: Must match pattern: `^[A-Z0-9\-]+$`
- ✅ **Examples**:
  - "INV001"
  - "PUR-2024-001"
  - "INV12345"
  - "SUPPLIER-001"
- ❌ **Invalid**: "inv001" (lowercase), "INV 001" (spaces), "INV/001" (slashes)

### **3. Date**
- ✅ **Type**: Date picker or text input
- ✅ **Format**: YYYY-MM-DD
- ✅ **Range**: Any date up to today
- ✅ **Examples**:
  - "2024-03-27"
  - "2024-01-15"
  - "2023-12-31"
- ❌ **Invalid**: Future dates, invalid date formats

### **4. Yarn Type**
- ✅ **Type**: Any text (free typing)
- ✅ **Length**: Any length (no minimum/maximum)
- ✅ **Characters**: Letters, numbers, spaces, special characters
- ✅ **Examples**:
  - "Cotton Yarn 40"
  - "Polyester Yarn"
  - "Cotton 40"
  - "Custom Yarn Type"
  - "Special Blend Yarn"
  - "Wool Yarn 30"

### **5. Quantity**
- ✅ **Type**: Numbers only (positive)
- ✅ **Range**: 1 to 10,000
- ✅ **Decimal**: No decimals (whole numbers only)
- ✅ **Examples**:
  - "100"
  - "500"
  - "1000"
  - "50"
- ❌ **Invalid**: "0", "-100", "100.5", "abc"

### **6. Unit**
- ✅ **Type**: Dropdown selection
- ✅ **Options**: "KG", "TONS", "METERS", "UNITS"
- ✅ **Examples**:
  - "KG" (kilograms)
  - "TONS" (metric tons)
  - "METERS" (length)
  - "UNITS" (individual pieces)

### **7. Rate**
- ✅ **Type**: Numbers only (positive)
- ✅ **Range**: 0.01 to 10,000
- ✅ **Decimal**: 2 decimal places maximum
- ✅ **Examples**:
  - "250.50"
  - "1000"
  - "75.25"
  - "5000.99"
- ❌ **Invalid**: "0", "-100", "abc", "10000.01"

### **8. Payment Status**
- ✅ **Type**: Dropdown selection
- ✅ **Options**: "Paid", "Unpaid", "Partial"
- ✅ **Auto-calculated**: Based on paid amount vs total
- ✅ **Examples**:
  - "Paid" (if paid amount >= total)
  - "Unpaid" (if paid amount = 0)
  - "Partial" (if paid amount < total)

### **9. Paid Amount**
- ✅ **Type**: Numbers only (positive or zero)
- ✅ **Range**: 0 to any amount
- ✅ **Decimal**: 2 decimal places maximum
- ✅ **Auto-calculates**: Balance and payment status
- ✅ **Examples**:
  - "0" (unpaid)
  - "5000.50"
  - "10000"
  - "25000.75"

### **10. Remarks**
- ✅ **Type**: Any text (optional)
- ✅ **Length**: Maximum 500 characters
- ✅ **Characters**: Any characters allowed
- ✅ **Examples**:
  - "Payment received via bank transfer"
  - "Quality check passed"
  - "Urgent delivery required"
  - "" (empty/blank)

---

## 🎯 **SALES FORM FIELDS**

### **1. Customer Name**
- ✅ **Type**: Any text (free typing)
- ✅ **Length**: Any length (no minimum/maximum)
- ✅ **Characters**: Letters, numbers, spaces, special characters
- ✅ **Examples**:
  - "A" (single character)
  - "John Customer"
  - "ABC Garments Ltd."
  - "Customer #456"
  - "Very Long Customer Name Inc."

### **2. Invoice Number**
- ✅ **Type**: Uppercase letters, numbers, hyphens only
- ✅ **Format**: Must match pattern: `^[A-Z0-9\-]+$`
- ✅ **Examples**:
  - "SAL001"
  - "SALE-2024-001"
  - "INV12345"
  - "CUSTOMER-001"

### **3. Date**
- ✅ **Type**: Date picker or text input
- ✅ **Format**: YYYY-MM-DD
- ✅ **Range**: Any date up to today
- ✅ **Examples**:
  - "2024-03-27"
  - "2024-01-15"

### **4. Product Name**
- ✅ **Type**: Any text (free typing)
- ✅ **Length**: Any length (no minimum/maximum)
- ✅ **Characters**: Letters, numbers, spaces, special characters
- ✅ **Examples**:
  - "Cotton Yarn 40"
  - "Polyester Yarn"
  - "Custom Product"
  - "Finished Fabric"
  - "Special Blend"

### **5. Product Type**
- ✅ **Type**: Dropdown selection
- ✅ **Options**: "Finished Product", "Yarn", "Raw Material"
- ✅ **Examples**:
  - "Finished Product" (completed goods)
  - "Yarn" (raw material)
  - "Raw Material" (unprocessed)

### **6. Quantity, Unit, Rate**
- ✅ **Same rules**: As purchase form
- ✅ **Same examples**: As purchase form

### **7. Payment Status, Paid Amount, Remarks**
- ✅ **Same rules**: As purchase form
- ✅ **Same examples**: As purchase form

---

## 🎮 **PRACTICAL EXAMPLES**

### **Example 1: Simple Purchase**
```
Supplier: "A"
Invoice: "PUR001"
Date: "2024-03-27"
Yarn Type: "Cotton Yarn 40"
Quantity: "100"
Unit: "KG"
Rate: "250.50"
Paid Amount: "10000"
Remarks: "Regular purchase"
```

### **Example 2: Complex Sale**
```
Customer: "XYZ Garments Ltd."
Invoice: "SALE-2024-001"
Date: "2024-03-27"
Product Name: "Special Blend Yarn"
Product Type: "Finished Product"
Quantity: "500"
Unit: "METERS"
Rate: "75.25"
Paid Amount: "25000"
Remarks: "Premium quality delivery"
```

### **Example 3: Minimal Entry**
```
Supplier: "B"
Invoice: "INV1"
Date: "2024-03-27"
Yarn Type: "Y"
Quantity: "1"
Unit: "UNITS"
Rate: "0.01"
Paid Amount: "0"
Remarks: ""
```

---

## 🎉 **KEY TAKEAWAYS**

### **Flexible Fields** (Free Typing):
- ✅ **Supplier Name**: Any text
- ✅ **Customer Name**: Any text
- ✅ **Yarn Type**: Any text
- ✅ **Product Name**: Any text
- ✅ **Remarks**: Any text (optional)

### **Structured Fields** (Specific Format):
- ✅ **Invoice Number**: Uppercase, numbers, hyphens only
- ✅ **Date**: YYYY-MM-DD format
- ✅ **Quantity**: 1-10,000, whole numbers
- ✅ **Rate**: 0.01-10,000, 2 decimals
- ✅ **Unit**: KG, TONS, METERS, UNITS
- ✅ **Product Type**: Finished Product, Yarn, Raw Material

### **Auto-Calculated Fields**:
- ✅ **Total**: Quantity × Rate
- ✅ **Balance**: Total - Paid Amount
- ✅ **Payment Status**: Based on paid vs total

---

## 🌐 **TRY IT NOW!**

```
🔗 http://localhost:5173
👤 Username: admin
🔑 Password: admin123
```

**Test different combinations of inputs - the system accepts all the examples above!** 🎉
