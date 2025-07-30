"""
Video Format Utilities for Klipify
Handles HLS (.m3u8) files and provides conversion options.
"""

import streamlit as st
import requests
import tempfile
import os


class VideoFormatHandler:
    """Handles different video formats and conversion options."""
    
    @staticmethod
    def create_hls_instructions():
        """Create instructions for handling HLS files."""
        return {
            'what_is_hls': 'HLS (.m3u8) is a streaming format that breaks video into small segments',
            'why_wont_play': 'Most browsers require special JavaScript libraries to play HLS directly',
            'solutions': {
                'vlc_player': {
                    'name': 'VLC Media Player (Recommended)',
                    'steps': [
                        '1. Copy the HLS stream URL',
                        '2. Open VLC Media Player',
                        '3. Go to Media → Open Network Stream',
                        '4. Paste the URL and click Play'
                    ],
                    'download_link': 'https://www.videolan.org/vlc/'
                },
                'online_players': {
                    'name': 'Online HLS Players',
                    'options': [
                        'HLS.js Demo Player: https://hls-js.netlify.app/demo/',
                        'VideoJS HLS: https://videojs.github.io/videojs-contrib-hls/',
                        'Flowplayer: https://flowplayer.com/developers/plugins/hlsjs'
                    ]
                },
                'conversion': {
                    'name': 'Convert to MP4',
                    'tools': [
                        'FFmpeg: ffmpeg -i "stream_url" -c copy output.mp4',
                        'VLC: Media → Convert/Save → Network → Add URL → Convert',
                        'Online converters (search "HLS to MP4 converter")'
                    ]
                }
            }
        }
    
    @staticmethod
    def display_video_player(stream_url, clip_title, clip_index):
        """Display a video player with enhanced fallback options."""
        
        if not stream_url:
            st.error("❌ No stream URL available")
            return
        
        st.markdown(f"### 🎥 {clip_title}")
        
        # Check if it's a Timeline-based URL (usually more reliable)
        is_timeline_based = 'timeline' in stream_url.lower() or 'videodb.io' in stream_url
        
        if is_timeline_based:
            st.info("✨ Timeline-based clip - Enhanced compatibility")
        
        # Try multiple approaches for video playback
        playback_success = False
        
        # Method 1: Try Streamlit's native video player
        try:
            st.video(stream_url)
            st.success("✅ Video loaded successfully!")
            playback_success = True
        except Exception as e:
            st.warning(f"⚠️ Direct playback failed: {str(e)}")
        
        # Method 2: If direct playback fails, try iframe embedding
        if not playback_success:
            try:
                # For VideoDB streams, try iframe approach
                iframe_html = f"""
                <iframe 
                    src="{stream_url}" 
                    width="100%" 
                    height="400" 
                    frameborder="0" 
                    allowfullscreen>
                </iframe>
                """
                st.markdown(iframe_html, unsafe_allow_html=True)
                st.info("🔄 Attempting iframe playback...")
                playback_success = True
            except Exception as e:
                st.warning(f"Iframe playback also failed: {str(e)}")
        
        # Method 3: Show alternatives if all else fails
        if not playback_success:
            VideoFormatHandler._show_playback_alternatives(stream_url)
        else:
            # Show URL for manual access
            with st.expander("🔗 Stream URL (for manual access)"):
                st.code(stream_url, language=None)
                st.markdown("Copy this URL to play in VLC or other compatible players.")
    
    @staticmethod
    def _show_playback_alternatives(stream_url):
        """Show alternative playback methods for HLS streams."""
        
        instructions = VideoFormatHandler.create_hls_instructions()
        
        # Create tabs for different solutions
        tab1, tab2, tab3 = st.tabs(["🎮 VLC Player", "🌐 Online Players", "🔄 Convert to MP4"])
        
        with tab1:
            st.markdown("### 📱 VLC Media Player (Recommended)")
            st.markdown("VLC can play HLS streams directly:")
            
            for step in instructions['solutions']['vlc_player']['steps']:
                st.markdown(f"- {step}")
            
            st.markdown("**Stream URL to copy:**")
            st.code(stream_url, language=None)
            
            st.link_button(
                "📥 Download VLC Player", 
                instructions['solutions']['vlc_player']['download_link'],
                use_container_width=True
            )
        
        with tab2:
            st.markdown("### 🌐 Online HLS Players")
            st.markdown("Use these web-based players:")
            
            players = [
                ("HLS.js Demo", "https://hls-js.netlify.app/demo/"),
                ("VideoJS Player", "https://videojs.github.io/videojs-contrib-hls/"),
                ("Flowplayer", "https://flowplayer.com/developers/plugins/hlsjs")
            ]
            
            for name, url in players:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{name}**")
                    st.markdown("Copy the stream URL and paste it into the player")
                with col2:
                    st.link_button("🔗 Open", url, use_container_width=True)
            
            st.markdown("**Stream URL to copy:**")
            st.code(stream_url, language=None)
        
        with tab3:
            st.markdown("### 🔄 Convert HLS to MP4")
            st.markdown("Convert the stream to a downloadable MP4 file:")
            
            # FFmpeg command
            st.markdown("**Using FFmpeg (Command Line):**")
            ffmpeg_cmd = f'ffmpeg -i "{stream_url}" -c copy output.mp4'
            st.code(ffmpeg_cmd, language='bash')
            
            # VLC conversion
            st.markdown("**Using VLC:**")
            vlc_steps = [
                "1. Open VLC → Media → Convert/Save",
                "2. Network tab → Enter the stream URL",
                "3. Click Convert/Save",
                "4. Choose MP4 format and destination",
                "5. Click Start"
            ]
            
            for step in vlc_steps:
                st.markdown(f"- {step}")
            
            # Online converters
            st.markdown("**Online Converters:**")
            st.markdown("Search for 'HLS to MP4 converter' - many free options available")
    
    @staticmethod
    def create_download_buttons(clip_data, youtube_id):
        """Create download buttons with multiple options."""
        from ..utils.helpers import create_youtube_link
        
        st.markdown("### 📥 Download Options")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # YouTube link (always available)
        youtube_link = create_youtube_link(youtube_id, clip_data.get('start_time', 0))
        with col1:
            st.link_button("▶️ YouTube", youtube_link, use_container_width=True)
        
        # HLS Stream
        with col2:
            if clip_data.get('stream_url'):
                if st.button("🎥 HLS Stream", key=f"hls_{id(clip_data)}", use_container_width=True):
                    st.session_state[f'show_player_{id(clip_data)}'] = True
            else:
                st.button("🎥 HLS (N/A)", disabled=True, use_container_width=True)
        
        # MP4 Download
        with col3:
            if clip_data.get('download_url'):
                st.link_button("📱 Download MP4", clip_data['download_url'], use_container_width=True)
            else:
                if st.button("📱 Convert MP4", key=f"convert_{id(clip_data)}", use_container_width=True):
                    VideoFormatHandler._show_conversion_help(clip_data.get('stream_url'))
        
        # Copy URL
        with col4:
            if st.button("📋 Copy URL", key=f"copy_{id(clip_data)}", use_container_width=True):
                st.code(clip_data.get('stream_url', youtube_link), language=None)
        
        # Show player if requested
        if st.session_state.get(f'show_player_{id(clip_data)}'):
            VideoFormatHandler.display_video_player(
                clip_data.get('stream_url'), 
                clip_data.get('concept', 'Video Clip'),
                id(clip_data)
            )
    
    @staticmethod
    def _show_conversion_help(stream_url):
        """Show help for converting HLS to MP4."""
        if not stream_url:
            st.error("No stream URL available for conversion")
            return
        
        st.info("💡 **MP4 Conversion Options:**")
        
        with st.expander("🔧 How to convert HLS to MP4"):
            VideoFormatHandler._show_playback_alternatives(stream_url)


