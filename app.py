from flask import Flask, render_template, request, jsonify
import random
import os
from datetime import datetime

# Built with Google Antigravity for PromptWars Challenge 2
# Google Services: Google Cloud Run, Flask web framework

app = Flask(__name__)

# Google Cloud Project ID (for Antigravity integration)
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'promptwars-project')

# Sample prompts store
prompts = {
    "ai1": "Write a poem about technology in the style of Shakespeare",
    "ai2": "Explain quantum computing like I'm 5 years old",
    "ai3": "Generate a recipe for a futuristic breakfast",
    "ai4": "Write a short story about a robot who dreams",
    "ai5": "Create a workout plan for a busy developer"
}

# Battle results store
battles = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_random_prompts', methods=['GET'])
def get_random_prompts():
    selected = random.sample(list(prompts.items()), 2)
    return jsonify({
        'prompt1': {'id': selected[0][0], 'text': selected[0][1]},
        'prompt2': {'id': selected[1][0], 'text': selected[1][1]}
    })

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    winner_id = data.get('winner_id')
    loser_id = data.get('loser_id')
    
    battle_record = {
        'winner': winner_id,
        'loser': loser_id,
        'winner_text': prompts.get(winner_id, ''),
        'loser_text': prompts.get(loser_id, ''),
        'timestamp': datetime.now().isoformat(),
        'user_ip': request.remote_addr
    }
    battles.append(battle_record)
    
    return jsonify({'status': 'success', 'total_battles': len(battles)})

@app.route('/stats', methods=['GET'])
def stats():
    win_count = {}
    for battle in battles:
        winner = battle['winner']
        win_count[winner] = win_count.get(winner, 0) + 1
    
    stats_data = []
    for prompt_id, count in win_count.items():
        stats_data.append({
            'id': prompt_id,
            'text': prompts.get(prompt_id, ''),
            'wins': count
        })
    
    stats_data.sort(key=lambda x: x['wins'], reverse=True)
    
    return jsonify({
        'total_battles': len(battles),
        'leaderboard': stats_data
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'project': PROJECT_ID})

@app.route('/add_prompt', methods=['POST'])
def add_prompt():
    data = request.json
    new_id = f"custom_{len(prompts) + 1}"
    prompts[new_id] = data.get('prompt_text')
    return jsonify({'status': 'success', 'id': new_id})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)