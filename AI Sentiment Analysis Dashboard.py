"""
Real-time Sentiment Analysis Dashboard
An impressive web-based application with NLP, data visualization, and modern UI
"""

from flask import Flask, render_template_string, request, jsonify
from textblob import TextBlob
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import json
from collections import deque
import numpy as np

app = Flask(__name__)

# Store message history (last 100 messages)
message_history = deque(maxlen=100)
sentiment_timeline = deque(maxlen=50)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Sentiment Analysis Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .input-section {
            grid-column: 1 / -1;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        #textInput {
            flex: 1;
            padding: 15px;
            border: 2px solid #667eea;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        #textInput:focus {
            outline: none;
            border-color: #764ba2;
        }
        
        button {
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: scale(0.98);
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        #messages {
            max-height: 400px;
            overflow-y: auto;
            margin-top: 15px;
        }
        
        .message {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .message.positive {
            border-left-color: #28a745;
            background: #d4edda;
        }
        
        .message.negative {
            border-left-color: #dc3545;
            background: #f8d7da;
        }
        
        .message-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 0.85em;
            color: #666;
        }
        
        .message-text {
            color: #333;
            font-size: 1em;
        }
        
        .sentiment-badge {
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 0.8em;
        }
        
        .sentiment-positive {
            background: #28a745;
            color: white;
        }
        
        .sentiment-negative {
            background: #dc3545;
            color: white;
        }
        
        .sentiment-neutral {
            background: #6c757d;
            color: white;
        }
        
        #chart1, #chart2, #chart3 {
            width: 100%;
            height: 400px;
        }
        
        .loading {
            text-align: center;
            color: #667eea;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 AI Sentiment Analysis Dashboard</h1>
        
        <div class="dashboard">
            <div class="card input-section">
                <h2>📝 Analyze Text</h2>
                <div class="input-group">
                    <input type="text" id="textInput" placeholder="Enter text to analyze sentiment...">
                    <button onclick="analyzeText()">Analyze</button>
                    <button onclick="generateSample()">Try Sample</button>
                </div>
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-label">Total Analyzed</div>
                        <div class="stat-value" id="totalCount">0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Average Sentiment</div>
                        <div class="stat-value" id="avgSentiment">0.0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Positivity Rate</div>
                        <div class="stat-value" id="positiveRate">0%</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📊 Sentiment Distribution</h2>
                <div id="chart1"></div>
            </div>
            
            <div class="card">
                <h2>📈 Sentiment Timeline</h2>
                <div id="chart2"></div>
            </div>
            
            <div class="card">
                <h2>💬 Recent Messages</h2>
                <div id="messages"></div>
            </div>
            
            <div class="card">
                <h2>🔤 Word Cloud Data</h2>
                <div id="chart3"></div>
            </div>
        </div>
    </div>

    <script>
        const samples = [
            "I absolutely love this product! It's amazing and exceeded all my expectations!",
            "This is terrible. Worst experience ever. Very disappointed.",
            "The weather is okay today. Nothing special.",
            "Fantastic job! You're doing great work here!",
            "I'm really frustrated with this situation. It's not working at all.",
            "The service was decent, not bad but not outstanding either.",
            "Brilliant idea! This is exactly what we needed!",
            "I hate waiting in long queues. So annoying!",
            "Pretty good overall, though there's room for improvement.",
            "Absolutely wonderful experience! Highly recommend to everyone!"
        ];
        
        function generateSample() {
            const sample = samples[Math.floor(Math.random() * samples.length)];
            document.getElementById('textInput').value = sample;
            analyzeText();
        }
        
        async function analyzeText() {
            const text = document.getElementById('textInput').value;
            if (!text.trim()) return;
            
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });
            
            const data = await response.json();
            updateDashboard(data);
            document.getElementById('textInput').value = '';
        }
        
        function updateDashboard(data) {
            // Update stats
            document.getElementById('totalCount').textContent = data.total_messages;
            document.getElementById('avgSentiment').textContent = data.avg_sentiment.toFixed(2);
            document.getElementById('positiveRate').textContent = data.positive_rate.toFixed(0) + '%';
            
            // Update pie chart
            const pieData = [{
                values: [data.sentiment_counts.positive, data.sentiment_counts.neutral, data.sentiment_counts.negative],
                labels: ['Positive', 'Neutral', 'Negative'],
                type: 'pie',
                marker: {
                    colors: ['#28a745', '#6c757d', '#dc3545']
                },
                textinfo: 'label+percent',
                hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
            }];
            
            const pieLayout = {
                margin: {t: 0, b: 0, l: 0, r: 0},
                showlegend: true,
                height: 350
            };
            
            Plotly.newPlot('chart1', pieData, pieLayout);
            
            // Update timeline
            const timelineData = [{
                x: data.timeline.map(d => d.time),
                y: data.timeline.map(d => d.sentiment),
                type: 'scatter',
                mode: 'lines+markers',
                marker: {
                    color: data.timeline.map(d => d.sentiment > 0.1 ? '#28a745' : d.sentiment < -0.1 ? '#dc3545' : '#6c757d'),
                    size: 8
                },
                line: {
                    color: '#667eea',
                    width: 2
                }
            }];
            
            const timelineLayout = {
                margin: {t: 20, b: 40, l: 50, r: 20},
                xaxis: {title: 'Time'},
                yaxis: {title: 'Sentiment Score', range: [-1, 1]},
                height: 350
            };
            
            Plotly.newPlot('chart2', timelineData, timelineLayout);
            
            // Update messages
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = '';
            data.recent_messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                const sentimentClass = msg.sentiment > 0.1 ? 'positive' : msg.sentiment < -0.1 ? 'negative' : '';
                const badgeClass = msg.sentiment > 0.1 ? 'sentiment-positive' : msg.sentiment < -0.1 ? 'sentiment-negative' : 'sentiment-neutral';
                const label = msg.sentiment > 0.1 ? 'Positive' : msg.sentiment < -0.1 ? 'Negative' : 'Neutral';
                
                messageDiv.className = `message ${sentimentClass}`;
                messageDiv.innerHTML = `
                    <div class="message-header">
                        <span>${msg.time}</span>
                        <span class="sentiment-badge ${badgeClass}">${label} (${msg.sentiment.toFixed(2)})</span>
                    </div>
                    <div class="message-text">${msg.text}</div>
                `;
                messagesDiv.appendChild(messageDiv);
            });
            
            // Update word frequency chart
            const words = data.word_freq.map(w => w[0]);
            const counts = data.word_freq.map(w => w[1]);
            
            const barData = [{
                x: counts,
                y: words,
                type: 'bar',
                orientation: 'h',
                marker: {
                    color: counts,
                    colorscale: 'Viridis'
                }
            }];
            
            const barLayout = {
                margin: {t: 20, b: 40, l: 100, r: 20},
                xaxis: {title: 'Frequency'},
                yaxis: {title: ''},
                height: 350
            };
            
            Plotly.newPlot('chart3', barData, barLayout);
        }
        
        // Allow Enter key to analyze
        document.getElementById('textInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                analyzeText();
            }
        });
        
        // Load initial data
        window.onload = function() {
            generateSample();
        };
    </script>
