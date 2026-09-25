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
