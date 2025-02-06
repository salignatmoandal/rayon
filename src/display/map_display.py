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
        """
        try:
            # Create map centered on search location
            map = folium.Map(
                location=center_coordinates,
                zoom_start=15  # Increased zoom level
            )
            
            # Add marker for search location
            folium.Marker(
                center_coordinates,
                popup="Votre position de recherche",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(map)
            
            # Add markers for suggestions with distance calculation
            for suggestion in suggestions:
                # Ensure coordinates are properly formatted
                coords = suggestion.get('coordinates', center_coordinates)
                if isinstance(coords, tuple) and len(coords) == 2:
                    folium.Marker(
                        coords,
                        popup=folium.Popup(
                            f"<b>{suggestion['nom']}</b><br>{suggestion['description']}",
                            max_width=300
                        ),
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(map)
            
            # Save and open map
            output_file = self.output_dir / "map.html"
            map.save(str(output_file))
            
            # Open the map in browser
            import webbrowser
            webbrowser.open(str(output_file))
            
            return str(output_file)
            
        except Exception as e:
            print(f"Error displaying map: {e}")
            return ""
