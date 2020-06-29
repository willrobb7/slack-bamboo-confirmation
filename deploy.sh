CWD=$(pwd)

echo "Removing old zip if present"
rm function.zip

echo "Zipping lambda and dependencies..."
cd venv/lib/python3.7/site-packages/
zip -r "${CWD}/function.zip" */*
cd $CWD

zip -r "${CWD}/function.zip" *.py message_format.json
echo "Updating function in AWS"

aws lambda update-function-code --profile sts --region eu-west-2 --function-name slack-bamboo-confirmation-dev --zip-file fileb://function.zip
aws lambda update-function-code --profile sts --region eu-west-2 --function-name slack-bamboo-callback-dev --zip-file fileb://function.zip
