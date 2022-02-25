from flask import Flask, request, abort
import json
import bot

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        alertUsers(data)
        return 'success', 200
    else:
        abort(400)

def prepareMessage(data):
    header = 'New Push\n\n'
    repoName = "Repository: " + data['repository']['full_name']
    commitID = "Commit ID: " + data['after']
    repoOwner = "Owner Name: " + data['repository']['owner']['name']
    repoOwnerEmail = "Owner Email ID: " + data['repository']['owner']['email']
    pusherName = "Pusher Name: " + data['pusher']['name']
    pusherEmail = "Pusher Email ID: " + data['pusher']['email']
    filesModified = "Files Modified:" + ' '.join(data['commits'][0]['added'])
    commitMessage = "Commit Message: " + data['head_commit']['message']
    timeStamp = "Timestamp: " + data['head_commit']['timestamp']

    commitDetails = [header, repoName, commitID, repoOwner, repoOwnerEmail, pusherName, pusherEmail, filesModified, commitMessage, timeStamp]

    alertMessage = '\n'.join(commitDetails)
    return alertMessage

def alertUsers(data):
    alertMessage = prepareMessage(data)
    print(alertMessage)
    for subscriber in open('subscribers.txt').read().strip().split():
        bot.sendMessage(subscriber, alertMessage)
        

if __name__ == '__main__':
    app.run()
    