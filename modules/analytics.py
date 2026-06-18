import logging
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional
import re
from collections import Counter
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_radar_chart(scores: Dict[str, int], title: str = "Paper Scores") -> go.Figure:
    """
    Create a radar chart for multi-dimensional scores.
    
    Args:
        scores: Dictionary with dimension names and values (0-10)
        title: Chart title
    
    Returns:
        Plotly figure object
    """
    if not scores or not isinstance(scores, dict):
        logger.warning("Invalid scores provided for radar chart")
        return go.Figure()
    
    try:
        categories = list(scores.keys())
        values = list(scores.values())
        
        # Ensure values are within 0-10 range
        values = [max(0, min(10, v)) for v in values]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Scores',
            line_color='#6495ff',
            fillcolor='rgba(100, 149, 255, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(size=10),
                    gridcolor='rgba(100, 149, 255, 0.2)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=11)
                ),
                bgcolor='rgba(17, 24, 39, 0.5)'
            ),
            showlegend=False,
            title=dict(
                text=title,
                font=dict(size=16, color='white')
            ),
            font=dict(color='white'),
            paper_bgcolor='rgba(10, 14, 39, 0)',
            plot_bgcolor='rgba(10, 14, 39, 0)',
            height=500,
            margin=dict(l=80, r=80, b=80, t=100)
        )
        
        logger.info(f"✅ Created radar chart: {title}")
        return fig
        
    except Exception as e:
        logger.error(f"Error creating radar chart: {e}")
        return go.Figure()


def create_keyword_frequency_chart(text: str, top_n: int = 15) -> go.Figure:
    """
    Create a bar chart of most frequent keywords.
    
    Args:
        text: Input text to analyze
        top_n: Number of top keywords to display
    
    Returns:
        Plotly figure object
    """
    if not text or len(text) < 50:
        logger.warning("Text too short for keyword analysis")
        return go.Figure()
    
    try:
        # Extract words and filter
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        # Filter common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through',
            'as', 'if', 'that', 'this', 'which', 'who', 'where', 'when', 'why',
            'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most'
        }
        
        filtered_words = [w for w in words if len(w) > 3 and w not in stop_words]
        word_freq = Counter(filtered_words)
        
        top_words = dict(word_freq.most_common(top_n))
        
        if not top_words:
            logger.warning("No valid keywords found")
            return go.Figure()
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(top_words.values()),
                y=list(top_words.keys()),
                orientation='h',
                marker=dict(
                    color=list(top_words.values()),
                    colorscale='Blues',
                    colorbar=dict(title="Frequency")
                ),
                text=list(top_words.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Top Keywords by Frequency",
            xaxis_title="Frequency",
            yaxis_title="Keywords",
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(10, 14, 39, 0)',
            plot_bgcolor='rgba(17, 24, 39, 0.5)',
            margin=dict(l=200, r=50, b=50, t=80)
        )
        
        logger.info(f"✅ Created keyword frequency chart with {len(top_words)} keywords")
        return fig
        
    except Exception as e:
        logger.error(f"Error creating keyword chart: {e}")
        return go.Figure()


def create_score_distribution_chart(
    scores_history: List[Dict[str, float]],
    title: str = "Score Distribution"
) -> go.Figure:
    """
    Create box plot showing score distribution.
    
    Args:
        scores_history: List of score dictionaries from multiple papers
        title: Chart title
    
    Returns:
        Plotly figure object
    """
    if not scores_history:
        logger.warning("No score history provided")
        return go.Figure()
    
    try:
        # Prepare data
        data_dict = {}
        for scores in scores_history:
            for dimension, score in scores.items():
                if dimension not in data_dict:
                    data_dict[dimension] = []
                data_dict[dimension].append(score)
        
        # Create box plot
        fig = go.Figure()
        
        for dimension, values in data_dict.items():
            fig.add_trace(go.Box(
                y=values,
                name=dimension,
                marker_color='#6495ff'
            ))
        
        fig.update_layout(
            title=title,
            yaxis_title="Score (0-10)",
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(10, 14, 39, 0)',
            plot_bgcolor='rgba(17, 24, 39, 0.5)',
            margin=dict(l=60, r=50, b=50, t=80)
        )
        
        logger.info(f"✅ Created score distribution chart")
        return fig
        
    except Exception as e:
        logger.error(f"Error creating distribution chart: {e}")
        return go.Figure()


