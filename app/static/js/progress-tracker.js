/**
 * Progress Tracker
 * Handles lesson completion tracking and playback position saving
 */

class ProgressTracker {
    constructor(courseId, lessonPath, lessonType) {
        this.courseId = courseId;
        this.lessonPath = lessonPath;
        this.lessonType = lessonType;
        this.isCompleted = false;
        this.savePositionInterval = null;
    }

    async init() {
        await this.loadProgress();
        this.setupEventListeners();
    }

    async loadProgress() {
        try {
            const response = await fetch(`/api/progress/${this.courseId}/lesson?lesson_path=${encodeURIComponent(this.lessonPath)}`);
            const result = await response.json();

            if (result.success && result.progress) {
                this.isCompleted = result.progress.completed;
                this.updateCompletionButton();

                if (this.lessonType === 'video' || this.lessonType === 'audio') {
                    this.restorePlaybackPosition(result.progress.last_position_seconds);
                }
            }
        } catch (error) {
            console.error('Error loading progress:', error);
        }
    }

    setupEventListeners() {
        const completionBtn = document.getElementById('markCompletedBtn');
        if (completionBtn) {
            completionBtn.addEventListener('click', () => this.toggleCompletion());
        }

        if (this.lessonType === 'video') {
            const videoPlayer = document.getElementById('lessonVideoPlayer');
            if (videoPlayer) {
                videoPlayer.addEventListener('ended', () => this.markCompleted());
                videoPlayer.addEventListener('timeupdate', () => this.savePlaybackPositionThrottled(videoPlayer));
                videoPlayer.addEventListener('pause', () => this.savePlaybackPosition(videoPlayer));
            }
        } else if (this.lessonType === 'audio') {
            const audioPlayer = document.getElementById('lessonAudioPlayer');
            if (audioPlayer) {
                audioPlayer.addEventListener('ended', () => this.markCompleted());
                audioPlayer.addEventListener('timeupdate', () => this.savePlaybackPositionThrottled(audioPlayer));
                audioPlayer.addEventListener('pause', () => this.savePlaybackPosition(audioPlayer));
            }
        } else {
            const nextBtn = document.querySelector('.ls-nav-button-next');
            if (nextBtn) {
                nextBtn.addEventListener('click', async (e) => {
                    if (!this.isCompleted) {
                        e.preventDefault();
                        await this.markCompleted();
                        window.location.href = nextBtn.href;
                    }
                });
            }
        }
    }

    restorePlaybackPosition(positionSeconds) {
        if (positionSeconds > 0) {
            const player = this.lessonType === 'video'
                ? document.getElementById('lessonVideoPlayer')
                : document.getElementById('lessonAudioPlayer');

            if (player) {
                player.currentTime = positionSeconds;
            }
        }
    }

    savePlaybackPositionThrottled(player) {
        if (!this.savePositionInterval) {
            this.savePositionInterval = setTimeout(() => {
                this.savePlaybackPosition(player);
                this.savePositionInterval = null;
            }, 5000);
        }
    }

    async savePlaybackPosition(player) {
        if (!player || player.currentTime === 0) return;

        try {
            await fetch(`/api/progress/${this.courseId}/playback-position`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    lesson_path: this.lessonPath,
                    position_seconds: player.currentTime
                })
            });
        } catch (error) {
            console.error('Error saving playback position:', error);
        }
    }

    async toggleCompletion() {
        if (this.isCompleted) {
            await this.markIncomplete();
        } else {
            await this.markCompleted();
        }
    }

    async markCompleted() {
        try {
            const response = await fetch(`/api/progress/${this.courseId}/lesson/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    lesson_path: this.lessonPath
                })
            });

            const result = await response.json();

            if (result.success) {
                this.isCompleted = true;
                this.updateCompletionButton();
            }
        } catch (error) {
            console.error('Error marking lesson as completed:', error);
        }
    }

    async markIncomplete() {
        try {
            const response = await fetch(`/api/progress/${this.courseId}/lesson/incomplete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    lesson_path: this.lessonPath
                })
            });

            const result = await response.json();

            if (result.success) {
                this.isCompleted = false;
                this.updateCompletionButton();
            }
        } catch (error) {
            console.error('Error marking lesson as incomplete:', error);
        }
    }

    updateCompletionButton() {
        const btn = document.getElementById('markCompletedBtn');
        if (!btn) return;

        if (this.isCompleted) {
            btn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span>Completed</span>
            `;
            btn.classList.add('ls-btn--success');
            btn.classList.remove('ls-btn--primary');
        } else {
            btn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                </svg>
                <span>Mark Completed</span>
            `;
            btn.classList.remove('ls-btn--success');
            btn.classList.add('ls-btn--primary');
        }

        // Update sidebar lesson item
        this.updateSidebarLesson();
    }

    updateSidebarLesson() {
        const sidebarLesson = document.querySelector(`.ls-sidebar-lesson.active`);
        if (!sidebarLesson) return;

        if (this.isCompleted) {
            sidebarLesson.classList.add('completed');

            // Add checkmark if it doesn't exist
            if (!sidebarLesson.querySelector('.ls-sidebar-lesson-check')) {
                const checkmark = document.createElement('div');
                checkmark.className = 'ls-sidebar-lesson-check';
                checkmark.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                `;
                sidebarLesson.appendChild(checkmark);
            }
        } else {
            sidebarLesson.classList.remove('completed');

            // Remove checkmark if it exists
            const checkmark = sidebarLesson.querySelector('.ls-sidebar-lesson-check');
            if (checkmark) {
                checkmark.remove();
            }
        }
    }
}

// Initialize progress tracker when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const lessonViewPage = document.querySelector('.ls-lesson-view-page');
    if (!lessonViewPage) return;

    const courseId = lessonViewPage.dataset.courseId;
    const lessonPath = lessonViewPage.dataset.lessonPath;
    const lessonType = lessonViewPage.dataset.lessonType;

    if (courseId && lessonPath && lessonType) {
        const tracker = new ProgressTracker(courseId, lessonPath, lessonType);
        tracker.init();
    }
});
