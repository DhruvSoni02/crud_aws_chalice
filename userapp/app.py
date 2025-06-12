from chalice import Chalice, Response
import boto3
import uuid

app = Chalice(app_name='userapp')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')  # DynamoDB table name

@app.route('/users', methods=['POST'])
def create_user():
    data = app.current_request.json_body

    user_id = str(uuid.uuid4())
    item = {
        'user_id': user_id,
        'name': data['name'],
        'email': data['email'],
        'age': int(data['age'])
    }

    table.put_item(Item=item)
    return {'message': 'User created', 'user_id': user_id}

@app.route('/users/{user_id}', methods=['GET'])
def get_user(user_id):
    response = table.get_item(Key={'user_id': user_id})
    item = response.get('Item')
    if item:
        return item
    return Response(body={'error': 'User not found'}, status_code=404)

@app.route('/users/{user_id}', methods=['PUT'])
def update_user(user_id):
    data = app.current_request.json_body

    response = table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET #nm = :n, email = :e, age = :a',
        ExpressionAttributeNames={'#nm': 'name'},
        ExpressionAttributeValues={
            ':n': data['name'],
            ':e': data['email'],
            ':a': int(data['age'])
        },
        ReturnValues='UPDATED_NEW'
    )

    return {'message': 'User updated', 'updated': response['Attributes']}

@app.route('/users/{user_id}', methods=['DELETE'])
def delete_user(user_id):
    table.delete_item(Key={'user_id': user_id})
    return {'message': 'User deleted'}
