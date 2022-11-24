# API Doc

## Sign In
> /signin
- POST
- param:
  - name
  - phone


## Get Exam Paper
> /getpaper
- GET
  - return
    ```json
    {
       "code":1,
       "message":"Success",
       "data":{
          "uid":"66afc201-7552-45d0-881f-8b448e991694",
          "start":"2022-11-24T10:41:12.773Z",
          "end":"2022-11-24T10:41:12.773Z",
          "paper1":{
             "uid":"b2e47632-30b0-4c68-95c1-86853bdbb6eb",
             "content":"aa a a"
          },
          "paper2":{
             "uid":"b2e47632-30b0-4c68-95c1-86853bdbb6eb",
             "content":"aa a a"
          }
       }
    }
    ```
    
## Submit Paper
> /submitpaper
- POST
- param
  - paper1
  - paper2

## Error

|Code|Message|
|-|-|
|0|General Error|
|1|Success|
|10001|User is not listed or not matched with phone number|
|10002|Login again|
|10003|This user don't enroll any exam|