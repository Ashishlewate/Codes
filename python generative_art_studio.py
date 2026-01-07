"""
Generative Art Studio - Create Stunning Visual Art for Instagram
Produces mesmerizing patterns, fractals, and animations perfect for social media
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from PIL import Image, ImageDraw, ImageFilter
import colorsys
from datetime import datetime
import os

class GenerativeArtStudio:
    def __init__(self, width=1080, height=1080):
        """Initialize with Instagram-perfect square dimensions"""
        self.width = width
        self.height = height
        self.dpi = 150
        
    def spiral_galaxy(self, arms=5, particles=5000):
        """Create mesmerizing spiral galaxy effect"""
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.axis('off')
        
        for arm in range(arms):
            theta = np.linspace(0, 4*np.pi, particles//arms)
            r = np.linspace(0.1, 2, particles//arms)
            
            # Add spiral offset for each arm
            offset = (2*np.pi*arm)/arms
            x = r * np.cos(theta*2 + offset) + np.random.normal(0, 0.05, particles//arms)
            y = r * np.sin(theta*2 + offset) + np.random.normal(0, 0.05, particles//arms)
            
            # Color gradient from center to edge
            colors = plt.cm.plasma(r/2)
            sizes = 100 * (1 - r/2) * np.random.random(particles//arms)
            
            ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, edgecolors='none')
        
        # Add central glow
        center_particles = 500
        r_center = np.random.exponential(0.1, center_particles)
        theta_center = np.random.uniform(0, 2*np.pi, center_particles)
        x_center = r_center * np.cos(theta_center)
        y_center = r_center * np.sin(theta_center)
        
        ax.scatter(x_center, y_center, c='white', s=50, alpha=0.8, edgecolors='none')
        
        plt.tight_layout(pad=0)
        return fig
    
    def mandelbrot_zoom(self, center_x=-0.5, center_y=0, zoom=1, max_iter=100):
        """Generate stunning Mandelbrot fractal"""
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.axis('off')
        
        x = np.linspace(center_x - 2/zoom, center_x + 2/zoom, self.width)
        y = np.linspace(center_y - 2/zoom, center_y + 2/zoom, self.height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j*Y
        
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        
        for i in range(max_iter):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i
        
        # Beautiful color mapping
        M = np.log(M + 1)
        im = ax.imshow(M, extent=[x.min(), x.max(), y.min(), y.max()],
                      cmap='twilight_shifted', interpolation='bilinear')
        
        plt.tight_layout(pad=0)
        return fig
    
    def particle_flow(self, num_particles=3000):
        """Create flowing particle animation"""
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Initialize particles
        particles = np.random.random((num_particles, 2))
        velocities = np.random.randn(num_particles, 2) * 0.01
        colors = np.random.random(num_particles)
        
        scatter = ax.scatter(particles[:, 0], particles[:, 1], 
                           c=colors, s=20, cmap='rainbow', alpha=0.6)
        
        def update(frame):
            nonlocal particles, velocities
            
            # Physics simulation
            center = np.array([0.5, 0.5])
            to_center = center - particles
            distance = np.linalg.norm(to_center, axis=1, keepdims=True)
            
            # Orbital force
            force = to_center / (distance**2 + 0.01)
            velocities += force * 0.0001
            
            # Add some turbulence
            velocities += np.random.randn(num_particles, 2) * 0.0005
            
            # Update positions
            particles += velocities
            
            # Boundary wrapping
            particles = particles % 1.0
            
            # Update scatter plot
            scatter.set_offsets(particles)
            scatter.set_array(np.sin(frame/10 + colors*2*np.pi))
            
            return scatter,
        
        anim = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
        return fig, anim
    
    def geometric_mandala(self, layers=12, symmetry=8):
        """Create intricate geometric mandala"""
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
        ax.set_facecolor('white')
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        for layer in range(layers):
            radius = 0.1 + layer * 0.08
            num_points = 50
            
            for sym in range(symmetry):
                angle_offset = (2 * np.pi * sym) / symmetry
                
                # Create petal-like shapes
                theta = np.linspace(0, 2*np.pi, num_points)
                r = radius * (1 + 0.3*np.sin(6*theta))
                
                x = r * np.cos(theta + angle_offset)
                y = r * np.sin(theta + angle_offset)
                
                # Color based on layer
                color = colorsys.hsv_to_rgb(layer/layers, 0.8, 0.9)
                ax.fill(x, y, color=color, alpha=0.6, edgecolor='black', linewidth=0.5)
                
                # Add decorative circles
                if layer % 2 == 0:
                    circle_x = radius * np.cos(angle_offset)
                    circle_y = radius * np.sin(angle_offset)
                    circle = plt.Circle((circle_x, circle_y), 0.03, 
                                      color=color, alpha=0.8, zorder=10)
                    ax.add_patch(circle)
        
        # Center decoration
        center_circle = plt.Circle((0, 0), 0.08, color='gold', zorder=20)
        ax.add_patch(center_circle)
        
        plt.tight_layout(pad=0)
        return fig
    
    def wave_interference(self, num_sources=5):
        """Create beautiful wave interference patterns"""
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.axis('off')
        
        x = np.linspace(-5, 5, self.width//2)
        y = np.linspace(-5, 5, self.height//2)
        X, Y = np.meshgrid(x, y)
        
        # Random wave sources
        sources = np.random.uniform(-3, 3, (num_sources, 2))
        Z = np.zeros_like(X)
        
        for source in sources:
            distance = np.sqrt((X - source[0])**2 + (Y - source[1])**2)
            Z += np.sin(distance * 3) / (distance + 1)
        
        im = ax.imshow(Z, extent=[-5, 5, -5, 5], cmap='twilight', 
                      interpolation='bilinear', vmin=-2, vmax=2)
        
        plt.tight_layout(pad=0)
        return fig
    
    def neon_grid(self, grid_size=20):
        """Create cyberpunk-style neon grid"""
        fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)
        ax.axis('off')
        
        # Draw grid with varying heights
        for i in range(grid_size):
            for j in range(grid_size):
                height = np.sin(i*0.5) * np.cos(j*0.5) + 1
                
                # Neon colors
                hue = (i + j) / (2 * grid_size)
                color = colorsys.hsv_to_rgb(hue, 1, 1)
                
                # Draw pillars with glow effect
                rect = plt.Rectangle((i, j), 0.8, height*0.8, 
                                    facecolor=color, alpha=0.7,
                                    edgecolor=color, linewidth=2)
                ax.add_patch(rect)
                
                # Add glow
                glow = plt.Rectangle((i-0.1, j-0.1), 1, height*0.9,
                                   facecolor=color, alpha=0.2)
                ax.add_patch(glow)
        
        plt.tight_layout(pad=0)
        return fig
    
    def save_art(self, fig, name, format='png'):
        """Save artwork in Instagram-ready format"""
        # Create output folder if it doesn't exist
        output_dir = "instagram_art"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f"art_{name}_{timestamp}.{format}")
        fig.savefig(filename, dpi=self.dpi, bbox_inches='tight', 
                   pad_inches=0, facecolor=fig.get_facecolor())
        
        # Get absolute path
        abs_path = os.path.abspath(filename)
        print(f"✨ Saved: {abs_path}")
        plt.close(fig)
        return filename
    
    def save_animation(self, fig, anim, name):
        """Save animation as GIF"""
        # Create output folder if it doesn't exist
        output_dir = "instagram_art"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f"art_{name}_{timestamp}.gif")
        writer = PillowWriter(fps=20)
        anim.save(filename, writer=writer, dpi=80)
        
        # Get absolute path
        abs_path = os.path.abspath(filename)
        print(f"🎬 Saved animation: {abs_path}")
        plt.close(fig)
        return filename

def main():
    """Generate a collection of stunning artworks"""
    print("🎨 Generative Art Studio - Instagram Edition")
    print("=" * 60)
    
    studio = GenerativeArtStudio(width=1080, height=1080)
    
    print("\n1. Creating Spiral Galaxy...")
    fig1 = studio.spiral_galaxy(arms=7, particles=8000)
    studio.save_art(fig1, "spiral_galaxy")
    
    print("2. Creating Mandelbrot Fractal...")
    fig2 = studio.mandelbrot_zoom(center_x=-0.75, center_y=0.1, zoom=2)
    studio.save_art(fig2, "mandelbrot")
    
    print("3. Creating Geometric Mandala...")
    fig3 = studio.geometric_mandala(layers=15, symmetry=12)
    studio.save_art(fig3, "mandala")
    
    print("4. Creating Wave Interference...")
    fig4 = studio.wave_interference(num_sources=7)
    studio.save_art(fig4, "waves")
    
    print("5. Creating Neon Grid...")
    fig5 = studio.neon_grid(grid_size=25)
    studio.save_art(fig5, "neon_grid")
    
    print("\n6. Creating Particle Flow Animation...")
    fig6, anim = studio.particle_flow(num_particles=2000)
    studio.save_animation(fig6, anim, "particle_flow")
    
    print("\n" + "=" * 60)
    print("✅ All artworks generated successfully!")
    print("📸 Ready to post on Instagram!")
    print("💡 Tip: Use filters and add music for maximum engagement")

if __name__ == "__main__":
    print("Required packages: numpy, matplotlib, pillow")
    print("Install: pip install numpy matplotlib pillow")
    print()
    main()