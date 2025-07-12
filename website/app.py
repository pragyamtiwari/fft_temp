from flask import Flask, render_template, request, redirect, url_for, session
import uuid

import os
import resend
from dotenv import load_dotenv
load_dotenv()

from supabase import create_client

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

from upstash_redis import Redis
resend.api_key = os.getenv("RESEND_API_KEY")

r = Redis(
    url=os.getenv("UPSTASH_REDIS_URL"),
    token=os.getenv("UPSTASH_REDIS_TOKEN")
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        email = request.form['email']
        send_magic_link(email)
        return render_template('sent.html')
    return render_template('index.html')

def send_magic_link(email_address):
    random_uuid = str(uuid.uuid4())
    
    params = {
        "from": "Food For Thou <auth@foodforthou.com>",
        "to": [email_address],
        "subject": "Food For Thou Authentication",
        "html": f"<strong>Click <a href='http://localhost:5001/magic/{random_uuid}'>here</a> to login</strong>",  
    }
    email = resend.Emails.send(params)
    print(email)

    r.set(random_uuid, email_address, ex=600)

@app.route('/magic/<random_uuid>', methods=['GET'])
def magic(random_uuid):
    if not r.exists(random_uuid):
        return render_template('index.html')
    
    email = r.get(random_uuid)
    return redirect(url_for('profile', random_uuid=random_uuid))

@app.route('/profile/<random_uuid>', methods=['GET', 'POST'])
def profile(random_uuid):    
    email = r.get(random_uuid)
    if not email:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        r.delete(random_uuid)
        name = request.form['name']
        in_usa = request.form.get('in_usa', False)
        zip_code = request.form.get('zip_code') if in_usa else None

        # Handle common interests (checkboxes)
        interests = request.form.getlist('common_interests')
        
        # Handle custom interests (comma-separated string from frontend)
        custom_interests_str = request.form.get('custom_interests', '').strip()
        custom_interests = []
        if custom_interests_str:
            # Split by comma and clean up each interest
            custom_interests = [interest.strip() for interest in custom_interests_str.split(',') if interest.strip()]
        
        try:
            supabase.table("users").update({
                "name": name,
                "zip_code": zip_code,
                "common_interests": interests,
                "custom_interests": custom_interests
            }).eq("email", email).execute()
            
            print(f"Updated user {email} with custom interests: {custom_interests}")
            
        except Exception as e:
            print(f"Error updating user: {e}")
            return render_template('profile.html', user=get_user(email), error="Failed to update profile")

        return redirect(url_for('index'))

    user = get_user(email)
    if not user:
        try:
            supabase.table("users").insert({
                "email": email
            }).execute()
            user = get_user(email)
        except Exception as e:
            print(f"Error creating user: {e}")
            return render_template('error.html', message="Failed to create user profile")
    
    # Prepare user data for template
    user_data = prepare_user_data(user)
    return render_template('profile.html', user=user_data)

def get_user(email):
    try:
        users = supabase.table("users").select("*").eq("email", email).execute()
        return users.data[0] if users.data else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def prepare_user_data(user):
    """Prepare user data for template rendering"""
    if not user:
        return None
    
    # Ensure custom_interests is properly formatted for the template
    custom_interests = user.get('custom_interests', [])
    
    # Handle different data types that might come from the database
    if isinstance(custom_interests, str):
        # If it's a string, split by comma
        custom_interests = custom_interests.split(',') if custom_interests else []
    elif custom_interests is None:
        custom_interests = []
    
    # Clean up the interests (remove empty strings and whitespace)
    custom_interests = [interest.strip() for interest in custom_interests if isinstance(interest, str) and interest.strip()]
    
    # Convert back to comma-separated string for the template
    custom_interests_str = ', '.join(custom_interests) if custom_interests else ''
    
    # Create a copy of user data with processed custom interests
    user_data = user.copy()
    user_data['custom_interests'] = custom_interests_str
    user_data['custom_interests_list'] = custom_interests  # Also provide as list for template flexibility
    
    # Ensure common_interests is always a list
    if not user_data.get('common_interests'):
        user_data['common_interests'] = []
    elif isinstance(user_data['common_interests'], str):
        user_data['common_interests'] = [user_data['common_interests']]
    
    return user_data

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)