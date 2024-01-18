import boto3
import ipaddress
 
# Set up the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
 
# Define the table name and attributes
table_name = 'Vikastable'
key_schema = [{'AttributeName': 'Sr.NO', 'KeyType': 'HASH'}]  # Primary key
attribute_definitions = [{'AttributeName': 'Sr.NO', 'AttributeType': 'N'}]  # Attribute definition
 
# Create the table
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
 
    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(f"Table '{table_name}' created successfully.")
 
    # Add items with Sr.NO values in order (1 to 10) and different CIDR ranges
    with table.batch_writer() as batch:
        for sr_no in range(1, 11):
            cidr_range = f'10.0.{sr_no}.0/24'
            item = {
                'Sr.NO': sr_no,
                'CIDR': cidr_range,
                'Status': 'Available'
            }
            batch.put_item(Item=item)
 
    print("Items added successfully.")
 
except Exception as e:
    print(f"Error: {e}")
