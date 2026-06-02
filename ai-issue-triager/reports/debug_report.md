## Bug Summary

The payment module crashes with a NameError due to a misspelled function name. The code attempts to call `proces_payment` instead of `process_payment`, causing the Python interpreter to raise a NameError because the function with the incorrect spelling doesn't exist.

## Root Cause

The root cause is a simple typographical error in the function call within the payment module. The developer mistakenly typed `proces_payment` (missing the 'c') instead of `process_payment`, resulting in an undefined name error during runtime.

## Technical Explanation

When Python executes the code, it encounters the line `print(proces_payment(100))`. Since there is no function named `proces_payment` defined anywhere in the scope, Python raises a NameError exception indicating that the name `proces_payment` is not defined. This occurs because the function `process_payment` was defined earlier in the code but was called with a different (incorrect) spelling.

## Suggested Fix

The fix is straightforward: correct the function name in the call from `proces_payment` to `process_payment` to match the actual function definition.

## Corrected Code

```python
def process_payment(amount):
    return amount

print(process_payment(100))
```

## Patch Diff

```diff
--- src/payment.py
+++ src/payment.py
@@ -3,4 +3,4 @@
 def process_payment(amount):
     return amount

-print(proces_payment(100))
+print(process_payment(100))
```