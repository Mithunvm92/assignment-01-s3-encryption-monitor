# Assignment 1 – Monitor Unencrypted S3 Buckets

## Objective

Create an AWS Lambda function using Python and Boto3 to identify Amazon S3 buckets that do not have server-side encryption enabled.

The Lambda function:

- Lists all S3 buckets in the AWS account.
- Checks the server-side encryption configuration of each bucket.
- Identifies encrypted and unencrypted buckets.
- Prints the results to CloudWatch Logs.
- Returns a summary of the encryption status.

---

## AWS Services Used

- AWS Lambda
- Amazon S3
- AWS IAM
- Amazon CloudWatch Logs

---

## Architecture

```text
                AWS Lambda
                    |
                    | Boto3
                    v
              Amazon S3
                    |
          +---------+---------+
          |                   |
     List Buckets       Check Encryption
          |                   |
          +---------+---------+
                    |
                    v
             Encryption Report
                    |
                    v
           CloudWatch Logs
```

---

## Prerequisites

- AWS account
- Permission to create Lambda functions
- Permission to create IAM roles and policies
- At least one S3 bucket in the AWS account
- Python 3.x runtime supported by AWS Lambda

---

# Step 1 – Create S3 Bucket

An S3 bucket was created for testing the Lambda function.

Example:

```text
lambda-encryption-test-<unique-name>
```

The S3 bucket was used as part of the encryption-status verification.

> **Note:** Amazon S3 may have server-side encryption enabled by default depending on the bucket configuration and AWS account behavior.

---

# Step 2 – Create IAM Role

An IAM execution role was created for the Lambda function.

Example role:

```text
monitor-unencrypted-s3-buckets-role
```

The role allows Lambda to:

- List S3 buckets
- Read the encryption configuration of S3 buckets

## IAM Policy

The following inline policy was attached to the Lambda execution role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListAndCheckS3Buckets",
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets",
        "s3:GetEncryptionConfiguration"
      ],
      "Resource": "*"
    }
  ]
}
```

### Permission Description

| Permission | Purpose |
|---|---|
| `s3:ListAllMyBuckets` | Allows Lambda to retrieve the list of S3 buckets |
| `s3:GetEncryptionConfiguration` | Allows Lambda to check the encryption configuration of each bucket |

---

# Step 3 – Create Lambda Function

A Lambda function was created with the following configuration:

| Configuration | Value |
|---|---|
| Function Name | `monitor-unencrypted-s3-buckets` |
| Runtime | Python 3.x |
| Architecture | x86_64 |
| Execution Role | `monitor-unencrypted-s3-buckets-role` |

---

# Step 4 – Lambda Function Code

The Lambda function uses Boto3 to list S3 buckets and check their encryption configuration.

```python
import boto3
from botocore.exceptions import ClientError


s3 = boto3.client("s3")


def lambda_handler(event, context):

    unencrypted_buckets = []
    encrypted_buckets = []

    response = s3.list_buckets()

    for bucket in response.get("Buckets", []):
        bucket_name = bucket["Name"]

        try:
            encryption = s3.get_bucket_encryption(
                Bucket=bucket_name
            )

            encrypted_buckets.append(bucket_name)

            print(
                f"ENCRYPTED: {bucket_name}"
            )

        except ClientError as error:

            error_code = error.response["Error"]["Code"]

            if error_code == "ServerSideEncryptionConfigurationNotFoundError":
                unencrypted_buckets.append(bucket_name)

                print(
                    f"UNENCRYPTED: {bucket_name}"
                )

            else:
                print(
                    f"ERROR checking {bucket_name}: "
                    f"{error_code}"
                )

    print("\n===== S3 ENCRYPTION REPORT =====")

    print(
        f"Encrypted buckets: {len(encrypted_buckets)}"
    )

    print(
        f"Unencrypted buckets: {len(unencrypted_buckets)}"
    )

    print("\nUnencrypted buckets:")

    for bucket in unencrypted_buckets:
        print(f"- {bucket}")

    return {
        "statusCode": 200,
        "encrypted_buckets": encrypted_buckets,
        "unencrypted_buckets": unencrypted_buckets
    }
```

---

# Step 5 – Test Configuration

A test event was created in AWS Lambda.

### Test Event

```json
{}
```

### Test Event Name

```text
test-s3-encryption-monitor
```

The Lambda function was manually invoked using this test event.

---

# Step 6 – Execution Result

The Lambda function executed successfully.

### Example Output

```text
===== S3 ENCRYPTION REPORT =====
Encrypted buckets: 2
Unencrypted buckets: 0

Unencrypted buckets:
```

The actual output depends on the S3 buckets available in the AWS account at the time of execution.

### Lambda Response

The Lambda response contains the encryption status lists:

```json
{
  "statusCode": 200,
  "encrypted_buckets": [
    "example-bucket"
  ],
  "unencrypted_buckets": []
}
```

---

# Step 7 – CloudWatch Logs

AWS Lambda automatically sends the function's output to Amazon CloudWatch Logs.

The logs can be viewed from:

```text
AWS Console
    ↓
Lambda
    ↓
monitor-unencrypted-s3-buckets
    ↓
Monitor
    ↓
View CloudWatch logs
```

The logs show which buckets were detected as encrypted or unencrypted.

---

# Testing

The Lambda function was tested by manually invoking it from the AWS Lambda console.

## Test Case

### Input

```json
{}
```

### Expected Behavior

The function should:

1. Retrieve the list of S3 buckets.
2. Check each bucket's encryption configuration.
3. Report encrypted buckets.
4. Report unencrypted buckets.
5. Return a successful Lambda response.

### Result

```text
Lambda execution: SUCCESS
```

---

# Troubleshooting

## AccessDenied – ListBuckets

During initial testing, the Lambda function returned an `AccessDenied` error for:

```text
s3:ListAllMyBuckets
```

The issue was resolved by adding the following permissions to the Lambda execution role:

```text
s3:ListAllMyBuckets
s3:GetEncryptionConfiguration
```

After updating the IAM policy, the Lambda function executed successfully.

---

# Screenshots

The following screenshots can be included as evidence for the assignment.

## 1. S3 Bucket

Show the S3 bucket created for testing.

Save as:

```text
screenshots/01-s3-bucket.png
```

---

## 2. IAM Role

Show the Lambda execution role and its S3 permissions.

Save as:

```text
screenshots/02-iam-policy.png
```

---

## 3. Lambda Configuration

Show the Lambda function name and Python runtime.

Save as:

```text
screenshots/03-lambda-configuration.png
```

---

## 4. Lambda Source Code

Show the deployed Lambda Python code.

Save as:

```text
screenshots/04-lambda-code.png
```

---

## 5. Successful Test

Show the successful Lambda test execution.

Save as:

```text
screenshots/05-lambda-test-success.png
```

---

## 6. CloudWatch Logs

Show the S3 encryption report in CloudWatch Logs.

Save as:

```text
screenshots/06-cloudwatch-logs.png
```

---

# Project Structure

```text
assignment-01-s3-encryption-monitor/
│
├── lambda_function.py
├── README.md
│
└── screenshots/
    ├── 01-s3-bucket.png
    ├── 02-iam-policy.png
    ├── 03-lambda-configuration.png
    ├── 04-lambda-code.png
    ├── 05-lambda-test-success.png
    └── 06-cloudwatch-logs.png
```

---

# Conclusion

This assignment demonstrates the use of AWS Lambda and Boto3 to automate S3 encryption monitoring.

The solution retrieves S3 buckets, checks their server-side encryption configuration, identifies unencrypted buckets, and records the results in CloudWatch Logs.
