/**
 * Social Footprint Analyzer - Frontend JavaScript
 */

// Global state
let currentResults = null;
let sentimentChart = null;
let platformChart = null;

// DOM Elements
const searchForm = document.getElementById('searchForm');
const searchQuery = document.getElementById('searchQuery');
const searchSection = document.getElementById('searchSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const backBtn = document.getElementById('backBtn');
const progressBar = document.getElementById('progressBar');
const loadingMessage = document.getElementById('loadingMessage');

// Loading messages
const loadingMessages = [
    "Searching Google...",
    "Scanning news articles...",
    "Analyzing social media...",
    "Processing sentiment...",
    "Calculating scores...",
    "Generating insights..."
];

// Event Listeners
searchForm.addEventListener('submit', handleSearch);
backBtn.addEventListener('click', resetToSearch);

/**
 * Handle search form submission
 */
async function handleSearch(e) {
    e.preventDefault();

    const query = searchQuery.value.trim();
    if (!query) return;

    // Show loading state
    showLoading();
    simulateProgress();

    try {
        // Call API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const data = await response.json();
        currentResults = data;

        // Show results
        setTimeout(() => {
            displayResults(data);
        }, 500);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze. Please check your API configuration and try again.');
        resetToSearch();
    }
}

/**
 * Simulate progress during loading
 */
function simulateProgress() {
    let progress = 0;
    let messageIndex = 0;

    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;

        progressBar.style.width = `${progress}%`;

        // Update message
        if (messageIndex < loadingMessages.length) {
            loadingMessage.textContent = loadingMessages[messageIndex];
            messageIndex++;
        }

    }, 800);

    // Store interval ID to clear later
    window.progressInterval = interval;
}

/**
 * Show loading section
 */
function showLoading() {
    searchSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
    progressBar.style.width = '0%';
}

/**
 * Display results
 */
function displayResults(data) {
    // Clear progress interval
    if (window.progressInterval) {
        clearInterval(window.progressInterval);
    }

    // Complete progress bar
    progressBar.style.width = '100%';

    // Hide loading, show results
    setTimeout(() => {
        loadingSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        // Populate data
        populateResults(data);

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 500);
}

/**
 * Populate results with data
 */
function populateResults(data) {
    // Header
    document.getElementById('resultQuery').textContent = data.query;
    document.getElementById('resultDate').textContent = new Date(data.analyzed_at).toLocaleString();

    // Scores with animation
    setTimeout(() => {
        animateScore('visibilityScore', 'visibilityBar', data.visibility_score);
    }, 100);

    setTimeout(() => {
        animateScore('perceptionScore', 'perceptionBar', data.perception_score);
    }, 300);

    setTimeout(() => {
        animateValue('totalMentions', data.total_mentions);
    }, 500);

    // Charts
    renderSentimentChart(data.sentiment_breakdown);
    renderPlatformChart(data.platform_distribution);

    // Keywords
    renderKeywords(data.keywords);

    // Recommendations
    renderRecommendations(data.recommendations);

    // Mentions
    renderMentions(data.top_mentions);
}

/**
 * Animate score display
 */
function animateScore(elementId, barId, targetValue) {
    const element = document.getElementById(elementId);
    const bar = document.getElementById(barId);
    let current = 0;
    const increment = targetValue / 50;

    const interval = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(interval);
        }
        element.textContent = Math.round(current);
        bar.style.width = `${current}%`;
    }, 20);
}

/**
 * Animate number value
 */
function animateValue(elementId, targetValue) {
    const element = document.getElementById(elementId);
    let current = 0;
    const increment = targetValue / 30;

    const interval = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(interval);
        }
        element.textContent = Math.round(current);
    }, 30);
}

/**
 * Render sentiment chart
 */
function renderSentimentChart(sentimentData) {
    const ctx = document.getElementById('sentimentChart').getContext('2d');

    if (sentimentChart) {
        sentimentChart.destroy();
    }

    sentimentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [
                    sentimentData.positive,
                    sentimentData.neutral,
                    sentimentData.negative
                ],
                backgroundColor: [
                    '#10B981',  // Green
                    '#6B7280',  // Gray
                    '#EF4444'   // Red
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Render platform distribution chart
 */
function renderPlatformChart(platformData) {
    const ctx = document.getElementById('platformChart').getContext('2d');

    if (platformChart) {
        platformChart.destroy();
    }

    const labels = platformData.map(p => p.platform);
    const data = platformData.map(p => p.count);

    platformChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mentions',
                data: data,
                backgroundColor: '#4F46E5',
                borderColor: '#4338CA',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

/**
 * Render keywords
 */
function renderKeywords(keywords) {
    const container = document.getElementById('keywordsContainer');
    container.innerHTML = '';

    if (keywords.length === 0) {
        container.innerHTML = '<p class="text-gray-500">No keywords extracted</p>';
        return;
    }

    keywords.forEach(keyword => {
        const tag = document.createElement('span');
        tag.className = 'px-4 py-2 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium';
        tag.textContent = keyword;
        container.appendChild(tag);
    });
}

/**
 * Render recommendations
 */
function renderRecommendations(recommendations) {
    const list = document.getElementById('recommendationsList');
    list.innerHTML = '';

    if (recommendations.length === 0) {
        list.innerHTML = '<p class="text-gray-600">No recommendations available</p>';
        return;
    }

    recommendations.forEach((rec, index) => {
        const item = document.createElement('li');
        item.className = 'flex items-start bg-white p-4 rounded-lg shadow-sm';
        item.innerHTML = `
            <span class="flex-shrink-0 w-6 h-6 bg-indigo-600 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">
                ${index + 1}
            </span>
            <p class="text-gray-700">${rec}</p>
        `;
        list.appendChild(item);
    });
}

/**
 * Render top mentions
 */
function renderMentions(mentions) {
    const container = document.getElementById('mentionsList');
    container.innerHTML = '';

    if (mentions.length === 0) {
        container.innerHTML = '<p class="text-gray-500">No mentions found</p>';
        return;
    }

    mentions.forEach(mention => {
        const sentimentColor = {
            'positive': 'bg-green-100 text-green-700',
            'neutral': 'bg-gray-100 text-gray-700',
            'negative': 'bg-red-100 text-red-700'
        }[mention.sentiment] || 'bg-gray-100 text-gray-700';

        const card = document.createElement('div');
        card.className = 'border border-gray-200 rounded-lg p-4 hover:shadow-md transition';
        card.innerHTML = `
            <div class="flex items-start justify-between mb-2">
                <h4 class="font-semibold text-gray-900 flex-1">${mention.title}</h4>
                <span class="px-2 py-1 ${sentimentColor} rounded text-xs font-medium ml-2">
                    ${mention.sentiment}
                </span>
            </div>
            <p class="text-sm text-gray-600 mb-2">${mention.snippet}</p>
            <div class="flex items-center justify-between">
                <span class="text-xs font-medium text-indigo-600">${mention.platform}</span>
                <a href="${mention.url}" target="_blank" class="text-xs text-cyan-600 hover:text-cyan-700 font-medium">
                    View Source →
                </a>
            </div>
        `;
        container.appendChild(card);
    });
}

/**
 * Reset to search view
 */
function resetToSearch() {
    resultsSection.classList.add('hidden');
    loadingSection.classList.add('hidden');
    searchSection.classList.remove('hidden');
    searchQuery.value = '';
    currentResults = null;

    // Destroy charts
    if (sentimentChart) {
        sentimentChart.destroy();
        sentimentChart = null;
    }
    if (platformChart) {
        platformChart.destroy();
        platformChart = null;
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
}
