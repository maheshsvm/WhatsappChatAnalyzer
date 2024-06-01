import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', dayfirst=True)

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

# Sample data
data = """
23/05/24, 06:48 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.
23/05/24, 06:48 - Gargi Teotiya Glb created group "Final year project 2k24"
23/05/24, 06:48 - Gargi Teotiya Glb added you
23/05/24, 06:48 - You're now an admin
23/05/24, 06:49 - Gargi Teotiya Glb changed this group's icon
23/05/24, 19:08 - @: Sab apni present lgao
23/05/24, 19:08 - @: Shant pda h group
23/05/24, 19:08 - @: Present ✋
23/05/24, 19:33 - Anjali Glb: Present sir
23/05/24, 19:39 - @: Good 👍
23/05/24, 19:40 - Gargi Teotiya Glb: Present 🙌
23/05/24, 19:41 - @: Good 👍
23/05/24, 19:42 - @: Y Mukesh kis kone m pda h
23/05/24, 19:42 - @: @916396615853 Nasha krke gir gya kya khi
23/05/24, 19:45 - Anjali Glb: Saste nashe m kon kon sa nsha aata h
23/05/24, 19:47 - @: Parle g ka powder sunghna
23/05/24, 19:47 - @: Dew , cocacola or thums up milake pee Jana etc.
23/05/24, 19:47 - @: @916396615853 konse vale kre h isme se?
23/05/24, 20:10 - Anjali Glb: Iodex ko bread pr lga kr khalo
23/05/24, 20:10 - Anjali Glb: Ye bhi ek nsha h
23/05/24, 20:10 - @: Ha anjali yhi vala prefer krti h
23/05/24, 20:44 - Anjali Glb: Shi m
23/05/24, 20:44 - Anjali Glb: Tune dekha h mujhe
23/05/24, 20:45 - Anjali Glb: Ese krte hue
23/05/24, 20:45 - @: Are ha fairwell vale din bhi to tu iodex layi thi <This message was edited>
23/05/24, 20:45 - @: Bol rhi thi jhukam h
23/05/24, 20:45 - @: 😁
23/05/24, 20:48 - Anjali Glb: Kmine
23/05/24, 20:48 - Anjali Glb: Km bol
23/05/24, 20:49 - @: Nashe to Mukesh krta h humme se
"""

# # Preprocess the data
# df = preprocess(data)
# print(df)
