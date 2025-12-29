# [99boundaries App](https://99boundaries.com)

A modern Svelte 5 frontend application for browsing and filtering geographical boundary data from 99boundaries.

## Features

- Interactive data table powered by AG Grid
- Multi-select filters for Parent Country, ISO Code, Admin Level, and Polygon Type
- Country flags display using flag-icons
- Responsive design with DaisyUI and Tailwind CSS
- Download links for GeoJSON and Shapefile formats
- Direct links to OpenStreetMap relations

## Tech Stack

- **Framework**: Svelte 5
- **Build Tool**: Vite
- **Styling**: Tailwind CSS v4, DaisyUI
- **Data Grid**: AG Grid Community
- **Icons**: Font Awesome, Flag Icons
- **UI Components**: svelte-select

## Get Started

Install the dependencies:

```bash
cd nintynine-boundaries-app
npm install
```

Start the development server:

```bash
npm run dev
```

Navigate to the URL shown in your terminal (usually [http://localhost:5173](http://localhost:5173)). The app will automatically reload when you save changes to files in the `src` directory.

## Building for Production

To create an optimized production build:

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```

## Project Structure

```
src/
├── components/
│   └── AgGrid.svelte       # AG Grid wrapper component
├── index.svelte            # Main application component
├── App.svelte              # Root component
├── main.js                 # Application entry point
├── app.css                 # Global styles
└── boundaries.json         # Boundary data
```

## Data Source

Boundaries are generated via [Overpass](http://overpass-api.de/) & [OSM Land Polygons](https://osmdata.openstreetmap.de/data/land-polygons.html) ([© OpenStreetMap contributors](https://www.openstreetmap.org/copyright)) and provided in [EPSG:4326](https://epsg.io/4326).
