## Requirements

### AWS Services

#### Cognito
In [Amazon Cognito](https://docs.aws.amazon.com/cognito/) create new user pool. In configure form select options as bellow:
1. Step 1
   1. Provider types: `Cognito user pool`
   2. Cognito user pool sign-in options: `Email` only
2. Step 2
   1. Password policy mode: up to you
   2. Multi-factor authentication: `No MFA`
   3. User account recovery: Disable `Enable self-service account recovery` option
3. Step 3
   1. No changes
4. Step 4
   1. Email provider: `Send email with Cognito`
5. Step 5
   1. User pool name: Enter pool name - name up to you
   2. Initial app client - App client name - Enter app name - name up to you
   3. Client secret - Select `Generate a client secret`
   4. Advanced app client settings - Authentication flows - add `ALLOW_USER_PASSWORD_AUTH`


After creating user pool open it, and and save `User pool ID` - it will be required later

Also in `App integration` tab, open created integration from `App clients and analytics` section, and save values for `Client ID` and  `Client secret`

#### S3 Bucket
Create new AWS S3 bucket which will be used to save data files

#### DynamoDB
Create new DynamoDB table which will be used to save informatoins about requests

#### SQS
Create new SQS queue which will be used to communicate between application parts

# ENV file
Create `.env` file from a copy of `.env.tempalte` file and set values for variables:
1. `AWS_S3_REGION` - Region of your AWS instance, eg. `eu-central-1`
2. `AWS_S3_BUCKET` - Name of your AWS S3 bucket
3. `AWS_DYNAMODB_TABLE_NAME` - Name of your DynamoDB Table
4. `AWS_SQS_QUEUE_NAME` - Name of your AWS SQS queue
5. `AWS_COGNITO_CLIENT_ID` - Cognito Client ID saved in instruction above
6. `AWS_COGNITO_CLIENT_SECRET` - Cognito Client Secret saved in instruction above
7. `AWS_COGNITO_USER_POOL_ID` - Cognito User Pool ID saved in instruction above
8. `AWS_ACCESS_KEY_ID` - AWS Access key used to communicate with AWS API
9. `AWS_SECRET_ACCESS_KEY` - AWS Secret Access key used to communicate with AWS API

# Running app locally

To start app locally, you need to have `Node v18` and `yarn` package manager on your machine

#### Install dependencies
`yarn install`

#### Start app
`yarn start:dev`
