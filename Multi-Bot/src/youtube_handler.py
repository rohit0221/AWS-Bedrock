from langchain_community.document_loaders import YoutubeLoader
import os

def create_transcript_file(video_url):
    transcript_file_path = '../youtube_transcripts/video-transcript.txt'
    if os.path.exists(transcript_file_path):
        os.remove(transcript_file_path)    
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=True)
    docs = loader.load()
    transcript=docs[0].page_content[:5000]

    with open(transcript_file_path, 'w') as file:
        # Write the content of the transcript to the file
        file.write(transcript)


