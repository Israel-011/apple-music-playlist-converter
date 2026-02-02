# Playlist Converter - Frontend

Beautiful, responsive React frontend for the Apple Music to Spotify Playlist Converter.

## 🎨 Features

- **Modern UI**: Built with React and Tailwind CSS
- **Responsive Design**: Works seamlessly on mobile and desktop
- **Real-time Status**: Live updates during playlist conversion
- **Smooth Animations**: Polished user experience with transitions
- **Dark Theme**: Eye-friendly dark mode interface

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env
```

### Development

```bash
# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
# Build the app
npm run build

# Preview production build
npm run preview
```

## 🔧 Configuration

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## 📱 Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Icons** - Icon library

## 🎯 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── Header.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── StatusDisplay.jsx
│   ├── services/        # API services
│   │   └── api.js
│   ├── App.jsx          # Main app component
│   ├── index.css        # Global styles
│   └── main.jsx         # Entry point
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

## 🎨 Customization

### Colors

Edit `tailwind.config.js` to customize the color scheme:

```js
theme: {
  extend: {
    colors: {
      primary: { /* your colors */ },
      spotify: { /* Spotify brand colors */ },
      apple: { /* Apple brand colors */ },
    },
  },
}
```

### Styling

Global styles and custom utility classes are in `src/index.css`.

## 🌐 API Integration

The frontend communicates with the Python backend via REST API. All API calls are centralized in `src/services/api.js`.

### API Endpoints Used

- `POST /api/convert` - Convert playlist
- `GET /api/conversion/:id` - Get conversion status
- `GET /api/auth/spotify` - Spotify authentication
- `GET /api/auth/spotify/status` - Check auth status

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔗 Connect Backend

Make sure the Python backend is running on `http://localhost:8000` (or update `VITE_API_URL` in `.env`).

## 📄 License

MIT
