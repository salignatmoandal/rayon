from typing import List, Dict, Tuple
import folium
from pathlib import Path

class MapDisplay:
    """Handle map display using Folium."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def display_map(self, center_coordinates: Tuple[float, float], suggestions: List[Dict]) -> str:
        """
        Create an HTML map with the suggestions.
        Args:
            center_coordinates: (latitude, longitude) of the search center
            suggestions: List of suggestions with coordinates
        Returns:
            Path to the generated HTML file
        """
        # Create map centered on search location
        map = folium.Map(
            location=center_coordinates,
            zoom_start=14
        )
        
        # Add marker for search location
        folium.Marker(
            center_coordinates,
            popup="Search Location",
            icon=folium.Icon(color='red')
        ).add_to(map)
        
        # Add markers for suggestions
        for suggestion in suggestions:
            folium.Marker(
                suggestion['coordinates'],
                popup=f"{suggestion['nom']}\n{suggestion['description']}",
                icon=folium.Icon(color='blue')
            ).add_to(map)
            
        # Save map
        output_file = self.output_dir / "map.html"
        map.save(str(output_file))
        return str(output_file)
