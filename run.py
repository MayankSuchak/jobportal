import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🚀 NextHire Job Portal is running on http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop the server.\n")
    app.run(host='0.0.0.0', port=port, debug=True)
