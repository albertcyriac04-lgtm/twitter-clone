// Character counter for tweet composer
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('tweet-content');
    const charCount = document.getElementById('char-count');
    const tweetBtn = document.getElementById('tweet-btn');

    if (textarea && charCount) {
        textarea.addEventListener('input', function () {
            const len = this.value.length;
            charCount.textContent = len + '/280';
            charCount.classList.toggle('warn', len > 260);
            if (tweetBtn) {
                tweetBtn.disabled = len === 0;
            }
        });
    }

    // Time ago for tweets
    document.querySelectorAll('.tweet-time[data-time]').forEach(function (el) {
        const date = new Date(el.dataset.time);
        const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
        let text;
        if (seconds < 60) text = seconds + 's';
        else if (seconds < 3600) text = Math.floor(seconds / 60) + 'm';
        else if (seconds < 86400) text = Math.floor(seconds / 3600) + 'h';
        else text = Math.floor(seconds / 86400) + 'd';
        el.textContent = text;
    });
});

// Toggle like via AJAX
function toggleLike(tweetId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const btn = document.querySelector('.like-btn[data-tweet-id="' + tweetId + '"]');

    fetch('/tweet/' + tweetId + '/like/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            const svg = btn.querySelector('svg');
            const countEl = btn.querySelector('.like-count');

            if (data.liked) {
                btn.classList.add('liked');
                svg.setAttribute('fill', '#f91880');
                svg.setAttribute('stroke', '#f91880');
            } else {
                btn.classList.remove('liked');
                svg.setAttribute('fill', 'none');
                svg.setAttribute('stroke', 'currentColor');
            }
            countEl.textContent = data.count;
        })
        .catch(function (err) { console.error('Like error:', err); });
}
