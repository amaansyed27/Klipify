"""
Video management page component for VideoDB integration.
"""

import streamlit as st

def show_my_videos_page():
    """Display the video management page."""
    st.markdown("""
    <div class="page-header">
        <h2>📁 My Videos</h2>
        <p class="page-subtitle">Manage your VideoDB videos and generate clips</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Import the video manager
    try:
        from ...services.videodb_manager import VideoDBManager
        
        # Initialize video manager
        video_manager = VideoDBManager()
        
        # Show upload status if available
        if 'last_upload_status' in st.session_state:
            status = st.session_state['last_upload_status']
            if status['success']:
                st.success(f"✅ Video '{status['title']}' uploaded successfully!")
            else:
                st.error(f"❌ Upload failed: {status['error']}")
            # Clear the status after showing
            del st.session_state['last_upload_status']
        
        # Search and filter options
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search videos...", placeholder="Search by name or description")
        with col2:
            refresh_clicked = st.button("🔄 Refresh", use_container_width=True)
        
        # Get videos list
        with st.spinner("Loading your videos..."):
            try:
                videos = video_manager.list_videos()
                
                if not videos:
                    st.markdown("""
                    <div class="empty-state">
                        <h3>No videos found</h3>
                        <p>You haven't uploaded any videos to VideoDB yet. Upload a video from the main page to get started!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    return
                
                # Filter videos based on search
                if search_term:
                    search_lower = search_term.lower()
                    filtered_videos = [
                        video for video in videos
                        if (search_lower in video.get('name', '').lower() or 
                            search_lower in video.get('description', '').lower())
                    ]
                else:
                    filtered_videos = videos
                
                if not filtered_videos:
                    st.info(f"No videos found matching '{search_term}'")
                    return
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Videos", len(videos))
                with col2:
                    st.metric("Filtered Results", len(filtered_videos))
                with col3:
                    total_duration = sum(video.get('length', 0) for video in filtered_videos)
                    st.metric("Total Duration", f"{total_duration/60:.1f} min")
                
                st.markdown("---")
                
                # Display videos
                for video in filtered_videos:
                    _display_video_card(video, video_manager)
                
            except Exception as e:
                st.error(f"Error loading videos: {str(e)}")
                st.info("Make sure your VideoDB credentials are configured correctly.")
    
    except ImportError:
        st.error("VideoDB manager not available. Please check your installation.")
    except Exception as e:
        st.error(f"Error initializing video manager: {str(e)}")


def _display_video_card(video, video_manager):
    """Display a single video card with management options."""
    video_id = video.get('id', '')
    video_name = video.get('name', 'Untitled Video')
    description = video.get('description', 'No description')
    length = video.get('length', 0)
    
    # Format duration
    if length > 0:
        minutes = int(length // 60)
        seconds = int(length % 60)
        duration_str = f"{minutes}:{seconds:02d}"
    else:
        duration_str = "Unknown"
    
    with st.container():
        st.markdown(f"""
        <div class="video-card">
            <div class="video-header">
                <h4>{video_name}</h4>
                <span class="video-status" style="background: var(--success-green); color: white;">Ready</span>
            </div>
            <div class="video-meta">
                ID: {video_id} • Duration: {duration_str}
            </div>
            <p style="color: var(--text-secondary); margin: 0.5rem 0;">{description[:150]}{'...' if len(description) > 150 else ''}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"🎬 Generate Clips", key=f"clips_{video_id}"):
                _generate_clips_from_video(video_id, video_name, video_manager)
        
        with col2:
            if st.button(f"ℹ️ View Details", key=f"details_{video_id}"):
                _show_video_details(video_id, video_manager)
        
        with col3:
            if st.button(f"🗑️ Delete", key=f"delete_{video_id}", type="secondary"):
                _confirm_delete_video(video_id, video_name, video_manager)


def _generate_clips_from_video(video_id, video_name, video_manager):
    """Generate clips from an existing video."""
    with st.spinner(f"Generating clips from '{video_name}'..."):
        try:
            result = video_manager.generate_clips_from_existing(video_id)
            
            if result['success']:
                # Store the result in session state
                st.session_state['video_data'] = result['video_data']
                st.success(f"✅ Generated {len(result['video_data'].get('clips', []))} clips from '{video_name}'!")
                st.info("Navigate to the 'Clips' page to view your generated clips.")
            else:
                st.error(f"Failed to generate clips: {result['error']}")
                
        except Exception as e:
            st.error(f"Error generating clips: {str(e)}")


def _show_video_details(video_id, video_manager):
    """Show detailed information about a video."""
    try:
        details = video_manager.get_video_details(video_id)
        
        if details:
            with st.expander(f"📋 Video Details - {details.get('name', 'Unknown')}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Basic Information:**")
                    st.text(f"ID: {details.get('id', 'N/A')}")
                    st.text(f"Name: {details.get('name', 'N/A')}")
                    st.text(f"Length: {details.get('length', 0):.1f} seconds")
                
                with col2:
                    st.markdown("**Status:**")
                    st.text(f"Created: {details.get('created_at', 'N/A')}")
                    st.text(f"Status: {details.get('status', 'N/A')}")
                
                if details.get('description'):
                    st.markdown("**Description:**")
                    st.text(details['description'])
        else:
            st.error("Could not retrieve video details")
            
    except Exception as e:
        st.error(f"Error retrieving video details: {str(e)}")


def _confirm_delete_video(video_id, video_name, video_manager):
    """Show confirmation dialog for video deletion."""
    st.warning(f"⚠️ Are you sure you want to delete '{video_name}'?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"✅ Yes, Delete", key=f"confirm_delete_{video_id}", type="primary"):
            with st.spinner("Deleting video..."):
                try:
                    success = video_manager.delete_video(video_id)
                    if success:
                        st.success(f"✅ Video '{video_name}' deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete video")
                except Exception as e:
                    st.error(f"Error deleting video: {str(e)}")
    
    with col2:
        if st.button(f"❌ Cancel", key=f"cancel_delete_{video_id}"):
            st.info("Delete cancelled")
            st.rerun()
