# flask address api
- clone repo 
- install dependencies: `pip3 install -r requirements.txt`
- run application:  `uvicorn main:app --reload`
- open swagger ui in browser: http://127.0.0.1:8000/docs
- save few addresses in database using create address api in swagger ui
- take below paylaod examples for create address: 

```
{
  "name": "Koramangala, Bengaluru, India",
  "lat": 12.9352,
  "long": 77.6245
}
```

```
{
  "name": "HSR Layout, Bengaluru, India",
  "lat": 12.9121,
  "long": 77.6446
}
```


```
{
  "name": "Andheri, Mumbai, India",
  "lat": 19.1136,
  "long": 72.8697
}
```

- Now run read address api in swagger ui, it should show all the 3 addresses
- Now go to nearby_addresses api and 
    - enter the latitute, longitute of 1st address (12.9352, 77.6245) and radius 0.1 (km)
    - it should show only one address in response
    - now change the radius to 10 (km), it will show both the bengaluru addresses in response
    - now change the radius to 1200, it will show all the 3 address, cause all are in range of 1000 km