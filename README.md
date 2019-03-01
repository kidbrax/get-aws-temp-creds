This script will read creds for a given profile from your ~/.aws/credentials file and then get temp session creds and then write those back out to your ~/.aws/credentials file with a '-temp' extension on the profile name.

To run and get temp creds for a profile named testacct:
`get-temp-creds.py testacct`

This is what your .aws/credentials will look like before and after:

Before:
```
[testacct]
aws_access_key_id = 11111222223333344444
aws_secret_access_key = adsfaewradsfqweradsfqewrasfqwerasfqwerfr
```

After running get-temp-creds.py:
```
[testacct]
aws_access_key_id = 11111222223333344444
aws_secret_access_key = adsfaewradsfqweradsfqewrasfqwerasfqwerfr

[testacct-temp]
aws_access_key_id = ASIA2ALERURSIMIZ77FL
aws_secret_access_key = wXfPeN7veAQ/897QVPfo+HtBEs8T9/ZQGp6n15rE
aws_session_token = FQoGZXIvYXdzEIz//////////wEaDChnQBbE0AFak5I/3yKwAQRG7aFjONqDI9gz9AaX/7L8iORM9kYl+7eGK6kfRuks4AzT/IeqYsaUS0knO4UqU9HxBeAZFuffnccazq6I5zC+7lVSZ/W8wQrWVkH1rByaNq80dfPN/9CaL/+3aor1csDa9yBnGkUAkf9NsXHgvWrPhCkCCLfNoTqoLlP4O/BNPccg7O8cru1kk9NnCcC7t++oYnUMmi3akNPU191r+qxvQNAEMp2VOTiMVDD8TBsGKNqg0d8F
expires = 2018-11-21 06:20:10+00:00
```

And every time you run the script, it will just replace the temp section with new creds.

So a typical AWS command using a profile name of testacct would look like this:
```
aws cloudformation create-stack \
    --stack-name my-stack-name \
    --template-body file://my-template.yaml \
    --profile testacct-temp
```