</body>
</html>
"""

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    return blob.sentiment.polarity

def get_word_frequencies(messages, top_n=10):
    """Get most frequent words from messages"""
    from collections import Counter
    import re
    
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'is', 'are', 'was', 'were', 'be', 'been', 'being', 'this', 'that', 'it'}
    
    words = []
    for msg in messages:
        # Extract words, lowercase, remove punctuation
        text_words = re.findall(r'\b[a-z]+\b', msg['text'].lower())
        words.extend([w for w in text_words if w not in stop_words and len(w) > 3])
    
    counter = Counter(words)
    return counter.most_common(top_n)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Analyze sentiment
    sentiment = analyze_sentiment(text)
    
    # Store message
    message = {
        'text': text,
        'sentiment': sentiment,
        'time': datetime.now().strftime('%H:%M:%S')
    }
    message_history.append(message)
    sentiment_timeline.append({
        'sentiment': sentiment,
        'time': datetime.now().strftime('%H:%M:%S')
    })
    
    # Calculate statistics
    sentiments = [m['sentiment'] for m in message_history]
    avg_sentiment = np.mean(sentiments)
    positive_count = sum(1 for s in sentiments if s > 0.1)
    neutral_count = sum(1 for s in sentiments if -0.1 <= s <= 0.1)
    negative_count = sum(1 for s in sentiments if s < -0.1)
    
    # Get word frequencies
    word_freq = get_word_frequencies(list(message_history))
    
    response = {
        'sentiment': sentiment,
        'total_messages': len(message_history),
        'avg_sentiment': avg_sentiment,
        'positive_rate': (positive_count / len(message_history)) * 100 if message_history else 0,
        'sentiment_counts': {
            'positive': positive_count,
            'neutral': neutral_count,
            'negative': negative_count
        },
        'recent_messages': list(reversed(list(message_history)[-10:])),
        'timeline': list(sentiment_timeline),
        'word_freq': word_freq
    }
    
    return jsonify(response)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI Sentiment Analysis Dashboard Starting...")
    print("=" * 60)
    print("\n📦 Required packages:")
    print("   pip install flask textblob plotly numpy")
    print("\n🔧 Setup TextBlob:")
    print("   python -m textblob.download_corpora")
    print("\n🌐 Access the dashboard at: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)