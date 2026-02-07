# Instructions for Friend to Fix Spotify OAuth

Hey! I need your help to fix the Spotify authentication in my app. I'm getting an "INVALID_CLIENT: Invalid redirect URI" error because the redirect URI isn't configured in your Spotify app.

## What You Need to Do (Takes 2 minutes):

1. Go to: **https://developer.spotify.com/dashboard**
2. Log in with your Spotify account
3. Find and click on your app with Client ID: **cbd86bfbffd943c0ad63748cc27ee02f**
4. Click the **"Edit Settings"** button (usually in the top right)
5. Scroll down to the **"Redirect URIs"** section
6. In the text box, add this exact URI:
   ```
   http://localhost:8000/api/auth/spotify/callback
   ```
7. Click the **"Add"** button next to the text box
8. Scroll to the bottom and click **"Save"**

That's it! Once you save this, the authentication will work.

## Why This Is Needed

Spotify requires all redirect URIs to be pre-registered in the app settings for security. When someone tries to authenticate, Spotify checks if the redirect URI matches what's in the dashboard. If it doesn't match, it rejects the request with "INVALID_CLIENT" error.

## What the Redirect URI Does

After a user authorizes the app on Spotify's website, Spotify redirects them back to this URL with an authorization code. The backend then exchanges that code for an access token. This is the standard OAuth 2.0 flow.

Thanks for your help! 🙏