def create_domain_distribution_chart(domains: List[str]) -> go.Figure:
    """
    Create pie chart of research domain distribution.
    
    Args:
        domains: List of domain names from analyzed papers
    
    Returns:
        Plotly figure object
    """
    if not domains:
        logger.warning("No domains provided")
        return go.Figure()
    
    try:
        domain_counts = Counter(domains)
        
        fig = go.Figure(data=[go.Pie(
            labels=list(domain_counts.keys()),
            values=list(domain_counts.values()),
            hole=0.3,
            marker=dict(
                colors=['#6495ff', '#0ea5e9', '#06b6d4', '#10b981', '#f59e0b'][:len(domain_counts)]
            ),
            textinfo='label+percent',
            textfont=dict(color='white')
        )])
        
        fig.update_layout(
            title="Research Domain Distribution",
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(10, 14, 39, 0)',
            margin=dict(l=50, r=50, b=50, t=80)
        )
        
        logger.info(f"✅ Created domain distribution chart with {len(domain_counts)} domains")
        return fig
        
    except Exception as e:
        logger.error(f"Error creating domain chart: {e}")
        return go.Figure()


def create_recommendation_summary_chart(
    recommendations: List[str]
) -> go.Figure:
    """
    Create horizontal bar chart of recommendation distribution.
    
    Args:
        recommendations: List of recommendations
    
    Returns:
        Plotly figure object
    """
    if not recommendations:
        logger.warning("No recommendations provided")
        return go.Figure()
    
    try:
        rec_counts = Counter(recommendations)
        
        # Define colors for each recommendation
        colors_map = {
            'Accept': '#10b981',
            'Minor Revision': '#f59e0b',
            'Major Revision': '#f97316',
            'Reject': '#ef4444'
        }
        
        colors = [colors_map.get(rec, '#6495ff') for rec in rec_counts.keys()]
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(rec_counts.values()),
                y=list(rec_counts.keys()),
                orientation='h',
                marker=dict(color=colors),
                text=list(rec_counts.values()),
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Recommendation Distribution",
            xaxis_title="Count",
            height=300,
            font=dict(color='white'),
            paper_bgcolor='rgba(10, 14, 39, 0)',
            plot_bgcolor='rgba(17, 24, 39, 0.5)',
            margin=dict(l=200, r=50, b=50, t=80),
            showlegend=False
        )
        
        logger.info(f"✅ Created recommendation summary chart")
        return fig
        
    except Exception as e:
        logger.error(f"Error creating recommendation chart: {e}")
        return go.Figure()


def create_metrics_summary(
    papers_analyzed: int,
    avg_score: float,
    top_domain: str,
    most_common_recommendation: str
) -> Dict[str, str]:
    """
    Create summary metrics for dashboard.
    
    Args:
        papers_analyzed: Total papers analyzed
        avg_score: Average score across papers
        top_domain: Most common domain
        most_common_recommendation: Most frequent recommendation
    
    Returns:
        Dictionary with formatted metrics
    """
    try:
        metrics = {
            "papers_analyzed": f"{papers_analyzed}",
            "average_score": f"{avg_score:.1f}/10",
            "top_domain": top_domain,
            "most_common_rec": most_common_recommendation
        }
        
        logger.info("✅ Created metrics summary")
        return metrics
        
    except Exception as e:
        logger.error(f"Error creating metrics summary: {e}")
        return {}