def check_video_compatibility(url):
    """Check if a video URL is compatible with different players."""
    if not url:
        return {'compatible': False, 'reason': 'No URL provided'}
    
    if '.m3u8' in url:
        return {
            'compatible': False,
            'format': 'HLS',
            'reason': 'HLS format requires special player',
            'solutions': ['VLC Player', 'Online HLS players', 'Convert to MP4']
        }
    elif '.mp4' in url:
        return {
            'compatible': True,
            'format': 'MP4',
            'reason': 'Compatible with most browsers'
        }
    else:
        return {
            'compatible': 'unknown',
            'format': 'Unknown',
            'reason': 'Format not detected from URL'
        }


def create_video_info_card(clip_data):
    """Create an information card about video format and playback."""
    compatibility = check_video_compatibility(clip_data.get('stream_url'))
    
    if compatibility['format'] == 'HLS':
        st.info(f"""
        🎥 **Video Format:** HLS (.m3u8)  
        ⚠️ **Browser Support:** Limited - requires special player  
        💡 **Recommended:** Download and play in VLC Media Player  
        🔧 **Alternatives:** Online HLS players or convert to MP4
        """)
    elif compatibility['format'] == 'MP4':
        st.success(f"""
        🎥 **Video Format:** MP4  
        ✅ **Browser Support:** Full compatibility  
        ▶️ **Playback:** Direct play in browser supported
        """)
    else:
        st.warning(f"""
        🎥 **Video Format:** Unknown  
        ❓ **Compatibility:** Cannot determine  
        🔍 **Suggestion:** Try VLC player if other methods fail
        """)
