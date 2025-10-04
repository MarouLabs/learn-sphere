class LessonPlayer {
    constructor() {
        this.init();
    }

    init() {
        this.setupVideoPlayer();
        this.setupAudioPlayer();
        this.setupHtmlTabs();
    }

    setupVideoPlayer() {
        const videoPlayer = document.getElementById('lessonVideoPlayer');
        const videoSpeedSelector = document.getElementById('videoSpeed');

        if (!videoPlayer || !videoSpeedSelector) return;

        const applyPlaybackSpeed = () => {
            const speed = parseFloat(videoSpeedSelector.value);
            if (speed && !isNaN(speed)) {
                videoPlayer.playbackRate = speed;
            }
        };

        videoPlayer.addEventListener('loadedmetadata', applyPlaybackSpeed);

        videoPlayer.addEventListener('canplay', applyPlaybackSpeed);

        videoSpeedSelector.addEventListener('change', (e) => {
            const speed = parseFloat(e.target.value);
            if (speed && !isNaN(speed)) {
                videoPlayer.playbackRate = speed;
                this.savePlaybackSpeed('video', speed);
            }
        });

        if (videoPlayer.readyState >= 1) {
            applyPlaybackSpeed();
        }
    }

    setupAudioPlayer() {
        const audioPlayer = document.getElementById('lessonAudioPlayer');
        const audioSpeedSelector = document.getElementById('audioSpeed');

        if (!audioPlayer || !audioSpeedSelector) return;

        const applyPlaybackSpeed = () => {
            const speed = parseFloat(audioSpeedSelector.value);
            if (speed && !isNaN(speed)) {
                audioPlayer.playbackRate = speed;
            }
        };

        audioPlayer.addEventListener('loadedmetadata', applyPlaybackSpeed);

        audioPlayer.addEventListener('canplay', applyPlaybackSpeed);

        audioSpeedSelector.addEventListener('change', (e) => {
            const speed = parseFloat(e.target.value);
            if (speed && !isNaN(speed)) {
                audioPlayer.playbackRate = speed;
                this.savePlaybackSpeed('audio', speed);
            }
        });

        if (audioPlayer.readyState >= 1) {
            applyPlaybackSpeed();
        }
    }

    setupHtmlTabs() {
        const tabButtons = document.querySelectorAll('.ls-tab-btn');

        if (tabButtons.length === 0) return;

        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const targetTab = e.target.dataset.tab;

                tabButtons.forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');

                document.querySelectorAll('.ls-tab-content').forEach(content => {
                    content.classList.remove('active');
                });

                document.getElementById(`${targetTab}-tab`).classList.add('active');
            });
        });
    }

    async savePlaybackSpeed(mediaType, speed) {
        try {
            const payload = {};
            if (mediaType === 'video') {
                payload.video_speed = speed;
            } else if (mediaType === 'audio') {
                payload.audio_speed = speed;
            }

            const response = await fetch('/api/user-preferences/playback-speed', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!result.success) {
                console.error('Failed to save playback speed:', result.error);
            }
        } catch (error) {
            console.error('Error saving playback speed:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new LessonPlayer();
});
