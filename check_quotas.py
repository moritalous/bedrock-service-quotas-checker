import argparse

import boto3


def get_region_names():
    """
    Retrieve a list of AWS regions where Amazon Bedrock service is available.

    Returns:
        list: A list of region names (strings) where Amazon Bedrock is available.
    """
    return boto3.Session().get_available_regions("bedrock")


def get_all_service_quotas(client, service_code: str):
    """
    Retrieve all service quotas for a specified AWS service, handling pagination.

    Args:
        client: boto3 service-quotas client instance
        service_code (str): The AWS service code to query (e.g., 'bedrock')

    Returns:
        list: A list of dictionaries containing quota information for the service.
        Each dictionary contains quota details like QuotaName, QuotaCode, and Value.
    """
    service_quotas = []

    # Get first page of results
    response = client.list_service_quotas(ServiceCode=service_code, MaxResults=100)
    service_quotas.extend(response["Quotas"])

    # Continue fetching remaining pages if they exist
    while "NextToken" in response:
        response = client.list_service_quotas(
            ServiceCode=service_code, MaxResults=100, NextToken=response["NextToken"]
        )
        service_quotas.extend(response["Quotas"])

    return service_quotas


def get_all_aws_default_service_quotas(client, service_code: str):
    """
    Retrieve all default AWS service quotas for a specified service, handling pagination.

    Args:
        client: boto3 service-quotas client instance
        service_code (str): The AWS service code to query (e.g., 'bedrock')

    Returns:
        list: A list of dictionaries containing default quota information.
        Each dictionary contains quota details including the default values.
    """
    service_quotas = []

    # Get first page of default quotas
    response = client.list_aws_default_service_quotas(
        ServiceCode=service_code, MaxResults=100
    )
    service_quotas.extend(response["Quotas"])

    # Continue fetching remaining pages if they exist
    while "NextToken" in response:
        response = client.list_aws_default_service_quotas(
            ServiceCode=service_code, MaxResults=100, NextToken=response["NextToken"]
        )
        service_quotas.extend(response["Quotas"])

    return service_quotas


def get_service_quotas(region: str, service_code: str):
    """
    Get both current and default service quotas for a specific region and service.
    Combines the information and enriches it with region and default value data.

    Args:
        region (str): AWS region name (e.g., 'us-east-1')
        service_code (str): The AWS service code to query (e.g., 'bedrock')

    Returns:
        list: A list of dictionaries containing enriched quota information.
        Each dictionary includes current values, default values, and region information.
    """
    # Create a service-quotas client for the specified region
    client = boto3.Session(region_name=region).client("service-quotas")
    service_quotas = []

    try:
        # Get both current and default quotas
        service_quotas = get_all_service_quotas(
            client=client, service_code=service_code
        )
        aws_default_service_quotas = get_all_aws_default_service_quotas(
            client=client, service_code=service_code
        )

        # Enrich each quota with its default value and region information
        for quota in service_quotas:
            default_value = list(
                filter(
                    lambda x: x["QuotaCode"] == quota["QuotaCode"],
                    aws_default_service_quotas,
                )
            )[0]["Value"]

            quota["DefaultValue"] = default_value
            quota["Region"] = region
    except Exception as e:
        pass

    return service_quotas


def print_service_quotas(service_quotas: list):
    """
    Print formatted service quota information, focusing on InvokeModel quotas.

    Args:
        service_quotas (list): List of service quota dictionaries to process and print.
            Each dictionary should contain quota details including QuotaName, Value,
            DefaultValue, Region, and QuotaCode.

    Prints:
        Formatted strings containing quota information for both 'requests per minute'
        and 'tokens per minute' quotas. Output format:
        "{key} | {QuotaName} | {Value} | {DefaultValue} | {Region} | {QuotaCode}"
    """
    # Process each type of quota separately
    for key in ["requests per minute", "tokens per minute"]:
        # Filter quotas by type
        items = list(
            filter(
                lambda x: str(x["QuotaName"]).startswith(
                    f"On-demand InvokeModel {key}"
                ),
                service_quotas,
            )
        )

        # Sort items by quota name
        items.sort(key=lambda x: x["QuotaName"])

        # Print each quota's details in a formatted string
        for item in items:
            item["key"] = key
            print(
                "{key} | {QuotaName} | {Value} | {DefaultValue} | {Region} | {QuotaCode} ".format(
                    **item
                )
            )


if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(
        description="Retrieve and display Amazon Bedrock service quotas across AWS regions."
    )
    parser.add_argument(
        "--regions",
        required=False,
        default=None,
        help="Comma-separated list of AWS regions to check",
    )
    parser.add_argument(
        "--all-region",
        required=False,
        default=False,
        action="store_true",
        help="Check quotas in all available regions",
    )
    args = parser.parse_args()

    # Determine which regions to process
    region_list = [boto3.Session().region_name]  # Default to current region
    if args.all_region:
        region_list = get_region_names()  # Get all available regions
    elif args.regions:
        region_list = [
            x.strip() for x in args.regions.split(",")
        ]  # Use specified regions

    service_code = "bedrock"

    print("Quota type | Quota name | Applied account-level quota value | AWS default quota value | Region | Quota code")

    # Process and print quotas for each region
    for region in region_list:
        service_quotas = get_service_quotas(region=region, service_code=service_code)
        print_service_quotas(service_quotas=service_quotas)
