CWD=$(pwd)
packages=$(pip freeze | sed -E "s/=.*//")
echo "Removing old zip if present"
rm function.zip
echo "Zipping lambda and dependencies..."
cd venv/lib/python3.7/site-packages/
for package in $packages
do
  zip -r "${CWD}/function.zip" "$package"/*
done
cd $CWD
zip -r "${CWD}/function.zip" *.py
echo "Updating function in AWS"

aws lambda update-function-code --profile sts --region eu-west-2 --function-name slack-bamboo-confirmation-dev --zip-file fileb://function.zip