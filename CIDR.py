import boto3
import time
 
 
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = 'Vikastable'  
table = dynamodb.Table(table_name)
 
# Set up EC2 resource
ec2 = boto3.resource('ec2', region_name='us-east-1')
 
def fetch_next_available_cidr_and_create_vpc():
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('Status').eq('Available')
    )
 
    # Get the first available item
    items = response.get('Items', [])
    if items:
        # Sort items based on 'Sr.NO' in ascending order
        sorted_items = sorted(items, key=lambda x: x['Sr.NO'])
        item = sorted_items[0]
 
        # Extract CIDR from the DynamoDB item
        cidr_range = item.get('CIDR')
 
        try:
            # Update DynamoDB item status to 'In-Progress'
            update_dynamodb_status(item['Sr.NO'], 'In-Progress')
 
            
            time.sleep(10)
 
            # Create VPC
            vpc = ec2.create_vpc(CidrBlock=cidr_range)
 
            
            time.sleep(5)
 
            # Update DynamoDB item status to 'In-Use' after successful creation
            update_dynamodb_status(item['Sr.NO'], 'In-Use')
 
            print(f"VPC created with CIDR: {cidr_range}")
        except Exception as e:
            # If VPC creation fails, update status back to 'Available'
            print(f"VPC creation failed with error: {str(e)}")
            update_dynamodb_status(item['Sr.NO'], 'Available')
    else:
        print("No available CIDR found in the DynamoDB table.")
 
def update_dynamodb_status(sr_no, new_status):
    table.update_item(
        Key={'Sr.NO': sr_no},
        UpdateExpression="SET #status = :new_status",
        ExpressionAttributeNames={'#status': 'Status'},
        ExpressionAttributeValues={':new_status': new_status},
        ReturnValues="UPDATED_NEW"
    )
 
if __name__ == "__main__":
    fetch_next_available_cidr_and_create_vpc()
