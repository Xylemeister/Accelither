import boto3
from botocore.exceptions import ClientError
import logging

MY_REGION_NAME = 'eu-west-2'

def update_high_score(player_id, new_score, dynamodb=None):
    """Update the high score for a player if the new score is higher."""
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb', region_name=MY_REGION_NAME)

    table = dynamodb.Table('Leaderboard')

    # Attempt to get the current high score for the player
    try:
        response = table.get_item(Key={'PlayerId': player_id})
        current_high_score = response.get('Item', {}).get('HighScore', 0)
    except ClientError as e:
        logging.error(e)
        return None

    # Update the high score if the new score is higher
    if new_score > current_high_score:
        try:
            response = table.update_item(
                Key={'PlayerId': player_id},
                UpdateExpression="set HighScore = :s",
                ExpressionAttributeValues={':s': new_score},
                ReturnValues="UPDATED_NEW"
            )
            return response
        except ClientError as e:
            logging.error(e)
            return None
        
        
def add_death(player_id, region_name=MY_REGION_NAME):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table('Leaderboard')

    try:
        response = table.update_item(
            Key={'PlayerId': player_id},
            UpdateExpression="set Death = Death + :increment",
            ExpressionAttributeValues={':increment': 1 },
            ReturnValues="UPDATED_NEW"
        )
        return response  
    except ClientError as e:
        logging.error(e)
        return None
    
def add_kill(player_id, region_name=MY_REGION_NAME):
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table('Leaderboard')

    try:
        response = table.update_item(
            Key={'PlayerId': player_id},
            UpdateExpression="set Kill= Kill + :increment",
            ExpressionAttributeValues={':increment': 1 },
            ReturnValues="UPDATED_NEW"
        )
        return response  
    except ClientError as e:
        logging.error(e)
        return None

    
def register_player(player_id, dynamodb=None):
    """Register a new player in the DynamoDB table."""
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb', region_name=MY_REGION_NAME)

    table = dynamodb.Table('Leaderboard')

    try:
        # Check if the player ID already exists
        response = table.get_item(
            Key={'PlayerId': player_id}
        )
        if 'Item' in response:
            logging.info(f"Player {player_id} already registered.")
            return response['Item']

        # Add new player with initial high score
        initial_high_score = 0
        initial_death = 0
        initial_kill = 0
        response = table.put_item(
            Item={
                'PlayerId': player_id,
                'HighScore': initial_high_score,
                'Death': initial_death,
                'Kill' : initial_kill
            }
        )
        logging.info(f"Player {player_id} registered with initial high score of {initial_high_score}.")
        return response
    except ClientError as e:
        logging.error(e)
        return None

def get_top_three_scores(dynamodb=None):
    """Retrieve the top three scores from the DynamoDB table."""
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb', region_name=MY_REGION_NAME)

    table = dynamodb.Table('Leaderboard')

    try:
        # Scan the table not efficient for large tables in NoSQL (Literally scans everything)
        response = table.scan()
        items = response.get('Items', [])

        # Sort the scores in descending order and get top 3
        top_three_scores = sorted(items, key=lambda x: x.get('HighScore', 0), reverse=True)[:3]

        for score in top_three_scores:
            score['HighScore'] = int(score['HighScore'])
            score['Death'] = int(score['Death'])
            score['Kill'] = int(score['Kill'])
        return top_three_scores
    except ClientError as e:
        logging.error(e)
        return None