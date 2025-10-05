# Team Setup Guide

## For Team Members

### Getting Your Own API Key (Recommended)

1. **Visit Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy the generated key**

### Setting Up Your Environment

1. **Create your .env file**:
   ```bash
   echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
   ```

2. **Replace the placeholder** with your real API key

3. **Run the application**:
   ```bash
   cd backend
   GOOGLE_API_KEY=$(cat ../.env | grep API_KEY | cut -d'=' -f2) python run.py
   ```

### Why Individual Keys?

- ✅ **Free**: Google provides free API keys
- ✅ **Secure**: No shared credentials
- ✅ **Private**: Your key stays with you
- ✅ **Flexible**: Easy to manage and revoke

### Team Collaboration

- Share the code repository (already done)
- Each person gets their own API key
- Follow the setup instructions in SETUP.md
- Ask questions in team chat/slack

### Need Help?

- Check the troubleshooting section in SETUP.md
- Ask the team lead for assistance
- Google AI Studio has documentation
