# Spotify OAuth Fix Guide

## Problem Summary
You're getting the error: **"INVALID_CLIENT: Invalid redirect URI"**

This happens because the redirect URI in your Spotify Developer Dashboard doesn't match the one your application is using.

## The Fix

### 1. Update Spotify Developer Dashboard (CRITICAL)

You **MUST** add the correct redirect URI to your Spotify app settings:

1. Go to: https://developer.spotify.com/dashboard
2. Log in and click on your app (Client ID: `cbd86bfbffd943c0ad63748cc27ee02f`)
3. Click **"Edit Settings"**
4. In the **"Redirect URIs"** section, add:
   ```
   http://localhost:8000/api/auth/spotify/callback
   ```
5. Click **"Add"** button
6. Scroll down and click **"Save"**

⚠️ **IMPORTANT**: The redirect URI must EXACTLY match what's in your code. No trailing slashes, correct port, correct path.

### 2. Restart Your Backend Server

After updating the Spotify Dashboard, restart your backend:

```bash
# Stop the current backend (Ctrl+C)
# Then restart it
make run-backend
# or
cd backend && uvicorn main:app --reload
```

### 3. Content-Security-Policy Warnings

The CSP warnings you're seeing:
```
Content-Security-Policy: The page's settings blocked an inline script...
```

**These are NOT errors in your code!** These are warnings from Spotify's own authorization page (`accounts.spotify.com`). They're harmless and won't prevent authentication from working. Spotify's website has CSP policies that block certain scripts - this is on Spotify's side, not yours.

## Why This Happened

Your `.env` file previously had:
```
REDIRECT_URL=http://localhost:5173/callback  ❌ Wrong
```

But your backend code uses:
```
REDIRECT_URL=http://localhost:8000/api/auth/spotify/callback  ✅ Correct
```

I've already fixed your `.env` file, but you still need to update the Spotify Developer Dashboard.

## Verification Steps

After making these changes:

1. ✅ Backend server is running on port 8000
2. ✅ Frontend is running on port 5173
3. ✅ Spotify Dashboard has the correct redirect URI: `http://localhost:8000/api/auth/spotify/callback`
4. ✅ `.env` file has been updated (already done)
5. ✅ Backend server has been restarted

Then try clicking "Connect Spotify" again. It should work!

## What Happens Next

When you click "Connect Spotify":
1. Frontend calls `/api/auth/spotify`
2. Backend generates Spotify auth URL with redirect_uri=`http://localhost:8000/api/auth/spotify/callback`
3. You're redirected to Spotify to authorize
4. Spotify validates the redirect URI against what's in your Dashboard
5. If it matches, Spotify redirects back to your backend callback
6. Backend exchanges the code for an access token
7. Backend redirects you back to frontend with success

The redirect URI mismatch breaks step 4.

## Still Having Issues?

If you still get errors after updating the Dashboard:

1. **Double-check the redirect URI** in Spotify Dashboard - copy/paste to ensure it's exact
2. **Wait a few seconds** - sometimes Spotify takes a moment to update
3. **Clear your browser cache** - old OAuth state might be cached
4. **Check backend logs** - look for error messages in the terminal running your backend

## Summary

- ✅ Fixed `.env` file (already done)
- ⚠️ **YOU NEED TO**: Update Spotify Developer Dashboard redirect URI
- ℹ️ CSP warnings are from Spotify's page, not your code - ignore them
