import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib
import json
import re
from typing import List, Dict, Optional
import time

# Page configuration
st.set_page_config(
    page_title="AI Prompt Library",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark theme
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --dark-bg: #0f172a;
        --card-bg: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --border-color: #334155;
        --hover-color: #475569;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: var(--text-primary);
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        color: var(--text-secondary);
        font-size: 1.2rem;
        font-weight: 400;
    }
    
    /* Card styling */
    .prompt-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .prompt-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.2);
    }
    
    .prompt-title {
        color: var(--text-primary);
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .prompt-description {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .prompt-content {
        background: #0f172a;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: var(--text-primary);
        white-space: pre-wrap;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .prompt-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    .category-tag {
        background: var(--primary-color);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--card-bg);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: var(--card-bg);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }
    
    /* Metrics styling */
    .metric-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Search styling */
    .search-container {
        margin-bottom: 2rem;
    }
    
    /* Animation for loading */
    .loading-spinner {
        border: 3px solid var(--border-color);
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Database functions
class PromptDatabase:
    def __init__(self, db_path: str = "prompts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usage_count INTEGER DEFAULT 0,
                rating REAL DEFAULT 0.0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                color TEXT DEFAULT '#6366f1'
            )
        """)
        
        # Insert default categories
        default_categories = [
            ('General', 'General purpose prompts', '#6366f1'),
            ('Creative Writing', 'Creative and storytelling prompts', '#8b5cf6'),
            ('Code Generation', 'Programming and development prompts', '#10b981'),
            ('Analysis', 'Data analysis and research prompts', '#f59e0b'),
            ('Security', 'Cybersecurity and penetration testing prompts', '#ef4444'),
            ('Business', 'Business and professional prompts', '#06b6d4'),
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO categories (name, description, color) 
            VALUES (?, ?, ?)
        """, default_categories)
        
        conn.commit()
        conn.close()
    
    def add_prompt(self, title: str, description: str, content: str, 
                   category: str, tags: List[str] = None) -> bool:
        """Add a new prompt to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tags_str = json.dumps(tags) if tags else "[]"
            
            cursor.execute("""
                INSERT INTO prompts (title, description, content, category, tags)
                VALUES (?, ?, ?, ?, ?)
            """, (title, description, content, category, tags_str))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error adding prompt: {e}")
            return False
    
    def get_prompts(self, category: str = None, search_term: str = None) -> pd.DataFrame:
        """Retrieve prompts with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM prompts WHERE 1=1"
        params = []
        
        if category and category != "All":
            query += " AND category = ?"
            params.append(category)
        
        if search_term:
            query += " AND (title LIKE ? OR description LIKE ? OR content LIKE ?)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        query += " ORDER BY created_at DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def update_prompt(self, prompt_id: int, title: str = None, description: str = None,
                     content: str = None, category: str = None, tags: List[str] = None) -> bool:
        """Update an existing prompt"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if title: updates.append("title = ?"); params.append(title)
            if description: updates.append("description = ?"); params.append(description)
            if content: updates.append("content = ?"); params.append(content)
            if category: updates.append("category = ?"); params.append(category)
            if tags: updates.append("tags = ?"); params.append(json.dumps(tags))
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                query = f"UPDATE prompts SET {', '.join(updates)} WHERE id = ?"
                params.append(prompt_id)
                
                cursor.execute(query, params)
                conn.commit()
            
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error updating prompt: {e}")
            return False
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """Delete a prompt"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error deleting prompt: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """Get all categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total prompts
        cursor.execute("SELECT COUNT(*) FROM prompts")
        total_prompts = cursor.fetchone()[0]
        
        # Prompts by category
        cursor.execute("SELECT category, COUNT(*) FROM prompts GROUP BY category")
        category_counts = dict(cursor.fetchall())
        
        # Recent prompts (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM prompts 
            WHERE created_at >= datetime('now', '-7 days')
        """)
        recent_prompts = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_prompts': total_prompts,
            'category_counts': category_counts,
            'recent_prompts': recent_prompts
        }

# Initialize database
@st.cache_resource
def init_db():
    return PromptDatabase()

# Main application
def main():
    load_css()
    db = init_db()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AI Prompt Library</h1>
        <p>Organize, manage, and deploy your AI prompts with precision</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Dashboard")
        
        # Statistics
        stats = db.get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_prompts']}</div>
                <div class="metric-label">Total Prompts</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['recent_prompts']}</div>
                <div class="metric-label">This Week</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "📖 Navigate",
            ["Browse Prompts", "Add New Prompt", "Manage Categories", "Import/Export"]
        )
        
        st.markdown("---")
        
        # Filters (for Browse page)
        if page == "Browse Prompts":
            st.markdown("### 🔍 Filters")
            
            categories = ["All"] + db.get_categories()
            selected_category = st.selectbox("Category", categories)
            
            search_term = st.text_input("🔎 Search", placeholder="Search prompts...")
            
            # Store in session state for main area
            st.session_state.selected_category = selected_category
            st.session_state.search_term = search_term
    
    # Main content area
    if page == "Browse Prompts":
        display_browse_prompts(db)
    elif page == "Add New Prompt":
        display_add_prompt(db)
    elif page == "Manage Categories":
        display_manage_categories(db)
    elif page == "Import/Export":
        display_import_export(db)

def display_browse_prompts(db: PromptDatabase):
    """Display the browse prompts page"""
    category = getattr(st.session_state, 'selected_category', 'All')
    search = getattr(st.session_state, 'search_term', '')
    
    # Get prompts
    prompts_df = db.get_prompts(category=category, search_term=search)
    
    if prompts_df.empty:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
            <h3>No prompts found</h3>
            <p>Try adjusting your filters or add a new prompt to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display prompts
    for _, prompt in prompts_df.iterrows():
        display_prompt_card(prompt, db)

def display_prompt_card(prompt: pd.Series, db: PromptDatabase):
    """Display a single prompt card"""
    tags = json.loads(prompt.get('tags', '[]'))
    
    st.markdown(f"""
    <div class="prompt-card">
        <div class="prompt-title">{prompt['title']}</div>
        <div class="prompt-description">{prompt.get('description', 'No description')}</div>
        <div class="prompt-content">{prompt['content'][:300]}{'...' if len(prompt['content']) > 300 else ''}</div>
        <div class="prompt-meta">
            <div>
                <span class="category-tag">{prompt['category']}</span>
                {' '.join([f'<span style="background: var(--hover-color); padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.6rem; margin-left: 0.5rem;">{tag}</span>' for tag in tags[:3]])}
            </div>
            <div>{prompt['created_at'][:10]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("📋 Copy", key=f"copy_{prompt['id']}"):
            st.code(prompt['content'], language="text")
            st.success("Prompt copied to clipboard area above!")
    
    with col2:
        if st.button("✏️ Edit", key=f"edit_{prompt['id']}"):
            st.session_state[f'editing_{prompt["id"]}'] = True
    
    with col3:
        if st.button("🔗 Share", key=f"share_{prompt['id']}"):
            share_url = f"#{hashlib.md5(str(prompt['id']).encode()).hexdigest()}"
            st.info(f"Share URL: {share_url}")
    
    with col4:
        if st.button("🗑️ Delete", key=f"delete_{prompt['id']}"):
            if db.delete_prompt(prompt['id']):
                st.success("Prompt deleted!")
                st.rerun()
    
    # Edit form (if editing)
    if st.session_state.get(f'editing_{prompt["id"]}', False):
        with st.expander("Edit Prompt", expanded=True):
            edit_title = st.text_input("Title", value=prompt['title'], key=f"edit_title_{prompt['id']}")
            edit_desc = st.text_area("Description", value=prompt.get('description', ''), key=f"edit_desc_{prompt['id']}")
            edit_content = st.text_area("Content", value=prompt['content'], height=200, key=f"edit_content_{prompt['id']}")
            edit_category = st.selectbox("Category", db.get_categories(), 
                                       index=db.get_categories().index(prompt['category']) if prompt['category'] in db.get_categories() else 0,
                                       key=f"edit_category_{prompt['id']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save", key=f"save_{prompt['id']}"):
                    if db.update_prompt(prompt['id'], edit_title, edit_desc, edit_content, edit_category):
                        st.success("Prompt updated!")
                        st.session_state[f'editing_{prompt["id"]}'] = False
                        st.rerun()
            
            with col2:
                if st.button("❌ Cancel", key=f"cancel_{prompt['id']}"):
                    st.session_state[f'editing_{prompt["id"]}'] = False
                    st.rerun()

def display_add_prompt(db: PromptDatabase):
    """Display the add new prompt page"""
    st.markdown("## ➕ Add New Prompt")
    
    with st.form("add_prompt_form"):
        title = st.text_input("Title *", placeholder="Enter a descriptive title for your prompt")
        description = st.text_area("Description", placeholder="Optional description of what this prompt does")
        content = st.text_area("Prompt Content *", height=200, 
                              placeholder="Enter your AI prompt here...")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category *", db.get_categories())
        
        with col2:
            tags_input = st.text_input("Tags", placeholder="tag1, tag2, tag3")
        
        submitted = st.form_submit_button("🚀 Add Prompt")
        
        if submitted:
            if not title or not content:
                st.error("Title and content are required!")
            else:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []
                
                if db.add_prompt(title, description, content, category, tags):
                    st.success("Prompt added successfully!")
                    time.sleep(1)
                    st.rerun()

def display_manage_categories(db: PromptDatabase):
    """Display the manage categories page"""
    st.markdown("## 📁 Manage Categories")
    
    # Add new category
    with st.expander("Add New Category"):
        with st.form("add_category_form"):
            cat_name = st.text_input("Category Name")
            cat_desc = st.text_area("Description")
            cat_color = st.color_picker("Color", "#6366f1")
            
            if st.form_submit_button("Add Category"):
                # Implementation for adding categories
                st.info("Category management coming soon!")
    
    # List existing categories
    categories = db.get_categories()
    stats = db.get_stats()
    
    for category in categories:
        count = stats['category_counts'].get(category, 0)
        st.markdown(f"""
        <div class="prompt-card">
            <div class="prompt-title">{category}</div>
            <div class="prompt-description">{count} prompts</div>
        </div>
        """, unsafe_allow_html=True)

def display_import_export(db: PromptDatabase):
    """Display the import/export page"""
    st.markdown("## 📤 Import/Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Prompts")
        if st.button("📥 Export to JSON"):
            prompts_df = db.get_prompts()
            json_data = prompts_df.to_json(orient='records', indent=2)
            st.download_button(
                "Download JSON",
                json_data,
                file_name=f"prompts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("### Import Prompts")
        uploaded_file = st.file_uploader("Choose a JSON file", type="json")
        
        if uploaded_file and st.button("📤 Import"):
            try:
                data = json.load(uploaded_file)
                # Implementation for import
                st.success(f"Ready to import {len(data)} prompts")
            except Exception as e:
                st.error(f"Error reading file: {e}")

if __name__ == "__main__":
    main()