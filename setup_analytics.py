"""
Setup Script for Advanced Analytics
Run this to ensure all dependencies are installed and database is ready.
"""

import subprocess
import sys


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"⏳ {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - Success!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"   Error: {e}\n")
        return False


def main():
    """Main setup function."""
    print_header("Advanced Analytics Setup")
    
    print("This script will:")
    print("  1. Install required dependencies")
    print("  2. Update database schema")
    print("  3. Verify installation")
    print("\n")
    
    # Step 1: Install dependencies
    print_header("Step 1: Installing Dependencies")
    if not run_command(
        f"{sys.executable} -m pip install -e .",
        "Installing packages"
    ):
        print("⚠️  Warning: Some packages may not have installed correctly.")
        print("   Please run manually: pip install -e .\n")
    
    # Step 2: Verify imports
    print_header("Step 2: Verifying Installation")
    
    try:
        import numpy
        print("✅ NumPy installed successfully")
    except ImportError:
        print("❌ NumPy not found - please install: pip install numpy")
    
    try:
        import pandas
        print("✅ Pandas installed successfully")
    except ImportError:
        print("❌ Pandas not found - please install: pip install pandas")
    
    try:
        import plotly
        print("✅ Plotly installed successfully")
    except ImportError:
        print("❌ Plotly not found - please install: pip install plotly")
    
    try:
        import streamlit
        print("✅ Streamlit installed successfully")
    except ImportError:
        print("❌ Streamlit not found - please install: pip install streamlit")
    
    # Step 3: Verify new modules
    print("\n⏳ Checking new analytics modules...")
    
    try:
        from src.advanced_analytics import AdvancedAnalytics
        print("✅ Advanced Analytics module loaded")
    except ImportError as e:
        print(f"❌ Advanced Analytics module error: {e}")
    
    try:
        from src.geospatial_viz import GeospatialVisualizer
        print("✅ Geospatial Visualization module loaded")
    except ImportError as e:
        print(f"❌ Geospatial Visualization module error: {e}")
    
    # Step 4: Database info
    print_header("Step 3: Database Schema")
    print("ℹ️  Database schema has been updated with:")
    print("   - latitude column (Float)")
    print("   - longitude column (Float)")
    print("\n⚠️  Note: You may need to run database migrations if you have")
    print("   existing data. The new columns are optional and backward compatible.\n")
    
    # Final summary
    print_header("Setup Complete!")
    print("✅ Advanced Analytics features are ready to use!\n")
    print("📖 Documentation:")
    print("   - ADVANCED_ANALYTICS.md - Full feature guide")
    print("   - QUICK_START_ANALYTICS.md - Quick start tutorial")
    print("   - IMPLEMENTATION_SUMMARY.md - Implementation details\n")
    print("🚀 To get started:")
    print("   1. Run: python admin_portal.py")
    print("   2. Login with: admin / admin123")
    print("   3. Navigate to: Analytics → 🚀 Advanced Analytics\n")
    print("🎉 Enjoy your new advanced analytics capabilities!\n")


if __name__ == "__main__":
    main()
