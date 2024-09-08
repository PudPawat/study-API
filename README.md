# study-API
### requirement 
`pip install fastapi uvicorn`

### running API 
`uvicorn main:app --reload`

#### How the API Works:
GET /get-coupon/: Returns one available coupon code and removes it from the list. If no coupons are available, it returns a 404 error.

GET /remaining-coupons/: Returns the number of remaining coupons in the list.

POST /add-coupon/:  Add random coupons follow amount
- Body `{ amount: {:number} }`