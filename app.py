from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # yt-dlp options including cookies support
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'cookiefile': 'cookies.txt'  # 🟡 Make sure this file exists in your project root
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', None)

        if video_url:
            return jsonify({'download_url': video_url})
        else:
            return jsonify({'error': 'Download URL not found'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Only used in local development — Render runs its own server
if __name__ == '__main__':
    app.run(debug=True)
