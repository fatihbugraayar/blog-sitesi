// Mobile Arama Fonksiyonları
function toggleMobileSearch() {
    const overlay = document.getElementById('mobileSearchOverlay');
    if(overlay.style.display === 'block') {
        overlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    } else {
        overlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

// Overlay Dışına Tıklama
document.getElementById('mobileSearchOverlay').addEventListener('click', function(e) {
    if(e.target === this) toggleMobileSearch();
});

// ESC ile Kapatma
document.addEventListener('keydown', (e) => {
    if(e.key === 'Escape') toggleMobileSearch();
});