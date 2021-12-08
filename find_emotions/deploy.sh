#Change aws_region and aws_account_id to run on each account
# account id: in aws console click support>support cente> number appears on the left
# Set variables
img_name='find-emotions'
aws_region=us-east-1
aws_account_id=873725303363

#HAcemos el update y construimos la imagen de docker

docker build -t $img_name .
docker tag $img_name $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$img_name
aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com

docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$img_name
