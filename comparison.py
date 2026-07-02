import sqlite3
import numpy as np

def analyze_topic_comparison(topic_a, topic_b):
    conn = sqlite3.connect('news_analysis.db')
    c = conn.cursor()
    
    metrics = {}
    
    for topic in [topic_a, topic_b]:
        c.execute('''
            SELECT emotion_score_overall, emotion_positive_score, emotion_negative_score, emotion_dispersion 
            FROM articles 
            WHERE topic = ?
        ''', (topic,))
        
        rows = c.fetchall()
        if not rows:
            print(f"No data found for topic: {topic}")
            continue
            
        # Extract columns into numpy arrays for quick math
        compounds = [r[0] for r in rows if r[0] is not None]
        positives = [r[1] for r in rows if r[1] is not None]
        negatives = [r[2] for r in rows if r[2] is not None]
        dispersions = [r[3] for r in rows if r[3] is not None]
        
        metrics[topic] = {
            "count": len(compounds),
            "avg_compound": np.mean(compounds) if compounds else 0,
            "avg_positive": np.mean(positives) if positives else 0,
            "avg_negative": np.mean(negatives) if negatives else 0,
            "avg_variance": np.mean(dispersions) if dispersions else 0,
            "raw_compounds": compounds # Saving these for plotting charts later!
        }
        
    conn.close()
    return metrics

def print_comparison_report(metrics, topic_a, topic_b):
    if topic_a not in metrics or topic_b not in metrics:
        print("Error: One or both topics missing data.")
        return
        
    a = metrics[topic_a]
    b = metrics[topic_b]
    
