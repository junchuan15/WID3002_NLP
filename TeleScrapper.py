import csv
import configparser
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import datetime as dt


# Reading Configs
config = configparser.ConfigParser()
config.read("telethon.config.txt")

# Setting configuration values
api_id = config['telethon_credentials']['api_id']
api_hash = config['telethon_credentials']['api_hash']
phone = config['telethon_credentials']['phone']
username = config['telethon_credentials']['username']

client = TelegramClient(username, api_id, api_hash)

async def main():
    await client.start()
    print("Client Created")
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    async def save_messages_to_csv():
        print("Retrieving all chat history...")
        chat_name = input("Enter the name of the group chat: ")
        entity = await client.get_entity(chat_name)
        all_messages = []
        total_count_limit = 0
        offset_id = 0
        limit = 20
        start_date = dt(2022, 9, 25)  # Rename datetime to dt
        end_date = dt(2022, 10, 4)

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", len(all_messages))
            history = await client(GetHistoryRequest(
                peer=entity,
                offset_id=offset_id,
                offset_date=start_date,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            all_messages.extend(messages)
            offset_id = messages[-1].id
            # Check if end date is reached
            if messages[-1].date < end_date.timestamp():
                break
            if total_count_limit != 0 and len(all_messages) >= total_count_limit:
                break

        # Save messages to CSV
        with open('inquiries_messages.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'date', 'from_id', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for message in all_messages:
                datetime = message.date.strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow({
                    'id': message.id,
                    'date': datetime,
                    'from_id': message.from_id.user_id if hasattr(message.from_id, 'user_id') else None,
                    'message': message.message
                })

    # Call the async function
    await save_messages_to_csv()

# Run the async function
with client:
    client.loop.run_until_complete(main())
