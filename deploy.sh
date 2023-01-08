#!/bin/bash
sflag=false
nflag=false
pflag=false
eflag=false

export AWS_DEFAULT_REGION=us-east-1

DIRNAME=$(pwd)

usage () { echo "
    -h -- Opens up this help message
    -n -- Name of the CloudFormation stack
    -p -- Name of the AWS profile to use
    -s -- Name of S3 bucket to upload artifacts to
    -e -- Name of the environment that will be deployed
"; }
options=':e:n:p:s:h'
while getopts "$options" option
do
    case "$option" in
        n  ) nflag=true; STACK_NAME=$OPTARG;;
        p  ) pflag=true; PROFILE=$OPTARG;;
        s  ) sflag=true; S3_BUCKET=$OPTARG;;
        e  ) eflag=true; ENV=$OPTARG;;
        h  ) usage; exit;;
        \? ) echo "Unknown option: -$OPTARG" >&2; exit 1;;
        :  ) echo "Missing option argument for -$OPTARG" >&2; exit 1;;
        *  ) echo "Unimplemented option: -$OPTARG" >&2; exit 1;;
    esac
done

echo "Environment: $ENV"

if ! "$pflag"
then
    echo "-p not specified, using default..." >&2
    PROFILE="default"
fi
if ! "$sflag"
then
    S3_BUCKET=$(sed -e 's/^"//' -e 's/"$//' <<<"$(aws ssm get-parameter --name /SDLF/S3/CFNBucket --profile "$PROFILE" --query "Parameter.Value")")
fi
if ! "$nflag"
then
    STACK_NAME="MasterProjectStack"
fi

if ! "$eflag"
then
    if [ "$ENV" == "dev" ] || [ "$ENV" == "test" ] || [ "$ENV" == "prod" ]; then
        echo "Environment to deploy $ENV ..." >&2
    else 
        echo "Environment value is not correct!. Use (dev, test, prod)..." >&2
        exit 1
    fi
fi


echo "Checking if bucket exists ..."
if ! aws s3 ls "$S3_BUCKET" --profile "$PROFILE"; then
  echo "S3 bucket named $S3_BUCKET does not exist. Create? [Y/N]"
  read -r choice
  if [ "$choice" == "Y" ] || [ "$choice" == "y" ]; then
    aws s3 mb s3://"$S3_BUCKET" --profile "$PROFILE"
  else
    echo "Bucket does not exist. Deploy aborted."
    exit 1
  fi
fi

mkdir "$DIRNAME"/output
sam package --profile "$PROFILE" --template-file "$DIRNAME"/2-stacks/template.yaml --s3-bucket "$S3_BUCKET" --s3-prefix foundations --output-template-file "$DIRNAME"/output/packaged-template.yaml

echo "Checking if stack exists ..."
if ! aws cloudformation describe-stacks --profile "$PROFILE" --stack-name "$STACK_NAME"; then
  echo -e "Stack does not exist, creating ..."
  aws cloudformation create-stack \
    --stack-name "$STACK_NAME" \
    --parameters file://"$DIRNAME/2-stacks/parameters/parameters-$ENV".json \
    --template-body file://"$DIRNAME"/output/packaged-template.yaml \
    --capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" \
    --profile "$PROFILE"

  echo "Waiting for stack to be created ..."
  aws cloudformation wait stack-create-complete --profile "$PROFILE" \
    --stack-name "$STACK_NAME"
else
  echo -e "Stack exists, attempting update ..."

  set +e
  update_output=$( aws cloudformation update-stack \
    --profile "$PROFILE" \
    --stack-name "$STACK_NAME" \
    --parameters file://"$DIRNAME/2-stacks/parameters/parameters-$ENV".json \
    --template-body file://"$DIRNAME"/output/packaged-template.yaml \
    --capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND" 2>&1)
  status=$?
  set -e

  echo "$update_output"

  if [ "$status" -ne 0 ] ; then
    # Don't fail for no-op update
    if [[ $update_output == *"ValidationError"* && $update_output == *"No updates"* ]] ; then
      echo -e "\nFinished create/update - no updates to be performed";
      exit 0;
    else
      exit "$status"
    fi
  fi

  echo "Waiting for stack update to complete ..."
  aws cloudformation wait stack-update-complete --profile "$PROFILE" \
    --stack-name "$STACK_NAME" 
  echo "Finished create/update successfully!"
fi
