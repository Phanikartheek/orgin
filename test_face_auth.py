"""
Test script to verify face authentication is working.
Run this standalone to see the camera window clearly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.auth.face_auth import authenticate_face

print("=" * 40)
print("  Face Authentication Test")
print("  Look at the camera window...")
print("=" * 40)

result = authenticate_face()

if result:
    print("\n[RESULT] AUTHENTICATED - Face recognized!")
else:
    print("\n[RESULT] DENIED - Face not recognized!")

input("\nPress Enter to exit...")
