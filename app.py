from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1205341406839701584/v7QuQqcNT2T02c-tpU-H9WVcrgWyuW-huWwJZ6VOkDsYfnPa-OOG7cixZ31xfYktya2e"


@app.route("/github", methods=["POST"])
def github_webhook():
    # Parse the incoming JSON from GitHub
    data = request.json

    # Extract relevant information (customize as needed)
    repo_name = data["repository"]["full_name"]
    commit_message = data["head_commit"]["message"]
    commit_url = data["head_commit"]["url"]

    # Prepare the Discord message
    discord_message = {
        "content": "New commit in repository",
        "embeds": [
            {
                "title": repo_name,
                "url": commit_url,
                "description": commit_message,
                "color": 5814783,
            }
        ],
    }

    # Send the message to Discord
    response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

    # Check if the request was successful
    if response.status_code == 204:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
