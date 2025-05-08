import os
import yt_dlp
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    youtube_url = request.args.get('url')

    if not youtube_url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'quiet': True,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            download_url = info_dict.get('url', None)

            if download_url:
                # Only return the download URL in the response
                response = {
                    'download_url': download_url
                }
                return jsonify(response), 200
            else:
                return jsonify({'error': 'Could not extract download URL'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
   import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
