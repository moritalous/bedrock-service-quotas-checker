
# Amazon Bedrock Service Quotas Checker

This tool helps you check Amazon Bedrock service quotas across different AWS regions. It provides information about both current and default quotas for InvokeModel requests and tokens per minute.

## Features

- Check Bedrock service quotas in:
  - Single region (default: your current AWS region)
  - Multiple specified regions
  - All available regions where Bedrock is available
- Compare current quotas with AWS default values
- Focus on important metrics:
  - Requests per minute for InvokeModel
  - Tokens per minute for InvokeModel

## Prerequisites

- AWS credentials configured (via AWS CLI, environment variables, or IAM role)
- (If not using AWS CloudShell) Python 3.x and `boto3` package

**Note:** When using this tool in AWS CloudShell, `boto3` is already installed, so additional installations via `pip` are unnecessary.

## Installation

### Running in AWS CloudShell

1. Clone this repository:
   ```bash
   git clone https://github.com/moritalous/bedrock-service-quotas-checker.git
   cd bedrock-service-quotas-checker
   ```

2. **No additional installation required in AWS CloudShell** because `boto3` is pre-installed.

### Running in Other Environments

If you are not using AWS CloudShell, you will need to install `boto3` as follows:

1. Clone this repository:
   ```bash
   git clone https://github.com/moritalous/bedrock-service-quotas-checker.git
   cd bedrock-service-quotas-checker
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage (Current Region)

In AWS CloudShell or other environments:
```bash
python check_quotas.py
```

### Check Specific Regions

Specify one or more regions:
```bash
python check_quotas.py --regions us-east-1,us-west-2,ap-northeast-1
```

### Check All Available Regions

To check quotas in all regions where Bedrock is available:
```bash
python check_quotas.py --all-region
```

## Output Format

The output is displayed in the following format:
```
{quota_type} | {quota_name} | {current_value} | {default_value} | {region} | {quota_code}
```

Example:
```
requests per minute | On-demand InvokeModel requests per minute for Anthropic Claude | 10 | 5 | us-east-1 | L-A8BAF44F
tokens per minute | On-demand InvokeModel tokens per minute for Anthropic Claude | 100000 | 50000 | us-east-1 | L-D40B4EF2
```

## Error Handling

- If a region is not available or doesn't have Bedrock service, it will be silently skipped
- Invalid region names will be ignored
- If AWS credentials are not configured, the script will fail with appropriate AWS SDK error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is not officially associated with Amazon Web Services (AWS). Please use it responsibly and be aware of any API rate limits in your AWS account.
